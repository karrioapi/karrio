"use client";

import {
  Tabs,
  TabsList,
  TabsTrigger,
} from "@karrio/insiders/components/ui/tabs";
import { dynamicMetadata } from "@karrio/core/components/metadata";

export const generateMetadata = dynamicMetadata("Developers");
export const description = "API access and transactions visualization.";

export default function Page() {
  return (
    <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold md:text-2xl">Developers</h1>
      </div>

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="api-keys">API Keys</TabsTrigger>
          <TabsTrigger value="api-logs">Logs</TabsTrigger>
          <TabsTrigger value="api-events">Events</TabsTrigger>
          <TabsTrigger value="webhooks">Webhooks</TabsTrigger>
        </TabsList>
      </Tabs>
    </main>
  );
}
