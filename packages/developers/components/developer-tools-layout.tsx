"use client";

import React from "react";
import { DeveloperToolsProvider } from "../context/developer-tools-context";
import { DeveloperToolsDrawer } from "./developer-tools-drawer";

interface DeveloperToolsLayoutProps {
    children: React.ReactNode;
}

export function DeveloperToolsLayout({ children }: DeveloperToolsLayoutProps) {
    return (
        <DeveloperToolsProvider>
            {children}
            <DeveloperToolsDrawer />
        </DeveloperToolsProvider>
    );
}
