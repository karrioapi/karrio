"use client";

import {
  Tabs,
  TabsList,
  TabsTrigger,
} from "@karrio/insiders/components/ui/tabs";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { Button } from "@karrio/insiders/components/ui/button";
import { Switch } from "@karrio/insiders/components/ui/switch";
import { Pencil, Trash2, Lock } from "lucide-react";

export const generateMetadata = dynamicMetadata("Carriers");
export const description =
  "A page displaying a list of carrier accounts with their details and actions.";

// Sample carrier data
const carriers = [
  {
    name: "DHL Parcel DE",
    id: "dhl-parcel-post-test",
    color: "bg-yellow-400",
    active: false,
  },
  {
    name: "FedEx Web Service",
    id: "fedex-truck-test",
    color: "bg-purple-700",
    active: false,
  },
  { name: "FedEx", id: "fedex-test", color: "bg-purple-700", active: false },
  { name: "Comet", id: "comet-live", color: "bg-orange-500", active: false },
  { name: "Sendle", id: "sendle-test", color: "bg-orange-600", active: true },
  {
    name: "Express Freight",
    id: "express-freight",
    color: "bg-red-600",
    active: false,
  },
  { name: "EasyPost", id: "easypost", color: "bg-blue-700", active: false },
  {
    name: "TST Overland",
    id: "tst-overland",
    color: "bg-green-600",
    active: true,
  },
  {
    name: "DHL Parcel Poland",
    id: "dhl-poland",
    color: "bg-yellow-400",
    active: false,
  },
  { name: "DHL Express", id: "DHL_M", color: "bg-yellow-400", active: false },
];

export default function Page() {
  return (
    <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold md:text-2xl">Carriers</h1>
        <Button>Register a carrier</Button>
      </div>

      <Tabs defaultValue="your-accounts">
        <TabsList>
          <TabsTrigger value="your-accounts">Your Accounts</TabsTrigger>
          <TabsTrigger value="system-accounts">System Accounts</TabsTrigger>
          <TabsTrigger value="rate-sheets">Rate Sheets</TabsTrigger>
        </TabsList>
      </Tabs>

      <div className="space-y-4">
        <h2 className="text-lg font-semibold">ACCOUNTS</h2>
        {carriers.map((carrier) => (
          <div
            key={carrier.id}
            className="flex items-center justify-between border-b pb-4"
          >
            <div className="flex items-center space-x-4">
              <div
                className={`w-48 h-12 ${carrier.color} rounded flex items-center justify-center text-white font-bold`}
              >
                {carrier.name}
              </div>
              <Button variant="outline" size="sm">
                Test
              </Button>
              <Switch checked={carrier.active} />
            </div>
            <div className="flex items-center space-x-8">
              <div>
                <div>
                  carrier_name: {carrier.name.toLowerCase().replace(" ", "_")}
                </div>
                <div className="flex items-center">
                  carrier_id: {carrier.id}
                  <Lock className="ml-2 h-4 w-4" />
                </div>
              </div>
              <div className="flex space-x-2">
                <Button variant="ghost" size="icon">
                  <Pencil className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
