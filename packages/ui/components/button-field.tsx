import React from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { cn } from "@karrio/ui/lib/utils";
import { Loader2 } from "lucide-react";

export interface ButtonFieldComponent
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
  size?: "default" | "sm" | "lg" | "icon";
  
  // Loading state
  loading?: boolean;
  loadingText?: string;
  
  // Only the legacy props that are actually used
  isSuccess?: boolean;
  isSmall?: boolean;
  
  // Icon support
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const ButtonField = React.forwardRef<HTMLButtonElement, ButtonFieldComponent>(
  ({
    variant,
    size,
    className,
    loading = false,
    loadingText = "Loading...",
    children,
    disabled,
    // Legacy props (only used ones)
    isSuccess,
    isSmall,
    leftIcon,
    rightIcon,
    ...props
  }, ref) => {
    
    // Simple mapping for legacy props to maintain exact behavior
    const finalVariant = variant || (isSuccess ? "default" : "default");
    const finalSize = size || (isSmall ? "sm" : "default");
    const isDisabled = disabled || loading;

    return (
      <Button
        ref={ref}
        variant={finalVariant}
        size={finalSize}
        className={className}
        disabled={isDisabled}
        {...props}
      >
        {loading && <Loader2 className="animate-spin -ml-1 mr-2 h-4 w-4" />}
        {leftIcon && !loading && <span className="mr-2">{leftIcon}</span>}
        {loading ? loadingText : children}
        {rightIcon && !loading && <span className="ml-2">{rightIcon}</span>}
      </Button>
    );
  }
);

ButtonField.displayName = "ButtonField";