"use client";

import { Button } from "@karrio/ui/components/ui/button";
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
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,var(--primary-color-50),transparent_50%)]" style={{
        '--primary-color-50': 'hsla(var(--primary) / 0.05)',
      } as React.CSSProperties} />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,var(--secondary-color-50),transparent_50%)]" style={{
        '--secondary-color-50': 'hsla(var(--secondary) / 0.05)',
      } as React.CSSProperties} />
      <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px] space-y-12">
        {/* Header */}
        <div className="text-center space-y-4">
          <h2 className="text-4xl font-bold">
            {title}
          </h2>
          <p className="dark:text-white/60 text-foreground/60 max-w-2xl mx-auto">
            {description}
          </p>
        </div>

        {/* Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-10">
          {/* Karrio OSS Card */}
          <div className="dark:bg-[#1A1630] bg-gray-50 rounded-xl overflow-hidden border dark:border-white/5 border-gray-200/70 text-foreground dark:text-white shadow-md relative group min-h-[380px] flex flex-col">
            <div className="p-6 md:p-8 space-y-5 md:space-y-6 relative z-10 w-full md:max-w-[75%] flex-1">
              <div className="w-12 md:w-14 h-12 md:h-14 flex items-center justify-center rounded-xl bg-[#30D9B7]/10 dark:bg-white/10">
                <Image src="/icon.svg" alt="Karrio Icon" width={28} height={28} className="w-7 h-7 md:w-8 md:h-8" />
              </div>

              <div className="space-y-3">
                <h3 className="text-xl md:text-2xl font-semibold">Karrio Open Source</h3>
                <p className="dark:text-white/60 text-gray-600">
                  The optimal solution for small projects.
                </p>
              </div>

              <Button variant="outline" size="lg" className="mt-2 dark:border-white/20 dark:text-white border-primary/40 text-primary hover:bg-primary/5 dark:hover:bg-white/10" asChild>
                <Link href="https://docs.karrio.io/product/self-hosting">
                  Deploy Open Source
                </Link>
              </Button>
            </div>

            {/* Background illustration */}
            <div className="absolute right-0 bottom-0 w-[45%] md:w-[50%] h-[70%] md:h-[80%] overflow-hidden pointer-events-none">
              <div className="relative w-full h-full flex items-center justify-center">
                <div className="absolute top-1/4 left-1/4 w-16 md:w-24 h-16 md:h-24 rounded-full bg-[#30D9B7]/20 dark:bg-[#30D9B7]/30 blur-xl"></div>
                <div className="absolute bottom-1/4 right-1/4 w-14 md:w-20 h-14 md:h-20 rounded-full bg-[#5722cc]/20 dark:bg-[#5722cc]/30 blur-xl"></div>
                <svg className="w-40 md:w-52 h-40 md:h-52" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="100" cy="100" r="80" stroke="var(--color-circle, #30D9B7)" strokeWidth="3" className="dark:opacity-100 opacity-70" style={{ "--color-circle": "#30D9B7" } as React.CSSProperties} />
                  <path d="M60 100C60 77.9086 77.9086 60 100 60C122.091 60 140 77.9086 140 100C140 122.091 122.091 140 100 140" stroke="var(--color-path, #5722cc)" strokeWidth="3" className="dark:opacity-100 opacity-70" style={{ "--color-path": "#5722cc" } as React.CSSProperties} />
                  <circle cx="100" cy="100" r="20" fill="var(--color-inner, #30D9B7)" fillOpacity="0.3" style={{ "--color-inner": "#30D9B7" } as React.CSSProperties} />
                </svg>
              </div>
            </div>
          </div>

          {/* Karrio Platform Card */}
          <div className="bg-[#0f0826] rounded-xl overflow-hidden border border-white/10 text-white shadow-md relative group min-h-[380px] flex flex-col">
            <div className="p-6 md:p-8 space-y-5 md:space-y-6 relative z-10 w-full md:max-w-[75%] flex-1">
              <div className="w-12 md:w-14 h-12 md:h-14 flex items-center justify-center rounded-xl bg-[#5722cc]/30">
                <Image src="/icon.svg" alt="Karrio Icon" width={28} height={28} className="w-7 h-7 md:w-8 md:h-8" />
              </div>

              <div className="space-y-3">
                <h3 className="text-xl md:text-2xl font-semibold">Karrio Platform</h3>
                <p className="text-white/60">
                  The optimal solution for teams with control and flexibility.
                </p>
              </div>

              <BookDemoButton
                size="lg"
                className="mt-2 bg-[#5722cc] hover:bg-[#5722cc]/90"
              />
            </div>

            {/* Enhanced illustration showing more advanced features */}
            <div className="absolute right-0 bottom-0 w-[45%] md:w-[50%] h-[70%] md:h-[80%] overflow-hidden pointer-events-none">
              <div className="relative w-full h-full flex items-center justify-center">
                <div className="absolute top-1/3 right-1/3 w-20 md:w-28 h-20 md:h-28 rounded-full bg-[#5722cc]/30 blur-xl"></div>
                <div className="absolute bottom-1/3 left-1/3 w-16 md:w-24 h-16 md:h-24 rounded-full bg-[#30D9B7]/30 blur-xl"></div>
                <svg className="w-40 md:w-60 h-40 md:h-60" viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg">
                  {/* Base circle - same as OSS but larger */}
                  <circle cx="120" cy="120" r="80" stroke="#5722cc" strokeWidth="3" />

                  {/* Inner arc - similar to OSS but with different start/end */}
                  <path d="M80 120C80 97.9086 97.9086 80 120 80C142.091 80 160 97.9086 160 120C160 142.091 142.091 160 120 160"
                    stroke="#30D9B7" strokeWidth="3" />

                  {/* Additional elements showing more features */}
                  <circle cx="120" cy="120" r="20" fill="#5722cc" fillOpacity="0.3" />

                  {/* Additional outer ring */}
                  <circle cx="120" cy="120" r="100" stroke="#30D9B7" strokeWidth="1.5" strokeDasharray="4 3" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
