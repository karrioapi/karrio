"use client";

import React, { useMemo, useState } from "react";
import { PlusIcon, Pencil1Icon, TrashIcon, ChevronDownIcon, ChevronRightIcon } from "@radix-ui/react-icons";
import type { MarkupType, MarkupMeta } from "@karrio/hooks/admin-markups";
import type { ServiceLevelWithZones } from "@karrio/ui/components/rate-sheet-editor";

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

const CATEGORY_ORDER = [
  "brokerage-fee",
  "insurance",
  "surcharge",
  "notification",
  "address-validation",
  "uncategorized",
];

interface MarkupsTabProps {
  markups: MarkupType[];
  onEditMarkup: (markup: MarkupType) => void;
  onAddMarkup: () => void;
  onRemoveMarkup: (markupId: string) => void;
  services?: ServiceLevelWithZones[];
  rateSheetPricingConfig?: Record<string, any>;
  onToggleSheetExclusion?: (markupId: string, excluded: boolean) => void;
  onToggleServiceExclusion?: (serviceId: string, markupId: string, excluded: boolean) => void;
}

export function MarkupsTab({
  markups,
  onEditMarkup,
  onAddMarkup,
  onRemoveMarkup,
  services = [],
  rateSheetPricingConfig,
  onToggleSheetExclusion,
  onToggleServiceExclusion,
}: MarkupsTabProps) {
  const [expandedMarkupId, setExpandedMarkupId] = useState<string | null>(null);

  const formatAmount = (markup: MarkupType): string => {
    if (markup.markup_type === "PERCENTAGE") {
      return `${markup.amount ?? 0}%`;
    }
    return `${markup.amount ?? 0}`;
  };

  const grouped = useMemo(() => {
    const groups: Record<string, MarkupType[]> = {};
    for (const markup of markups) {
      const meta = (markup as any).meta as MarkupMeta | undefined;
      const category = meta?.type || "uncategorized";
      if (!groups[category]) groups[category] = [];
      groups[category].push(markup);
    }
    return CATEGORY_ORDER
      .filter((cat) => groups[cat]?.length > 0)
      .map((cat) => ({
        category: cat,
        label: META_TYPE_LABELS[cat] || "Uncategorized",
        items: groups[cat],
      }));
  }, [markups]);

  const hasExclusionControls = !!(onToggleServiceExclusion && services.length > 0);

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
    <div className="space-y-6 h-full overflow-y-auto pr-2">
      <div className="flex items-center justify-between sticky top-0 bg-background z-10 py-2">
        <h3 className="text-lg font-medium">Brokerage Configuration</h3>
        <button
          onClick={onAddMarkup}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md transition-colors"
        >
          <PlusIcon className="h-4 w-4" />
          Add Markup
        </button>
      </div>

      {grouped.map(({ category, label, items }) => (
        <div key={category}>
          <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2">
            {label}
          </h4>
          <div className="border border-border rounded-md overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border bg-muted/50">
                  {hasExclusionControls && (
                    <th className="w-8 px-2 py-2"></th>
                  )}
                  <th className="text-left font-medium text-muted-foreground px-4 py-2">Name</th>
                  <th className="text-left font-medium text-muted-foreground px-4 py-2">Type</th>
                  <th className="text-left font-medium text-muted-foreground px-4 py-2">Amount</th>
                  <th className="text-left font-medium text-muted-foreground px-4 py-2">Plan</th>
                  <th className="text-left font-medium text-muted-foreground px-4 py-2">Status</th>
                  <th className="w-20 px-4 py-2"></th>
                </tr>
              </thead>
              <tbody>
                {items.map((markup, index) => {
                  const meta = (markup as any).meta as MarkupMeta | undefined;
                  const isExpanded = expandedMarkupId === markup.id;

                  return (
                    <React.Fragment key={markup.id}>
                      <tr
                        className={cn(
                          "hover:bg-muted/30 transition-colors",
                          index < items.length - 1 && !isExpanded && "border-b border-border"
                        )}
                      >
                        {hasExclusionControls && (
                          <td className="px-2 py-2.5">
                            <button
                              onClick={() => setExpandedMarkupId(isExpanded ? null : markup.id)}
                              className="p-0.5 text-muted-foreground hover:text-foreground transition-colors"
                              title={isExpanded ? "Collapse" : "Expand per-service exclusions"}
                            >
                              {isExpanded
                                ? <ChevronDownIcon className="h-3.5 w-3.5" />
                                : <ChevronRightIcon className="h-3.5 w-3.5" />
                              }
                            </button>
                          </td>
                        )}
                        <td className="px-4 py-2.5">
                          <div className="flex items-center gap-2">
                            <span className="font-medium text-foreground">
                              {markup.name}
                            </span>
                            {meta?.show_in_preview && (
                              <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
                                Preview
                              </span>
                            )}
                          </div>
                        </td>
                        <td className="px-4 py-2.5 text-muted-foreground">
                          {markup.markup_type === "PERCENTAGE" ? "Percentage" : "Fixed"}
                        </td>
                        <td className="px-4 py-2.5 font-medium text-foreground">
                          {formatAmount(markup)}
                        </td>
                        <td className="px-4 py-2.5 text-muted-foreground">
                          {meta?.plan || "\u2014"}
                        </td>
                        <td className="px-4 py-2.5">
                          <span
                            className={cn(
                              "inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold",
                              markup.active
                                ? "bg-green-500 text-white dark:bg-green-600"
                                : "bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300"
                            )}
                          >
                            {markup.active ? "Active" : "Inactive"}
                          </span>
                        </td>
                        <td className="px-4 py-2.5">
                          <div className="flex items-center justify-end gap-1">
                            <button
                              onClick={() => onEditMarkup(markup)}
                              className="p-1.5 text-muted-foreground hover:text-foreground hover:bg-accent rounded transition-colors"
                              title="Edit"
                            >
                              <Pencil1Icon className="h-3.5 w-3.5" />
                            </button>
                            <button
                              onClick={() => onRemoveMarkup(markup.id)}
                              className="p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded transition-colors"
                              title="Delete"
                            >
                              <TrashIcon className="h-3.5 w-3.5" />
                            </button>
                          </div>
                        </td>
                      </tr>

                      {/* Per-service exclusion rows */}
                      {hasExclusionControls && isExpanded && (
                        <tr className={cn(index < items.length - 1 && "border-b border-border")}>
                          <td colSpan={8} className="px-0 py-0">
                            <div className="bg-muted/20 border-t border-border">
                              <div className="px-6 py-2">
                                <p className="text-xs font-medium text-muted-foreground mb-2">
                                  Per-service exclusions for "{markup.name}"
                                </p>
                                <div className="space-y-1 max-h-48 overflow-y-auto">
                                  {services.map((service) => {
                                    const svcPricingConfig = service.pricing_config || {};
                                    const svcExcludedIds: string[] = svcPricingConfig.excluded_markup_ids || [];
                                    const isServiceExcluded = svcExcludedIds.includes(markup.id);

                                    return (
                                      <label
                                        key={service.id}
                                        className="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-muted/50 cursor-pointer"
                                      >
                                        <input
                                          type="checkbox"
                                          checked={isServiceExcluded}
                                          onChange={() => onToggleServiceExclusion!(service.id, markup.id, !isServiceExcluded)}
                                          className="h-3.5 w-3.5 rounded border-border"
                                        />
                                        <span className="text-sm text-foreground">
                                          {service.service_name}
                                        </span>
                                        <span className="text-xs text-muted-foreground ml-auto">
                                          {service.service_code}
                                        </span>
                                      </label>
                                    );
                                  })}
                                </div>
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
}

export default MarkupsTab;
