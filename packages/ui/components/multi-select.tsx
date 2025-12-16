"use client";

import * as React from "react";
import { Check, ChevronDown, X } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";
import { Button } from "@karrio/ui/components/ui/button";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@karrio/ui/components/ui/popover";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@karrio/ui/components/ui/command";
import { Badge } from "@karrio/ui/components/ui/badge";

export interface MultiSelectOption {
    label: string;
    value: string;
}

interface MultiSelectProps {
    value: string[];
    onValueChange: (values: string[]) => void;
    options: MultiSelectOption[];
    placeholder?: string;
    disabled?: boolean;
    className?: string;
    maxBadges?: number; // how many badges to show before "+N"
}

export const MultiSelect: React.FC<MultiSelectProps> = ({
    value,
    onValueChange,
    options,
    placeholder = "Select options",
    disabled = false,
    className,
    maxBadges = 3,
}) => {
    const [open, setOpen] = React.useState(false);
    const [search, setSearch] = React.useState("");
    const [showSelectedOnly, setShowSelectedOnly] = React.useState(false);

    const selectedSet = React.useMemo(() => new Set(value), [value]);

    const filtered = React.useMemo(() => {
        const term = search.trim().toLowerCase();
        if (!term) return options;
        return options.filter((opt) =>
            `${opt.label} ${opt.value}`.toLowerCase().includes(term)
        );
    }, [options, search]);

    const displayed = React.useMemo(() => {
        const base = filtered;
        return showSelectedOnly ? base.filter(o => selectedSet.has(o.value)) : base;
    }, [filtered, showSelectedOnly, selectedSet]);

    const toggle = (val: string) => {
        if (selectedSet.has(val)) {
            onValueChange(value.filter((v) => v !== val));
        } else {
            onValueChange([...value, val]);
        }
    };

    const clear = (e?: React.MouseEvent) => {
        e?.stopPropagation();
        onValueChange([]);
    };

    const visibleBadges = value.slice(0, maxBadges);
    const extraCount = Math.max(0, value.length - visibleBadges.length);
    const valueToLabel = React.useMemo(() => {
        const map = new Map(options.map((o) => [o.value, o.label] as const));
        return (v: string) => map.get(v) || v;
    }, [options]);

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button
                    type="button"
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    disabled={disabled}
                    className={cn(
                        "w-full justify-between h-8",
                        value.length === 0 && "text-muted-foreground",
                        className
                    )}
                >
                    <div className="flex flex-wrap gap-1 items-center">
                        {value.length === 0 ? (
                            <span className="truncate">{placeholder}</span>
                        ) : (
                            <>
                                {visibleBadges.map((v) => (
                                    <Badge key={v} variant="secondary" className="px-2 py-0.5 flex items-center gap-1">
                                        {valueToLabel(v)}
                                        <span
                                            role="button"
                                            tabIndex={0}
                                            aria-label={`Remove ${valueToLabel(v)}`}
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                e.preventDefault();
                                                onValueChange(value.filter((x) => x !== v));
                                            }}
                                            onKeyDown={(e) => {
                                                if (e.key === "Enter" || e.key === " ") {
                                                    e.stopPropagation();
                                                    e.preventDefault();
                                                    onValueChange(value.filter((x) => x !== v));
                                                }
                                            }}
                                            className="hover:text-foreground text-muted-foreground cursor-pointer"
                                        >
                                            <X className="h-3 w-3" />
                                        </span>
                                    </Badge>
                                ))}
                                {extraCount > 0 && (
                                    <Badge variant="secondary" className="px-2 py-0.5">+{extraCount}</Badge>
                                )}
                            </>
                        )}
                    </div>
                    <div className="flex items-center gap-2">
                        {value.length > 0 && (
                            <span
                                role="button"
                                tabIndex={0}
                                onClick={clear}
                                onKeyDown={(e) => {
                                    if (e.key === "Enter" || e.key === " ") {
                                        clear(e as any);
                                    }
                                }}
                                className="cursor-pointer"
                            >
                                <X className="h-4 w-4 text-muted-foreground hover:text-foreground" />
                            </span>
                        )}
                        <ChevronDown className="h-4 w-4 opacity-60" />
                    </div>
                </Button>
            </PopoverTrigger>
            <PopoverContent
                className="w-[var(--radix-popover-trigger-width)] p-0"
                align="start"
                onOpenAutoFocus={(e) => e.preventDefault()}
            >
                <Command shouldFilter={false}>
                    <CommandInput
                        placeholder="Search..."
                        value={search}
                        onValueChange={setSearch}
                    />
                    <CommandList
                        className="max-h-72 overflow-y-auto overscroll-contain"
                        onWheelCapture={(e) => e.stopPropagation()}
                    >
                        <CommandEmpty>No results found.</CommandEmpty>
                        <CommandGroup>
                            {displayed.map((opt) => {
                                const selected = selectedSet.has(opt.value);
                                return (
                                    <CommandItem
                                        key={opt.value}
                                        onSelect={() => toggle(opt.value)}
                                        className="cursor-pointer"
                                    >
                                        <Check
                                            className={cn(
                                                "mr-2 h-4 w-4",
                                                selected ? "opacity-100" : "opacity-0"
                                            )}
                                        />
                                        <span className="flex-1 truncate">{opt.label}</span>
                                        <span className="text-xs text-muted-foreground ml-2">({opt.value})</span>
                                    </CommandItem>
                                );
                            })}
                        </CommandGroup>
                    </CommandList>
                    <div className="flex justify-between p-2 border-t">
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setShowSelectedOnly((s) => !s)}
                            disabled={value.length === 0 && !showSelectedOnly}
                        >
                            {showSelectedOnly ? "All Countries" : "Selected"}
                        </Button>
                        {value.length > 0 && (
                            <Button variant="ghost" size="sm" onClick={clear}>Clear</Button>
                        )}
                    </div>
                </Command>
            </PopoverContent>
        </Popover>
    );
};

MultiSelect.displayName = "MultiSelect";


