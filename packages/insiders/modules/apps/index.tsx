"use client";

import { Button } from "@karrio/insiders/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@karrio/insiders/components/ui/card";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { Badge } from "@karrio/insiders/components/ui/badge";
import { Star, ArrowRight } from "lucide-react";
import Link from "next/link";

export const generateMetadata = dynamicMetadata("App Store");
export const description =
  "A products dashboard with a sidebar navigation and a main content area. The dashboard has a header with a search input and a user menu. The sidebar has a logo, navigation links, and a card with a call to action. The main content area shows an empty state with a call to action.";
const apps = [
  {
    id: 1,
    name: "Tracking Pro",
    description: "Advanced shipment tracking and notifications",
    category: "Tracking",
    rating: 4.5,
    installs: "10k+",
  },
  {
    id: 2,
    name: "Invoice Generator",
    description: "Automated invoice creation for shipments",
    category: "Billing",
    rating: 4.2,
    installs: "5k+",
  },
  {
    id: 3,
    name: "Route Optimizer",
    description: "AI-powered route optimization for deliveries",
    category: "Logistics",
    rating: 4.8,
    installs: "8k+",
  },
  {
    id: 4,
    name: "Customer Portal",
    description: "Branded tracking page for your customers",
    category: "Customer Service",
    rating: 4.3,
    installs: "3k+",
  },
  {
    id: 5,
    name: "Inventory Sync",
    description: "Real-time inventory management integration",
    category: "Inventory",
    rating: 4.6,
    installs: "7k+",
  },
  {
    id: 6,
    name: "Customs Docs",
    description: "Automated customs documentation preparation",
    category: "International",
    rating: 4.4,
    installs: "4k+",
  },
];

const AppCard = ({ app }: { app: (typeof apps)[0] }) => (
  <Card className="w-full">
    <CardHeader>
      <CardTitle className="flex items-center justify-between">
        <span>{app.name}</span>
        <Badge variant="secondary">{app.category}</Badge>
      </CardTitle>
      <CardDescription>{app.description}</CardDescription>
    </CardHeader>
    <CardContent>
      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
        <Star className="h-4 w-4 fill-yellow-400 stroke-yellow-400" />
        <span>{app.rating}</span>
        <span>•</span>
        <span>{app.installs} installs</span>
      </div>
    </CardContent>
    <CardFooter>
      <Link href={`/app-store/${app.id}`} className="w-full">
        <Button variant="outline" className="w-full">
          View Details
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </Link>
    </CardFooter>
  </Card>
);
export default function Dashboard() {
  return (
    <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
      <div className="flex items-center">
        <h1 className="text-lg font-semibold md:text-2xl">App Store</h1>
      </div>

      <section className="mb-8">
        <h4 className="text-xl font-semibold mb-4">Featured Apps</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {apps.slice(0, 3).map((app) => (
            <AppCard key={app.id} app={app} />
          ))}
        </div>
      </section>

      <section>
        <h4 className="text-xl font-semibold mb-4">All Apps</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {apps.map((app) => (
            <AppCard key={app.id} app={app} />
          ))}
        </div>
      </section>
    </main>
  );
}
