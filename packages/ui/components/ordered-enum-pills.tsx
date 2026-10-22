"use client";

import * as React from "react";
import { ChevronLeft, ChevronRight, GripVertical, Plus, X } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";
import { badgeVariants } from "./ui/badge";
import { Button } from "./ui/button";

export interface OrderedEnumPillsProps {
  options: string[];
  value?: string[] | null;
  onChange: (value: string[] | null) => void;
  formatLabel?: (option: string) => string;
  disabled?: boolean;
  className?: string;
}

const unique = (values: string[]) =>
  values.filter((value, index) => values.indexOf(value) === index);

const move = (values: string[], from: number, to: number) => {
  if (from === to || to < 0 || to >= values.length) return values;
  const next = [...values];
  const [item] = next.splice(from, 1);
  next.splice(to, 0, item);
  return next;
};

/**
 * Ordered selection of enum values rendered as pills.
 *
 * Selected values keep their order and can be reordered by dragging or with
 * the move buttons; unselected values are offered as add-pills. An empty
 * selection is reported as `null` so the value is unset rather than `[]`.
 */
export const OrderedEnumPills: React.FC<OrderedEnumPillsProps> = ({
  options,
  value,
  onChange,
  formatLabel = (option) => option,
  disabled,
  className,
}) => {
  const selected = unique(Array.isArray(value) ? value : []);
  const available = options.filter((option) => !selected.includes(option));
  const [dragIndex, setDragIndex] = React.useState<number | null>(null);

  const emit = (next: string[]) => onChange(next.length > 0 ? next : null);

  const handleDrop = (event: React.DragEvent, target: number) => {
    event.preventDefault();
    if (dragIndex !== null) emit(move(selected, dragIndex, target));
    setDragIndex(null);
  };

  return (
    <div className={cn("space-y-2", className)}>
      <ol
        className="flex flex-wrap gap-2"
        aria-label="Selected values in order"
      >
        {selected.length === 0 && (
          <li className="text-sm text-muted-foreground">None selected</li>
        )}
        {selected.map((option, index) => (
          <li
            key={option}
            draggable={!disabled}
            onDragStart={(event) => {
              event.dataTransfer.effectAllowed = "move";
              event.dataTransfer.setData("text/plain", option);
              setDragIndex(index);
            }}
            onDragOver={(event) => event.preventDefault()}
            onDrop={(event) => handleDrop(event, index)}
            onDragEnd={() => setDragIndex(null)}
            className={cn(
              badgeVariants({ variant: "secondary" }),
              "gap-1 py-1 pl-1 pr-1",
              !disabled && "cursor-grab",
              dragIndex === index && "opacity-50",
            )}
          >
            <GripVertical
              className="h-3 w-3 text-muted-foreground"
              aria-hidden
            />
            <span className="px-1 text-muted-foreground">{index + 1}.</span>
            <span>{formatLabel(option)}</span>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="h-5 w-5"
              disabled={disabled || index === 0}
              onClick={() => emit(move(selected, index, index - 1))}
              aria-label={`Move ${formatLabel(option)} earlier`}
            >
              <ChevronLeft className="h-3 w-3" />
            </Button>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="h-5 w-5"
              disabled={disabled || index === selected.length - 1}
              onClick={() => emit(move(selected, index, index + 1))}
              aria-label={`Move ${formatLabel(option)} later`}
            >
              <ChevronRight className="h-3 w-3" />
            </Button>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="h-5 w-5"
              disabled={disabled}
              onClick={() => emit(selected.filter((item) => item !== option))}
              aria-label={`Remove ${formatLabel(option)}`}
            >
              <X className="h-3 w-3" />
            </Button>
          </li>
        ))}
      </ol>

      {available.length > 0 && (
        <div className="flex flex-wrap gap-2" aria-label="Available values">
          {available.map((option) => (
            <button
              key={option}
              type="button"
              disabled={disabled}
              onClick={() => emit([...selected, option])}
              className={cn(
                badgeVariants({ variant: "outline" }),
                "gap-1 border-dashed font-normal text-muted-foreground hover:text-foreground",
              )}
              aria-label={`Add ${formatLabel(option)}`}
            >
              <Plus className="h-3 w-3" />
              {formatLabel(option)}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
