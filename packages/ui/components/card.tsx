import React from "react";
import { Card as ShadCNCard, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { cn } from "@karrio/ui/lib/utils";

interface CardComponent extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

interface CardHeaderComponent extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

interface CardBodyComponent extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

interface CardFooterComponent extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

// Main Card component that mimics Bulma card structure
export const Card = ({ className, children, ...props }: CardComponent) => {
  return (
    <ShadCNCard 
      className={cn("shadow-sm border border-gray-200", className)} 
      {...props}
    >
      {children}
    </ShadCNCard>
  );
};

// Card Header component (equivalent to Bulma card-header)
export const CardHeaderSection = ({ className, children, ...props }: CardHeaderComponent) => {
  return (
    <CardHeader className={cn("px-3 py-2", className)} {...props}>
      {children}
    </CardHeader>
  );
};

// Card Body component (equivalent to Bulma card-content)
export const CardBody = ({ className, children, ...props }: CardBodyComponent) => {
  return (
    <CardContent className={cn("p-3", className)} {...props}>
      {children}
    </CardContent>
  );
};

// Card Footer component (equivalent to Bulma card-footer)
export const CardFooter = ({ className, children, ...props }: CardFooterComponent) => {
  return (
    <div className={cn("px-3 py-1 border-t border-gray-200", className)} {...props}>
      {children}
    </div>
  );
};

// Section title component for card headers
export const CardSectionTitle = ({ className, children, ...props }: { className?: string; children: React.ReactNode }) => {
  return (
    <span 
      className={cn("text-xs font-bold uppercase tracking-wide text-gray-700", className)} 
      {...props}
    >
      {children}
    </span>
  );
};
