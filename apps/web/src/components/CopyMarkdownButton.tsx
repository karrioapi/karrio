"use client";

import { usePathname } from "next/navigation";
import { useCallback, useState } from "react";
import { Button } from "@karrio/ui/components/ui/button";

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

    return (
        <Button
            variant="ghost"
            size="sm"
            className="copy-llm-btn border border-blue-300/60 text-blue-600 dark:text-blue-200 dark:border-blue-800 transition-colors"
            onClick={handleCopy}
            disabled={busy}
            aria-label="Copy Markdown for LLM"
        >
            {copied ? "Copied" : busy ? "Preparing..." : "Copy for LLM"}
        </Button>
    );
}


