"use client";

import React from 'react';
import Image from 'next/image';
import { DocsLayout } from './DocsLayout';
import { DocsCard } from './DocsCard';
import { DocsMDX } from './DocsMDX';
import MermaidClient from '../MermaidClient';
import { Rocket, Server, Code } from 'lucide-react';

interface DocsHomePageProps {
  children?: React.ReactNode;
}

export function DocsHomePage({ children }: DocsHomePageProps) {
  return (
    <DocsLayout>
      <div className="space-y-10">
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold">Getting Started</h1>
          <h2 className="text-4xl font-bold tracking-tight">Introduction</h2>
        </div>

        {/* Hero Image */}
        <div className="relative w-full aspect-[3/1] overflow-hidden rounded-lg border border-gray-200 dark:border-white/10 bg-gray-100 dark:bg-gray-900">
          <Image
            src="/docs-hero.svg"
            alt="Karrio Docs"
            fill
            className="object-contain"
            priority
          />
        </div>

        {/* Content Block */}
        <div className="prose prose-gray max-w-none dark:prose-invert">
          <p className="lead">
            Welcome to the Karrio Documentation! Karrio is an open-source multi-carrier shipping API
            that helps you integrate with multiple shipping carriers like USPS, DHL, UPS, Canada Post, and more.
          </p>

          <h2>Quick Start</h2>

          <p>
            To quickly get started with Karrio, you can follow the guides below:
          </p>
        </div>

        {/* Card Grid */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <DocsCard
            href="/docs/introduction"
            title="Start developing"
            description="Follow our quickstart guide to start developing with Karrio"
            icon={<Rocket className="h-5 w-5" />}
          />

          <DocsCard
            href="/docs/self-hosting"
            title="Self Host"
            description="Learn how to self-host Karrio for controlled instance"
            icon={<Server className="h-5 w-5" />}
          />

          <DocsCard
            href="/docs/api-v2-reference"
            title="API"
            description="Learn how to use Karrio's API to CRUD various Karrio resources programmatically"
            icon={<Code className="h-5 w-5" />}
          />
        </div>

        {/* Mermaid Example */}
        <div className="prose prose-gray max-w-none dark:prose-invert">
          <h2>MermaidJS Example</h2>

          <p>
            Karrio documentation supports Mermaid diagrams for better visualization of processes and workflows:
          </p>

          <div className="my-8 rounded-lg bg-gray-50 dark:bg-gray-900 p-4 border border-gray-200 dark:border-gray-800">
            <MermaidClient
              chart={`
                  graph TD
                    A[Start] --> B{Is it working?}
                    B -->|Yes| C[Great!]
                    B -->|No| D[Debug]
                    D --> B
                `}
            />
          </div>
        </div>

        {/* Additional Content */}
        {children}
      </div>
    </DocsLayout>
  );
}
