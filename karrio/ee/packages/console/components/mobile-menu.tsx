"use client";

import { Sheet, SheetContent, SheetTrigger, SheetClose } from "@karrio/ui/components/ui/sheet";
import { Button } from "@karrio/ui/components/ui/button";
import { Menu } from "lucide-react";
import Link from "next/link";

export function MobileMenu() {
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

            <SheetClose asChild>
              <Link
                href="/"
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
