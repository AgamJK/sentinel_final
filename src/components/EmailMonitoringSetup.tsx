import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Eye, EyeOff, Mail, MessageSquare, Shield, InfoIcon, CheckCircle2 } from "lucide-react";

interface EmailConfig {
  email: string;
  appPassword: string;
  telegramUserId: string;
}

interface EmailMonitoringSetupProps {
  onConfigSaved: (config: EmailConfig) => void;
  existingConfig?: EmailConfig | null;
}

const EmailMonitoringSetup = ({ onConfigSaved, existingConfig }: EmailMonitoringSetupProps) => {
  const [config, setConfig] = useState<EmailConfig>({
    email: existingConfig?.email || '',
    appPassword: existingConfig?.appPassword || '',
    telegramUserId: existingConfig?.telegramUserId || ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleInputChange = (field: keyof EmailConfig, value: string) => {
    setConfig(prev => ({ ...prev, [field]: value }));
    setError(null);
    setSuccess(false);
  };

  const validateConfig = () => {
    if (!config.email.trim()) {
      setError("Email address is required");
      return false;
    }
    if (!config.email.includes('@')) {
      setError("Please enter a valid email address");
      return false;
    }
    if (!config.appPassword.trim()) {
      setError("App password is required");
      return false;
    }
    if (config.appPassword.length < 4) {
      setError("App password must be at least 4 characters long");
      return false;
    }
    if (!config.telegramUserId.trim()) {
      setError("Telegram User ID is required");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log("Form submitted with config:", config);
    
    if (!validateConfig()) {
      console.log("Validation failed");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      console.log("Sending request to backend...");
      
      // Save configuration to backend (backend will handle data reset automatically)
      const response = await fetch('http://localhost:5000/api/email-config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config),
      });

      console.log("Response received:", response.status);

      if (!response.ok) {
        const errorData = await response.text();
        console.error("Response error:", errorData);
        throw new Error(`Failed to save email configuration: ${response.status}`);
      }

      const result = await response.json();
      console.log("Success result:", result);
      
      // Check if data was reset due to new configuration
      if (result.data_reset) {
        console.log("✅ Data was automatically reset due to new email/password configuration");
      }
      
      setSuccess(true);
      onConfigSaved(config);
      
    } catch (err) {
      console.error("Error saving config:", err);
      setError(err instanceof Error ? err.message : 'Failed to save configuration');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="bg-gradient-card border-border glow-primary">
      <CardHeader>
        <CardTitle className="text-2xl font-semibold text-foreground flex items-center">
          <Mail className="mr-3 text-primary" size={24} />
          Email Monitoring Setup
        </CardTitle>
        <CardDescription className="text-muted-foreground">
          Configure your email monitoring settings to start tracking customer sentiment
        </CardDescription>
      </CardHeader>
      
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {success && (
            <Alert className="border-green-500 bg-green-500/10">
              <CheckCircle2 className="h-4 w-4" />
              <AlertDescription className="text-green-600">
                ✅ Configuration saved successfully! Data has been reset to start from zero.
                Your email monitoring is now ready to begin fresh tracking.
              </AlertDescription>
            </Alert>
          )}

          {error && (
            <Alert className="border-destructive bg-destructive/10">
              <InfoIcon className="h-4 w-4" />
              <AlertDescription className="text-destructive">
                {error}
              </AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert className="border-green-500 bg-green-500/10">
              <InfoIcon className="h-4 w-4" />
              <AlertDescription className="text-green-600">
                Configuration saved successfully! You can now start monitoring.
              </AlertDescription>
            </Alert>
          )}

          {/* Email Address */}
          <div className="space-y-2">
            <Label htmlFor="email" className="text-sm font-medium text-foreground">
              Gmail Address
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="your.email@gmail.com"
              value={config.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              className="bg-input border-border"
              required
            />
            <p className="text-xs text-muted-foreground">
              The Gmail account you want to monitor for customer emails
            </p>
          </div>

          {/* App Password */}
          <div className="space-y-2">
            <Label htmlFor="appPassword" className="text-sm font-medium text-foreground">
              Gmail App Password
            </Label>
            <div className="relative">
              <Input
                id="appPassword"
                type={showPassword ? "text" : "password"}
                placeholder="xxxx xxxx xxxx xxxx"
                value={config.appPassword}
                onChange={(e) => handleInputChange('appPassword', e.target.value)}
                className="bg-input border-border pr-10"
                required
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <Eye className="h-4 w-4 text-muted-foreground" />
                )}
              </Button>
            </div>
            <div className="text-xs text-muted-foreground space-y-1">
              <p>• Generate an App Password from your Google Account settings</p>
              <p>• Go to Account → Security → 2-Step Verification → App passwords</p>
              <p>• Select "Mail" and your device to generate the password</p>
            </div>
          </div>

          {/* Telegram User ID */}
          <div className="space-y-2">
            <Label htmlFor="telegramUserId" className="text-sm font-medium text-foreground">
              Telegram User ID
            </Label>
            <Input
              id="telegramUserId"
              type="text"
              placeholder="123456789"
              value={config.telegramUserId}
              onChange={(e) => handleInputChange('telegramUserId', e.target.value)}
              className="bg-input border-border"
              required
            />
            <div className="text-xs text-muted-foreground space-y-1">
              <p>• Message @userinfobot on Telegram to get your User ID</p>
              <p>• Used for sending real-time sentiment alerts</p>
            </div>
          </div>

          {/* Security Notice */}
          <Alert className="border-blue-500 bg-blue-500/10">
            <Shield className="h-4 w-4" />
            <AlertDescription className="text-blue-600">
              Your credentials are securely encrypted and stored. We only use them to monitor your specified email account.
            </AlertDescription>
          </Alert>

          {/* Submit Button */}
          <div className="pt-4">
            <Button 
              type="submit" 
              className="w-full cta-button text-lg py-6"
              disabled={loading}
              onClick={(e) => {
                console.log("Button clicked!", { loading, config });
              }}
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Saving Configuration...
                </>
              ) : (
                <>
                  <MessageSquare className="mr-2" size={20} />
                  Save & Start Monitoring
                </>
              )}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default EmailMonitoringSetup;
