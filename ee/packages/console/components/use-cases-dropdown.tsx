"use client";

import Link from "next/link";
import { Truck, Building, ShoppingCart, ChevronDown } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@karrio/insiders/components/ui/dropdown-menu";

// Define use case items with descriptions
const USE_CASES = [
  {
    icon: Truck,
    title: "Logistics Providers",
    description: "Logistics partner network",
    href: "/use-cases/logistics-providers",
    color: "#79e5dd"
  },
  {
    icon: ShoppingCart,
    title: "Platforms",
    description: "Shipping integration",
    href: "/use-cases/platforms",
    color: "#79e5dd"
  },
  {
    icon: Building,
    title: "Enterprise",
    description: "Custom shipping solution",
    href: "/use-cases/enterprise-solutions",
    color: "#79e5dd"
  }
];

export function UseCasesDropdown() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="text-white/80 hover:text-white transition-colors flex items-center">
        Use Cases
        <ChevronDown className="ml-1 h-3.5 w-3.5 opacity-70" />
      </DropdownMenuTrigger>
      <DropdownMenuContent
        className="bg-[#1a103d] border border-white/10 rounded-lg p-1.5 shadow-xl backdrop-blur-sm min-w-[240px] animate-in fade-in-80 zoom-in-95 data-[side=bottom]:slide-in-from-top-2"
        align="center"
      >
        <div className="grid gap-1.5">
          {USE_CASES.map((useCase, index) => {
            const Icon = useCase.icon;
            return (
              <DropdownMenuItem
                key={index}
                className="rounded-md px-3 py-2 text-white hover:bg-white/10 focus:bg-white/10 cursor-pointer transition-colors duration-150"
              >
                <Link href={useCase.href} className="w-full">
                  <div className="flex items-start gap-2.5">
                    <div className="rounded-full bg-[#2d1d63] p-1.5 mt-0.5">
                      <Icon className="h-4 w-4" style={{ color: useCase.color }} />
                    </div>
                    <div className="flex-1">
                      <div className="font-medium text-sm">{useCase.title}</div>
                      <p className="text-xs text-white/60 mt-0.5">{useCase.description}</p>
                    </div>
                  </div>
                </Link>
              </DropdownMenuItem>
            );
          })}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
