"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home,
  Truck,
  Package,
  Package2,
  Navigation,
  LayoutGrid,
  ShoppingCart,
  Zap,
  Terminal,
  Book,
  Cog,
} from "lucide-react";

export const Sidebar = () => {
  const pathname = usePathname();

  const links = [
    { href: "/", icon: Home, label: "Dashboard" },
    { href: "/shipments", icon: Package, label: "Shipments" },
    { href: "/trackers", icon: Navigation, label: "Trackers" },
    { href: "/orders", icon: ShoppingCart, label: "Orders" },
    { href: "/connections", icon: Truck, label: "Carriers" },
    { href: "/automation", icon: Zap, label: "Automation" },
    { href: "/apps", icon: LayoutGrid, label: "Apps" },
    { href: "/developers", icon: Terminal, label: "Developers" },
    { href: "/resources", icon: Book, label: "Resources" },
    { href: "/settings", icon: Cog, label: "Settings" },
  ];

  return (
    <div className="hidden border-r md:block">
      <div className="flex h-full max-h-screen flex-col gap-2">
        <div className="flex h-14 items-center px-4 lg:h-[60px] lg:px-6">
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <Package2 className="h-6 w-6" />
            <span className="">Purple Store</span>
          </Link>
        </div>

        <div className="flex-1">
          <nav className="grid items-start px-2 text-sm font-medium lg:px-4">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:text-primary ${
                  pathname === link.href
                    ? "bg-muted text-primary"
                    : "text-muted-foreground"
                }`}
              >
                <link.icon className="h-4 w-4" />
                {link.label}
              </Link>
            ))}
          </nav>
        </div>

        <div className="mt-auto p-4">
          <span>Version: 2024.6.5</span>
        </div>
      </div>
    </div>
  );
};
