"use client";

import React from 'react';
import Image from 'next/image';
import { cn } from '@karrio/ui/lib/utils';
import MermaidClient from '../MermaidClient';

interface DocsMDXProps {
    children: React.ReactNode;
    className?: string;
}

interface MermaidProps {
    chart: string;
    className?: string;
}

// MDX components mapping
const components = {
    h1: ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
        <h1
            className={cn("mt-2 scroll-m-20 text-4xl font-bold tracking-tight", className)}
            {...props}
        />
    ),
    h2: ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
        <h2
            className={cn("mt-12 scroll-m-20 border-b border-gray-200 pb-2 text-2xl font-semibold tracking-tight first:mt-0 dark:border-white/10", className)}
            {...props}
        />
    ),
    h3: ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
        <h3
            className={cn("mt-8 scroll-m-20 text-xl font-semibold tracking-tight", className)}
            {...props}
        />
    ),
    h4: ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
        <h4
            className={cn("mt-6 scroll-m-20 text-lg font-semibold tracking-tight", className)}
            {...props}
        />
    ),
    p: ({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
        <p
            className={cn("leading-7 [&:not(:first-child)]:mt-6", className)}
            {...props}
        />
    ),
    ul: ({ className, ...props }: React.HTMLAttributes<HTMLUListElement>) => (
        <ul className={cn("my-6 ml-6 list-disc", className)} {...props} />
    ),
    ol: ({ className, ...props }: React.HTMLAttributes<HTMLOListElement>) => (
        <ol className={cn("my-6 ml-6 list-decimal", className)} {...props} />
    ),
    li: ({ className, ...props }: React.HTMLAttributes<HTMLLIElement>) => (
        <li className={cn("mt-2", className)} {...props} />
    ),
    blockquote: ({ className, ...props }: React.HTMLAttributes<HTMLQuoteElement>) => (
        <blockquote
            className={cn("mt-6 border-l-2 border-gray-300 pl-6 italic text-gray-800 dark:border-gray-600 dark:text-gray-200", className)}
            {...props}
        />
    ),
    img: ({
        className,
        alt,
        src,
        ...props
    }: React.ImgHTMLAttributes<HTMLImageElement>) => {
        // Make sure src is provided and is a string
        if (!src || typeof src !== 'string') {
            return null;
        }

        return (
            <Image
                className={cn("rounded-md border border-gray-200 dark:border-gray-800", className)}
                alt={alt || ""}
                src={src}
                width={800}
                height={400}
                {...Object.fromEntries(
                    Object.entries(props).filter(
                        ([key]) => !['width', 'height', 'loading', 'priority', 'quality', 'unoptimized'].includes(key)
                    )
                )}
            />
        );
    },
    hr: ({ ...props }) => (
        <hr className="my-8 border-gray-200 dark:border-gray-800" {...props} />
    ),
    table: ({ className, ...props }: React.HTMLAttributes<HTMLTableElement>) => (
        <div className="my-6 w-full overflow-y-auto">
            <table className={cn("w-full", className)} {...props} />
        </div>
    ),
    tr: ({ className, ...props }: React.HTMLAttributes<HTMLTableRowElement>) => (
        <tr
            className={cn("m-0 border-t border-gray-200 p-0 even:bg-gray-50 dark:border-gray-800 dark:even:bg-gray-900", className)}
            {...props}
        />
    ),
    th: ({ className, ...props }: React.HTMLAttributes<HTMLTableCellElement>) => (
        <th
            className={cn("border border-gray-200 px-4 py-2 text-left font-semibold dark:border-gray-800", className)}
            {...props}
        />
    ),
    td: ({ className, ...props }: React.HTMLAttributes<HTMLTableCellElement>) => (
        <td
            className={cn("border border-gray-200 px-4 py-2 text-left dark:border-gray-800", className)}
            {...props}
        />
    ),
    pre: ({ className, ...props }: React.HTMLAttributes<HTMLPreElement>) => (
        <pre
            className={cn("mb-4 mt-6 overflow-x-auto rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-800 dark:bg-gray-900", className)}
            {...props}
        />
    ),
    code: ({ className, ...props }: React.HTMLAttributes<HTMLElement>) => (
        <code
            className={cn("relative rounded bg-gray-100 px-[0.3rem] py-[0.2rem] font-mono text-sm dark:bg-gray-800", className)}
            {...props}
        />
    ),
    // Custom components
    Mermaid: ({ chart, className }: MermaidProps) => (
        <MermaidClient chart={chart} className={className} />
    ),
};

export function DocsMDX({ children, className }: DocsMDXProps) {
    return (
        <div className={cn("mdx-content prose prose-gray max-w-none dark:prose-invert", className)}>
            {React.Children.map(children, (child) => {
                if (!React.isValidElement(child)) return child;

                const childType = child.type as keyof typeof components | string;

                // Check if the component exists in our mapping
                if (typeof childType === 'string' && childType in components) {
                    const Component = components[childType as keyof typeof components];
                    return <Component {...(child.props as any)} />;
                }

                // If not in our mapping, return the original child
                return child;
            })}
        </div>
    );
}
