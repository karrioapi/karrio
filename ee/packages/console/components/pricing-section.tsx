"use client";

import { Button } from "@karrio/insiders/components/ui/button";
import { Check } from "lucide-react";
import { useState } from "react";

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
  features: PricingFeature[];
  button: {
    text: string;
    variant?: "default" | "outline";
  };
};

const PRICING_PLANS: Record<string, { cloud: PricingPlan; selfHosted?: PricingPlan }> = {
  insiders: {
    cloud: {
      name: "Insiders",
      description: "Advanced features included. Dedicated support team. Scale your operations.",
      price: "$299",
      priceDetail: "/month",
      popular: true,
      button: {
        text: "Join Waitlist",
      },
      features: [
        { text: "10,000 labels/trackers a month" },
        { text: "$0.04 overage beyond" },
        { text: "Multi-tenant & User management" },
        { text: "Email & Slack support" },
        { text: "Customizable dashboard", soon: true },
        { text: "Platform Admin dashboard" },
        { text: "Platform APIs" },
      ],
    },
    selfHosted: {
      name: "Insiders",
      description: "Advanced features included. Dedicated support team. Scale your operations.",
      price: "$299",
      priceDetail: "/month",
      popular: true,
      button: {
        text: "Join Now",
      },
      features: [
        { text: "Unlimited labels/trackers a month" },
        { text: "No overages" },
        { text: "Multi-tenant & User management" },
        { text: "Email & Slack support" },
        { text: "Customizable dashboard", soon: true },
        { text: "Platform Admin dashboard" },
        { text: "Platform APIs" },
      ],
    },
  },
  scale: {
    cloud: {
      name: "Scale",
      description: "High-volume enterprise features. Premium support included. Enterprise-grade security.",
      price: "$2,499",
      priceDetail: "/month",
      button: {
        text: "Get Started",
        variant: "outline",
      },
      features: [
        { text: "100,000 labels/trackers a month" },
        { text: "$0.02 overage beyond" },
        { text: "One-on-one developer calls" },
        { text: "Up to 5 new carrier integrations/month" },
        { text: "Expedited features and integrations" },
        { text: "SLA (99.999% uptime)" },
        { text: "Compliance Check SOC2, HIPAA", soon: true },
      ],
    },
    selfHosted: {
      name: "Scale",
      description: "High-volume enterprise features. Premium support included. Enterprise-grade security.",
      price: "$2,499",
      priceDetail: "/month",
      button: {
        text: "Get Started",
        variant: "outline",
      },
      features: [
        { text: "Unlimited labels/trackers a month" },
        { text: "No overages" },
        { text: "One-on-one developer calls" },
        { text: "Up to 5 new carrier integrations/month" },
        { text: "Expedited features and integrations" },
        { text: "SLA (99.999% uptime)" },
        { text: "Compliance Check SOC2, HIPAA", soon: true },
      ],
    },
  },
  enterprise: {
    cloud: {
      name: "Enterprise",
      description: "Custom-tailored solution. Unlimited shipping volume. Dedicated enterprise support.",
      price: "Contact us",
      button: {
        text: "Contact Sales",
        variant: "outline",
      },
      features: [
        { text: "Unlimited labels/trackers a month" },
        { text: "No overages" },
        { text: "One-on-one developer calls" },
        { text: "Dedicated carrier onboarding support" },
        { text: "Expedited features and integrations" },
        { text: "SLA (99.999% uptime)" },
        { text: "Volume Discount" },
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
      <div className="min-h-[220px]">
        <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
        <div className="text-3xl font-bold mb-4">
          {plan.price}
          {plan.priceDetail && <span className="text-lg font-normal text-white/60">{plan.priceDetail}</span>}
        </div>
        <p className="text-base text-white/60 mb-6">{plan.description}</p>
        <Button
          variant={plan.button.variant}
          className={`w-full mb-8 ${plan.button.variant === undefined ? 'bg-[#5722cc] hover:bg-[#5722cc]/90' : ''}`}
        >
          {plan.button.text}
        </Button>
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
  const [deploymentType, setDeploymentType] = useState<"cloud" | "self-hosted">("cloud");

  return (
    <section className="py-24 relative">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,#5722cc1a,transparent_70%)]" />
      <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
      <div className="absolute inset-0 backdrop-blur-[100px]" />
      <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
        <div className="text-center mb-16">
          <div className="text-[#79e5dd] mb-4">Pricing</div>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Simple, transparent pricing
          </h2>
          <p className="text-base text-white/60 max-w-2xl mx-auto">
            Choose the plan that best fits your business needs. All plans include access to our core features.
          </p>
        </div>

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

        <div className="grid md:grid-cols-3 gap-12">
          {Object.entries(PRICING_PLANS).map(([key, { cloud, selfHosted: selfHosted }]) => {
            const plan = deploymentType === "cloud" ? cloud : (selfHosted ?? cloud);
            return (
              <PricingCard
                key={key}
                plan={plan}
                className={key === "premium" ? "bg-gradient-to-b from-[#5722cc]/20 to-transparent border-[#5722cc]/30" : ""}
              />
            );
          })}
        </div>
      </div>
    </section>
  );
}
