"use client";
import { SheetHeader, SheetTitle, SheetDescription } from "@karrio/ui/components/ui/sheet";
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
    const handleConfigure = () => {
        // TODO: Implement app configuration
        console.log("Configure app:", app.id);
    };

    return (
        <div className="h-full flex flex-col">
            <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
                <div className="flex items-center justify-between">
                    <SheetTitle className="text-lg font-semibold">
                        {app.manifest.name}
                    </SheetTitle>
                </div>
                <SheetDescription className="sr-only">
                    Running {app.manifest.name} application in embedded view.
                </SheetDescription>
            </SheetHeader>

            <div className="flex-1 overflow-y-auto px-4 py-4 space-y-6 pb-32">
                {/* App Header */}
                <div className="space-y-4">
                    <div className="flex items-start gap-4">
                        <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-xl font-semibold flex-shrink-0">
                            {app.manifest.name?.charAt(0) || 'A'}
                        </div>
                        <div className="flex-1 min-w-0">
                            <h2 className="text-xl font-semibold text-slate-900 mb-1">
                                {app.manifest.name}
                            </h2>
                            <p className="text-sm text-slate-600 mb-2">
                                by {app.manifest.developer?.name || 'Unknown Developer'}
                            </p>
                            <Badge variant="default" className="text-xs">
                                Running
                            </Badge>
                        </div>
                    </div>
                </div>

                {/* App features/tags */}
                {app.manifest.features && app.manifest.features.length > 0 && (
                    <div className="space-y-4">
                        <div>
                            <h3 className="text-sm font-semibold text-slate-900 mb-2">Features</h3>
                            <div className="flex flex-wrap gap-2">
                                {app.manifest.features.slice(0, 3).map((feature: string) => (
                                    <Badge key={feature} variant="secondary" className="text-xs">
                                        {feature}
                                    </Badge>
                                ))}
                                {app.manifest.features.length > 3 && (
                                    <Badge variant="outline" className="text-xs">
                                        +{app.manifest.features.length - 3} more
                                    </Badge>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {/* App Content Container */}
                <div className="space-y-4">
                    <div>
                        <h3 className="text-sm font-semibold text-slate-900 mb-2">Application</h3>
                        <div className="border border-slate-200 rounded-lg overflow-hidden bg-white">
                            <AppContainer
                                appId={app.id}
                                viewport="dashboard"
                                context={{
                                    workspace: { id: "current", name: "Current Workspace" },
                                    user: { id: "current", name: "Current User", email: "user@example.com" },
                                }}
                                className="w-full h-[500px]"
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* Floating Action Buttons */}
            <div className="sticky bottom-0 z-10 bg-white border-t px-4 py-4">
                <div className="flex items-center justify-between">
                    <div>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={handleConfigure}
                            className="text-slate-600 border-slate-200 hover:bg-slate-50"
                        >
                            <Settings className="h-4 w-4 mr-1" />
                            Configure
                        </Button>
                    </div>
                    <div className="flex items-center gap-3">
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={onClose}
                        >
                            <X className="h-4 w-4 mr-1" />
                            Close
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}
