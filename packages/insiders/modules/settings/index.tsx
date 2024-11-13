"use client";

import { dynamicMetadata } from "@karrio/core/components/metadata";

export const generateMetadata = dynamicMetadata("Settings");
export const description = "Settings and adminstration.";

export default function Page() {
  return (
    <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold md:text-2xl">Settings</h1>
      </div>
    </main>
  );
}
