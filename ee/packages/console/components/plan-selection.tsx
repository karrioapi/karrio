"use client";

import { Button } from "@karrio/insiders/components/ui/button";
import { Check, InfoIcon } from "lucide-react";
import { cn } from "@karrio/insiders/lib/utils";

interface Plan {
  id: string;
  name: string;
  description: string | null;
  price: number;
  currency: string;
  interval: string;
  features: string[];
  metadata: Record<string, string>;
}

interface PlanSelectionProps {
  plans: Plan[];
  selectedPlan: string | null;
  onPlanSelect: (planId: string) => void;
  onConfirm: () => void;
  onCancel: () => void;
  isLoading?: boolean;
  hasPaymentMethod?: boolean;
}

export function PlanSelection({
  plans,
  selectedPlan,
  onPlanSelect,
  onConfirm,
  onCancel,
  isLoading,
  hasPaymentMethod,
}: PlanSelectionProps) {
  const sortedPlans = [...plans].sort((a, b) => a.price - b.price);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {sortedPlans.map((plan) => (
          <div
            key={plan.id}
            className={cn(
              "relative rounded-lg border p-6 shadow-sm transition-all",
              selectedPlan === plan.id
                ? "border-primary bg-primary/5"
                : "hover:border-primary/50",
            )}
          >
            <div className="space-y-4">
              <div className="space-y-1">
                <h3 className="font-semibold">{plan.name}</h3>
                <p className="text-sm text-muted-foreground">
                  {plan.description}
                </p>
              </div>

              <div className="text-3xl font-bold">
                {new Intl.NumberFormat("en-US", {
                  style: "currency",
                  currency: plan.currency,
                }).format(plan.price)}
                <span className="text-sm font-normal text-muted-foreground">
                  /{plan.interval}
                </span>
              </div>

              <ul className="space-y-2 text-sm">
                {plan.features.map((feature: string, index: number) => (
                  <li key={index} className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-primary" />
                    {feature}
                  </li>
                ))}
              </ul>

              <Button
                variant={selectedPlan === plan.id ? "default" : "outline"}
                className="w-full"
                onClick={() => onPlanSelect(plan.id)}
              >
                {selectedPlan === plan.id ? "Selected" : "Select Plan"}
              </Button>
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-end gap-4 pt-4 border-t">
        {!hasPaymentMethod && selectedPlan && (
          <div className="flex-1 text-sm text-amber-600">
            <InfoIcon className="inline-block h-4 w-4 mr-1" />
            You'll need to add a payment method to complete your subscription
          </div>
        )}
        <Button variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button onClick={onConfirm} disabled={!selectedPlan || isLoading}>
          {isLoading ? "Processing..." : "Confirm"}
        </Button>
      </div>
    </div>
  );
}
