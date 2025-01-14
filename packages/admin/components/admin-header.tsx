"use client";

import { Switch } from "@karrio/insiders/components/ui/switch";
import { Input } from "@karrio/insiders/components/ui/input";
import { useAppMode } from "@karrio/hooks/app-mode";
import { DASHBOARD_VERSION, p } from "@karrio/lib";
import { Search } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export function AdminHeader() {
  const { testMode, switchMode } = useAppMode();

  return (
    <header className="fixed left-0 right-0 top-0 z-50 flex h-14 items-center justify-between gap-4 bg-white px-4 border-b border-gray-200">
      <div className="flex items-center gap-4">
        <Link href="/" className="flex items-center gap-2">
          <Image
            src={p`/icon.svg`}
            width={25}
            height={25}
            className="m-1"
            alt="logo"
          />
        </Link>
        <span className="rounded bg-gray-100 px-2 py-1 text-xs text-gray-600">
          {DASHBOARD_VERSION}
        </span>
      </div>

      <div className="flex-1 px-20">
        <div className="relative max-w-[460px]">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            type="search"
            placeholder="Search"
            className="h-9 w-full bg-gray-50 pl-9 text-gray-900 placeholder:text-gray-500 border-gray-200 ring-offset-0 focus-visible:ring-1 focus-visible:ring-gray-300"
          />
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div className="flex items-center gap-2 rounded-lg px-3 py-1.5 hover:bg-gray-50">
          <span className={`text-sm ${testMode ? 'text-[#C15517]' : 'text-gray-700'}`}>Test mode</span>
          <Switch
            checked={testMode}
            onCheckedChange={switchMode}
            className={`${testMode ? 'bg-[#C15517]' : 'bg-gray-200'} data-[state=checked]:bg-[#C15517] data-[state=unchecked]:bg-gray-200`}
            title={testMode ? "Disable test mode" : "Enable test mode"}
          />
        </div>
      </div>
    </header>
  );
}
