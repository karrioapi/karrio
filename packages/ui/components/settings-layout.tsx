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
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
          <p className="text-sm text-gray-600 mt-1">
            Manage your account settings and preferences
          </p>
        </div>
        {createButton && (
          <Button onClick={createButton.onClick}>
            {createButton.icon}
            {createButton.label}
          </Button>
        )}
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <SettingsNavigation showOrganization={showOrganization} />
      </div>

      <div className="space-y-6">
        {children}
      </div>
    </div>
  );
}
