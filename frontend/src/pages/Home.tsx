import { ArrowRight, Instagram, Sparkles, Zap, CheckCircle2, TrendingUp, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Navigation from "@/components/Navigation";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen">
      <Navigation />
      
      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-6 overflow-hidden">
        {/* Gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-primary/5 pointer-events-none" />
        <div className="absolute top-20 right-20 w-96 h-96 bg-accent/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-20 left-20 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="container mx-auto max-w-6xl relative z-10">
          <div className="text-center space-y-6 animate-fade-in-up">
            <Badge variant="secondary" className="mb-4 text-sm py-1.5 px-4">
              <Sparkles className="w-3 h-3 mr-1.5" />
              AI-Powered Listing Generator
            </Badge>
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold leading-tight bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
              Transform posts into
              <br />
              <span className="italic font-light bg-gradient-to-r from-accent to-primary bg-clip-text">perfect listings</span>
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Autolist turns your Instagram product posts into comprehensive Amazon listings in seconds using AI.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-8">
              <Button
                size="lg"
                className="rounded-full text-lg px-8 py-6 shadow-lg hover:shadow-xl transition-all"
                onClick={() => navigate("/dashboard")}
              >
                Get Started Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="rounded-full text-lg px-8 py-6"
                onClick={() => navigate("/dashboard")}
              >
                View Demo
              </Button>
            </div>
            
            {/* Stats */}
            <div className="flex flex-wrap justify-center gap-8 mt-16 pt-8 border-t border-border/50">
              <div className="text-center">
                <div className="text-3xl font-bold">10K+</div>
                <div className="text-sm text-muted-foreground">Listings Generated</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold">5 sec</div>
                <div className="text-sm text-muted-foreground">Average Time</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold">98%</div>
                <div className="text-sm text-muted-foreground">Accuracy Rate</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6 bg-gradient-to-b from-secondary/20 to-transparent">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">How it works</h2>
            <p className="text-xl text-muted-foreground">Three simple steps to perfect listings</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="border-none shadow-lg hover:shadow-xl transition-all duration-300 animate-scale-in group" style={{ animationDelay: "0.1s" }}>
              <CardContent className="pt-8 pb-8 text-center space-y-4">
                <div className="relative">
                  <div className="w-16 h-16 mx-auto bg-gradient-to-br from-accent/20 to-accent/10 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Instagram className="h-8 w-8 text-accent" />
                  </div>
                  <Badge className="absolute -top-2 -right-12 bg-accent text-accent-foreground">Step 1</Badge>
                </div>
                <h3 className="text-2xl font-bold">Connect Instagram</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Import your product posts directly from Instagram with a single click. No manual data entry needed.
                </p>
              </CardContent>
            </Card>

            <Card className="border-none shadow-lg hover:shadow-xl transition-all duration-300 animate-scale-in group" style={{ animationDelay: "0.2s" }}>
              <CardContent className="pt-8 pb-8 text-center space-y-4">
                <div className="relative">
                  <div className="w-16 h-16 mx-auto bg-gradient-to-br from-primary/20 to-primary/10 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Sparkles className="h-8 w-8 text-primary" />
                  </div>
                  <Badge className="absolute -top-2 -right-12 bg-primary text-primary-foreground">Step 2</Badge>
                </div>
                <h3 className="text-2xl font-bold">AI Generation</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Our AI analyzes your posts and creates optimized Amazon listings automatically with smart categories.
                </p>
              </CardContent>
            </Card>

            <Card className="border-none shadow-lg hover:shadow-xl transition-all duration-300 animate-scale-in group" style={{ animationDelay: "0.3s" }}>
              <CardContent className="pt-8 pb-8 text-center space-y-4">
                <div className="relative">
                  <div className="w-16 h-16 mx-auto bg-gradient-to-br from-green-500/20 to-green-500/10 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Zap className="h-8 w-8 text-green-600" />
                  </div>
                  <Badge className="absolute -top-2 -right-12 bg-green-600 text-white">Step 3</Badge>
                </div>
                <h3 className="text-2xl font-bold">Edit & Export</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Review, edit, and confirm your listings. Export in multiple formats including PDF, CSV, and JSON.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h2 className="text-4xl md:text-5xl font-bold">Why choose Autolist?</h2>
              <div className="space-y-4">
                <div className="flex gap-4 items-start">
                  <CheckCircle2 className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-semibold text-lg">Save Time</h4>
                    <p className="text-muted-foreground">Generate complete listings in seconds, not hours</p>
                  </div>
                </div>
                <div className="flex gap-4 items-start">
                  <CheckCircle2 className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-semibold text-lg">AI-Powered Accuracy</h4>
                    <p className="text-muted-foreground">Smart category detection and keyword optimization</p>
                  </div>
                </div>
                <div className="flex gap-4 items-start">
                  <CheckCircle2 className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-semibold text-lg">Multiple Export Formats</h4>
                    <p className="text-muted-foreground">Download as PDF, CSV, JSON, or HTML</p>
                  </div>
                </div>
                <div className="flex gap-4 items-start">
                  <CheckCircle2 className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h4 className="font-semibold text-lg">Easy Editing</h4>
                    <p className="text-muted-foreground">Fine-tune every detail before exporting</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <Card className="border-none shadow-lg bg-gradient-to-br from-accent/10 to-transparent">
                <CardContent className="pt-6 pb-6">
                  <TrendingUp className="w-8 h-8 text-accent mb-3" />
                  <div className="text-3xl font-bold mb-1">10x</div>
                  <div className="text-sm text-muted-foreground">Faster than manual</div>
                </CardContent>
              </Card>
              <Card className="border-none shadow-lg bg-gradient-to-br from-primary/10 to-transparent">
                <CardContent className="pt-6 pb-6">
                  <Clock className="w-8 h-8 text-primary mb-3" />
                  <div className="text-3xl font-bold mb-1">&lt;5s</div>
                  <div className="text-sm text-muted-foreground">Generation time</div>
                </CardContent>
              </Card>
              <Card className="border-none shadow-lg bg-gradient-to-br from-green-500/10 to-transparent">
                <CardContent className="pt-6 pb-6">
                  <CheckCircle2 className="w-8 h-8 text-green-600 mb-3" />
                  <div className="text-3xl font-bold mb-1">98%</div>
                  <div className="text-sm text-muted-foreground">Accuracy rate</div>
                </CardContent>
              </Card>
              <Card className="border-none shadow-lg bg-gradient-to-br from-purple-500/10 to-transparent">
                <CardContent className="pt-6 pb-6">
                  <Sparkles className="w-8 h-8 text-purple-600 mb-3" />
                  <div className="text-3xl font-bold mb-1">9+</div>
                  <div className="text-sm text-muted-foreground">Categories supported</div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-primary/5 pointer-events-none" />
        <div className="container mx-auto max-w-4xl text-center space-y-6 relative z-10">
          <h2 className="text-5xl md:text-6xl font-bold">
            Ready to automate your
            <br />
            <span className="italic font-light bg-gradient-to-r from-accent to-primary bg-clip-text text-transparent">listing workflow?</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Join thousands of sellers using AI to create perfect Amazon listings
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-8">
            <Button
              size="lg"
              className="rounded-full text-lg px-8 py-6 shadow-lg hover:shadow-xl transition-all"
              onClick={() => navigate("/dashboard")}
            >
              Start Free Now
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
