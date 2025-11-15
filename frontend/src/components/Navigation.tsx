import { NavLink } from "./NavLink";
import { Button } from "./ui/button";

const Navigation = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <NavLink to="/" className="flex items-center gap-2 text-2xl font-bold">
            <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
              <span className="text-primary-foreground text-sm">A</span>
            </div>
            <span>Autolist</span>
          </NavLink>

          <div className="hidden md:flex items-center gap-8">
            <NavLink
              to="/"
              className="text-foreground/70 hover:text-foreground transition-colors"
              activeClassName="text-foreground font-medium"
            >
              Home
            </NavLink>
            <NavLink
              to="/dashboard"
              className="text-foreground/70 hover:text-foreground transition-colors"
              activeClassName="text-foreground font-medium"
            >
              Dashboard
            </NavLink>
          </div>

          <NavLink to="/dashboard">
            <Button size="lg" className="rounded-full">
              Get Started
            </Button>
          </NavLink>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
