"use client";

import { SettingsNavigation } from './settings-navigation';

interface SettingsLayoutProps {
    children: React.ReactNode;
    showOrganization?: boolean;
    title?: string;
}

export function SettingsLayout({
    children,
    showOrganization = false,
    title = "Settings"
}: SettingsLayoutProps) {
    return (
        <div className="flex-1 space-y-6 p-8 pt-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
            </div>

            <SettingsNavigation showOrganization={showOrganization} />

            <div className="space-y-6">
                {children}
            </div>
        </div>
    );
}
