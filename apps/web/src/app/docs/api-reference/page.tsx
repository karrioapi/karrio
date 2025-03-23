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
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="w-full h-full bg-white dark:bg-neutral-950">
      <elements-api
        apiDescriptionUrl="/openapi.yml"
        router="hash"
        layout="responsive"
        theme={mounted ? (theme === 'dark' ? 'dark' : 'light') : 'light'}
        className="w-full h-[calc(100vh-56px)]"
        hideSchemas="true"
        hideTryIt="true"
      />
    </div>
  );
}
