import { Inter, JetBrains_Mono } from "next/font/google";
import localFont from "next/font/local";

export const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-jetbrains-mono",
});

// Load Cal Sans font locally
export const calSans = localFont({
  src: [
    {
      path: '../../public/fonts/CalSans-SemiBold.woff2',
      weight: '600',
      style: 'normal',
    },
  ],
  variable: "--font-cal",
  display: "swap",
});
