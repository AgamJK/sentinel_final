import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Plug, Brain, AlertTriangle, Heart, TrendingUp, Shield, Zap } from "lucide-react";
import Navigation from "@/components/Navigation";
import LiveSentimentDemo from "@/components/LiveSentimentDemo";
import AnimatedFlow from "@/components/InteractiveFlow";

const Index = () => {
  const howItWorksSteps = [
    {
      icon: Plug,
      title: "Connect your support inbox or chat",
      description: "Seamlessly integrate with Zendesk, Intercom, Gmail, and Slack in minutes"
    },
    {
      icon: Brain,
      title: "AI reads every ticket for emotion & urgency",
      description: "Advanced sentiment analysis detects anger, frustration, confusion, and joy in real-time"
    },
    {
      icon: AlertTriangle,
      title: "Get alerts when sentiment turns negative",
      description: "Instant notifications to your team when customer emotions spike toward negativity"
    }
  ];

  const benefits = [
    {
      icon: AlertTriangle,
      title: "Real-time alerts on customer frustration",
      description: "Never miss another escalating customer issue with instant sentiment monitoring"
    },
    {
      icon: TrendingUp,
      title: "Detect trends across chat, email & support",
      description: "Identify patterns in customer emotions across all your communication channels"
    },
    {
      icon: Shield,
      title: "Prevent churn before it happens",
      description: "Proactively address negative sentiment before customers decide to leave"
    },
    {
      icon: Zap,
      title: "Integrates with Zendesk, Intercom & Slack",
      description: "Works seamlessly with your existing support infrastructure"
    }
  ];

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Enhanced Animated Background Elements */}
      <div className="absolute inset-0 opacity-30 pointer-events-none">
        {/* Floating orbs with purple/blue theme */}
        <div className="absolute top-20 left-10 w-40 h-40 bg-gradient-to-r from-purple-500/40 to-blue-500/40 rounded-full blur-2xl animate-float"></div>
        <div className="absolute top-40 right-20 w-32 h-32 bg-gradient-to-r from-violet-500/30 to-purple-500/30 rounded-full blur-xl animate-float-delay"></div>
        <div className="absolute bottom-40 left-20 w-48 h-48 bg-gradient-to-r from-blue-600/30 to-indigo-500/30 rounded-full blur-3xl animate-float-slow"></div>
        <div className="absolute bottom-20 right-10 w-36 h-36 bg-gradient-to-r from-purple-600/40 to-pink-500/40 rounded-full blur-xl animate-float"></div>
        <div className="absolute top-1/2 left-1/3 w-24 h-24 bg-gradient-to-r from-cyan-400/20 to-blue-500/20 rounded-full blur-lg animate-float-delay"></div>
        <div className="absolute top-1/4 right-1/4 w-28 h-28 bg-gradient-to-r from-indigo-500/25 to-purple-600/25 rounded-full blur-xl animate-float-slow"></div>
      </div>

      {/* Animated grid pattern */}
      <div className="absolute inset-0 opacity-10 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-br from-transparent via-purple-500/5 to-transparent animate-grid-move"></div>
        <div className="grid-pattern"></div>
      </div>
      
      <Navigation />
      
      {/* Hero Section */}
      <section className="relative bg-gradient-hero py-24 px-6">
        <div className="container mx-auto text-center relative z-10">
          <h1 className="text-5xl md:text-6xl font-bold text-foreground mb-6 max-w-4xl mx-auto hover:scale-105 transition-transform duration-500">
            Stay Ahead of Rising{" "}
            <span className="bg-gradient-primary bg-clip-text text-transparent animate-pulse-subtle">
              Customer Frustration
            </span>
          </h1>
          
          <p className="text-xl text-muted-foreground mb-12 max-w-2xl mx-auto opacity-90 hover:opacity-100 transition-opacity duration-300">
            AI analyzes support conversations and alerts your team before sentiment turns toxic.
            Prevent churn with emotional intelligence.
          </p>
          
          <Link to="/start-monitoring">
            <Button className="cta-button text-lg px-12 py-6 hover:scale-110 transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/25">
              Start Monitoring
            </Button>
          </Link>
        </div>
        
        {/* Reactive particle effects */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-emotion-positive/20 rounded-full blur-xl animate-float-delay hover-grow"></div>
          <div className="absolute top-1/2 right-1/3 w-24 h-24 bg-emotion-negative/15 rounded-full blur-xl animate-float hover-grow"></div>
          <div className="absolute bottom-1/3 left-1/2 w-40 h-40 bg-primary/10 rounded-full blur-xl animate-float-slow hover-grow"></div>
          <div className="absolute top-1/3 right-1/4 w-20 h-20 bg-purple-400/20 rounded-full blur-lg animate-float-delay hover-grow"></div>
          <div className="absolute bottom-1/4 left-1/5 w-28 h-28 bg-blue-500/15 rounded-full blur-xl animate-float hover-grow"></div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-24 px-6 bg-background">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4">
              How It Works
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Three simple steps to transform your customer support with AI-powered emotion detection
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {howItWorksSteps.map((step, index) => (
              <Card key={index} className="bg-gradient-card border-border glow-primary">
                <CardHeader className="text-center">
                  <div className="w-16 h-16 bg-gradient-primary rounded-xl flex items-center justify-center mx-auto mb-4">
                    <step.icon size={28} className="text-primary-foreground" />
                  </div>
                  <CardTitle className="text-xl font-semibold text-foreground">
                    {step.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-center text-muted-foreground">
                    {step.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
        
        {/* Interactive Flow Diagram */}
        <div className="mt-16">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold text-foreground mb-4">
              Interactive Data Flow
            </h3>
            <p className="text-muted-foreground">
              See how your customer data flows through our AI-powered sentiment analysis
            </p>
          </div>
          <AnimatedFlow />
        </div>
      </section>

      {/* Interactive Demo Section */}
      <section className="py-24 px-6 bg-background">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4">
              Try Our Live Demo
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Experience real-time sentiment analysis in action
            </p>
          </div>
          
          <LiveSentimentDemo />
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-24 px-6 bg-gradient-card/50">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4">
              Why CX Teams Love CustomerSentinel
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Empower your support team with emotional intelligence and proactive customer care
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {benefits.map((benefit, index) => (
              <Card key={index} className="bg-gradient-card border-border hover:glow-primary transition-all duration-300">
                <CardHeader>
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-accent rounded-lg flex items-center justify-center">
                      <benefit.icon size={24} className="text-accent-foreground" />
                    </div>
                    <CardTitle className="text-xl font-semibold text-foreground">
                      {benefit.title}
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-muted-foreground">
                    {benefit.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="py-24 px-6 bg-gradient-hero">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl font-bold text-foreground mb-6">
            Ready to hear what your customers are{" "}
            <span className="emotion-positive">really feeling</span>?
          </h2>
          
          <p className="text-xl text-muted-foreground mb-12 max-w-2xl mx-auto">
            Join forward-thinking CX teams who prevent churn with emotional intelligence
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/start-monitoring">
              <Button className="cta-button text-lg px-8 py-4">
                <Heart className="mr-2" size={20} />
                Start Monitoring Now
              </Button>
            </Link>
            <Link to="/schedule-demo">
              <Button variant="outline" className="border-border text-foreground hover:bg-muted text-lg px-8 py-4">
                Schedule Demo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 bg-card border-t border-border">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-3 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-sm">CS</span>
              </div>
              <span className="text-lg font-semibold text-foreground">CustomerSentinel</span>
            </div>
            
            <div className="flex space-x-6 text-sm text-muted-foreground mb-4 md:mb-0">
              <Link to="#" className="hover:text-foreground transition-colors">About</Link>
              <Link to="#" className="hover:text-foreground transition-colors">Privacy</Link>
              <Link to="#" className="hover:text-foreground transition-colors">Terms</Link>
            </div>
            
            <p className="text-sm text-muted-foreground">
              Made with 💙 in India for teams that care.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
