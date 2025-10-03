"use client";

import { Button } from "@karrio/ui/components/ui/button";
import { useEffect } from "react";
import { getCalApi } from "@calcom/embed-react";
import { ReactNode } from "react";

interface BookDemoButtonProps {
  size?: "default" | "sm" | "lg" | "icon";
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
  className?: string;
  children?: ReactNode;
  calLink?: string;
}

export function BookDemoButton({
  size = "lg",
  variant = "default",
  className = "",
  children = "Book a demo",
  calLink = "karrio/demo"
}: BookDemoButtonProps) {
  useEffect(() => {
    (async function () {
      const cal = await getCalApi({ "namespace": "demo" });
      cal("ui", { "theme": "dark", "hideEventTypeDetails": false, "layout": "month_view" });
    })();
  }, []);

  return (
    <Button
      size={size}
      variant={variant}
      className={className}
      data-cal-namespace="demo"
      data-cal-link={calLink}
      data-cal-config='{"layout":"month_view","theme":"dark"}'
    >
      {children}
    </Button>
  );
}
