import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Gọi /api/... sẽ được chuyển sang Django, khỏi lo CORS khi dev
    proxy: { "/api": process.env.API_URL || "http://127.0.0.1:8000" },
  },
});
