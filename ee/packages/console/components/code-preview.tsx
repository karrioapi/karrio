"use client";

import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from "@karrio/insiders/components/ui/tabs";
import { cn } from "@karrio/insiders/lib/utils";

interface CodePreviewProps {
  languages: {
    label: string;
    value: string;
    code: string;
    response?: string;
  }[];
}

export function CodePreview({ languages }: CodePreviewProps) {
  return (
    <Tabs defaultValue={languages[0].value} className="w-full">
      <div className="p-4 pb-0">
        <TabsList className="bg-[#2C2252] h-8 w-auto inline-flex rounded-md p-1">
          {languages.map((lang) => (
            <TabsTrigger
              key={lang.value}
              value={lang.value}
              className="rounded px-3 py-1 text-xs data-[state=active]:bg-[#5722cc] data-[state=active]:text-white"
            >
              {lang.label}
            </TabsTrigger>
          ))}
        </TabsList>
      </div>
      {languages.map((lang) => (
        <TabsContent
          key={lang.value}
          value={lang.value}
          className="space-y-0 mt-0"
        >
          <div className="p-2 pt-6">
            <div className="rounded bg-[#080718]">
              <pre className="text-sm text-white/90 scrollbar-none p-4 overflow-x-auto touch-auto">
                <code className="language-javascript">{lang.code}</code>
              </pre>
            </div>
          </div>

          {lang.response && (
            <div className="p-2 pt-2">
              <div className="bg-[#080718] px-4 py-2 text-xs text-white/60 flex items-center justify-between rounded-t">
                <div>Response</div>
                <div className="text-[#79e5dd] bg-[#79e5dd]/20 px-2 py-0.5 rounded text-xs">HTTP 200</div>
              </div>
              <div className="bg-[#080718] overflow-auto touch-auto">
                <pre className="text-sm text-[#79e5dd] px-4 py-3 scrollbar-none overflow-x-auto">
                  <code className="block">{lang.response}</code>
                </pre>
              </div>
            </div>
          )}
        </TabsContent>
      ))}
    </Tabs>
  );
}
