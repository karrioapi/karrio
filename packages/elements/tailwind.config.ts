import type { Config } from "tailwindcss";
import baseConfig from "../ui/tailwind.config";

const config: Config = {
  ...baseConfig,
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "../ui/components/**/*.{js,ts,jsx,tsx}",
    "../ui/hooks/**/*.{js,ts,jsx,tsx}",
    "../ui/lib/**/*.{js,ts,jsx,tsx}",
    "../developers/components/**/*.{js,ts,jsx,tsx}",
    "../developers/modules/**/*.{js,ts,jsx,tsx}",
    "../developers/context/**/*.{js,ts,jsx,tsx}",
  ],
};

export default config;
