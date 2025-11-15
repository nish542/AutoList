import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import Navigation from "@/components/Navigation";
import { ArrowLeft, Check, Download, FileJson, FileText, Sheet } from "lucide-react";
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
    toast.success("Listing confirmed successfully!");
    setTimeout(() => {
      navigate("/dashboard");
    }, 1500);
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
      
      <div className="pt-32 pb-20 px-6">
        <div className="container mx-auto max-w-7xl">
          <Button
            variant="ghost"
            className="mb-8"
            onClick={() => navigate("/dashboard")}
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Dashboard
          </Button>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Preview Section */}
            <div className="space-y-6 animate-fade-in">
              <Card className="border-none shadow-lg">
                <CardHeader>
                  <CardTitle>Original Post</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="aspect-square rounded-lg overflow-hidden mb-4 bg-muted">
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
                        className="w-full h-full object-cover"
                      />
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {post.caption}
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Editor Section */}
            <div className="space-y-6 animate-fade-in" style={{ animationDelay: "0.1s" }}>
              <Card className="border-none shadow-lg">
                <CardHeader>
                  <CardTitle>Generated Amazon Listing</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="title">Product Title</Label>
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
                    <Label htmlFor="description">Description</Label>
                    <Textarea
                      id="description"
                      value={listing.description}
                      onChange={(e) =>
                        setListing({ ...listing, description: e.target.value })
                      }
                      rows={6}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label>Bullet Points</Label>
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
                    <Label htmlFor="keywords">Keywords</Label>
                    <Input
                      id="keywords"
                      value={listing.keywords}
                      onChange={(e) =>
                        setListing({ ...listing, keywords: e.target.value })
                      }
                    />
                  </div>

                  {/* Download Section */}
                  <div className="space-y-3 pt-4 border-t">
                    <p className="text-sm font-medium text-muted-foreground">Download Listing</p>
                    <div className="grid grid-cols-2 gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="rounded-lg"
                        onClick={() => handleDownload("json")}
                      >
                        <FileJson className="mr-2 h-4 w-4" />
                        JSON
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="rounded-lg"
                        onClick={() => handleDownload("csv")}
                      >
                        <Sheet className="mr-2 h-4 w-4" />
                        CSV
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="rounded-lg"
                        onClick={() => handleDownload("html")}
                      >
                        <FileText className="mr-2 h-4 w-4" />
                        HTML
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="rounded-lg"
                        onClick={() => handleDownload("pdf")}
                      >
                        <Download className="mr-2 h-4 w-4" />
                        PDF
                      </Button>
                    </div>
                  </div>

                  <div className="flex gap-3 pt-4">
                    <Button
                      className="flex-1 rounded-full"
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
        </div>
      </div>
    </div>
  );
};

export default ListingEditor;
