import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TrendingUp, Play, Pause, RotateCcw } from "lucide-react";

interface EmotionDataPoint {
  time: string;
  positive: number;
  negative: number;
  neutral: number;
  alerts: number;
}

const InteractiveEmotionChart = () => {
  const [data, setData] = useState<EmotionDataPoint[]>([
    { time: '09:00', positive: 65, negative: 20, neutral: 15, alerts: 2 },
    { time: '10:00', positive: 70, negative: 18, neutral: 12, alerts: 1 },
    { time: '11:00', positive: 60, negative: 25, neutral: 15, alerts: 3 },
    { time: '12:00', positive: 55, negative: 30, neutral: 15, alerts: 4 },
  ]);
  
  const [isLive, setIsLive] = useState(false);
  const [chartType, setChartType] = useState<'line' | 'area'>('area');
  const [error, setError] = useState<string | null>(null);
  const [isLiveMonitoring, setIsLiveMonitoring] = useState(false);
  const [hasStartedMonitoring, setHasStartedMonitoring] = useState(false);

  // Live button now automatically starts email monitoring and resets data
  const startLiveMonitoring = async () => {
    try {
      setError(null);
      console.log('🔄 Starting live monitoring with fresh data...');
      
      const response = await fetch('http://localhost:5000/api/start-live-monitoring', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          user_id: 'default_user',
          reset_data: true  // Always reset data when starting live monitoring
        }),
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('✅ Live monitoring started successfully!', result);
        setIsLiveMonitoring(true);
        setHasStartedMonitoring(true);
        
        // Clear current data to show fresh start
        setData([]);
        
        // Show success message about data reset
        if (result.data_reset) {
          console.log('📊 Data reset to zero - monitoring will show fresh results');
        }
      } else {
        const errorData = await response.text();
        throw new Error(`Failed to start monitoring: ${errorData}`);
      }
    } catch (error) {
      console.error('❌ Failed to start live monitoring:', error);
      setError('Failed to start live monitoring. Please check your email configuration.');
    }
  };

  // Function to fetch real emotion trends data from backend
  const fetchEmotionTrends = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/emotion-trends');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const json = await response.json();
      
      if (json.trends) {
        // Transform backend data to chart format
        const chartData: EmotionDataPoint[] = [];
        
        // If trends is an object with time keys
        if (typeof json.trends === 'object' && !Array.isArray(json.trends)) {
          Object.entries(json.trends).forEach(([time, emotions]: [string, any]) => {
            const total = (emotions.joy || 0) + (emotions.anger || 0) + (emotions.confusion || 0) + (emotions.neutral || 0);
            const positive = total > 0 ? Math.round(((emotions.joy || 0) / total) * 100) : 0;
            const negative = total > 0 ? Math.round(((emotions.anger || 0) + (emotions.confusion || 0)) / total * 100) : 0;
            const neutral = total > 0 ? Math.round(((emotions.neutral || 0) / total) * 100) : 0;
            
            chartData.push({
              time,
              positive,
              negative: negative,
              neutral,
              alerts: emotions.anger || 0
            });
          });
        } else if (Array.isArray(json.trends)) {
          // If trends is an array (current API format)
          json.trends.forEach((trend: any) => {
            const total = (trend.joy || 0) + (trend.anger || 0) + (trend.confusion || 0) + (trend.neutral || 0);
            const positive = total > 0 ? Math.round(((trend.joy || 0) / total) * 100) : 0;
            const negative = total > 0 ? Math.round(((trend.anger || 0) + (trend.confusion || 0)) / total * 100) : 0;
            const neutral = total > 0 ? Math.round(((trend.neutral || 0) / total) * 100) : 0;
            
            chartData.push({
              time: trend.time,
              positive,
              negative: negative,
              neutral,
              alerts: trend.anger || 0
            });
          });
        }
        
        // Sort by time and take last 12 hours
        chartData.sort((a, b) => a.time.localeCompare(b.time));
        setData(chartData.length > 0 ? chartData.slice(-12) : chartData);
        setError(null);
      } else {
        throw new Error('No trends data received from backend');
      }
    } catch (error) {
      console.error('Failed to fetch emotion trends:', error);
      setError(`Failed to fetch real data: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  // Fetch real data from backend on mount
  useEffect(() => {
    fetchEmotionTrends();
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isLive) {
      // Start live email monitoring when Live mode is activated
      if (!isLiveMonitoring) {
        startLiveMonitoring();
      }
      
      // Fetch real data every 10 seconds when live mode is active (faster updates)
      interval = setInterval(() => {
        fetchEmotionTrends();
      }, 10000); // 10 seconds interval for real-time updates
    } else {
      setIsLiveMonitoring(false);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isLive, isLiveMonitoring]);

  const resetData = async () => {
    try {
      setIsLive(false);
      setIsLiveMonitoring(false);
      setError(null);
      
      console.log('🔄 Resetting all emotion data...');
      
      const response = await fetch('http://localhost:5000/api/reset-emotion-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'default_user' }),
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('✅ Data reset successfully:', result);
        
        // Clear the chart data to show reset
        setData([]);
        
        // Fetch fresh data
        fetchEmotionTrends();
      } else {
        throw new Error('Failed to reset data');
      }
    } catch (error) {
      console.error('❌ Failed to reset data:', error);
      setError('Failed to reset data. Please try again.');
      // Still fetch data in case of error
      fetchEmotionTrends();
    }
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card border border-border rounded-lg p-3 shadow-lg">
          <p className="text-foreground font-medium">{`Time: ${label}`}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {`${entry.dataKey}: ${entry.value}${entry.dataKey === 'alerts' ? '' : '%'}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <Card className="bg-gradient-card border-border">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5" />
              <span>Real-time Emotion Trends</span>
              {isLive && <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>}
              {isLiveMonitoring && (
                <span className="text-xs text-green-500 font-normal">
                  • Email monitoring active - starting from zero
                </span>
              )}
            </CardTitle>
            <CardDescription>
              {isLiveMonitoring 
                ? "Live monitoring active - data resets to zero on each new session"
                : "Interactive sentiment analysis across all customer touchpoints"
              }
            </CardDescription>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setChartType(chartType === 'line' ? 'area' : 'line')}
              className="border-border"
            >
              {chartType === 'line' ? 'Area' : 'Line'}
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                if (!isLive) {
                  // When turning on live mode, start monitoring
                  startLiveMonitoring();
                } else {
                  // When turning off live mode, just stop the updates
                  setIsLiveMonitoring(false);
                }
                setIsLive(!isLive);
              }}
              className={`border-border ${isLive ? 'bg-red-500/10 text-red-500' : 'bg-green-500/10 text-green-500'}`}
            >
              {isLive ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              {isLive ? 'Pause Live' : 'Start Live'}
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={resetData}
              className="border-border"
            >
              <RotateCcw className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {error && (
          <div className="mb-4 p-2 bg-red-900/60 text-red-200 rounded border border-red-700">
            {error}
          </div>
        )}
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            {chartType === 'area' ? (
              <AreaChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(217 32% 17%)" />
                <XAxis 
                  dataKey="time" 
                  stroke="hsl(215 20% 65%)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="hsl(215 20% 65%)"
                  fontSize={12}
                />
                <Tooltip content={<CustomTooltip />} />
                <Area 
                  type="monotone" 
                  dataKey="positive" 
                  stackId="1"
                  stroke="hsl(120 100% 60%)" 
                  fill="hsl(120 100% 60%)"
                  fillOpacity={0.6}
                />
                <Area 
                  type="monotone" 
                  dataKey="neutral" 
                  stackId="1"
                  stroke="hsl(60 20% 60%)" 
                  fill="hsl(60 20% 60%)"
                  fillOpacity={0.6}
                />
                <Area 
                  type="monotone" 
                  dataKey="negative" 
                  stackId="1"
                  stroke="hsl(0 100% 60%)" 
                  fill="hsl(0 100% 60%)"
                  fillOpacity={0.6}
                />
              </AreaChart>
            ) : (
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(217 32% 17%)" />
                <XAxis 
                  dataKey="time" 
                  stroke="hsl(215 20% 65%)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="hsl(215 20% 65%)"
                  fontSize={12}
                />
                <Tooltip content={<CustomTooltip />} />
                <Line 
                  type="monotone" 
                  dataKey="positive" 
                  stroke="hsl(120 100% 60%)" 
                  strokeWidth={3}
                  dot={{ fill: "hsl(120 100% 60%)", strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, stroke: "hsl(120 100% 60%)", strokeWidth: 2 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="negative" 
                  stroke="hsl(0 100% 60%)" 
                  strokeWidth={3}
                  dot={{ fill: "hsl(0 100% 60%)", strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, stroke: "hsl(0 100% 60%)", strokeWidth: 2 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="neutral" 
                  stroke="hsl(60 20% 60%)" 
                  strokeWidth={3}
                  dot={{ fill: "hsl(60 20% 60%)", strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, stroke: "hsl(60 20% 60%)", strokeWidth: 2 }}
                />
              </LineChart>
            )}
          </ResponsiveContainer>
        </div>
        
        <div className="mt-4 flex justify-center space-x-6 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-emotion-positive rounded-full"></div>
            <span className="text-muted-foreground">Positive</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-emotion-negative rounded-full"></div>
            <span className="text-muted-foreground">Negative</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-emotion-neutral rounded-full"></div>
            <span className="text-muted-foreground">Neutral</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default InteractiveEmotionChart;