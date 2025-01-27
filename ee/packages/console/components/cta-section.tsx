"use client";

import { Button } from "@karrio/insiders/components/ui/button";
import Image from "next/image";

export function CTASection() {
  return (
    <section className="py-24 relative">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,#5722cc0d,transparent_50%)]" />
      <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
      <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px] space-y-12">
        {/* Header */}
        <div className="text-center space-y-4">
          <h2 className="text-4xl font-bold">
            Two hosting options, same benefits
          </h2>
          <p className="text-white/60 max-w-2xl mx-auto">
            Whether you choose the cloud version or decide to host the solution
            yourself, you will benefit from our powerful API and user-friendly
            interface.
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

            <Button variant="outline" size="lg" className="w-full sm:w-auto">
              Deploy Open Source
            </Button>

            <div className="aspect-video relative rounded-lg overflow-hidden">
              <Image
                src="/placeholder-dark.svg"
                alt="Karrio OSS Interface"
                fill
                className="object-cover"
              />
            </div>
          </div>

          {/* Karrio Premium Card */}
          <div className="bg-[#0f0826] rounded-xl p-8 space-y-8 border border-white/10">
            <div className="space-y-4">
              <Image src="/icon.svg" alt="Karrio Icon" width={40} height={40} />
              <h3 className="text-2xl font-semibold">Karrio Premium</h3>
              <p className="text-white/60">
                The optimal solution for teams with control and flexibility.
              </p>
            </div>

            <Button
              size="lg"
              className="w-full sm:w-auto bg-[#5722cc] hover:bg-[#5722cc]/90"
            >
              Book a demo
            </Button>

            <div className="aspect-video relative rounded-lg overflow-hidden">
              <Image
                src="/placeholder-dark.svg"
                alt="Karrio Premium Interface"
                fill
                className="object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
