"use client";

import * as React from "react";
import { cn } from "@karrio/ui/lib/utils";

interface StickyTableWrapperProps {
  children: React.ReactNode;
  className?: string;
}

export const StickyTableWrapper: React.FC<StickyTableWrapperProps> = ({
  children,
  className,
}) => {
  const wrapperRef = React.useRef<HTMLDivElement>(null);
  const [isScrolled, setIsScrolled] = React.useState(false);

  React.useEffect(() => {
    const wrapper = wrapperRef.current;
    if (!wrapper) return;

    const handleScroll = () => {
      setIsScrolled(wrapper.scrollLeft > 0);
    };

    wrapper.addEventListener('scroll', handleScroll);
    return () => wrapper.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div 
      ref={wrapperRef}
      className={cn(
        "overflow-auto relative m-0 p-0",
        "sticky-table-wrapper",
        className
      )}
      data-scrolled={isScrolled}
    >
      <style jsx>{`
        .sticky-table-wrapper :global(.sticky-left) {
          position: sticky;
          left: -1px;
          z-index: 5;
          background: white;
          margin-left: -1px;
        }
        
        .sticky-table-wrapper :global(.sticky-right) {
          position: sticky;
          right: -1px;
          z-index: 5;
          background: white;
          margin-right: -1px;
        }
        
        /* Mobile only - show gray background when scrolling */
        @media (max-width: 768px) {
          .sticky-table-wrapper[data-scrolled="true"] :global(.sticky-left) {
            background: rgba(243, 244, 246, 0.95);
            box-shadow: 2px 0 6px rgba(0, 0, 0, 0.12);
          }
          
          .sticky-table-wrapper[data-scrolled="true"] :global(.sticky-right) {
            background: rgba(243, 244, 246, 0.95);
            box-shadow: -2px 0 6px rgba(0, 0, 0, 0.12);
          }
        }
        
        /* Ensure table cells have white background */
        .sticky-table-wrapper :global(.sticky-left td),
        .sticky-table-wrapper :global(.sticky-left th),
        .sticky-table-wrapper :global(.sticky-right td),
        .sticky-table-wrapper :global(.sticky-right th) {
          background: inherit;
        }
        
        /* Handle hover states */
        .sticky-table-wrapper :global(tr:hover .sticky-left td),
        .sticky-table-wrapper :global(tr:hover .sticky-left th),
        .sticky-table-wrapper :global(tr:hover .sticky-right td),
        .sticky-table-wrapper :global(tr:hover .sticky-right th) {
          background: inherit;
        }
      `}</style>
      {children}
    </div>
  );
};