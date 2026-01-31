import nextra from 'nextra';
import path from "path";

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || "";

/** @type {import('next').NextConfig} */
const nextConfig = {
  basePath: BASE_PATH,
  reactStrictMode: true,
  transpilePackages: [
    "@karrio/ui",
  ],
  env: {
    NEXT_PUBLIC_POSTHOG_KEY: process.env.NEXT_PUBLIC_POSTHOG_KEY,
    NEXT_PUBLIC_POSTHOG_HOST: process.env.NEXT_PUBLIC_POSTHOG_HOST,
  },
  sassOptions: {
    includePaths: [path.join("src", "styles")],
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'Content-Security-Policy',
            value: "frame-ancestors 'none';",
          },
        ],
      },
    ];
  },
  webpack: (config) => {
    config.resolve.fallback = { fs: false, net: false, tls: false };
    config.externals.push("pino-pretty", "encoding");
    return config;
  },

  // Configure pageExtensions to include md and mdx
  pageExtensions: ['js', 'jsx', 'md', 'mdx', 'ts', 'tsx'],
}

// Create a simpler configuration that can be serialized
const withNextra = nextra({
  contentDirBasePath: '/blog',
  defaultShowCopyCode: false,
  // Disable nextra's built-in syntax highlighting since we're using our custom component
  codeHighlight: false
})

// Combine Next.js config with Nextra config
export default withNextra(nextConfig)
