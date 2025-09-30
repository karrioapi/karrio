import * as React from 'react';
import { cn } from '../../lib/utils';

interface ShippingCardProps extends React.HTMLAttributes<HTMLDivElement> {
  title: string;
  description?: string;
  footer?: React.ReactNode;
  children: React.ReactNode;
}

export function ShippingCard({
  title,
  description,
  footer,
  children,
  className,
  ...props
}: ShippingCardProps) {
  return (
    <div
      className={cn(
        "rounded-lg border bg-card text-card-foreground shadow-sm",
        className
      )}
      {...props}
    >
      <div className="flex flex-col space-y-1.5 p-6">
        <h3 className="text-lg font-semibold leading-none tracking-tight">{title}</h3>
        {description && <p className="text-sm text-gray-500">{description}</p>}
      </div>
      <div className="p-6 pt-0">{children}</div>
      {footer && (
        <div className="flex items-center p-6 pt-0">
          {footer}
        </div>
      )}
    </div>
  );
}
