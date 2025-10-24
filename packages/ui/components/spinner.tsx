import React from "react";
import { cn } from "@karrio/ui/lib/utils";

interface SpinnerProps {
  className?: string;
  size?: number;
}

export const Spinner = ({ className, size }: SpinnerProps): JSX.Element => {
  // Map Bulma size to Tailwind classes (matches original behavior)
  const getSizeClasses = (size?: number) => {
    switch (size) {
      case 1: return "h-8 w-8"; // Large (matches is-size-1)
      case 2: return "h-6 w-6"; // Medium
      case 3: return "h-4 w-4"; // Small
      default: return "h-8 w-8"; // Default to large like original
    }
  };

  return (
    <div
      className={cn(
        "my-6 p-6 flex justify-center", // Matches original: my-6 p-6 has-text-centered
        className
      )}
      style={{ background: "transparent" }}
    >
      <div
        className={cn(
          "animate-spin rounded-full border-2 border-primary border-t-transparent", // Tailwind spinner
          getSizeClasses(size)
        )}
        style={{ background: "transparent" }}
      />
    </div>
  );
};