"use client";

import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Building } from "lucide-react";

interface OrganizationFormProps {
    initialName?: string;
    onSave: (name: string) => Promise<void>;
    isLoading?: boolean;
}

export function OrganizationForm({ initialName = "", onSave, isLoading }: OrganizationFormProps) {
    const [name, setName] = useState(initialName);
    const [hasChanges, setHasChanges] = useState(false);
    const [isSaving, setIsSaving] = useState(false);

    useEffect(() => {
        setHasChanges(name !== initialName);
    }, [name, initialName]);

    const handleSave = async () => {
        if (!hasChanges || isSaving) return;

        setIsSaving(true);
        try {
            await onSave(name);
        } finally {
            setIsSaving(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && hasChanges && !isSaving) {
            handleSave();
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Building className="h-5 w-5" />
                    Organization Settings
                </CardTitle>
                <CardDescription>
                    Manage your organization's basic information and settings.
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="space-y-2">
                    <Label htmlFor="organization-name">Organization Name</Label>
                    <div className="flex space-x-3">
                        <Input
                            id="organization-name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Enter organization name"
                            className="flex-1"
                            disabled={isLoading || isSaving}
                        />
                        <Button
                            onClick={handleSave}
                            disabled={!hasChanges || isLoading || isSaving}
                            size="sm"
                        >
                            {isSaving ? "Saving..." : "Save"}
                        </Button>
                    </div>
                    <p className="text-sm text-muted-foreground">
                        This name will be visible to all team members and in your organization settings.
                    </p>
                </div>
            </CardContent>
        </Card>
    );
}
