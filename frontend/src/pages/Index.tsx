import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Play, ChevronDown, Globe, Brain, Settings, CheckCircle, Loader2, History } from "lucide-react";

interface VideoInfo {
  title: string;
  thumbnail: string;
  duration: string;
  channelName: string;
}

const Index = () => {
  const navigate = useNavigate();
  const [url, setUrl] = useState("");
  const [isValidating, setIsValidating] = useState(false);
  const [videoInfo, setVideoInfo] = useState<VideoInfo | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState("auto");
  const [selectedProvider, setSelectedProvider] = useState("gpt-4");
  const [customFilename, setCustomFilename] = useState("");
  const [proxySettings, setProxySettings] = useState("");
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Mock video validation
  useEffect(() => {
    const validateUrl = async () => {
      if (!url || !url.includes("youtube.com") && !url.includes("youtu.be")) {
        setVideoInfo(null);
        return;
      }

      setIsValidating(true);
      
      // Simulate API call
      setTimeout(() => {
        setVideoInfo({
          title: "The Future of AI: Transforming Our Digital World",
          thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
          duration: "15:32",
          channelName: "Tech Insights"
        });
        setIsValidating(false);
      }, 1000);
    };

    const debounce = setTimeout(validateUrl, 500);
    return () => clearTimeout(debounce);
  }, [url]);

  const handleSubmit = () => {
    if (!videoInfo) {
      toast.error("Please enter a valid YouTube URL");
      return;
    }

    setIsSubmitting(true);
    
    // Simulate form submission
    setTimeout(() => {
      navigate(`/processing?url=${encodeURIComponent(url)}&title=${encodeURIComponent(videoInfo.title)}`);
    }, 800);
  };

  const isValidUrl = url && (url.includes("youtube.com") || url.includes("youtu.be"));

  return (
    <div className="min-h-screen bg-gradient-background">
      <div className="max-w-4xl mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-12 pt-8">
          <div className="w-20 h-20 bg-gradient-primary rounded-full flex items-center justify-center mx-auto mb-6 shadow-glow">
            <Play className="w-10 h-10 text-primary-foreground" />
          </div>
          <h1 className="text-4xl font-bold text-foreground mb-4">
            YouTube to Blog Converter
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Transform any YouTube video into a well-structured blog post using advanced AI technology
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* URL Input */}
            <Card className="p-8 bg-card/50 backdrop-blur-sm shadow-elegant">
              <div className="space-y-4">
                <div>
                  <Label htmlFor="url" className="text-lg font-semibold text-foreground">
                    YouTube URL
                  </Label>
                  <p className="text-sm text-muted-foreground mb-3">
                    Paste the YouTube video URL you want to convert
                  </p>
                </div>
                
                <div className="relative">
                  <Input
                    id="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://www.youtube.com/watch?v=..."
                    className="text-lg h-14 pr-12"
                  />
                  {isValidating && (
                    <Loader2 className="absolute right-4 top-1/2 transform -translate-y-1/2 w-5 h-5 animate-spin text-muted-foreground" />
                  )}
                  {videoInfo && !isValidating && (
                    <CheckCircle className="absolute right-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-accent" />
                  )}
                </div>

                {/* Video Preview */}
                {videoInfo && (
                  <div className="mt-6 p-4 bg-accent/5 border border-accent/20 rounded-lg">
                    <div className="flex items-center gap-4">
                      <img 
                        src={videoInfo.thumbnail} 
                        alt="Video thumbnail"
                        className="w-24 h-18 object-cover rounded"
                        onError={(e) => {
                          e.currentTarget.src = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjEwMCIgaGVpZ2h0PSIxMDAiIGZpbGw9IiNmMGYwZjAiLz48cGF0aCBkPSJNNDAgMzBMMTAgNjBINDBWMzBaIiBmaWxsPSIjZDBkMGQwIi8+PC9zdmc+";
                        }}
                      />
                      <div className="flex-1">
                        <h3 className="font-semibold text-foreground mb-1">
                          {videoInfo.title}
                        </h3>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span>{videoInfo.channelName}</span>
                          <span>•</span>
                          <span>{videoInfo.duration}</span>
                        </div>
                      </div>
                      <Badge className="bg-accent/20 text-accent">
                        Valid
                      </Badge>
                    </div>
                  </div>
                )}
              </div>
            </Card>

            {/* Language & Provider Selection */}
            <Card className="p-8 bg-card/50 backdrop-blur-sm shadow-elegant">
              <div className="grid md:grid-cols-2 gap-8">
                {/* Language Selection */}
                <div className="space-y-4">
                  <div>
                    <Label className="text-lg font-semibold text-foreground flex items-center gap-2">
                      <Globe className="w-5 h-5" />
                      Transcript Language
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Choose the video's language for transcription
                    </p>
                  </div>
                  
                  <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                    <SelectTrigger className="h-12">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="auto">Auto-detect</SelectItem>
                      <SelectItem value="en">English</SelectItem>
                      <SelectItem value="es">Spanish</SelectItem>
                      <SelectItem value="fr">French</SelectItem>
                      <SelectItem value="de">German</SelectItem>
                      <SelectItem value="it">Italian</SelectItem>
                      <SelectItem value="pt">Portuguese</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* LLM Provider Selection */}
                <div className="space-y-4">
                  <div>
                    <Label className="text-lg font-semibold text-foreground flex items-center gap-2">
                      <Brain className="w-5 h-5" />
                      AI Provider
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Select the AI model for content generation
                    </p>
                  </div>
                  
                  <RadioGroup value={selectedProvider} onValueChange={setSelectedProvider}>
                    <div className="space-y-3">
                      <div className="flex items-center space-x-3 p-3 bg-primary/5 border border-primary/20 rounded-lg">
                        <RadioGroupItem value="gpt-4" id="gpt-4" />
                        <div className="flex-1">
                          <Label htmlFor="gpt-4" className="font-medium text-foreground">GPT-4</Label>
                          <p className="text-xs text-muted-foreground">Best for creative and detailed content</p>
                        </div>
                        <Badge className="bg-primary/20 text-primary">Recommended</Badge>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-3 border border-border rounded-lg">
                        <RadioGroupItem value="claude" id="claude" />
                        <div className="flex-1">
                          <Label htmlFor="claude" className="font-medium text-foreground">Claude</Label>
                          <p className="text-xs text-muted-foreground">Excellent for structured analysis</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-3 border border-border rounded-lg">
                        <RadioGroupItem value="gemini" id="gemini" />
                        <div className="flex-1">
                          <Label htmlFor="gemini" className="font-medium text-foreground">Gemini</Label>
                          <p className="text-xs text-muted-foreground">Fast processing, good quality</p>
                        </div>
                      </div>
                    </div>
                  </RadioGroup>
                </div>
              </div>
            </Card>

            {/* Advanced Options */}
            <Collapsible open={showAdvanced} onOpenChange={setShowAdvanced}>
              <CollapsibleTrigger asChild>
                <Card className="p-6 bg-card/30 backdrop-blur-sm cursor-pointer hover:bg-card/50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Settings className="w-5 h-5 text-muted-foreground" />
                      <span className="font-medium text-foreground">Advanced Options</span>
                    </div>
                    <ChevronDown className={`w-5 h-5 text-muted-foreground transition-transform ${showAdvanced ? 'rotate-180' : ''}`} />
                  </div>
                </Card>
              </CollapsibleTrigger>
              
              <CollapsibleContent>
                <Card className="p-6 bg-card/50 backdrop-blur-sm shadow-elegant mt-2">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label htmlFor="filename" className="text-foreground">Custom Filename</Label>
                      <Input
                        id="filename"
                        value={customFilename}
                        onChange={(e) => setCustomFilename(e.target.value)}
                        placeholder="my-blog-post"
                      />
                      <p className="text-xs text-muted-foreground">Leave empty for auto-generated name</p>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="proxy" className="text-foreground">Proxy Settings</Label>
                      <Input
                        id="proxy"
                        value={proxySettings}
                        onChange={(e) => setProxySettings(e.target.value)}
                        placeholder="http://proxy.company.com:8080"
                      />
                      <p className="text-xs text-muted-foreground">For enterprise users only</p>
                    </div>
                  </div>
                </Card>
              </CollapsibleContent>
            </Collapsible>

            {/* Submit Button */}
            <Card className="p-8 bg-card/50 backdrop-blur-sm shadow-elegant">
              <Button
                onClick={handleSubmit}
                disabled={!isValidUrl || !videoInfo || isSubmitting}
                className="w-full h-14 text-lg bg-gradient-primary hover:opacity-90"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Starting Conversion...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5 mr-2" />
                    Convert to Blog Post
                  </>
                )}
              </Button>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <Card className="p-6 bg-card/50 backdrop-blur-sm shadow-elegant">
              <h3 className="font-semibold text-foreground mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <Button 
                  onClick={() => navigate("/history")} 
                  variant="outline" 
                  className="w-full justify-start"
                >
                  <History className="w-4 h-4 mr-2" />
                  View History
                </Button>
              </div>
            </Card>

            {/* Features */}
            <Card className="p-6 bg-card/50 backdrop-blur-sm shadow-elegant">
              <h3 className="font-semibold text-foreground mb-4">What You Get</h3>
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-accent mt-0.5" />
                  <div>
                    <p className="font-medium text-foreground">AI-Powered Content</p>
                    <p className="text-sm text-muted-foreground">Professional blog posts with proper structure</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-accent mt-0.5" />
                  <div>
                    <p className="font-medium text-foreground">Multiple Formats</p>
                    <p className="text-sm text-muted-foreground">Download as Markdown, HTML, or plain text</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-accent mt-0.5" />
                  <div>
                    <p className="font-medium text-foreground">Editable Output</p>
                    <p className="text-sm text-muted-foreground">Customize and refine before downloading</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-accent mt-0.5" />
                  <div>
                    <p className="font-medium text-foreground">History Tracking</p>
                    <p className="text-sm text-muted-foreground">Access all your previous conversions</p>
                  </div>
                </div>
              </div>
            </Card>

            {/* Supported Languages */}
            <Card className="p-6 bg-card/50 backdrop-blur-sm shadow-elegant">
              <h3 className="font-semibold text-foreground mb-4">Supported Languages</h3>
              <div className="flex flex-wrap gap-2">
                {["English", "Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Korean"].map((lang) => (
                  <Badge key={lang} variant="outline" className="text-xs">
                    {lang}
                  </Badge>
                ))}
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
