import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { SignedIn, SignedOut, RedirectToSignIn } from "@clerk/clerk-react";
import EmailMonitoringSetup from "@/components/EmailMonitoringSetup";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

const GmailSetup = () => {
  const [existingConfig, setExistingConfig] = useState(null);
  const navigate = useNavigate();

  // Check if email is already configured
  useEffect(() => {
    const checkEmailConfig = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/email-config');
        if (response.ok) {
          const config = await response.json();
          setExistingConfig(config);
        }
      } catch (error) {
        console.error('Failed to fetch email config:', error);
      }
    };

    checkEmailConfig();
  }, []);

  const handleConfigSaved = (config: any) => {
    console.log("Email configuration saved:", config);
    // Redirect to dashboard after successful configuration
    navigate("/dashboard");
  };

  return (
    <>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
      <SignedIn>
        <div className="min-h-screen bg-gradient-hero waveform p-6">
          <div className="container mx-auto max-w-2xl">
            {/* Back Button */}
            <div className="mb-6">
              <Button
                variant="outline"
                onClick={() => navigate("/start-monitoring")}
                className="flex items-center space-x-2"
              >
                <ArrowLeft size={16} />
                <span>Back to Start Monitoring</span>
              </Button>
            </div>

            {/* Header */}
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-foreground mb-4">
                Gmail Monitoring Setup
              </h1>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                Connect your Gmail account to start monitoring customer sentiment in real-time
              </p>
            </div>

            {/* Email Configuration Component */}
            <EmailMonitoringSetup 
              onConfigSaved={handleConfigSaved}
              existingConfig={existingConfig}
            />

            {/* Background Visualization */}
            <div className="mt-12 text-center">
              <div className="w-full h-32 bg-gradient-accent/10 rounded-xl flex items-center justify-center waveform">
                <p className="text-muted-foreground">Secure email monitoring setup</p>
              </div>
            </div>
          </div>
        </div>
      </SignedIn>
    </>
  );
};

export default GmailSetup;