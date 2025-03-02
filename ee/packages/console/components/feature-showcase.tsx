"use client";

import {
  Card, CardContent
} from "@karrio/insiders/components/ui/card";
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
        <div>
          <div className="space-y-4 flex flex-col justify-between">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">{title}</h3>
              <p className="text-white/60 mb-6">{description}</p>
            </div>
            {/* Simplified content display without tabs */}
            <div className="mb-4">
              {tabs[0].content}
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
        </div>
      </CardContent>
    </Card>
  );
}
