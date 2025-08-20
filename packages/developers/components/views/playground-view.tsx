"use client";
import React from "react";
import { PlaygroundModule } from "@karrio/developers/modules/playground";

export function PlaygroundView() {
  return (
    <div className="h-full w-full overflow-y-auto overflow-x-hidden">
      <PlaygroundModule />
    </div>
  );
}