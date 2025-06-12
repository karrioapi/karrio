import { withSentryConfig } from "@sentry/nextjs";
import path from "path";

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || "";

/** @type {import('next').NextConfig} */
const nextConfig = {
  basePath: BASE_PATH,
  reactStrictMode: true,
  transpilePackages: [
    "@karrio/core",
    "@karrio/hooks",
    "@karrio/ui",
    "@karrio/lib",
    "@karrio/types",
    "@karrio/trpc",
    "@karrio/admin",
    "@karrio/developers",
  ],
  sassOptions: {
    includePaths: [path.join("src", "styles")],
  },
  webpack: (config) => {
    config.resolve.fallback = { fs: false, net: false, tls: false };
    config.externals.push("pino-pretty", "encoding");
    return config;
  },
};

const sentryWebpackPluginOptions = {
  silent: !process.env.CI,
  disableLogger: true,
};

export default withSentryConfig(nextConfig, sentryWebpackPluginOptions);
