"use client";

import { usePathname } from "next/navigation";
import { useCallback, useState } from "react";
import { Button } from "@karrio/ui/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
} from "@karrio/ui/components/ui/dropdown-menu";
import { ChevronDown } from "lucide-react";

export function CopyMarkdownButton() {
    const pathname = usePathname();
    const [busy, setBusy] = useState(false);
    const [copied, setCopied] = useState(false);

    const handleCopy = useCallback(async () => {
        if (!pathname || !pathname.startsWith("/docs/")) return;
        setBusy(true);
        try {
            const res = await fetch(`/api/docs-source?p=${encodeURIComponent(pathname)}`, { cache: "no-store" });
            if (!res.ok) return;
            const text = await res.text();
            await navigator.clipboard.writeText(text);
            setCopied(true);
            setTimeout(() => setCopied(false), 1400);
        } finally {
            setBusy(false);
        }
    }, [pathname]);

    function buildRawMdxUrl(currentPath: string | null, branch = "main") {
        const clean = (currentPath || "").split(/[?#]/)[0].replace(/\/$/, "");
        if (!clean.startsWith("/docs/")) return null;
        return `https://raw.githubusercontent.com/karrioapi/karrio/refs/heads/${branch}/apps/web/src/app${clean}/page.mdx`;
    }

    function buildPrefillText(currentPath: string | null) {
        const url = buildRawMdxUrl(currentPath);
        if (!url) return null;
        return `Read from ${url} so I can ask questions about it.`;
    }

    async function openClaudeWithPrefill() {
        const prefill = buildPrefillText(pathname);
        let target = "https://claude.ai/new";
        if (prefill) {
            // Append as q= param to attempt prefill (no clipboard copy here)
            const q = encodeURIComponent(prefill);
            target = `https://claude.ai/new?q=${q}`;
        }
        try {
            window.open(target, "_blank", "noopener,noreferrer");
        } catch { }
    }

    return (
        <DropdownMenu>
            <div className="inline-flex items-stretch">
                {/* Primary action: click to copy */}
                <Button
                    variant="ghost"
                    size="sm"
                    className="copy-llm-btn border border-blue-300/60 text-blue-600 dark:text-blue-200 dark:border-blue-800 transition-colors rounded-r-none"
                    onClick={handleCopy}
                    disabled={busy}
                    aria-label="Copy Markdown for LLM"
                >
                    {copied ? "Copied" : busy ? "Preparing..." : "Copy for LLM"}
                </Button>

                {/* Secondary: opens dropdown */}
                <DropdownMenuTrigger asChild>
                    <Button
                        variant="ghost"
                        size="sm"
                        className="copy-llm-btn border border-l-0 border-blue-300/60 text-blue-600 dark:text-blue-200 dark:border-blue-800 rounded-l-none transition-colors"
                        aria-label="More copy options"
                    >
                        <ChevronDown className="h-4 w-4" />
                    </Button>
                </DropdownMenuTrigger>
            </div>

            <DropdownMenuContent align="end">
                <DropdownMenuItem
                    onClick={handleCopy}
                    className="data-[highlighted]:bg-blue-50 dark:data-[highlighted]:bg-blue-900/40 data-[highlighted]:text-blue-900 dark:data-[highlighted]:text-blue-100"
                >
                    Copy for LLM
                </DropdownMenuItem>
                <DropdownMenuItem
                    onClick={() => {
                        const url = buildRawMdxUrl(pathname);
                        if (url) window.open(url, "_blank", "noopener,noreferrer");
                    }}
                    className="data-[highlighted]:bg-blue-50 dark:data-[highlighted]:bg-blue-900/40 data-[highlighted]:text-blue-900 dark:data-[highlighted]:text-blue-100"
                >
                    Open Markdown View
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                    onClick={openClaudeWithPrefill}
                    className="data-[highlighted]:bg-blue-50 dark:data-[highlighted]:bg-blue-900/40 data-[highlighted]:text-blue-900 dark:data-[highlighted]:text-blue-100"
                >
                    Open in Claude
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}


