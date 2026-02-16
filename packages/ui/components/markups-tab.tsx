"use client";

import React from "react";
import { PlusIcon, Pencil1Icon, TrashIcon } from "@radix-ui/react-icons";
import type { MarkupType, MarkupMeta } from "@karrio/hooks/admin-markups";

function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(" ");
}

const META_TYPE_LABELS: Record<string, string> = {
  "brokerage-fee": "Brokerage Fee",
  "insurance": "Insurance",
  "surcharge": "Surcharge",
  "notification": "Notification",
  "address-validation": "Address Validation",
};

interface MarkupsTabProps {
  markups: MarkupType[];
  onEditMarkup: (markup: MarkupType) => void;
  onAddMarkup: () => void;
  onRemoveMarkup: (markupId: string) => void;
}

export function MarkupsTab({
  markups,
  onEditMarkup,
  onAddMarkup,
  onRemoveMarkup,
}: MarkupsTabProps) {
  const formatAmount = (markup: MarkupType): string => {
    if (markup.markup_type === "PERCENTAGE") {
      return `${markup.amount ?? 0}%`;
    }
    return `${markup.amount ?? 0}`;
  };

  const formatType = (markup: MarkupType): string => {
    return markup.markup_type === "PERCENTAGE" ? "Percentage" : "Fixed Amount";
  };

  const formatMetaType = (markup: MarkupType): string => {
    const meta = (markup as any).meta as MarkupMeta | undefined;
    if (!meta?.type) return "\u2014";
    return META_TYPE_LABELS[meta.type] || meta.type;
  };

  const getMetaPlan = (markup: MarkupType): string => {
    const meta = (markup as any).meta as MarkupMeta | undefined;
    return meta?.plan || "\u2014";
  };

  const isShowInPreview = (markup: MarkupType): boolean => {
    const meta = (markup as any).meta as MarkupMeta | undefined;
    return meta?.show_in_preview ?? false;
  };

  if (markups.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-muted-foreground p-8">
        <p className="mb-4">No markups configured yet.</p>
        <button
          onClick={onAddMarkup}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md transition-colors"
        >
          <PlusIcon className="h-4 w-4" />
          Add Markup
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4 h-full overflow-y-auto pr-2">
      <div className="flex items-center justify-between sticky top-0 bg-background z-10 py-2">
        <h3 className="text-lg font-medium">Markup Configuration</h3>
        <button
          onClick={onAddMarkup}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md transition-colors"
        >
          <PlusIcon className="h-4 w-4" />
          Add Markup
        </button>
      </div>

      {markups.map((markup, index) => (
        <div
          key={markup.id}
          className="bg-card border border-border rounded-lg shadow-sm hover:border-primary/50 transition-colors"
        >
          <div className="px-6 py-4 space-y-4">
            {/* Header with name, active badge, and actions */}
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <h4 className="font-semibold text-foreground text-base">
                  {markup.name || `Markup ${index + 1}`}
                </h4>
                <span
                  className={cn(
                    "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold",
                    markup.active
                      ? "bg-green-500 text-white dark:bg-green-600 dark:text-white"
                      : "bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300"
                  )}
                >
                  {markup.active ? "Active" : "Inactive"}
                </span>
                {isShowInPreview(markup) && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
                    Preview
                  </span>
                )}
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => onEditMarkup(markup)}
                  className="p-1.5 text-muted-foreground hover:text-foreground hover:bg-accent rounded transition-colors"
                  title="Edit Markup"
                >
                  <Pencil1Icon className="h-4 w-4" />
                </button>
                <button
                  onClick={() => onRemoveMarkup(markup.id)}
                  className="p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded transition-colors"
                  title="Delete Markup"
                >
                  <TrashIcon className="h-4 w-4" />
                </button>
              </div>
            </div>

            {/* Markup details grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                  Type:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {formatType(markup)}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                  Amount:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {formatAmount(markup)}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                  Category:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {formatMetaType(markup)}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                  Plan:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {getMetaPlan(markup)}
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default MarkupsTab;
