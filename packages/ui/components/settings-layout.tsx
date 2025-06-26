"use client";

import { SettingsNavigation } from './settings-navigation';
import { Button } from './ui/button';

interface SettingsLayoutProps {
  children: React.ReactNode;
  showOrganization?: boolean;
  title?: string;
  createButton?: {
    label: string;
    onClick: () => void;
    icon: React.ReactNode;
  };
}

export function SettingsLayout({
  children,
  showOrganization = false,
  title = "Settings",
  createButton
}: SettingsLayoutProps) {
  return (
    <div className="flex-1 space-y-6 py-6 px-0">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
      </div>

      <SettingsNavigation showOrganization={showOrganization} />

      <div className="space-y-6">
        {children}
      </div>
    </div>
  );
}
