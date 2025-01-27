"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@karrio/insiders/components/ui/accordion";
import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from "@karrio/insiders/components/ui/tabs";
import { useMediaQuery } from "@karrio/console/hooks/use-media-query";
import { Button } from "@karrio/insiders/components/ui/button";
import { ChevronRight } from "lucide-react";

interface FeatureTab {
  icon: React.ReactNode;
  label: string;
  value: string;
  title: string;
  description: string;
  features: string[];
  demo: React.ReactNode;
}

interface FeatureTabsProps {
  tabs: FeatureTab[];
}

export function FeatureTabs({ tabs }: FeatureTabsProps) {
  const isMobile = useMediaQuery("(max-width: 768px)");

  if (isMobile) {
    return (
      <div className="w-full mx-auto bg-gradient-to-br from-[#1a103d]/80 to-[#0f0826]/90 backdrop-blur-sm rounded-xl border border-white/10">
        <Accordion type="single" collapsible className="w-full space-y-2 p-2">
          {tabs.map((tab) => (
            <AccordionItem
              key={tab.value}
              value={tab.value}
              className="bg-white/5 rounded-lg"
            >
              <AccordionTrigger className="px-8 py-5 hover:no-underline">
                <div className="flex items-center gap-2">
                  {tab.icon}
                  <span className="text-sm font-medium">{tab.label}</span>
                </div>
              </AccordionTrigger>
              <AccordionContent>
                <div className="px-8 pb-8 space-y-6">
                  <div className="space-y-3">
                    <h3 className="text-xl font-bold bg-gradient-to-r from-white to-white/90 bg-clip-text text-transparent">
                      {tab.title}
                    </h3>
                    <div className="h-px w-12 bg-gradient-to-r from-[#79e5dd] to-transparent" />
                    <p className="text-sm text-white/70 leading-relaxed">
                      {tab.description}
                    </p>
                  </div>

                  <div className="space-y-4">
                    <div className="h-px w-full bg-white/10" />
                    <ul className="space-y-3">
                      {tab.features.map((feature, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <div className="size-1.5 rounded-full bg-[#79e5dd] mt-1.5" />
                          <span className="text-sm text-white/80 flex-1">
                            {feature}
                          </span>
                        </li>
                      ))}
                    </ul>
                    <div className="h-px w-full bg-white/10" />
                    <Button
                      variant="link"
                      className="text-[#79e5dd] p-0 h-auto font-semibold text-sm hover:text-[#79e5dd]/90 hover:no-underline"
                    >
                      Learn more
                      <ChevronRight className="ml-1 h-3 w-3" />
                    </Button>
                  </div>

                  <div className="bg-white/5 rounded-lg p-6 sm:p-8 overflow-hidden">
                    <div className="w-[95%] mx-auto">
                      <div className="relative w-full aspect-[5/4]">
                        {tab.demo}
                      </div>
                    </div>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    );
  }

  return (
    <div className="w-full mx-auto bg-gradient-to-br from-[#1a103d]/80 to-[#0f0826]/90 backdrop-blur-sm rounded-xl border border-white/10">
      <Tabs defaultValue={tabs[0].value} className="w-full">
        <div className="p-2 sm:p-3 md:p-4">
          <TabsList className="w-full flex pt-2 pb-4 justify-between border-b border-white/10 bg-transparent h-12 overflow-x-auto scrollbar-none">
            {tabs.map((tab) => (
              <TabsTrigger
                key={tab.value}
                value={tab.value}
                className="flex items-center shrink-0 justify-center gap-1.5 px-6 py-2.5 flex-1 data-[state=active]:bg-[#5722cc] data-[state=active]:text-white text-sm font-medium transition-colors hover:text-white/90"
              >
                {tab.icon}
                <span className="whitespace-nowrap">{tab.label}</span>
              </TabsTrigger>
            ))}
          </TabsList>
        </div>
        {tabs.map((tab) => (
          <TabsContent
            key={tab.value}
            value={tab.value}
            className="p-4 sm:p-5 md:p-6 lg:p-8"
          >
            <div className="grid grid-cols-1 lg:grid-cols-[0.4fr,0.6fr] gap-4 sm:gap-6 md:gap-8 lg:gap-16 items-start">
              <div className="space-y-4 sm:space-y-6 md:space-y-8">
                <div className="space-y-3 sm:space-y-4">
                  <h3 className="text-xl sm:text-2xl lg:text-3xl font-bold bg-gradient-to-r from-white to-white/90 bg-clip-text text-transparent">
                    {tab.title}
                  </h3>
                  <div className="h-px w-12 sm:w-16 bg-gradient-to-r from-[#79e5dd] to-transparent" />
                  <p className="text-sm sm:text-base lg:text-lg text-white/70 leading-relaxed">
                    {tab.description}
                  </p>
                </div>
                <div className="space-y-4 sm:space-y-6">
                  <div className="h-px w-full bg-white/10" />
                  <ul className="space-y-3 sm:space-y-4">
                    {tab.features.map((feature, index) => (
                      <li
                        key={index}
                        className="flex items-start gap-2 sm:gap-3"
                      >
                        <div className="size-1.5 sm:size-2 rounded-full bg-[#79e5dd] mt-1.5 sm:mt-2" />
                        <span className="text-sm sm:text-base text-white/80 flex-1">
                          {feature}
                        </span>
                      </li>
                    ))}
                  </ul>
                  <div className="h-px w-full bg-white/10" />
                  <Button
                    variant="link"
                    className="text-[#79e5dd] p-0 h-auto font-semibold text-sm sm:text-base hover:text-[#79e5dd]/90 hover:no-underline"
                  >
                    Learn more
                    <ChevronRight className="ml-1 h-3 w-3 sm:h-4 sm:w-4" />
                  </Button>
                </div>
              </div>
              <div className="bg-white/5 rounded-lg p-8 lg:p-10">
                <div className="mx-auto w-[85%]">
                  <div className="relative w-full h-full">{tab.demo}</div>
                </div>
              </div>
            </div>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}
