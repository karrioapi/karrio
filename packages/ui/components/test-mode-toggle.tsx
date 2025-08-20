"use client";

import { Switch } from "@karrio/ui/components/ui/switch";
import { useAppMode } from "@karrio/hooks/app-mode";

export function TestModeToggle() {
  const { testMode, switchMode } = useAppMode();

  return (
    <div className="flex items-center gap-2 rounded-lg px-3 py-1.5 border border-gray-200 hover:bg-gray-50 rounded-full !rounded-full border-radius-50">
      <span className={`hidden sm:block text-sm font-medium ${testMode ? 'text-[#C15517]' : 'text-gray-700'}`}>
        Test mode
      </span>
      <Switch
        checked={testMode}
        onCheckedChange={switchMode}
        className={`${testMode ? 'bg-[#C15517]' : 'bg-gray-200'} data-[state=checked]:bg-[#C15517] data-[state=unchecked]:bg-gray-200`}
        title={testMode ? "Disable test mode" : "Enable test mode"}
      />
    </div>
  );
}
