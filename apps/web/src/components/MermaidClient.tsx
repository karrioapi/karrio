"use client"

import React, { useEffect, useRef, useState } from 'react'
import { useTheme } from 'next-themes'
import mermaid from 'mermaid'

interface MermaidProps {
  chart: string;
  className?: string;
}

// Initialize mermaid config
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  fontFamily: 'inherit',
})

// Custom Mermaid component
const MermaidClient = ({ chart, className = '' }: MermaidProps) => {
  const ref = useRef<HTMLDivElement>(null);
  const [svgCode, setSvgCode] = useState<string>('');
  const { resolvedTheme } = useTheme();
  const isDarkMode = resolvedTheme === 'dark';

  useEffect(() => {
    const renderDiagram = async () => {
      if (ref.current) {
        try {
          // Update theme based on current mode
          mermaid.initialize({
            startOnLoad: false,
            theme: isDarkMode ? 'dark' : 'default',
            securityLevel: 'loose',
            fontFamily: 'inherit',
          });

          // Generate and set SVG
          const { svg } = await mermaid.render('mermaid-diagram', chart);
          setSvgCode(svg);
        } catch (error) {
          console.error('Failed to render mermaid diagram:', error);
          setSvgCode(`<div class="text-red-500 p-4">Diagram rendering failed</div>`);
        }
      }
    };

    renderDiagram();
  }, [chart, isDarkMode]);

  return (
    <div
      ref={ref}
      className={`mermaid-container overflow-auto my-6 ${className}`}
      dangerouslySetInnerHTML={{ __html: svgCode }}
    />
  );
};

export default MermaidClient;
