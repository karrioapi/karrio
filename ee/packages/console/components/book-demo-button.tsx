"use client";

import { Button } from "@karrio/insiders/components/ui/button";
import { useEffect } from "react";
import { getCalApi } from "@calcom/embed-react";

interface BookDemoButtonProps {
  size?: "default" | "sm" | "lg" | "icon";
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
  className?: string;
}

export function BookDemoButton({
  size = "lg",
  variant = "default",
  className = "bg-[#5722cc] hover:bg-[#5722cc]/90",
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
      data-cal-link="karrio/demo"
      data-cal-config='{"layout":"month_view","theme":"dark"}'
    >
      Book a demo
    </Button>
  );
}
