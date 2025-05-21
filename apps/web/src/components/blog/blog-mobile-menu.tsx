"use client";

import { Sheet, SheetContent, SheetTrigger, SheetClose } from "@karrio/ui/components/ui/sheet";
import { Button } from "@karrio/ui/components/ui/button";
import { Menu } from "lucide-react";
import Link from "next/link";
import { ThemeToggle } from "./theme-toggle";

export function BlogMobileMenu() {
    return (
        <div className="md:hidden ml-[-8px] mr-1">
            <Sheet>
                <SheetTrigger asChild>
                    <Button variant="ghost" size="icon" className="dark:text-white text-foreground p-0 m-0">
                        <Menu className="h-6 w-6" />
                        <span className="sr-only">Toggle menu</span>
                    </Button>
                </SheetTrigger>
                <SheetContent side="left" className="bg-background backdrop-blur-sm dark:backdrop-blur-none dark:text-white text-foreground dark:border-white/10 border-border/30 shadow-md dark:shadow-none w-[250px] p-0 pt-6">
                    <div className="px-6 py-4 border-b border-border/30 dark:border-white/10">
                        <h2 className="text-lg font-semibold dark:text-white text-foreground">Blog Menu</h2>
                    </div>
                    <nav className="flex flex-col mt-4">
                        <SheetClose asChild>
                            <Link
                                href="/docs"
                                className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors px-6 py-3 font-medium"
                            >
                                Docs
                            </Link>
                        </SheetClose>

                        <SheetClose asChild>
                            <Link
                                href="/blog"
                                className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors px-6 py-3 font-medium"
                            >
                                Blog
                            </Link>
                        </SheetClose>

                        <SheetClose asChild>
                            <Link
                                href="/carriers"
                                className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors px-6 py-3 font-medium"
                            >
                                Carriers
                            </Link>
                        </SheetClose>

                        <SheetClose asChild>
                            <Link
                                href="/platform"
                                className="dark:text-white/80 dark:hover:text-white text-foreground/80 hover:text-foreground transition-colors px-6 py-3 font-medium"
                            >
                                Platform
                            </Link>
                        </SheetClose>

                        <div className="border-t border-border/30 dark:border-white/10 mt-4 pt-4 px-6 py-3">
                            <div className="flex items-center">
                                <span className="dark:text-white/80 text-foreground/80 font-medium mr-2">Toggle Theme</span>
                                <ThemeToggle />
                            </div>
                        </div>
                    </nav>
                </SheetContent>
            </Sheet>
        </div>
    );
}
