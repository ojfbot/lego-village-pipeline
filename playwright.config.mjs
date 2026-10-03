import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/browser",
  testMatch: "*.spec.mjs",
  use: {
    baseURL: "http://127.0.0.1:4187",
    browserName: "chromium",
  },
  webServer: {
    command: "pnpm dev",
    env: { PORT: "4187" },
    url: "http://127.0.0.1:4187/",
    reuseExistingServer: false,
  },
});
