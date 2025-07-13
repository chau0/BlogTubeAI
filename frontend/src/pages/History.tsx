import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import { Search, Download, Trash2, Calendar, Globe, Brain, FileText, RotateCcw, Archive } from "lucide-react";

interface HistoryItem {
  id: string;
  title: string;
  url: string;
  content: string;
  createdAt: string;
  provider: string;
  language: string;
}

const History = () => {
  const navigate = useNavigate();
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [filteredHistory, setFilteredHistory] = useState<HistoryItem[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedProvider, setSelectedProvider] = useState("all");
  const [selectedLanguage, setSelectedLanguage] = useState("all");
  const [selectedItems, setSelectedItems] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState("newest");

  useEffect(() => {
    // Load history from localStorage
    const savedHistory = JSON.parse(localStorage.getItem("conversionHistory") || "[]");
    setHistory(savedHistory);
    setFilteredHistory(savedHistory);
  }, []);

  useEffect(() => {
    // Filter and sort history
    let filtered = history.filter(item => {
      const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           item.url.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesProvider = selectedProvider === "all" || item.provider === selectedProvider;
      const matchesLanguage = selectedLanguage === "all" || item.language === selectedLanguage;
      
      return matchesSearch && matchesProvider && matchesLanguage;
    });

    // Sort results
    filtered.sort((a, b) => {
      switch (sortBy) {
        case "newest":
          return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
        case "oldest":
          return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
        case "title":
          return a.title.localeCompare(b.title);
        default:
          return 0;
      }
    });

    setFilteredHistory(filtered);
  }, [history, searchTerm, selectedProvider, selectedLanguage, sortBy]);

  const handleDownload = (item: HistoryItem) => {
    const blob = new Blob([item.content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${item.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast.success("File downloaded successfully!");
  };

  const handleDelete = (id: string) => {
    const updatedHistory = history.filter(item => item.id !== id);
    setHistory(updatedHistory);
    localStorage.setItem("conversionHistory", JSON.stringify(updatedHistory));
    setSelectedItems(selectedItems.filter(itemId => itemId !== id));
    toast.success("Item deleted successfully!");
  };

  const handleBulkDownload = () => {
    selectedItems.forEach(id => {
      const item = history.find(h => h.id === id);
      if (item) handleDownload(item);
    });
    setSelectedItems([]);
  };

  const handleBulkDelete = () => {
    const updatedHistory = history.filter(item => !selectedItems.includes(item.id));
    setHistory(updatedHistory);
    localStorage.setItem("conversionHistory", JSON.stringify(updatedHistory));
    setSelectedItems([]);
    toast.success(`${selectedItems.length} items deleted successfully!`);
  };

  const handleSelectItem = (id: string, checked: boolean) => {
    if (checked) {
      setSelectedItems([...selectedItems, id]);
    } else {
      setSelectedItems(selectedItems.filter(itemId => itemId !== id));
    }
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedItems(filteredHistory.map(item => item.id));
    } else {
      setSelectedItems([]);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  };

  const getProviderColor = (provider: string) => {
    switch (provider.toLowerCase()) {
      case "gpt-4": return "bg-primary/20 text-primary";
      case "claude": return "bg-accent/20 text-accent";
      case "gemini": return "bg-secondary/20 text-secondary-foreground";
      default: return "bg-muted/20 text-muted-foreground";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-background">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-2">Conversion History</h1>
              <p className="text-muted-foreground">
                Manage and download your previous blog conversions
              </p>
            </div>
            <Button onClick={() => navigate("/")} className="bg-gradient-primary">
              <RotateCcw className="w-4 h-4 mr-2" />
              New Conversion
            </Button>
          </div>

          {/* Filters */}
          <Card className="p-6 bg-card/50 backdrop-blur-sm">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <Input
                  placeholder="Search by title or URL..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <Select value={selectedProvider} onValueChange={setSelectedProvider}>
                <SelectTrigger>
                  <SelectValue placeholder="All Providers" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Providers</SelectItem>
                  <SelectItem value="GPT-4">GPT-4</SelectItem>
                  <SelectItem value="Claude">Claude</SelectItem>
                  <SelectItem value="Gemini">Gemini</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                <SelectTrigger>
                  <SelectValue placeholder="All Languages" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Languages</SelectItem>
                  <SelectItem value="English">English</SelectItem>
                  <SelectItem value="Spanish">Spanish</SelectItem>
                  <SelectItem value="French">French</SelectItem>
                  <SelectItem value="German">German</SelectItem>
                </SelectContent>
              </Select>

              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger>
                  <SelectValue placeholder="Sort by..." />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="newest">Newest First</SelectItem>
                  <SelectItem value="oldest">Oldest First</SelectItem>
                  <SelectItem value="title">Title A-Z</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Bulk Actions */}
            {selectedItems.length > 0 && (
              <div className="flex items-center gap-4 p-4 bg-muted/10 rounded-lg">
                <span className="text-sm text-foreground">
                  {selectedItems.length} item{selectedItems.length !== 1 ? 's' : ''} selected
                </span>
                <Button size="sm" variant="outline" onClick={handleBulkDownload}>
                  <Download className="w-4 h-4 mr-2" />
                  Download All
                </Button>
                <Button size="sm" variant="destructive" onClick={handleBulkDelete}>
                  <Trash2 className="w-4 h-4 mr-2" />
                  Delete All
                </Button>
              </div>
            )}
          </Card>
        </div>

        {/* Results */}
        {filteredHistory.length === 0 ? (
          <Card className="p-12 text-center bg-card/50 backdrop-blur-sm">
            <Archive className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-foreground mb-2">
              {history.length === 0 ? "No Conversions Yet" : "No Results Found"}
            </h3>
            <p className="text-muted-foreground mb-6">
              {history.length === 0 
                ? "Start converting YouTube videos to blog posts to see your history here."
                : "Try adjusting your search filters to find what you're looking for."
              }
            </p>
            {history.length === 0 && (
              <Button onClick={() => navigate("/")} className="bg-gradient-primary">
                <RotateCcw className="w-4 h-4 mr-2" />
                Start Your First Conversion
              </Button>
            )}
          </Card>
        ) : (
          <div className="space-y-4">
            {/* Select All */}
            <div className="flex items-center gap-2 px-2">
              <Checkbox
                checked={selectedItems.length === filteredHistory.length}
                onCheckedChange={handleSelectAll}
              />
              <span className="text-sm text-muted-foreground">
                Select all ({filteredHistory.length} items)
              </span>
            </div>

            {/* History Items */}
            {filteredHistory.map((item) => (
              <Card key={item.id} className="p-6 bg-card/50 backdrop-blur-sm hover:bg-card/70 transition-colors">
                <div className="flex items-start gap-4">
                  <Checkbox
                    checked={selectedItems.includes(item.id)}
                    onCheckedChange={(checked) => handleSelectItem(item.id, checked as boolean)}
                  />
                  
                  <div className="w-12 h-12 bg-gradient-primary rounded-lg flex items-center justify-center flex-shrink-0">
                    <FileText className="w-6 h-6 text-primary-foreground" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-foreground truncate pr-4">
                        {item.title}
                      </h3>
                      <div className="flex items-center gap-2 flex-shrink-0">
                        <Badge className={getProviderColor(item.provider)}>
                          <Brain className="w-3 h-3 mr-1" />
                          {item.provider}
                        </Badge>
                        <Badge variant="outline">
                          <Globe className="w-3 h-3 mr-1" />
                          {item.language}
                        </Badge>
                      </div>
                    </div>
                    
                    <p className="text-sm text-muted-foreground mb-3 truncate">
                      {item.url}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {formatDate(item.createdAt)}
                        </span>
                        <span>{item.content.split(' ').length} words</span>
                      </div>
                      
                      <div className="flex gap-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => handleDownload(item)}
                        >
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </Button>
                        <Button 
                          size="sm" 
                          variant="destructive" 
                          onClick={() => handleDelete(item.id)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default History;