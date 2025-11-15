import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: "::",
    port: 5173,
    proxy: {
      // Proxy all /api calls to the backend server during development
      "/categories": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/generate": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/validate": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/export": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  plugins: [react(), mode === "development" && componentTagger()].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
