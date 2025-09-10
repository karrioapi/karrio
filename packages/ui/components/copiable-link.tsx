"use client";

import * as React from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Copy, Check } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";

interface CopiableLinkProps {
  text: string;
  title?: string;
  className?: string;
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
  size?: "default" | "sm" | "lg" | "icon";
}

export const CopiableLink: React.FC<CopiableLinkProps> = ({
  text,
  title = "Copy to clipboard",
  className,
  variant = "ghost",
  size = "sm",
}) => {
  const [copied, setCopied] = React.useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      // Fallback for older browsers
      const input = document.createElement("input");
      input.setAttribute("value", text);
      document.body.appendChild(input);
      input.select();
      document.execCommand("copy");
      document.body.removeChild(input);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <Button
      variant={variant}
      size={size}
      onClick={copyToClipboard}
      className={cn("h-8 px-3 gap-2", className)}
      title={title}
    >
      <span className="text-[10px] font-mono">{text}</span>
      {copied ? (
        <Check className="h-3 w-3 text-green-600" />
      ) : (
        <Copy className="h-3 w-3" />
      )}
    </Button>
  );
};