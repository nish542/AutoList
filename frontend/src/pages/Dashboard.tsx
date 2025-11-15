import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Navigation from "@/components/Navigation";
import { Instagram, Loader2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { generateListing as apiGenerateListing } from "@/services/api";

interface InstagramPost {
  id: string;
  caption: string;
  media_type: string;
  media_url: string;
  permalink: string;
  timestamp: string;
  username?: string;
}

const Dashboard = () => {
  const [posts, setPosts] = useState<InstagramPost[]>([]);
  const [loading, setLoading] = useState(false);
  const [generatingId, setGeneratingId] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchInstagramPosts = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        "https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,permalink,timestamp&access_token=IGAAf4avVPanxBZAFRFZAUxRZA2x0c0tXWGJnVlpLb3k3c19jOXl6a2l3TGdTUWszWVV6MEpNdGJfTG85c1BYMkVuLUxxZAXpnZAkpHNXFuY19UWVFYdzNpWEpfR245ODRWaUNGbldiRmVaTldfSkVNRDVLb0VpSjB1V3MxbllJeXktbwZDZD"
      );
      const data = await response.json();
      
      if (data.data) {
        setPosts(data.data);
        toast.success(`Loaded ${data.data.length} posts successfully!`);
      } else {
        toast.error("Failed to fetch posts. Please check your access token.");
      }
    } catch (error) {
      toast.error("Error fetching Instagram posts");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const generateListing = async (post: InstagramPost) => {
    setGeneratingId(post.id);
    try {
      // Fetch the image from Instagram URL and convert to File
      let imageFile: File | undefined;
      if (post.media_url && post.media_type === "IMAGE") {
        try {
          const imageResponse = await fetch(post.media_url);
          const imageBlob = await imageResponse.blob();
          imageFile = new File([imageBlob], "instagram-post.jpg", {
            type: "image/jpeg",
          });
        } catch (imageError) {
          console.warn("Failed to fetch image:", imageError);
          // Continue without image
        }
      }

      const response = await apiGenerateListing({
        text_content: post.caption || "",
        images: imageFile ? [imageFile] : undefined,
      });

      if (!response.success) {
        throw new Error(response.error || "Failed to generate listing");
      }

      navigate("/listing-editor", { state: { post, listing: response.listing } });
      toast.success("Listing generated successfully!");
    } catch (error) {
      console.error("Error generating listing:", error);
      toast.error(
        error instanceof Error
          ? error.message
          : "Failed to generate listing. Please try again."
      );
      setGeneratingId(null);
    }
  };

  return (
    <div className="min-h-screen">
      <Navigation />
      
      <div className="pt-32 pb-20 px-6">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center space-y-6 mb-12 animate-fade-in">
            <h1 className="text-5xl md:text-6xl font-bold">
              Your Instagram
              <br />
              <span className="italic font-light">Posts</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Connect your Instagram account and transform your product posts into Amazon listings
            </p>
          </div>

          {posts.length === 0 ? (
            <Card className="max-w-md mx-auto border-2 border-dashed animate-scale-in">
              <CardContent className="pt-12 pb-12 text-center space-y-6">
                <div className="w-20 h-20 mx-auto bg-accent/10 rounded-full flex items-center justify-center">
                  <Instagram className="h-10 w-10 text-accent" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-2xl font-bold">Fetch Your Posts</h3>
                  <p className="text-muted-foreground">
                    Click the button below to load your Instagram posts
                  </p>
                </div>
                <Button
                  size="lg"
                  className="rounded-full"
                  onClick={fetchInstagramPosts}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Loading...
                    </>
                  ) : (
                    <>
                      <Instagram className="mr-2 h-5 w-5" />
                      Fetch My Posts
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-8">
              <div className="flex justify-between items-center">
                <p className="text-lg text-muted-foreground">
                  {posts.length} posts loaded
                </p>
                <Button
                  variant="outline"
                  onClick={fetchInstagramPosts}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Refreshing...
                    </>
                  ) : (
                    "Refresh Posts"
                  )}
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {posts.map((post, index) => (
                  <Card
                    key={post.id}
                    className="overflow-hidden border-none shadow-lg hover:shadow-xl transition-all duration-300 animate-scale-in"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div className="aspect-square relative overflow-hidden bg-muted">
                      {post.media_type === "VIDEO" ? (
                        <video
                          src={post.media_url}
                          className="w-full h-full object-cover"
                          controls
                        />
                      ) : (
                        <img
                          src={post.media_url}
                          alt={post.caption?.substring(0, 50) || "Instagram post"}
                          className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                        />
                      )}
                    </div>
                    <CardContent className="pt-4 pb-4 space-y-3">
                      <p className="text-sm text-muted-foreground line-clamp-3">
                        {post.caption || "No caption"}
                      </p>
                      <Button
                        className="w-full rounded-full"
                        onClick={() => generateListing(post)}
                        disabled={generatingId === post.id}
                      >
                        {generatingId === post.id ? (
                          <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Generating...
                          </>
                        ) : (
                          "Generate Listing"
                        )}
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
