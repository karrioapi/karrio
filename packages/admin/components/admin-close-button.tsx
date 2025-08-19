"use client";

import { useAppMode } from "@karrio/hooks/app-mode";

export function AdminCloseButton() {
  const { basePath } = useAppMode();

  return (
    <div className="fixed top-16 right-4 md:right-8 z-10">
      <a
        href={basePath}
        className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-white shadow-sm border hover:bg-gray-50 text-gray-600 hover:text-gray-800"
      >
        <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span className="sr-only">Close admin console</span>
      </a>
    </div>
  );
}
