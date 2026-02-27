import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm"],
  dts: true,
  sourcemap: true,
  clean: true,
  outDir: "dist",
  platform: "node",
  target: "node18",
  banner: {
    js: "#!/usr/bin/env node",
  },
});
