import { ReactNode } from "react";

interface CardGridProps {
  children: ReactNode;
  columns?: number;
}

export function CardGrid({ children, columns = 3 }: CardGridProps) {
  return <div className={`grid gap-6 md:grid-cols-${columns}`}>{children}</div>;
}
