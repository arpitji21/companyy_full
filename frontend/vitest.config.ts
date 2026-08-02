/// <reference types="vitest/config" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

// Deliberately a separate config from vite.config.ts rather than adding
// `test: {...}` there — that file is generated/managed by
// @lovable.dev/vite-tanstack-config, which explicitly warns against
// touching its plugin setup by hand. This config only needs enough to run
// tests: React + the same "@/*" -> "./src/*" alias from tsconfig.json,
// not the full app build pipeline (Tailwind, Nitro, TanStack Start SSR).
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
  },
});
