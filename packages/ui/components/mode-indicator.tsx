"use client";

import { useAppMode } from "@karrio/hooks/app-mode";

export function ModeIndicator() {
  const { testMode } = useAppMode();

  if (!testMode) {
    return null;
  }

  return (
    <div className="fixed top-0 left-0 right-0 z-[100] bg-[#C15517] text-white px-4 py-1 text-sm font-medium shadow-lg">
      {/* <div className="flex items-center justify-center gap-1">
        <span className="font-bold">TEST MODE</span>
      </div> */}
    </div>
  );
}
