"use client";

import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from "@karrio/insiders/components/ui/tabs";
import { Card, CardContent } from "@karrio/insiders/components/ui/card";
import { Button } from "@karrio/insiders/components/ui/button";
import { ChevronRight } from "lucide-react";

interface FeatureShowcaseProps {
  title: string;
  description: string;
  tabs: {
    label: string;
    value: string;
    content: React.ReactNode;
  }[];
  learnMoreHref: string;
}

export function FeatureShowcase({
  title,
  description,
  tabs,
  learnMoreHref,
}: FeatureShowcaseProps) {
  return (
    <Card className="bg-white/5 border-white/10">
      <CardContent className="p-6">
        <div className="grid lg:grid-cols-2 gap-8">
          <div className="space-y-4 flex flex-col justify-between h-full">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">{title}</h3>
              <p className="text-white/60">{description}</p>
            </div>
            <Button
              variant="link"
              className="text-[#79e5dd] p-0 h-auto font-semibold self-start"
              asChild
            >
              <a href={learnMoreHref}>
                Learn more
                <ChevronRight className="ml-1 h-4 w-4" />
              </a>
            </Button>
          </div>
          <div className="flex items-center">
            <Tabs defaultValue={tabs[0].value} className="w-full">
              <TabsList className="bg-white/5 w-full justify-start mb-4">
                {tabs.map((tab) => (
                  <TabsTrigger
                    key={tab.value}
                    value={tab.value}
                    className="data-[state=active]:bg-[#5722cc] data-[state=active]:text-white"
                  >
                    {tab.label}
                  </TabsTrigger>
                ))}
              </TabsList>
              {tabs.map((tab) => (
                <TabsContent key={tab.value} value={tab.value}>
                  {tab.content}
                </TabsContent>
              ))}
            </Tabs>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
