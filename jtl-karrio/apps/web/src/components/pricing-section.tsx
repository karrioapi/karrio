"use client";

import { Button } from "@karrio/ui/components/ui/button";
import { Check } from "lucide-react";
import { useState } from "react";
import Link from "next/link";

type PricingFeature = {
  text: string;
  soon?: boolean;
};

type PricingPlan = {
  name: string;
  description: string;
  price: string | "Contact us";
  priceDetail?: string;
  popular?: boolean;
  limitedSpots?: boolean;
  features: PricingFeature[];
  button: {
    text: string;
    variant?: "default" | "outline";
    href?: string;
    target?: string;
  };
};

const PRICING_PLANS: Record<string, { cloud: PricingPlan; selfHosted?: PricingPlan }> = {
  scale: {
    cloud: {
      name: "Scale",
      description: "Pay-as-you-go managed platform. Perfect for growing businesses that need reliable shipping infrastructure.",
      price: "$499",
      priceDetail: "/month base + usage",
      popular: true,
      limitedSpots: true,
      button: {
        text: "Join Waitlist",
        variant: "outline",
        href: "https://share.hsforms.com/1xRE12oYoRFWUR8LvOW2Eqwcvwq2",
        target: "_blank"
      },
      features: [
        { text: "Pay-as-you-go pricing model" },
        { text: "$0.03 per label/tracker" },
        { text: "Managed infrastructure" },
        { text: "Email & Slack support" },
        { text: "Multi-tenant support" },
        { text: "Platform APIs" },
        { text: "Real-time tracking", soon: true },
        { text: "Custom integrations", soon: true },
      ],
    },
  },
  enterprise: {
    cloud: {
      name: "Enterprise",
      description: "Self-hosted solution with full control. Custom-tailored for enterprise needs with dedicated support.",
      price: "Contact us",
      button: {
        text: "Contact Sales",
        variant: "outline",
        href: "https://share.hsforms.com/1xRE12oYoRFWUR8LvOW2Eqwcvwq2",
        target: "_blank"
      },
      features: [
        { text: "Self-hosted deployment" },
        { text: "Unlimited labels/trackers" },
        { text: "Full source code access" },
        { text: "One-on-one developer calls" },
        { text: "Dedicated carrier onboarding support" },
        { text: "Custom integrations" },
        { text: "SLA (99.999% uptime)" },
        { text: "Compliance Check SOC2, HIPAA", soon: true },
      ],
    },
  },
};

function PricingCard({ plan, className = "" }: { plan: PricingPlan; className?: string }) {
  return (
    <div className={`bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 relative flex flex-col min-h-[800px] ${className}`}>
      {plan.popular && (
        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-[#5722cc] text-white text-sm px-3 py-1 rounded-full">
          Most Popular
        </div>
      )}
      {plan.limitedSpots && (
        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-[#5722cc] text-white text-sm px-3 py-1 rounded-full">
          Limited Spots
        </div>
      )}
      <div className="min-h-[220px]">
        <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
        <div className="text-3xl font-bold mb-4">
          {plan.price}
          {plan.priceDetail && <span className="text-lg font-normal text-white/60">{plan.priceDetail}</span>}
        </div>
        <p className="text-base text-white/60 mb-6">{plan.description}</p>
        {plan.button.href ? (
          <Button
            variant={plan.button.variant}
            className={`w-full mb-8 ${plan.button.variant === undefined ? 'bg-[#5722cc] hover:bg-[#5722cc]/90' : ''}`}
            asChild
          >
            <Link href={plan.button.href} target={plan.button.target}>
              {plan.button.text}
            </Link>
          </Button>
        ) : (
          <Button
            variant={plan.button.variant}
            className={`w-full mb-8 ${plan.button.variant === undefined ? 'bg-[#5722cc] hover:bg-[#5722cc]/90' : ''}`}
          >
            {plan.button.text}
          </Button>
        )}
      </div>
      <ul className="space-y-4 flex-grow border-t border-white/10 pt-4">
        {plan.features.map((feature, index) => (
          <li key={index} className="flex items-start gap-3">
            <div className="mt-1 rounded-full bg-[#79e5dd]/10 p-1">
              <Check className="h-3 w-3 text-[#79e5dd]" />
            </div>
            <span>
              {feature.text}
              {feature.soon && <span className="text-white/40 ml-1">(soon)</span>}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function PricingSection() {
  // Set default to "cloud" and remove the selector UI
  const [deploymentType, setDeploymentType] = useState<"cloud" | "self-hosted">("cloud");

  return (
    <section id="pricing" className="py-24 relative">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,#5722cc1a,transparent_70%)]" />
      <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
      <div className="absolute inset-0 backdrop-blur-[100px]" />
      <div className="container relative mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl">
        <div className="text-center mb-16">
          <div className="text-[#79e5dd] mb-4">Pricing</div>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Simple, transparent pricing
          </h2>
          <p className="text-base text-white/60 max-w-2xl mx-auto">
            Choose between our managed Scale platform or self-hosted Enterprise solution. 
            Scale is coming soon with pay-as-you-go pricing.
          </p>
        </div>

        {/* Deployment type selector commented out */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex items-center gap-4 bg-white/5 rounded-lg p-2">
            <button
              onClick={() => setDeploymentType("cloud")}
              className={`px-4 py-2 rounded-md transition-colors ${deploymentType === "cloud"
                ? "bg-[#5722cc] text-white"
                : "text-white/60 hover:text-white"
                }`}
            >
              Cloud Hosted
            </button>
            <button
              onClick={() => setDeploymentType("self-hosted")}
              className={`px-4 py-2 rounded-md transition-colors ${deploymentType === "self-hosted"
                ? "bg-[#5722cc] text-white"
                : "text-white/60 hover:text-white"
                }`}
            >
              Self Hosted
            </button>
          </div>
        </div>


        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 justify-items-center max-w-5xl mx-auto">
          {Object.entries(PRICING_PLANS).map(([key, { cloud, selfHosted: selfHosted }]) => {
            const plan = deploymentType === "cloud" ? cloud : (selfHosted ?? cloud);
            return (
              <PricingCard
                key={key}
                plan={plan}
                className={`${key === "premium" ? "bg-gradient-to-b from-[#5722cc]/20 to-transparent border-[#5722cc]/30" : ""} max-w-md w-full`}
              />
            );
          })}
        </div>
      </div>
    </section>
  );
}
