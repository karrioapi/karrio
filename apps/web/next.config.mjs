import nextra from 'nextra';
import path from "path";

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || "";

// Create a simpler configuration that can be serialized
const withNextra = nextra({
  defaultShowCopyCode: true,
  codeHighlight: true,
})

// Combine Next.js config with Nextra config
export default withNextra({
  basePath: BASE_PATH,
  reactStrictMode: true,
  transpilePackages: [
    "@karrio/ui",
  ],
  sassOptions: {
    includePaths: [path.join("src", "styles")],
  },
  webpack: (config) => {
    config.resolve.fallback = { fs: false, net: false, tls: false };
    config.externals.push("pino-pretty", "encoding");
    return config;
  },

  // Configure pageExtensions to include md and mdx
  pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'md', 'mdx'],

  // Add custom webpack configuration if needed
  webpack: (config) => {
    return config;
  }
})
