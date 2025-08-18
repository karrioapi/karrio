import React from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { cn } from "@karrio/ui/lib/utils";

export interface ButtonFieldComponent
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  // ShadCN Button variants
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
  size?: "default" | "sm" | "lg" | "icon";
  
  // Bulma compatibility props
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  
  // Loading state
  loading?: boolean;
  loadingText?: string;
  
  // Common button styles (Bulma compatibility)
  isSuccess?: boolean;
  isInfo?: boolean;
  isDanger?: boolean;
  isWarning?: boolean;
  isLight?: boolean;
  isDark?: boolean;
  isPrimary?: boolean;
  isSmall?: boolean;
  isLarge?: boolean;
  isFullwidth?: boolean;
  isInverted?: boolean;
  isOutlined?: boolean;
  
  // Icon support
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const ButtonField = React.forwardRef<HTMLButtonElement, ButtonFieldComponent>(
  ({
    variant,
    size,
    className,
    fieldClass,
    controlClass,
    wrapperClass,
    loading = false,
    loadingText = "Loading...",
    children,
    disabled,
    // Bulma compatibility props
    isSuccess,
    isInfo,
    isDanger,
    isWarning,
    isLight,
    isDark,
    isPrimary,
    isSmall,
    isLarge,
    isFullwidth,
    isInverted,
    isOutlined,
    leftIcon,
    rightIcon,
    ...props
  }, ref) => {
    
    // Map Bulma styles to ShadCN variants
    const getVariantFromBulmaProps = (): typeof variant => {
      if (isDanger) return "destructive";
      if (isOutlined) return "outline";
      if (isLight || isDark) return "secondary";
      if (isSuccess || isInfo || isPrimary) return "default";
      return variant || "default";
    };

    // Map Bulma sizes to ShadCN sizes
    const getSizeFromBulmaProps = (): typeof size => {
      if (isSmall) return "sm";
      if (isLarge) return "lg";
      return size || "default";
    };

    const finalVariant = getVariantFromBulmaProps();
    const finalSize = getSizeFromBulmaProps();

    // Build additional classes for Bulma compatibility
    const additionalClasses = cn(
      isFullwidth && "w-full",
      isInverted && "bg-transparent border-current text-current hover:bg-current hover:text-white",
      className
    );

    const isDisabled = disabled || loading;

    return (
      <div className={cn("inline-block", fieldClass, wrapperClass)}>
        <div className={cn("relative", controlClass)}>
          <Button
            ref={ref}
            variant={finalVariant}
            size={finalSize}
            className={additionalClasses}
            disabled={isDisabled}
            {...props}
          >
            {loading && (
              <svg
                className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
            )}
            {leftIcon && !loading && <span className="mr-2">{leftIcon}</span>}
            {loading ? loadingText : children}
            {rightIcon && !loading && <span className="ml-2">{rightIcon}</span>}
          </Button>
        </div>
      </div>
    );
  }
);

ButtonField.displayName = "ButtonField";