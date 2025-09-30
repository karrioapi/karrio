"use client";

import React, { useState } from "react";
import { Button } from "@karrio/ui/components/ui/button";
import {
    CopyIcon,
    AlertCircle,
    AlertTriangle,
    ExternalLink,
    Loader2,
    Key,
    Eye,
    EyeOff,
} from "lucide-react";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { toast } from "@karrio/ui/hooks/use-toast";
import { trpc } from "@karrio/console/trpc/client";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@karrio/ui/components/ui/dialog";

interface ConnectModalProps {
    projectId: string;
    tenantEmail: string | null;
    dashboardUrl?: string;
}

// Helper function to ensure URL has proper protocol
const formatDashboardUrl = (url?: string): string | undefined => {
    if (!url) return undefined;

    // If URL already has protocol, return as is
    if (url.startsWith('http://') || url.startsWith('https://')) {
        return url;
    }

    // Default to https for dashboard URLs
    return `https://${url}`;
};

export function ConnectModal({
    projectId,
    tenantEmail,
    dashboardUrl
}: ConnectModalProps) {
    const [open, setOpen] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [credentials, setCredentials] = useState<{
        password: string;
        isFirstTime: boolean;
    } | null>(null);

    const formattedDashboardUrl = formatDashboardUrl(dashboardUrl);

    const resetPassword = trpc.projects.tenant.resetAdminPassword.useMutation({
        onSuccess: (data) => {
            setCredentials({
                password: data.password!,
                isFirstTime: data.isFirstTime,
            });
        },
        onError: (error) => {
            toast({
                title: "Failed to get credentials",
                description: error.message,
                variant: "destructive",
            });
        },
    });

    const handleConnect = () => {
        resetPassword.mutate({ projectId });
    };

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
        toast({
            title: "Copied to clipboard",
            description: "The credentials have been copied to your clipboard",
            variant: "default",
        });
    };

    const handleOpenChange = (newOpen: boolean) => {
        setOpen(newOpen);
        if (!newOpen) {
            // Clear credentials when modal closes
            setCredentials(null);
            setShowPassword(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={handleOpenChange}>
            <DialogTrigger asChild>
                <Button variant="outline" size="sm">
                    <Key className="h-4 w-4 mr-2" />
                    Connect
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>Admin Dashboard Credentials</DialogTitle>
                    <DialogDescription>
                        {credentials?.isFirstTime
                            ? "Here are your admin credentials to sign into the dashboard."
                            : "A new password has been generated for your admin account."
                        }
                    </DialogDescription>
                </DialogHeader>

                <div className="space-y-6">
                    {!credentials ? (
                        <div className="space-y-4">
                            <Alert>
                                <AlertCircle className="h-4 w-4" />
                                <AlertDescription>
                                    {resetPassword.status === "loading"
                                        ? "Generating admin credentials..."
                                        : "Click the button below to get your dashboard access credentials."
                                    }
                                </AlertDescription>
                            </Alert>

                            <Button
                                onClick={handleConnect}
                                disabled={resetPassword.status === "loading"}
                                className="w-full"
                            >
                                {resetPassword.status === "loading" ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Generating Credentials...
                                    </>
                                ) : (
                                    <>
                                        <Key className="mr-2 h-4 w-4" />
                                        Get Dashboard Credentials
                                    </>
                                )}
                            </Button>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {!credentials.isFirstTime && (
                                <Alert variant="destructive">
                                    <AlertTriangle className="h-4 w-4" />
                                    <AlertDescription>
                                        Your previous password has been reset. Use the new credentials below.
                                    </AlertDescription>
                                </Alert>
                            )}

                            <div className="space-y-4 p-4 bg-muted rounded-lg">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Email:</label>
                                    <div className="flex items-center gap-2">
                                        <code className="flex-1 rounded-md bg-background px-3 py-2 font-mono text-sm">
                                            {tenantEmail}
                                        </code>
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => copyToClipboard(tenantEmail || "")}
                                        >
                                            <CopyIcon className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Password:</label>
                                    <div className="flex items-center gap-2">
                                        <code className="flex-1 rounded-md bg-background px-3 py-2 font-mono text-sm">
                                            {showPassword ? credentials.password : "••••••••••••••••"}
                                        </code>
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => setShowPassword(!showPassword)}
                                        >
                                            {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                        </Button>
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => copyToClipboard(credentials.password)}
                                        >
                                            <CopyIcon className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                            </div>

                            {formattedDashboardUrl && (
                                <Button
                                    onClick={() => window.open(formattedDashboardUrl, "_blank")}
                                    className="w-full"
                                    variant="default"
                                >
                                    <ExternalLink className="mr-2 h-4 w-4" />
                                    Open Dashboard to Sign In
                                </Button>
                            )}

                            <Alert>
                                <AlertCircle className="h-4 w-4" />
                                <AlertDescription>
                                    Save these credentials securely. The password won't be shown again unless you reset it.
                                </AlertDescription>
                            </Alert>
                        </div>
                    )}
                </div>
            </DialogContent>
        </Dialog>
    );
}
