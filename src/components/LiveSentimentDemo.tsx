import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MessageCircle, TrendingUp, AlertTriangle, Smile, Frown, Meh } from "lucide-react";

interface EmotionMessage {
  id: string;
  customer: string;
  message: string;
  emotion: "positive" | "negative" | "neutral";
  severity: "high" | "medium" | "low";
  timestamp: Date;
}

const LiveSentimentDemo = () => {
  const [messages, setMessages] = useState<EmotionMessage[]>([]);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [stats, setStats] = useState({
    positive: 0,
    negative: 0,
    neutral: 0,
    alerts: 0
  });

  const sampleMessages = [
    { customer: "Sarah J.", message: "This service is absolutely terrible! I've been waiting for hours!", emotion: "negative" as const, severity: "high" as const },
    { customer: "Mike C.", message: "Thanks for the quick response, really appreciate it!", emotion: "positive" as const, severity: "low" as const },
    { customer: "Emma D.", message: "I'm confused about how this works, can you help?", emotion: "neutral" as const, severity: "medium" as const },
    { customer: "John B.", message: "I'm getting really frustrated with these constant errors!", emotion: "negative" as const, severity: "high" as const },
    { customer: "Lisa M.", message: "Great product, exactly what I needed!", emotion: "positive" as const, severity: "low" as const },
    { customer: "Tom R.", message: "Is there a way to change my subscription?", emotion: "neutral" as const, severity: "low" as const },
    { customer: "Anna K.", message: "This is the worst experience I've ever had!", emotion: "negative" as const, severity: "high" as const },
    { customer: "Chris L.", message: "Outstanding customer service, thank you!", emotion: "positive" as const, severity: "low" as const },
  ];

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isMonitoring) {
      interval = setInterval(() => {
        const randomMessage = sampleMessages[Math.floor(Math.random() * sampleMessages.length)];
        const newMessage: EmotionMessage = {
          id: Date.now().toString(),
          ...randomMessage,
          timestamp: new Date()
        };
        
        setMessages(prev => [newMessage, ...prev.slice(0, 9)]);
        
        setStats(prev => ({
          ...prev,
          [newMessage.emotion]: prev[newMessage.emotion] + 1,
          alerts: newMessage.emotion === 'negative' && newMessage.severity === 'high' 
            ? prev.alerts + 1 
            : prev.alerts
        }));
      }, 2000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isMonitoring]);

  const getEmotionIcon = (emotion: string) => {
    switch (emotion) {
      case "positive": return <Smile className="w-4 h-4 text-emotion-positive" />;
      case "negative": return <Frown className="w-4 h-4 text-emotion-negative" />;
      default: return <Meh className="w-4 h-4 text-emotion-neutral" />;
    }
  };

  const getEmotionColor = (emotion: string) => {
    switch (emotion) {
      case "positive": return "bg-green-500/10 text-emotion-positive border-green-500/20";
      case "negative": return "bg-red-500/10 text-emotion-negative border-red-500/20";
      default: return "bg-yellow-500/10 text-emotion-neutral border-yellow-500/20";
    }
  };

  return (
    <div className="space-y-6">
      {/* Demo Controls */}
      <Card className="bg-gradient-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <MessageCircle className="w-6 h-6 text-primary" />
            <span>Live Sentiment Monitoring Demo</span>
          </CardTitle>
          <CardDescription>
            Watch AI analyze customer messages in real-time and detect emotional sentiment
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-4">
            <Button
              onClick={() => setIsMonitoring(!isMonitoring)}
              className={isMonitoring ? "bg-red-500 hover:bg-red-600" : "cta-button"}
            >
              {isMonitoring ? "Stop Monitoring" : "Start Live Demo"}
            </Button>
            <div className={`w-3 h-3 rounded-full ${isMonitoring ? "bg-green-500 animate-pulse" : "bg-gray-400"}`}></div>
            <span className="text-sm text-muted-foreground">
              {isMonitoring ? "Monitoring Active" : "Monitoring Stopped"}
            </span>
          </div>
        </CardContent>
      </Card>

      {/* Real-time Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Smile className="w-5 h-5 text-emotion-positive" />
              <div>
                <p className="text-2xl font-bold text-emotion-positive">{stats.positive}</p>
                <p className="text-xs text-muted-foreground">Positive</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Frown className="w-5 h-5 text-emotion-negative" />
              <div>
                <p className="text-2xl font-bold text-emotion-negative">{stats.negative}</p>
                <p className="text-xs text-muted-foreground">Negative</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Meh className="w-5 h-5 text-emotion-neutral" />
              <div>
                <p className="text-2xl font-bold text-emotion-neutral">{stats.neutral}</p>
                <p className="text-xs text-muted-foreground">Neutral</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-red-500" />
              <div>
                <p className="text-2xl font-bold text-red-500">{stats.alerts}</p>
                <p className="text-xs text-muted-foreground">Alerts</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Live Message Feed */}
      <Card className="bg-gradient-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5" />
            <span>Live Message Analysis</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {messages.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <MessageCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Start monitoring to see live sentiment analysis</p>
              </div>
            ) : (
              messages.map((message) => (
                <div key={message.id} className="flex items-start space-x-3 p-3 bg-muted/10 rounded-lg">
                  <div className="flex-shrink-0">
                    {getEmotionIcon(message.emotion)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="font-medium text-foreground">{message.customer}</span>
                      <Badge variant="outline" className={getEmotionColor(message.emotion)}>
                        {message.emotion}
                      </Badge>
                      {message.emotion === "negative" && message.severity === "high" && (
                        <Badge variant="destructive" className="text-xs">
                          ALERT
                        </Badge>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground">{message.message}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default LiveSentimentDemo;