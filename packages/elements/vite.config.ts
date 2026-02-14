import { defineConfig, Plugin } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

/**
 * Vite plugin that rewrites bare `require("lodash.xxx")` calls in
 * @karrio/lib/helper.ts to ESM default imports so the browser bundle
 * does not contain any CJS `require()` at runtime.
 */
function rewriteLodashRequires(): Plugin {
  const lodashModules: Record<string, string> = {
    "lodash.isequal": "__lodash_isEqual",
    "lodash.snakecase": "__lodash_snakeCase",
    "lodash.groupby": "__lodash_groupBy",
    "lodash.tonumber": "__lodash_toNumber",
  };

  return {
    name: "rewrite-lodash-requires",
    enforce: "pre",
    transform(code, id) {
      // Only transform the specific file that uses require()
      if (!id.includes("packages/lib/helper") && !id.includes("packages\\lib\\helper")) {
        return null;
      }
      if (!code.includes("require(")) return null;

      // Build ESM import statements
      const imports = Object.entries(lodashModules)
        .map(([pkg, varName]) => `import ${varName} from "${pkg}";`)
        .join("\n");

      // Replace each require() call with the corresponding variable
      let transformed = code;
      for (const [pkg, varName] of Object.entries(lodashModules)) {
        transformed = transformed.replace(
          new RegExp(`require\\(["']${pkg.replace(".", "\\.")}["']\\)`, "g"),
          varName,
        );
      }

      return { code: imports + "\n" + transformed, map: null };
    },
  };
}

/**
 * Vite plugin that redirects relative `./karrio` and `./session` imports
 * within packages/hooks/ to our embed-compatible shims.
 *
 * This is critical for the devtools build: the hooks (api-token, webhook,
 * events, etc.) use relative imports to ./karrio and ./session.  Standard
 * Vite aliases only match import specifiers, not resolved file paths, so
 * they miss these relative imports.  This plugin intercepts the resolution
 * step to redirect them.
 */
function redirectHooksInternals(): Plugin {
  const embedKarrio = path.resolve(__dirname, "src/shims/embed-karrio.tsx");
  const embedSession = path.resolve(__dirname, "src/shims/embed-session.tsx");
  const embedApiMetadata = path.resolve(
    __dirname,
    "src/providers/api-metadata-embed-provider.tsx",
  );

  return {
    name: "redirect-hooks-internals",
    enforce: "pre",
    resolveId(source, importer) {
      if (!importer) return null;

      // Only intercept imports originating from packages/hooks/
      const normImporter = importer.replace(/\\/g, "/");
      if (!normImporter.includes("packages/hooks/")) return null;

      // Don't intercept imports from our own shims/providers
      if (normImporter.includes("packages/elements/")) return null;

      if (source === "./karrio" || source === "./karrio.tsx") {
        return embedKarrio;
      }
      if (source === "./session" || source === "./session.tsx") {
        return embedSession;
      }
      if (source === "./api-metadata" || source === "./api-metadata.tsx") {
        return embedApiMetadata;
      }

      return null;
    },
  };
}

/**
 * Vite plugin that forces the CarrierImage component to always use the
 * generic inline SVG badge instead of file-based carrier logo assets.
 *
 * This keeps the elements bundle light by removing the dependency on
 * 50+ carrier SVG files.  The IMAGES array is replaced with an empty
 * array so `has_image` is always false in carrier-image.tsx.
 */
function stripCarrierImages(): Plugin {
  return {
    name: "strip-carrier-images",
    enforce: "pre",
    transform(code, id) {
      const normId = id.replace(/\\/g, "/");
      if (!normId.includes("packages/types/base")) return null;
      if (!code.includes("export const IMAGES")) return null;

      const transformed = code.replace(
        /export const IMAGES[^;]*;/,
        "export const IMAGES: string[] = [];",
      );
      if (transformed === code) return null;
      return { code: transformed, map: null };
    },
  };
}

/**
 * Vite plugin that rewrites `Bearer` auth prefix to `Token` in the
 * Playground and GraphiQL modules.
 *
 * The original developer-tools modules use `Bearer ${session.accessToken}`
 * because the dashboard session provides a JWT.  In embed mode the token
 * is a Karrio API key which requires the `Token` prefix.
 */
function rewriteBearerAuth(): Plugin {
  return {
    name: "rewrite-bearer-auth",
    enforce: "pre",
    transform(code, id) {
      const normId = id.replace(/\\/g, "/");
      if (
        !normId.includes("packages/developers/modules/playground") &&
        !normId.includes("packages/developers/modules/graphiql")
      ) {
        return null;
      }
      if (!code.includes("Bearer")) return null;

      // Replace template-literal `Bearer ${…}` with `Token ${…}`
      const transformed = code.replace(/`Bearer \$\{/g, "`Token ${");
      if (transformed === code) return null;
      return { code: transformed, map: null };
    },
  };
}

export default defineConfig({
  plugins: [
    rewriteLodashRequires(),
    redirectHooksInternals(),
    rewriteBearerAuth(),
    stripCarrierImages(),
    react(),
  ],
  resolve: {
    alias: {
      // Embed-compatible providers (replaces hook imports in devtools & ratesheet)
      "@karrio/hooks/api-metadata": path.resolve(
        __dirname,
        "src/providers/api-metadata-embed-provider.tsx",
      ),
      "@karrio/hooks/session": path.resolve(
        __dirname,
        "src/shims/embed-session.tsx",
      ),
      "@karrio/hooks/karrio": path.resolve(
        __dirname,
        "src/shims/embed-karrio.tsx",
      ),

      // Shim out Next.js dependencies
      "next-auth/react": path.resolve(__dirname, "src/shims/next-auth.ts"),
      "next-auth": path.resolve(__dirname, "src/shims/next-auth.ts"),
      "next/navigation": path.resolve(
        __dirname,
        "src/shims/next-navigation.ts",
      ),
      "next/legacy/image": path.resolve(
        __dirname,
        "src/shims/next-image.tsx",
      ),
      "next/image": path.resolve(
        __dirname,
        "src/shims/next-image.tsx",
      ),
      "next-runtime-env": path.resolve(
        __dirname,
        "src/shims/next-runtime-env.ts",
      ),

      // Workspace package aliases
      "@karrio/developers": path.resolve(__dirname, "../developers"),
      "@karrio/ui": path.resolve(__dirname, "../ui"),
      "@karrio/hooks": path.resolve(__dirname, "../hooks"),
      "@karrio/lib": path.resolve(__dirname, "../lib"),
      "@karrio/types": path.resolve(__dirname, "../types"),
    },
  },
  css: {
    postcss: path.resolve(__dirname, "postcss.config.mjs"),
  },
  base: "./",
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        ratesheet: path.resolve(__dirname, "src/entries/ratesheet.tsx"),
        devtools: path.resolve(__dirname, "src/entries/devtools.tsx"),
        "template-editor": path.resolve(__dirname, "src/entries/template-editor.tsx"),
        connections: path.resolve(__dirname, "src/entries/connections.tsx"),
        elements: path.resolve(__dirname, "src/host/elements.ts"),
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "[name].[ext]",
      },
    },
  },
});
