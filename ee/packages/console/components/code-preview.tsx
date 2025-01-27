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
      <TabsList className="bg-white/5">
        {languages.map((lang) => (
          <TabsTrigger
            key={lang.value}
            value={lang.value}
            className="data-[state=active]:bg-[#5722cc] data-[state=active]:text-white"
          >
            {lang.label}
          </TabsTrigger>
        ))}
      </TabsList>
      {languages.map((lang) => (
        <TabsContent
          key={lang.value}
          value={lang.value}
          className="mt-4 space-y-4"
        >
          <div className="rounded-lg bg-black/50 p-4">
            <pre className="text-sm text-white/90">
              <code className="language-javascript">{lang.code}</code>
            </pre>
          </div>
          {lang.response && (
            <div className="rounded-lg bg-black/50 p-4 mt-4">
              <div className="flex items-center text-xs text-white/60 mb-2">
                <div className="flex-1">Response</div>
                <div>HTTP 200</div>
              </div>
              <pre className="text-sm text-[#79e5dd]">
                <code>{lang.response}</code>
              </pre>
            </div>
          )}
        </TabsContent>
      ))}
    </Tabs>
  );
}
