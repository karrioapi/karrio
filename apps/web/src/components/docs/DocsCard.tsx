"use client";

import React from 'react';
import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

interface DocsCardProps {
  href: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  external?: boolean;
}

export function DocsCard({
  href,
  title,
  description,
  icon,
  external = false
}: DocsCardProps) {
  const Card = () => (
    <div className="relative flex flex-col items-start rounded-lg border border-gray-200 p-6 transition-all duration-200 dark:border-white/10 hover:border-gray-300 dark:hover:border-white/20 hover:shadow-sm group">
      <div className="flex items-center">
        <div className="flex h-10 w-10 items-center justify-center rounded-md bg-gray-100 dark:bg-gray-800">
          {icon}
        </div>
        <h3 className="ml-3 text-lg font-medium">{title}</h3>
      </div>
      <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">
        {description}
      </p>
      <div className="absolute right-4 top-4 opacity-0 transition-opacity group-hover:opacity-100">
        <ArrowUpRight className="h-5 w-5 text-gray-400 dark:text-gray-600" />
      </div>
    </div>
  );

  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer">
        <Card />
      </a>
    );
  }

  return (
    <Link href={href}>
      <Card />
    </Link>
  );
}
