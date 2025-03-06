"use client";

import { Button } from "@karrio/insiders/components/ui/button";
import { Sheet, SheetContent, SheetTrigger, SheetClose } from "@karrio/insiders/components/ui/sheet";
import { Menu, Truck, Building, ShoppingCart, ChevronDown } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

// Define use case items with descriptions - copied from UseCasesDropdown
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

export function MobileMenu() {
    const [useCasesOpen, setUseCasesOpen] = useState(false);

    return (
        <div className="md:hidden ml-[-8px] mr-1">
            <Sheet>
                <SheetTrigger asChild>
                    <Button variant="ghost" size="icon" className="text-white p-0 m-0">
                        <Menu className="h-6 w-6" />
                        <span className="sr-only">Toggle menu</span>
                    </Button>
                </SheetTrigger>
                <SheetContent side="left" className="bg-[#0f0826] text-white border-white/10 w-[250px] p-0 pt-6">
                    <nav className="flex flex-col mt-8">
                        <SheetClose asChild>
                            <Link
                                href="https://docs.karrio.io"
                                className="text-white/80 hover:text-white transition-colors px-6 py-3"
                            >
                                Docs
                            </Link>
                        </SheetClose>

                        <SheetClose asChild>
                            <Link
                                href="https://karrio.io/blog"
                                className="text-white/80 hover:text-white transition-colors px-6 py-3"
                            >
                                Blog
                            </Link>
                        </SheetClose>

                        <SheetClose asChild>
                            <Link
                                href="https://docs.karrio.io/carriers/"
                                className="text-white/80 hover:text-white transition-colors px-6 py-3"
                            >
                                Carriers
                            </Link>
                        </SheetClose>

                        <div className="text-white/80">
                            <button
                                onClick={() => setUseCasesOpen(!useCasesOpen)}
                                className="flex items-center justify-between w-full text-white/80 hover:text-white transition-colors px-6 py-3 hover:bg-white/5"
                            >
                                <span>Use Cases</span>
                                <ChevronDown
                                    className={`h-4 w-4 transition-transform ${useCasesOpen ? 'rotate-180' : ''}`}
                                />
                            </button>

                            {useCasesOpen && (
                                <div className="bg-[#1a103d]/50 pl-4">
                                    {USE_CASES.map((useCase, index) => {
                                        const Icon = useCase.icon;
                                        return (
                                            <SheetClose key={index} asChild>
                                                <Link
                                                    href={useCase.href}
                                                    className="flex items-center gap-2 px-6 py-3 text-white/80 hover:text-white hover:bg-white/5 transition-colors"
                                                >
                                                    <div className="rounded-full bg-[#2d1d63] p-1.5">
                                                        <Icon className="h-4 w-4" style={{ color: useCase.color }} />
                                                    </div>
                                                    <div>
                                                        <div className="text-sm">{useCase.title}</div>
                                                        <p className="text-xs text-white/60">{useCase.description}</p>
                                                    </div>
                                                </Link>
                                            </SheetClose>
                                        );
                                    })}
                                </div>
                            )}
                        </div>

                        <SheetClose asChild>
                            <Link
                                href="https://docs.karrio.io/platform"
                                className="text-white/80 hover:text-white transition-colors px-6 py-3"
                            >
                                Platform
                            </Link>
                        </SheetClose>
                    </nav>
                </SheetContent>
            </Sheet>
        </div>
    );
} 