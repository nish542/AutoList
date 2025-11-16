import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import Navigation from "@/components/Navigation";
import { ArrowLeft, Check, Download, FileJson, FileText, Sheet, FileCog, Sparkles, Home } from "lucide-react";
import { toast } from "sonner";
import {
  exportAsJSON,
  exportAsCSV,
  exportAsHTML,
  exportAsPDF,
  type ListingData,
} from "@/lib/exportUtils";

const ListingEditor = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const post = location.state?.post;
  const generatedListing = location.state?.listing;

  const [showDownloadDialog, setShowDownloadDialog] = useState(false);

  // Use generated listing if available, otherwise use default
  const [listing, setListing] = useState(
    generatedListing
      ? {
          title: generatedListing.title || "Product Title",
          description: generatedListing.description || "Product description goes here...",
          bulletPoints: generatedListing.bullets || [
            "High-quality materials and construction",
            "Perfect for everyday use",
            "Available in multiple sizes and colors",
            "Easy to maintain and clean",
            "Great value for money",
          ],
          keywords: (generatedListing.search_terms || []).join(", "),
          price: generatedListing.attributes?.price || "29.99",
          category: generatedListing.category || "Home & Kitchen",
          color: generatedListing.attributes?.color || "#ffffff",
          dimensions_size: generatedListing.dimensions_size || "",
          weight: generatedListing.weight || "",
          primary_use: generatedListing.primary_use || "",
          included_items: generatedListing.included_items || "",
        }
      : {
          title: post?.caption?.split("\n")[0]?.substring(0, 100) || "Product Title",
          description: post?.caption || "Product description goes here...",
          bulletPoints: [
            "High-quality materials and construction",
            "Perfect for everyday use",
            "Available in multiple sizes and colors",
            "Easy to maintain and clean",
            "Great value for money",
          ],
          keywords: "product, quality, durable, lifestyle",
          price: "29.99",
          category: "Home & Kitchen",
          color: "#ffffff",
          dimensions_size: "",
          weight: "",
          primary_use: "",
          included_items: "",
        }
  );

  if (!post) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <h2 className="text-2xl font-bold">No post selected</h2>
          <Button onClick={() => navigate("/dashboard")}>
            Return to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  const handleConfirm = () => {
    setShowDownloadDialog(true);
    toast.success("Listing confirmed! Choose your download format.");
  };

  const handleGoHome = () => {
    setShowDownloadDialog(false);
    navigate("/");
  };

  const handleDownload = async (format: "json" | "csv" | "html" | "pdf") => {
    try {
      const filename = `amazon-listing-${Date.now()}`;
      
      switch (format) {
        case "json":
          exportAsJSON(listing as ListingData, `${filename}.json`);
          toast.success("Downloaded as JSON");
          break;
        case "csv":
          exportAsCSV(listing as ListingData, `${filename}.csv`);
          toast.success("Downloaded as CSV");
          break;
        case "html":
          exportAsHTML(listing as ListingData, `${filename}.html`);
          toast.success("Downloaded as HTML");
          break;
        case "pdf":
          await exportAsPDF(listing as ListingData, `${filename}.pdf`);
          toast.success("Downloaded as PDF");
          break;
      }
    } catch (error) {
      console.error("Download error:", error);
      toast.error(
        error instanceof Error ? error.message : "Failed to download listing"
      );
    }
  };

  return (
    <div className="min-h-screen">
      <Navigation />
      
      <div className="pt-32 pb-20 px-6 bg-gradient-to-b from-secondary/20 to-transparent min-h-screen">
        <div className="container mx-auto max-w-7xl">
          <div className="mb-8 space-y-4">
            <Button
              variant="ghost"
              onClick={() => navigate("/dashboard")}
              className="-ml-4 hover:bg-transparent"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Button>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Sparkles className="h-6 w-6 text-accent" />
                <h1 className="text-4xl font-bold">Edit Your Listing</h1>
              </div>
              <p className="text-lg text-muted-foreground">
                Review and refine your AI-generated Amazon listing before exporting
              </p>
            </div>
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Preview Section */}
            <div className="space-y-6 animate-fade-in">
              <Card className="border-none shadow-lg hover:shadow-xl transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="h-5 w-5" />
                    Original Post
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="aspect-square rounded-lg overflow-hidden mb-4 bg-muted group">
                    {post.media_type === "VIDEO" ? (
                      <video
                        src={post.media_url}
                        className="w-full h-full object-cover"
                        controls
                      />
                    ) : (
                      <img
                        src={post.media_url}
                        alt="Instagram post"
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {post.caption}
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Editor Section */}
            <div className="space-y-6 animate-fade-in" style={{ animationDelay: "0.1s" }}>
              <Card className="border-none shadow-lg hover:shadow-xl transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-accent" />
                    Generated Amazon Listing
                  </CardTitle>
                  <p className="text-sm text-muted-foreground">Edit any field to customize your listing</p>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="title" className="text-base font-semibold">Product Title</Label>
                    <Input
                      id="title"
                      value={listing.title}
                      onChange={(e) =>
                        setListing({ ...listing, title: e.target.value })
                      }
                      className="text-lg font-medium"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="description" className="text-base font-semibold">Description</Label>
                    <Textarea
                      id="description"
                      value={listing.description}
                      onChange={(e) =>
                        setListing({ ...listing, description: e.target.value })
                      }
                      rows={6}
                      className="resize-none"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label className="text-base font-semibold">Bullet Points</Label>
                    {listing.bulletPoints.map((point, index) => (
                      <Input
                        key={index}
                        value={point}
                        onChange={(e) => {
                          const newPoints = [...listing.bulletPoints];
                          newPoints[index] = e.target.value;
                          setListing({ ...listing, bulletPoints: newPoints });
                        }}
                        className="mb-2"
                      />
                    ))}
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="price">Price ($)</Label>
                      <Input
                        id="price"
                        value={listing.price}
                        onChange={(e) =>
                          setListing({ ...listing, price: e.target.value })
                        }
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="category">Category</Label>
                      <Input
                        id="category"
                        value={listing.category}
                        onChange={(e) =>
                          setListing({ ...listing, category: e.target.value })
                        }
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="color">Dominant Color</Label>
                      <div className="flex items-center gap-3">
                        <input
                          id="color"
                          type="color"
                          value={listing.color}
                          onChange={(e) => setListing({ ...listing, color: e.target.value })}
                          className="w-12 h-10 p-0 border-none"
                        />
                        <Input
                          value={listing.color}
                          onChange={(e) => setListing({ ...listing, color: e.target.value })}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="dimensions_size">Dimensions / Size</Label>
                    <Input
                      id="dimensions_size"
                      placeholder="e.g., 13.3 inches, 500ml capacity"
                      value={listing.dimensions_size}
                      onChange={(e) =>
                        setListing({ ...listing, dimensions_size: e.target.value })
                      }
                    />
                    <p className="text-xs text-muted-foreground">Auto-filled based on product type. Edit if needed.</p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="weight">Weight</Label>
                    <Input
                      id="weight"
                      placeholder="e.g., 1.2kg, 250g"
                      value={listing.weight}
                      onChange={(e) =>
                        setListing({ ...listing, weight: e.target.value })
                      }
                    />
                    <p className="text-xs text-muted-foreground">Auto-filled with intelligent default. Edit if needed.</p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="primary_use">Primary Use / Purpose</Label>
                    <Input
                      id="primary_use"
                      placeholder="e.g., Home office work, Outdoor sports"
                      value={listing.primary_use}
                      onChange={(e) =>
                        setListing({ ...listing, primary_use: e.target.value })
                      }
                    />
                    <p className="text-xs text-muted-foreground">Auto-filled based on category. Edit if needed.</p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="included_items">What's Included / Accessories</Label>
                    <Input
                      id="included_items"
                      placeholder="e.g., USB cable, Carrying case, Manual"
                      value={listing.included_items}
                      onChange={(e) =>
                        setListing({ ...listing, included_items: e.target.value })
                      }
                    />
                    <p className="text-xs text-muted-foreground">Auto-filled with typical items. Edit if needed.</p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="keywords">Keywords</Label>
                    <Input
                      id="keywords"
                      value={listing.keywords}
                      onChange={(e) =>
                        setListing({ ...listing, keywords: e.target.value })
                      }
                    />
                  </div>

                  <div className="flex gap-3 pt-4">
                    <Button
                      className="flex-1 rounded-full shadow-lg hover:shadow-xl transition-all"
                      size="lg"
                      onClick={handleConfirm}
                    >
                      <Check className="mr-2 h-5 w-5" />
                      Confirm Listing
                    </Button>
                    <Button
                      variant="outline"
                      className="rounded-full"
                      size="lg"
                      onClick={() => navigate("/dashboard")}
                    >
                      Cancel
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Download Dialog */}
          <AlertDialog open={showDownloadDialog} onOpenChange={setShowDownloadDialog}>
            <AlertDialogContent className="max-w-2xl">
              <AlertDialogHeader>
                <AlertDialogTitle className="flex items-center gap-2 text-2xl">
                  <Download className="h-6 w-6 text-accent" />
                  Download Your Listing
                </AlertDialogTitle>
                <AlertDialogDescription className="text-base">
                  Your Amazon listing is ready! Choose your preferred format to download.
                </AlertDialogDescription>
              </AlertDialogHeader>
              
              <div className="space-y-6 py-4">
                {/* Download Format Options */}
                <div className="grid grid-cols-2 gap-4">
                  <Button
                    variant="outline"
                    className="h-auto flex-col gap-3 py-6 hover:bg-accent hover:text-accent-foreground transition-all hover:scale-105"
                    onClick={() => handleDownload("json")}
                  >
                    <FileJson className="h-10 w-10" />
                    <div className="text-center">
                      <div className="font-semibold text-lg">JSON</div>
                      <div className="text-xs text-muted-foreground">Developer format</div>
                    </div>
                  </Button>
                  <Button
                    variant="outline"
                    className="h-auto flex-col gap-3 py-6 hover:bg-accent hover:text-accent-foreground transition-all hover:scale-105"
                    onClick={() => handleDownload("csv")}
                  >
                    <Sheet className="h-10 w-10" />
                    <div className="text-center">
                      <div className="font-semibold text-lg">CSV</div>
                      <div className="text-xs text-muted-foreground">Spreadsheet</div>
                    </div>
                  </Button>
                  <Button
                    variant="outline"
                    className="h-auto flex-col gap-3 py-6 hover:bg-accent hover:text-accent-foreground transition-all hover:scale-105"
                    onClick={() => handleDownload("html")}
                  >
                    <FileText className="h-10 w-10" />
                    <div className="text-center">
                      <div className="font-semibold text-lg">HTML</div>
                      <div className="text-xs text-muted-foreground">Web page</div>
                    </div>
                  </Button>
                  <Button
                    variant="outline"
                    className="h-auto flex-col gap-3 py-6 hover:bg-accent hover:text-accent-foreground transition-all hover:scale-105"
                    onClick={() => handleDownload("pdf")}
                  >
                    <FileCog className="h-10 w-10" />
                    <div className="text-center">
                      <div className="font-semibold text-lg">PDF</div>
                      <div className="text-xs text-muted-foreground">Print ready</div>
                    </div>
                  </Button>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 pt-4 border-t">
                  <Button
                    variant="outline"
                    className="flex-1"
                    onClick={() => setShowDownloadDialog(false)}
                  >
                    Edit More
                  </Button>
                  <Button
                    className="flex-1"
                    onClick={handleGoHome}
                  >
                    <Home className="mr-2 h-4 w-4" />
                    Go to Home
                  </Button>
                </div>
              </div>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </div>
    </div>
  );
};

export default ListingEditor;
