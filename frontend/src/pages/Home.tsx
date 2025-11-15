import { ArrowRight, Instagram, Sparkles, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Navigation from "@/components/Navigation";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen">
      <Navigation />
      
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-6 animate-fade-in-up">
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold leading-tight">
              Transform posts into
              <br />
              <span className="italic font-light">perfect listings</span>
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto">
              Autolist turns your Instagram product posts into comprehensive Amazon listings in seconds using AI.
            </p>
            <Button
              size="lg"
              className="rounded-full text-lg px-8 py-6 mt-8"
              onClick={() => navigate("/dashboard")}
            >
              Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6 bg-secondary/30">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="border-none shadow-lg animate-scale-in" style={{ animationDelay: "0.1s" }}>
              <CardContent className="pt-8 pb-8 text-center space-y-4">
                <div className="w-16 h-16 mx-auto bg-accent/10 rounded-2xl flex items-center justify-center">
                  <Instagram className="h-8 w-8 text-accent" />
                </div>
                <h3 className="text-2xl font-bold">Connect Instagram</h3>
                <p className="text-muted-foreground">
                  Import your product posts directly from Instagram with a single click.
                </p>
              </CardContent>
            </Card>

            <Card className="border-none shadow-lg animate-scale-in" style={{ animationDelay: "0.2s" }}>
              <CardContent className="pt-8 pb-8 text-center space-y-4">
                <div className="w-16 h-16 mx-auto bg-accent/10 rounded-2xl flex items-center justify-center">
                  <Sparkles className="h-8 w-8 text-accent" />
                </div>
                <h3 className="text-2xl font-bold">AI Generation</h3>
                <p className="text-muted-foreground">
                  Our AI analyzes your posts and creates optimized Amazon listings automatically.
                </p>
              </CardContent>
            </Card>

            <Card className="border-none shadow-lg animate-scale-in" style={{ animationDelay: "0.3s" }}>
              <CardContent className="pt-8 pb-8 text-center space-y-4">
                <div className="w-16 h-16 mx-auto bg-accent/10 rounded-2xl flex items-center justify-center">
                  <Zap className="h-8 w-8 text-accent" />
                </div>
                <h3 className="text-2xl font-bold">Edit & Export</h3>
                <p className="text-muted-foreground">
                  Review, edit, and confirm your listings before exporting to Amazon.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-4xl text-center space-y-6">
          <h2 className="text-5xl md:text-6xl font-bold">
            Ready to automate your
            <br />
            <span className="italic font-light">listing workflow?</span>
          </h2>
          <Button
            size="lg"
            className="rounded-full text-lg px-8 py-6 mt-8"
            onClick={() => navigate("/dashboard")}
          >
            Start Now
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;
