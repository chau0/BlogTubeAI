import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { CheckCircle, Clock, Loader2, Play, X } from "lucide-react";

interface ProcessingStep {
  id: string;
  title: string;
  description: string;
  status: "pending" | "processing" | "completed" | "error";
}

const Processing = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [estimatedTime, setEstimatedTime] = useState(120); // seconds
  const [isProcessing, setIsProcessing] = useState(true);

  const steps: ProcessingStep[] = [
    {
      id: "validate",
      title: "Validating URL",
      description: "Checking YouTube video accessibility",
      status: "completed"
    },
    {
      id: "info",
      title: "Fetching Video Info",
      description: "Getting video metadata and details",
      status: "completed"
    },
    {
      id: "transcript",
      title: "Getting Transcript",
      description: "Extracting audio and generating transcript",
      status: "processing"
    },
    {
      id: "generate",
      title: "Generating Blog",
      description: "AI processing content into blog format",
      status: "pending"
    },
    {
      id: "format",
      title: "Formatting Output",
      description: "Finalizing markdown and styling",
      status: "pending"
    }
  ];

  const videoUrl = searchParams.get("url");
  const videoTitle = searchParams.get("title");

  useEffect(() => {
    if (!videoUrl) {
      navigate("/");
      return;
    }

    // Simulate processing with realistic timing
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 1;
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsProcessing(false);
          // Navigate to results after completion
          setTimeout(() => {
            navigate(`/result?url=${encodeURIComponent(videoUrl)}&title=${encodeURIComponent(videoTitle || "")}`);
          }, 1000);
        }
        return newProgress;
      });
    }, 1200); // ~2 minutes total

    // Update steps based on progress
    const stepInterval = setInterval(() => {
      setCurrentStep(prev => {
        const nextStep = Math.min(prev + 1, steps.length - 1);
        setEstimatedTime(prev => Math.max(0, prev - 30));
        return nextStep;
      });
    }, 24000); // Update every 24 seconds

    return () => {
      clearInterval(interval);
      clearInterval(stepInterval);
    };
  }, [videoUrl, navigate, videoTitle]);

  const handleCancel = () => {
    navigate("/");
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-gradient-background flex items-center justify-center p-6">
      <div className="max-w-2xl w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-primary rounded-full flex items-center justify-center mx-auto mb-4 shadow-glow">
            <Play className="w-8 h-8 text-primary-foreground" />
          </div>
          <h1 className="text-3xl font-bold text-foreground mb-2">Converting Your Video</h1>
          <p className="text-muted-foreground">
            {videoTitle ? `"${videoTitle}"` : "Processing your YouTube video into a blog post"}
          </p>
        </div>

        {/* Progress Card */}
        <Card className="p-8 bg-card/50 backdrop-blur-sm border-border shadow-elegant">
          <div className="space-y-6">
            {/* Progress Bar */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-foreground font-medium">{Math.round(progress)}% Complete</span>
                <span className="text-muted-foreground">
                  Est. {formatTime(estimatedTime)} remaining
                </span>
              </div>
              <Progress value={progress} className="h-3" />
            </div>

            {/* Steps */}
            <div className="space-y-4">
              {steps.map((step, index) => {
                const isActive = index === currentStep;
                const isCompleted = index < currentStep;
                const isFuture = index > currentStep;

                return (
                  <div
                    key={step.id}
                    className={`flex items-center gap-4 p-4 rounded-lg transition-all duration-300 ${
                      isActive 
                        ? "bg-primary/10 border border-primary/20" 
                        : isCompleted 
                        ? "bg-accent/5" 
                        : "bg-muted/5"
                    }`}
                  >
                    <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                      isCompleted 
                        ? "bg-accent text-accent-foreground" 
                        : isActive 
                        ? "bg-primary text-primary-foreground" 
                        : "bg-muted text-muted-foreground"
                    }`}>
                      {isCompleted ? (
                        <CheckCircle className="w-5 h-5" />
                      ) : isActive ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                      ) : (
                        <Clock className="w-5 h-5" />
                      )}
                    </div>
                    <div className="flex-1">
                      <h3 className={`font-medium ${isActive || isCompleted ? "text-foreground" : "text-muted-foreground"}`}>
                        {step.title}
                      </h3>
                      <p className="text-sm text-muted-foreground">{step.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Cancel Button */}
            <div className="pt-4 border-t border-border">
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button variant="outline" className="w-full">
                    <X className="w-4 h-4 mr-2" />
                    Cancel Conversion
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Cancel Conversion?</AlertDialogTitle>
                    <AlertDialogDescription>
                      Are you sure you want to cancel this conversion? All progress will be lost and you'll be redirected to the home page.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Continue Processing</AlertDialogCancel>
                    <AlertDialogAction onClick={handleCancel} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                      Cancel Conversion
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Processing;