import { BarChart3, Bell, TrendingUp, Users, Activity, MessageCircle, Settings, Mail } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import InteractiveEmotionChart from "@/components/InteractiveEmotionChart";
import { useState, useEffect } from "react";
import { SignedIn, SignedOut, RedirectToSignIn } from "@clerk/clerk-react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [emotionData, setEmotionData] = useState([
    { type: "Anger", count: 0, trend: "+0%", color: "emotion-negative" },
    { type: "Confusion", count: 0, trend: "+0%", color: "emotion-negative" },
    { type: "Joy", count: 0, trend: "+0%", color: "emotion-positive" },
    { type: "Neutral", count: 0, trend: "+0%", color: "emotion-neutral" },
  ]);

  const [recentTickets, setRecentTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [emailConfig, setEmailConfig] = useState(null);
  const navigate = useNavigate();

  // Fetch real emotion overview data from backend
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch emotion overview
        const emotionResponse = await fetch('http://localhost:5000/api/emotion-overview');
        if (emotionResponse.ok) {
          const emotionJson = await emotionResponse.json();
          
          const updatedEmotionData = [
            { 
              type: "Anger", 
              count: emotionJson.anger?.count || 0, 
              trend: emotionJson.anger?.percentage_text || `${emotionJson.anger?.count || 0}/0 (0%)`, 
              color: "emotion-negative" 
            },
            { 
              type: "Confusion", 
              count: emotionJson.confusion?.count || 0, 
              trend: emotionJson.confusion?.percentage_text || `${emotionJson.confusion?.count || 0}/0 (0%)`, 
              color: "emotion-negative" 
            },
            { 
              type: "Joy", 
              count: emotionJson.joy?.count || 0, 
              trend: emotionJson.joy?.percentage_text || `${emotionJson.joy?.count || 0}/0 (0%)`, 
              color: "emotion-positive" 
            },
            { 
              type: "Neutral", 
              count: emotionJson.neutral?.count || 0, 
              trend: emotionJson.neutral?.percentage_text || `${emotionJson.neutral?.count || 0}/0 (0%)`, 
              color: "emotion-neutral" 
            },
          ];
          setEmotionData(updatedEmotionData);
        }

        // Fetch recent negative sentiment messages for tickets
        const ticketsResponse = await fetch('http://localhost:5000/alerts?limit=3');
        if (ticketsResponse.ok) {
          const ticketsJson = await ticketsResponse.json();
          if (ticketsJson.messages && Array.isArray(ticketsJson.messages)) {
            const formattedTickets = ticketsJson.messages.map((msg: any, index: number) => ({
              id: `#${msg.id || (4521 - index)}`,
              customer: msg.sender || 'Unknown Customer',
              emotion: (msg.sentiment || msg.emotion || 'unknown').charAt(0).toUpperCase() + (msg.sentiment || msg.emotion || 'unknown').slice(1),
              severity: msg.sentiment === 'angry' ? 'High' : msg.sentiment === 'confused' ? 'Medium' : 'Low',
              time: msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString() : 'Unknown'
            }));
            setRecentTickets(formattedTickets);
          }
        }

        // Fetch email configuration
        const configResponse = await fetch('http://localhost:5000/api/email-config');
        if (configResponse.ok) {
          const configJson = await configResponse.json();
          setEmailConfig(configJson);
        }

        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
        setError('Failed to load dashboard data');
        setLoading(false);
      }
    };

    fetchDashboardData();
    
    // Refresh data every 30 seconds for more frequent updates
    const interval = setInterval(fetchDashboardData, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const sidebarItems = [
    { icon: BarChart3, label: "Overview", active: true },
    { icon: TrendingUp, label: "Trends", active: false },
    { icon: Bell, label: "Alerts", active: false },
    { icon: Users, label: "Settings", active: false },
  ];

  return (
    <>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
      <SignedIn>
        <div className="min-h-screen bg-background">
      <div className="flex">
        {/* Sidebar */}
        <div className="w-64 bg-gradient-card border-r border-border p-6">
          <div className="flex items-center space-x-3 mb-8">
            <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">CS</span>
            </div>
            <span className="text-lg font-semibold text-foreground">Dashboard</span>
          </div>
          
          <nav className="space-y-2">
            {sidebarItems.map((item) => (
              <Button
                key={item.label}
                variant={item.active ? "default" : "ghost"}
                className={`w-full justify-start space-x-3 ${
                  item.active ? "bg-gradient-primary" : "hover:bg-muted"
                }`}
              >
                <item.icon size={18} />
                <span>{item.label}</span>
              </Button>
            ))}
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-8">
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-foreground mb-2">
                  Emotion Monitoring Overview
                </h1>
                <p className="text-muted-foreground">
                  Real-time insights into customer sentiment across all channels
                </p>
              </div>
              {emailConfig && (
                <div className="text-right">
                  <div className="flex items-center space-x-2 text-sm text-muted-foreground mb-1">
                    <Mail size={16} />
                    <span>Monitoring:</span>
                  </div>
                  <div className="font-medium text-foreground">{emailConfig.email}</div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigate('/start-monitoring')}
                    className="mt-2"
                  >
                    <Settings size={14} className="mr-1" />
                    Change Settings
                  </Button>
                </div>
              )}
            </div>
            
            {!emailConfig && (
              <Card className="border-orange-200 bg-orange-50 dark:bg-orange-950/20 mb-6">
                <CardContent className="pt-4">
                  <div className="flex items-center space-x-3">
                    <Mail className="text-orange-500" size={20} />
                    <div className="flex-1">
                      <p className="text-orange-800 dark:text-orange-200 font-medium">
                        No Email Monitoring Configured
                      </p>
                      <p className="text-orange-600 dark:text-orange-300 text-sm">
                        Set up email monitoring to start tracking customer sentiment
                      </p>
                    </div>
                    <Button
                      onClick={() => navigate('/start-monitoring')}
                      className="bg-orange-500 hover:bg-orange-600"
                    >
                      Configure Now
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {emotionData.map((emotion) => (
              <Card key={emotion.type} className="bg-gradient-card border-border">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-muted-foreground">
                    {emotion.type}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className={`text-2xl font-bold ${emotion.color}`}>
                      {loading ? "..." : emotion.count}
                    </span>
                    <span className="text-sm text-muted-foreground">
                      {loading ? "..." : emotion.trend}
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-900/20 border border-red-800 text-red-300 rounded-lg">
              {error}
            </div>
          )}

          {/* Interactive Emotion Trend Chart */}
          <div className="mb-8">
            <InteractiveEmotionChart />
          </div>

          {/* Recent Tickets */}
          <Card className="bg-gradient-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageCircle size={20} />
                <span>Recent Flagged Conversations</span>
              </CardTitle>
              <CardDescription>
                Latest customer interactions requiring attention
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {loading ? (
                  <div className="text-center py-8 text-muted-foreground">
                    Loading recent conversations...
                  </div>
                ) : recentTickets.length > 0 ? (
                  recentTickets.map((ticket: any) => (
                    <div key={ticket.id} className="flex items-center justify-between p-4 bg-muted/10 rounded-lg">
                      <div className="flex items-center space-x-4">
                        <span className="font-mono text-sm text-muted-foreground">{ticket.id}</span>
                        <span className="font-medium text-foreground">{ticket.customer}</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          ticket.emotion === 'Angry' ? 'emotion-negative bg-red-500/10' :
                          ticket.emotion === 'Confused' ? 'emotion-negative bg-orange-500/10' :
                          'emotion-positive bg-green-500/10'
                        }`}>
                          {ticket.emotion}
                        </span>
                      </div>
                      <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                        <span>{ticket.severity}</span>
                        <span>{ticket.time}</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    No recent flagged conversations
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
    </SignedIn>
  </>
);
};

export default Dashboard;