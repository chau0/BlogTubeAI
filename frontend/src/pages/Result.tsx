import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "sonner";
import { Download, Edit3, Share2, RotateCcw, Copy, FileText, FileDown, Globe } from "lucide-react";

const Result = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [isEditing, setIsEditing] = useState(false);
  const [blogContent, setBlogContent] = useState(`# The Future of AI: Transforming Our Digital World

In today's rapidly evolving technological landscape, artificial intelligence has emerged as a transformative force that's reshaping industries, redefining human interaction with technology, and opening doors to possibilities we once thought were purely science fiction.

## Understanding AI's Current Impact

Artificial Intelligence is no longer a distant concept confined to research labs and sci-fi movies. It's actively integrated into our daily lives through:

- **Smart assistants** that understand and respond to natural language
- **Recommendation systems** that personalize our online experiences
- **Autonomous vehicles** that promise to revolutionize transportation
- **Medical diagnosis tools** that assist healthcare professionals

## Key Developments and Breakthroughs

### Machine Learning Revolution

The advancement in machine learning algorithms has enabled computers to learn from data without explicit programming. This breakthrough has led to:

1. **Improved accuracy** in pattern recognition
2. **Better decision-making** capabilities
3. **Enhanced automation** across various sectors

### Natural Language Processing

The development of sophisticated NLP models has transformed how machines understand and generate human language, making interactions more intuitive and natural.

## Future Implications

As we look toward the future, AI promises to:

- Accelerate scientific research and discovery
- Enhance creative processes and artistic expression
- Solve complex global challenges like climate change
- Create new job categories while transforming existing ones

## Challenges and Considerations

While the potential is immense, we must address:

- **Ethical implications** of AI decision-making
- **Privacy concerns** related to data usage
- **Economic disruption** and job displacement
- **Regulatory frameworks** for responsible AI development

## Conclusion

The AI revolution is not just about technology—it's about reimagining what's possible. As we navigate this transformation, the key lies in embracing AI's potential while thoughtfully addressing its challenges. The future belongs to those who can harness AI's power responsibly and creatively.

---

*This blog post was generated from a YouTube video using AI technology, demonstrating the very capabilities discussed within.*`);

  const videoUrl = searchParams.get("url");
  const videoTitle = searchParams.get("title") || "Untitled Video";

  const handleDownload = (format: string) => {
    const blob = new Blob([blogContent], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `blog-post.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast.success(`Blog post downloaded as ${format.toUpperCase()}`);
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(blogContent);
    toast.success("Blog content copied to clipboard!");
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: "Generated Blog Post",
        text: blogContent.substring(0, 100) + "...",
        url: window.location.href,
      });
    } else {
      handleCopyToClipboard();
    }
  };

  const handleSaveToHistory = () => {
    // In a real app, this would save to a backend or localStorage
    const historyItem = {
      id: Date.now().toString(),
      title: videoTitle,
      url: videoUrl,
      content: blogContent,
      createdAt: new Date().toISOString(),
      provider: "GPT-4",
      language: "English"
    };
    
    const existingHistory = JSON.parse(localStorage.getItem("conversionHistory") || "[]");
    existingHistory.unshift(historyItem);
    localStorage.setItem("conversionHistory", JSON.stringify(existingHistory));
    
    toast.success("Blog post saved to history!");
  };

  return (
    <div className="min-h-screen bg-gradient-background">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-2">Conversion Complete!</h1>
              <p className="text-muted-foreground">Your blog post is ready for review and download</p>
            </div>
            <Badge variant="secondary" className="bg-accent/20 text-accent-foreground">
              Success
            </Badge>
          </div>
          
          {/* Video Info */}
          <Card className="p-4 bg-card/50 backdrop-blur-sm">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-primary rounded-lg flex items-center justify-center">
                <FileText className="w-8 h-8 text-primary-foreground" />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-foreground">{videoTitle}</h3>
                <p className="text-sm text-muted-foreground">{videoUrl}</p>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={() => navigate("/")}>
                  <RotateCcw className="w-4 h-4 mr-2" />
                  Convert Another
                </Button>
              </div>
            </div>
          </Card>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <Card className="bg-card/50 backdrop-blur-sm">
              <Tabs defaultValue="preview" className="w-full">
                <div className="p-6 pb-0">
                  <div className="flex items-center justify-between mb-4">
                    <TabsList>
                      <TabsTrigger value="preview">Preview</TabsTrigger>
                      <TabsTrigger value="edit">Edit</TabsTrigger>
                    </TabsList>
                    <Button variant="ghost" size="sm" onClick={handleCopyToClipboard}>
                      <Copy className="w-4 h-4 mr-2" />
                      Copy
                    </Button>
                  </div>
                </div>

                <TabsContent value="preview" className="p-6 pt-0">
                  <div className="prose prose-invert max-w-none">
                    <div 
                      className="text-foreground"
                      dangerouslySetInnerHTML={{ 
                        __html: blogContent
                          .replace(/^# (.*$)/gm, '<h1 class="text-2xl font-bold mb-4 text-foreground">$1</h1>')
                          .replace(/^## (.*$)/gm, '<h2 class="text-xl font-semibold mb-3 mt-6 text-foreground">$1</h2>')
                          .replace(/^### (.*$)/gm, '<h3 class="text-lg font-medium mb-2 mt-4 text-foreground">$3</h3>')
                          .replace(/^\* (.*$)/gm, '<li class="mb-1 text-muted-foreground">$1</li>')
                          .replace(/^- (.*$)/gm, '<li class="mb-1 text-muted-foreground">$1</li>')
                          .replace(/^\d+\. (.*$)/gm, '<li class="mb-1 text-muted-foreground">$1</li>')
                          .replace(/\*\*(.*?)\*\*/g, '<strong class="text-foreground">$1</strong>')
                          .replace(/\*(.*?)\*/g, '<em class="text-muted-foreground">$1</em>')
                          .replace(/\n\n/g, '</p><p class="mb-4 text-muted-foreground">')
                          .replace(/^(?!<[h|l])/gm, '<p class="mb-4 text-muted-foreground">')
                      }}
                    />
                  </div>
                </TabsContent>

                <TabsContent value="edit" className="p-6 pt-0">
                  <div className="space-y-4">
                    <Textarea
                      value={blogContent}
                      onChange={(e) => setBlogContent(e.target.value)}
                      className="min-h-[600px] font-mono text-sm"
                      placeholder="Edit your blog content here..."
                    />
                    <div className="flex gap-2">
                      <Button onClick={() => setIsEditing(false)} variant="outline">
                        <Edit3 className="w-4 h-4 mr-2" />
                        Preview Changes
                      </Button>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </Card>
          </div>

          {/* Sidebar Actions */}
          <div className="space-y-6">
            {/* Download Options */}
            <Card className="p-6 bg-card/50 backdrop-blur-sm">
              <h3 className="font-semibold text-foreground mb-4">Download Options</h3>
              <div className="space-y-3">
                <Button 
                  onClick={() => handleDownload("md")} 
                  className="w-full justify-start"
                  variant="outline"
                >
                  <FileText className="w-4 h-4 mr-2" />
                  Markdown (.md)
                </Button>
                <Button 
                  onClick={() => handleDownload("txt")} 
                  className="w-full justify-start"
                  variant="outline"
                >
                  <FileDown className="w-4 h-4 mr-2" />
                  Plain Text (.txt)
                </Button>
                <Button 
                  onClick={() => handleDownload("html")} 
                  className="w-full justify-start"
                  variant="outline"
                >
                  <Globe className="w-4 h-4 mr-2" />
                  HTML (.html)
                </Button>
              </div>
            </Card>

            {/* Share Options */}
            <Card className="p-6 bg-card/50 backdrop-blur-sm">
              <h3 className="font-semibold text-foreground mb-4">Share & Save</h3>
              <div className="space-y-3">
                <Button onClick={handleShare} className="w-full justify-start" variant="outline">
                  <Share2 className="w-4 h-4 mr-2" />
                  Share Content
                </Button>
                <Button onClick={handleSaveToHistory} className="w-full justify-start">
                  <Download className="w-4 h-4 mr-2" />
                  Save to History
                </Button>
              </div>
            </Card>

            {/* Conversion Stats */}
            <Card className="p-6 bg-card/50 backdrop-blur-sm">
              <h3 className="font-semibold text-foreground mb-4">Conversion Details</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Processing Time:</span>
                  <span className="text-foreground">2m 14s</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Word Count:</span>
                  <span className="text-foreground">347 words</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Provider:</span>
                  <span className="text-foreground">GPT-4</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Language:</span>
                  <span className="text-foreground">English</span>
                </div>
              </div>
            </Card>

            {/* Quick Actions */}
            <div className="space-y-3">
              <Button 
                onClick={() => navigate("/")} 
                className="w-full bg-gradient-primary hover:opacity-90"
              >
                <RotateCcw className="w-4 h-4 mr-2" />
                Convert Another Video
              </Button>
              <Button 
                onClick={() => navigate("/history")} 
                variant="outline" 
                className="w-full"
              >
                View Conversion History
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Result;