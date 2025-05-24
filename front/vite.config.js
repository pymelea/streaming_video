import { defineConfig } from "vite";
import { defineConfig as defineVitestConfig } from 'vitest/config';
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig(
  defineVitestConfig({
    plugins: [react()],
    resolve: {
      extensions: ['.js', '.jsx', '.ts', '.tsx'],
    },
    optimizeDeps: {
      include: ['lucide-react'],
    },
    server: {
      port: 3000,
      host: "0.0.0.0",
    },
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: ['./src/test/setup.js'],
      exclude: ['**/node_modules/**', '**/coverage/**', 'postcss.config.js', 'tailwind.config.js'],
      coverage: {
        provider: 'v8',
        reporter: ['text', 'lcov', 'html'],
        include: ['src/**/*.{js,jsx,ts,tsx}'],
        exclude: ['**/node_modules/**', '**/coverage/**', 'postcss.config.js', 'tailwind.config.js'],
      },
    },
     preview: {
    port: parseInt(process.env.PORT) || 4173
  }
  })
);
