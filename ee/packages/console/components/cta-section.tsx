"use client";

import { Button } from "@karrio/insiders/components/ui/button";
import Image from "next/image";
import Link from "next/link";
import { BookDemoButton } from "./book-demo-button";

interface CTASectionProps {
  title: string;
  description: string;
}

export function CTASection({
  title,
  description,
}: CTASectionProps) {
  return (
    <section className="py-24 relative">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,#5722cc0d,transparent_50%)]" />
      <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
      <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px] space-y-12">
        {/* Header */}
        <div className="text-center space-y-4">
          <h2 className="text-4xl font-bold">
            {title}
          </h2>
          <p className="text-white/60 max-w-2xl mx-auto">
            {description}
          </p>
        </div>

        {/* Cards */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Karrio OSS Card */}
          <div className="bg-white/5 rounded-xl p-8 space-y-8">
            <div className="space-y-4">
              <Image src="/icon.svg" alt="Karrio Icon" width={40} height={40} />
              <h3 className="text-2xl font-semibold">Karrio Open Source</h3>
              <p className="text-white/60">
                The optimal solution for small projects.
              </p>
            </div>

            <Button variant="outline" size="lg" className="w-full sm:w-auto" asChild>
              <Link href="https://docs.karrio.io/product/self-hosting">
                Deploy Open Source
              </Link>
            </Button>

            <div className="aspect-video relative rounded-lg overflow-hidden bg-black/40 flex items-center justify-center">
              <div className="absolute w-full h-full">
                <div className="absolute top-1/2 left-1/4 w-32 h-32 md:w-44 md:h-44 rounded-full bg-[#30D9B7]/30 blur-xl"></div>
                <div className="absolute top-1/3 right-1/4 w-28 h-28 md:w-40 md:h-40 rounded-full bg-[#5722cc]/30 blur-xl"></div>
                <div className="absolute w-full h-full flex items-center justify-center">
                  <svg width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="100" cy="100" r="80" stroke="#30D9B7" strokeWidth="4" />
                    <path d="M60 100C60 77.9086 77.9086 60 100 60C122.091 60 140 77.9086 140 100C140 122.091 122.091 140 100 140" stroke="#5722cc" strokeWidth="4" />
                    <circle cx="100" cy="100" r="20" fill="#30D9B7" fillOpacity="0.3" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Karrio Platform Card */}
          <div className="bg-[#0f0826] rounded-xl p-8 space-y-8 border border-white/10">
            <div className="space-y-4">
              <Image src="/icon.svg" alt="Karrio Icon" width={40} height={40} />
              <h3 className="text-2xl font-semibold">Karrio Platform</h3>
              <p className="text-white/60">
                The optimal solution for teams with control and flexibility.
              </p>
            </div>

            <BookDemoButton
              size="lg"
              className="w-full sm:w-auto bg-[#5722cc] hover:bg-[#5722cc]/90"
            />

            <div className="aspect-video relative rounded-lg overflow-hidden bg-black/40 flex items-center justify-center">
              <div className="absolute w-full h-full">
                <div className="absolute top-1/3 left-1/3 w-36 h-36 md:w-48 md:h-48 rounded-full bg-[#5722cc]/30 blur-xl"></div>
                <div className="absolute top-1/2 right-1/4 w-32 h-32 md:w-44 md:h-44 rounded-full bg-[#30D9B7]/30 blur-xl"></div>
                <div className="absolute w-full h-full flex items-center justify-center">
                  <svg width="220" height="220" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                    {/* OSS Core Foundation (similar to OSS illustration) */}
                    <circle cx="100" cy="100" r="35" stroke="#30D9B7" strokeWidth="2" fill="rgba(48, 217, 183, 0.05)" />
                    <path d="M80 100C80 89.0589 89.0589 80 100 80C110.941 80 120 89.0589 120 100C120 110.941 110.941 120 100 120"
                      stroke="#5722cc" strokeWidth="2" />

                    {/* Platform Expansion Elements */}
                    <circle cx="100" cy="100" r="60" stroke="#5722cc" strokeWidth="1.5" stroke-dasharray="4 3" />

                    {/* Reduced Modular Components (3 instead of 5) */}
                    <rect x="50" y="75" width="25" height="25" rx="5" stroke="#30D9B7" strokeWidth="2" fill="rgba(48, 217, 183, 0.1)" />
                    <rect x="145" y="100" width="25" height="25" rx="5" stroke="#30D9B7" strokeWidth="2" fill="rgba(48, 217, 183, 0.1)" />
                    <rect x="100" y="145" width="25" height="25" rx="5" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />

                    {/* Reduced Connector lines */}
                    <path d="M80 85L75 85" stroke="#30D9B7" strokeWidth="1.5" />
                    <path d="M130 100L145 110" stroke="#30D9B7" strokeWidth="1.5" />
                    <path d="M110 120L112 145" stroke="#5722cc" strokeWidth="1.5" />

                    {/* Outer ring showing ecosystem expansion */}
                    <circle cx="100" cy="100" r="85" stroke="url(#platformGradient)" strokeWidth="2" stroke-dasharray="1 2" />

                    {/* Reduced Accent elements - only one in the center */}
                    <circle cx="100" cy="100" r="12" fill="#5722cc" fillOpacity="0.3" />

                    {/* Gradient definition */}
                    <defs>
                      <linearGradient id="platformGradient" x1="15" y1="15" x2="185" y2="185" gradientUnits="userSpaceOnUse">
                        <stop offset="0%" stopColor="#5722cc" />
                        <stop offset="100%" stopColor="#30D9B7" />
                      </linearGradient>
                    </defs>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
