"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@karrio/ui/lib/utils";
import React, { useRef, useEffect } from "react";

export function PlatformSubnav() {
  const pathname = usePathname();
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const navItems = [
    { label: "Overview", href: "/platform" },
    { label: "LSPs", href: "/platform/use-cases/logistics-providers" },
    { label: "Platforms", href: "/platform/use-cases/platforms" },
    { label: "Enterprises", href: "/platform/use-cases/enterprise-solutions" },
    { label: "Embed", href: "/platform/embed" },
    // { label: "Pricing", href: "/platform/#pricing" },
  ];

  // Ensure horizontal scrolling still works with no scrollbars
  useEffect(() => {
    const scrollContainer = scrollContainerRef.current;
    if (!scrollContainer) return;

    const handleWheel = (e: WheelEvent) => {
      if (e.deltaY !== 0) {
        e.preventDefault();
        scrollContainer.scrollLeft += e.deltaY;
      }
    };

    scrollContainer.addEventListener('wheel', handleWheel, { passive: false });

    return () => {
      scrollContainer.removeEventListener('wheel', handleWheel);
    };
  }, []);

  return (
    <div className="bg-[#150d34] border-b border-white/10">
      <div className="container mx-auto px-4 sm:px-6 lg:px-2 max-w-6xl">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between py-2 gap-y-2">
          <div className="font-bold text-lg text-white tracking-wide flex items-center">
            <div className="relative mr-2 flex items-center">
              <div className="bg-[#5722cc] w-5 h-5 rounded-full absolute right-[-4px]"></div>
              <div className="bg-[#30D9B7] w-5 h-5 rounded-full opacity-80"></div>
            </div>
            Platform
          </div>

          {/* Use a wrapper to hide scrollbar overflow */}
          <div className="-mx-4 px-4 pb-1 sm:mx-0 sm:px-0 sm:pb-0 overflow-hidden">
            {/* Scrollable container without visible scrollbar */}
            <div
              ref={scrollContainerRef}
              style={{
                overflowX: 'auto',
                scrollbarWidth: 'none',
                msOverflowStyle: 'none',
              }}
              className="flex space-x-6 md:space-x-8"
            >
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "py-2 sm:py-3 px-1 text-sm font-medium border-b-2 whitespace-nowrap transition-colors flex-shrink-0",
                    pathname === item.href
                      ? "text-white border-[#5722cc]"
                      : "text-white/70 border-transparent hover:text-white hover:border-white/30"
                  )}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
