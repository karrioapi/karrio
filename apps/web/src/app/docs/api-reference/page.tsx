'use client';

import { useTheme } from 'next-themes';
import { useEffect, useState } from 'react';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'elements-api': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
        apiDescriptionUrl: string;
        router?: string;
        layout?: string;
        basePath?: string;
        theme?: string;
        hideSchemas?: string;
        hideTryIt?: string;
      }, HTMLElement>;
    }
  }
}

export default function ApiReferencePage() {
  const { resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const getStoredTheme = (): 'light' | 'dark' => {
    if (typeof window === 'undefined') return 'light';
    try {
      const stored = window.localStorage.getItem('theme-content');
      if (stored === 'dark' || stored === 'light') return stored;
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) return 'dark';
    } catch { }
    return 'light';
  };
  // Revert to light-mode-only code styling (rely on component defaults for dark)
  useEffect(() => {
    if (!mounted) return;
  }, [mounted]);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="w-full h-full bg-background dark:bg-neutral-950">
      <elements-api
        key={(mounted ? (resolvedTheme as 'light' | 'dark' | undefined) : undefined) ?? getStoredTheme()}
        apiDescriptionUrl="/openapi.yml"
        router="hash"
        layout="responsive"
        theme={((mounted ? resolvedTheme : undefined) ?? getStoredTheme()) === 'dark' ? 'dark' : 'light'}
        className="w-full h-[calc(100vh-56px)] custom-docs-theme"
        data-theme={(mounted ? (resolvedTheme as 'light' | 'dark' | undefined) : undefined) ?? getStoredTheme()}
        style={{
          background: 'transparent',
          // Attempt to override internal surface variables used by some web components
          ['--color-canvas' as any]: 'transparent',
          ['--color-bg' as any]: 'transparent',
          ['--sl-color-bg' as any]: 'transparent',
          ['--sl-color-surface' as any]: 'transparent'
        } as React.CSSProperties}
        hideSchemas="true"
        hideTryIt="true"
      />
    </div>
  );
}
