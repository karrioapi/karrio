"use client";
import React from "react";
import { GraphiQLModule } from "@karrio/developers/modules/graphiql";

export function GraphiQLView() {
  return (
    <div className="h-full w-full">
      <GraphiQLModule />
    </div>
  );
}