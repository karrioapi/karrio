"use client";

import Image from "next/image";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import React from "react";

export const HowItWorksSection = () => {
  const [mounted, setMounted] = useState(false);
  const [selectedStep, setSelectedStep] = useState(1);

  // Wait for component to mount to avoid hydration mismatch
  useEffect(() => {
    setMounted(true);
  }, []);

  const steps = [
    {
      number: 1,
      title: "Manage carrier connections",
      description: "Setup accounts and API credentials to enable Karrio's connection to your carriers.",
      image: "/edit-carrier-action-image.png"
    },
    {
      number: 2,
      title: "Fetch live rates",
      description: "Your users can fetch live rates from a network of carriers by submitting shipment details using the user interface or programmatically via API.",
      image: "/live-rates-image.png"
    },
    {
      number: 3,
      title: "Generate shipping labels",
      description: "Karrio will generate shipping labels based on your preferred shipping service. You can then download and print generated labels.",
      image: "/print-label-image.png"
    },
    {
      number: 4,
      title: "Track packages",
      description: "Labels purchased on Karrio are automatically linked with a package tracker to provide real-time delivery status. You can also create trackers for shipments made outside of Karrio.",
      image: "/track-shipment-image.png"
    }
  ];

  return (
    <section className="py-12 md:py-28 bg-gradient-to-b from-white to-gray-50 dark:from-[#0f0826] dark:to-[#0a051b]">
      <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl">
        <div className="text-center mb-16">
          <h2 className="text-sm uppercase tracking-wider text-primary font-medium mb-4">How it works</h2>
          <h3 className="text-3xl md:text-5xl font-bold mb-8">Effortless shipping integration</h3>
          <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            A simple four-step process to integrate shipping into your platform
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-8 md:gap-16 items-start">
          {/* Steps navigation column */}
          <div className="md:col-span-2 space-y-8">
            {steps.map((step) => (
              <div
                key={step.number}
                className={`group cursor-pointer transition-all duration-300 ease-in-out`}
                onClick={() => setSelectedStep(step.number)}
              >
                <div className="flex items-start">
                  <div className="relative">
                    <span
                      className={`flex h-10 w-10 shrink-0 rounded-full items-center justify-center font-bold z-10 transition-all text-sm
                        ${selectedStep === step.number
                          ? "bg-primary text-white scale-110 ring-2 ring-primary/20"
                          : "bg-gray-100 dark:bg-white/5 text-gray-500 dark:text-gray-400"}`}
                    >
                      {step.number}
                    </span>
                    {step.number < steps.length && (
                      <div
                        className={`absolute top-10 bottom-0 left-1/2 w-0.5 -ml-[1px] h-[calc(100%+1rem)]
                          ${selectedStep === step.number || selectedStep === step.number + 1
                            ? "bg-primary/30"
                            : "bg-gray-200 dark:bg-white/10"}`}
                      ></div>
                    )}
                  </div>

                  <div className="ml-6">
                    <h4
                      className={`text-xl font-semibold mb-3 transition-colors
                        ${selectedStep === step.number
                          ? "text-primary"
                          : "text-gray-900 dark:text-white group-hover:text-primary/80 dark:group-hover:text-primary/80"}`}
                    >
                      {step.title}
                    </h4>
                    <p
                      className={`transition-colors
                        ${selectedStep === step.number
                          ? "text-gray-800 dark:text-gray-200"
                          : "text-gray-600 dark:text-gray-400"}`}
                    >
                      {step.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Image display column */}
          <div className="md:col-span-3 relative">
            <div className="min-h-[300px] md:aspect-[4/3] w-full relative flex items-center justify-center">
              {/* Background decorative elements */}
              <div className="absolute inset-0 w-full h-full overflow-hidden rounded-lg">
                <div className="absolute -top-16 -right-16 w-64 h-64 bg-primary/3 dark:bg-primary/5 rounded-full blur-3xl"></div>
                <div className="absolute -bottom-16 -left-16 w-64 h-64 bg-secondary/3 dark:bg-secondary/5 rounded-full blur-3xl"></div>
              </div>

              {/* Card container */}
              <div className="relative z-10 w-full max-w-xl mx-auto">
                {mounted && steps.map((step) => (
                  <div
                    key={step.number}
                    className={`transition-all duration-300 ease-in-out ${selectedStep === step.number
                      ? 'opacity-100 translate-y-0 relative'
                      : 'opacity-0 translate-y-8 absolute inset-0'
                      }`}
                  >
                    <div className="bg-[#f2f4f7] dark:bg-[#131033] rounded-lg overflow-hidden border-0 p-6 md:p-8">
                      <div className="rounded-lg overflow-hidden">
                        <Image
                          src={step.image}
                          alt={`${step.title} interface`}
                          width={500}
                          height={350}
                          className="w-full h-auto rounded-md"
                          priority={selectedStep === step.number}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
