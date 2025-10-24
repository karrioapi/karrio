"use client";

import * as React from "react";
import { Badge } from "@karrio/ui/components/ui/badge";
import { cn } from "@karrio/ui/lib/utils";

interface StatusCodeBadgeProps {
  code: string | number;
  className?: string;
}

export const StatusCodeBadge: React.FC<StatusCodeBadgeProps> = ({
  code,
  className,
}) => {
  const codeStr = String(code);
  const firstChar = codeStr[0];
  
  const getVariantClass = () => {
    switch (firstChar) {
      case '2':
        return "bg-green-100 text-green-800 border-green-200";
      case '4':
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case '5':
        return "bg-red-100 text-red-800 border-red-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };
  
  return (
    <Badge 
      variant="secondary"
      className={cn(
        "text-xs px-2 py-1 font-mono",
        getVariantClass(),
        className
      )}
    >
      {code}
    </Badge>
  );
};