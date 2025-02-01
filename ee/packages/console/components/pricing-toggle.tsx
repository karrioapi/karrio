import * as React from "react";
import { cn } from "@karrio/insiders/lib/utils";

interface PricingToggleProps {
    value: "cloud" | "self-hosted";
    onChange: (value: "cloud" | "self-hosted") => void;
}

export function PricingToggle({ value, onChange }: PricingToggleProps) {
    return (
        <div className="flex items-center justify-center gap-4 mb-8">
            <button
                onClick={() => onChange("cloud")}
                className={cn(
                    "px-4 py-2 rounded-full text-sm font-medium transition-colors",
                    value === "cloud"
                        ? "bg-[#5722cc] text-white"
                        : "text-white/60 hover:text-white"
                )}
            >
                Cloud
            </button>
            <button
                onClick={() => onChange("self-hosted")}
                className={cn(
                    "px-4 py-2 rounded-full text-sm font-medium transition-colors",
                    value === "self-hosted"
                        ? "bg-[#5722cc] text-white"
                        : "text-white/60 hover:text-white"
                )}
            >
                Self-hosted
            </button>
        </div>
    );
}
