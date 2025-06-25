"use client";
// Sheet components removed - using custom sidebar
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Settings, X } from "lucide-react";
import { AppContainer } from "@karrio/app-store";
import React from "react";

interface PhysicalApp {
  id: string;
  manifest: any;
  isInstalled: boolean;
  installation?: any;
}

interface AppSheetProps {
  app: PhysicalApp;
  onClose: () => void;
}

export function AppSheet({ app, onClose }: AppSheetProps) {
  return (
    <div className="h-full flex flex-col">
      <div className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">
            {app.manifest.name}
          </h2>
          <div>
            <Button variant="ghost" size="sm" onClick={onClose} className="p-0 rounded-full">
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      <div className="overflow-y-auto bg-white flex-1">
        <AppContainer
          key={`${app.id}-${app.installation?.updated_at || Date.now()}`}
          appId={app.id}
          viewport="dashboard"
          className="w-full h-full pb-16"
        />
      </div>
    </div>
  );
}
