"use client";

import {
  Tabs,
  TabsList,
  TabsTrigger,
} from "@karrio/insiders/components/ui/tabs";
import { dynamicMetadata } from "@karrio/core/components/metadata";

export const generateMetadata = dynamicMetadata("Automation");
export const description = "Shipping automation tooling.";

export default function Page() {
  return (
    <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold md:text-2xl">Automation</h1>
      </div>

      <Tabs defaultValue="your-accounts">
        <TabsList>
          <TabsTrigger value="your-accounts">Workflows</TabsTrigger>
          <TabsTrigger value="system-accounts">Shipping Rules</TabsTrigger>
        </TabsList>
      </Tabs>
    </main>
  );
}
