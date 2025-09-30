"use client";

import * as React from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { CheckIcon } from "@radix-ui/react-icons";

interface PricingTableProps {
  plans: Array<{
    id: string;
    name: string;
    description: string;
    price: number;
    currency: string;
    interval: string;
    features: string[];
    metadata: {
      tier: string;
      recommended?: string;
      max_projects?: string;
      max_users?: string;
      support_level?: string;
      description_points?: string;
      highlight_features?: string;
      action?: string;
    };
  }>;
  currentPlanId?: string;
  onSelectPlan: (planId: string) => void;
  isLoading?: boolean;
}

export function PricingTable({
  plans,
  currentPlanId,
  onSelectPlan,
  isLoading,
}: PricingTableProps) {
  if (!plans?.length) return null;

  return (
    <div
      className={`grid gap-8 max-w-[1200px] mx-auto ${plans.length === 1
          ? "md:grid-cols-1 max-w-md"
          : plans.length === 2
            ? "md:grid-cols-2 max-w-2xl"
            : "md:grid-cols-3"
        }`}
    >
      {plans.map((plan) => {
        const isRecommended = plan.metadata.recommended === "true";
        const highlightFeatures =
          plan.metadata.highlight_features?.split(",") || [];
        const descriptionPoints =
          plan.metadata.description_points?.split(",") || [];

        return (
          <div
            key={plan.id}
            className={`relative rounded-2xl p-8 bg-white/5 border transition-all hover:border-[#5722cc]/50 ${isRecommended
                ? "border-[#5722cc] shadow-lg shadow-[#5722cc]/20"
                : "border-white/10"
              }`}
          >
            {isRecommended && (
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-[#5722cc] text-white px-6 py-1.5 rounded-full text-sm font-medium">
                Most Popular
              </div>
            )}

            <div className="text-center mb-8">
              <h3 className="text-2xl font-bold mb-3">{plan.name}</h3>
              <div className="text-4xl font-bold mb-3">
                ${plan.price}
                <span className="text-lg font-normal text-white/60">
                  /{plan.interval}
                </span>
              </div>
              <p className="text-white/60 text-sm">{plan.description}</p>

              {/* Highlight Features */}
              {highlightFeatures.length > 0 && (
                <div className="mt-6 grid grid-cols-2 gap-4">
                  {highlightFeatures.map((feature) => (
                    <div
                      key={feature}
                      className="bg-white/5 rounded-lg p-3 text-center"
                    >
                      <div className="text-lg font-bold text-[#5722cc]">
                        {feature.split(":")[0]}
                      </div>
                      <div className="text-sm text-white/60">
                        {feature.split(":")[1]}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Description Points */}
              {descriptionPoints.length > 0 && (
                <div className="mt-6 space-y-2 text-sm text-white/80">
                  {descriptionPoints.map((point) => (
                    <p key={point}>{point.trim()}</p>
                  ))}
                </div>
              )}

              {/* Features List */}
              <ul className="mt-8 space-y-4 text-sm">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center text-white/80">
                    <CheckIcon className="w-5 h-5 mr-3 text-[#5722cc]" />
                    {feature.trim()}
                  </li>
                ))}
              </ul>

              {/* Additional Info */}
              {plan.metadata.max_projects && (
                <div className="mt-4 text-sm text-white/60">
                  Up to {plan.metadata.max_projects} projects
                </div>
              )}
              {plan.metadata.max_users && (
                <div className="text-sm text-white/60">
                  Up to {plan.metadata.max_users} team members
                </div>
              )}
              {plan.metadata.support_level && (
                <div className="text-sm text-white/60">
                  {plan.metadata.support_level} support
                </div>
              )}
            </div>

            <Button
              onClick={() => onSelectPlan(plan.id)}
              disabled={isLoading}
              className={`w-full h-11 text-sm font-medium transition-all ${isRecommended
                  ? "bg-[#5722cc] hover:bg-[#5722cc]/90 shadow-md hover:shadow-lg"
                  : "hover:bg-white/10"
                }`}
              variant={isRecommended ? "default" : "outline"}
            >
              {isLoading
                ? "Processing..."
                : plan.metadata.action || "Get Started"}
            </Button>
          </div>
        );
      })}
    </div>
  );
}
