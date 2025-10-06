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

    const selectedSet = React.useMemo(() => new Set(value), [value]);

    const filtered = React.useMemo(() => {
        const term = search.trim().toLowerCase();
        if (!term) return options;
        return options.filter((opt) =>
            `${opt.label} ${opt.value}`.toLowerCase().includes(term)
        );
    }, [options, search]);

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
                                        <button
                                            type="button"
                                            aria-label={`Remove ${valueToLabel(v)}`}
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                onValueChange(value.filter((x) => x !== v));
                                            }}
                                            className="hover:text-foreground text-muted-foreground"
                                        >
                                            <X className="h-3 w-3" />
                                        </button>
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
                            <X
                                className="h-4 w-4 text-muted-foreground hover:text-foreground"
                                onClick={clear}
                            />
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
                    <div
                        className="max-h-72 overflow-y-auto"
                        onWheel={(e) => {
                            const el = e.currentTarget as HTMLDivElement;
                            const canScrollUp = el.scrollTop > 0;
                            const canScrollDown = el.scrollTop < el.scrollHeight - el.clientHeight;
                            if ((e.deltaY < 0 && canScrollUp) || (e.deltaY > 0 && canScrollDown)) {
                                e.stopPropagation();
                            }
                        }}
                    >
                        <CommandList>
                            <CommandEmpty>No results found.</CommandEmpty>
                            <CommandGroup>
                                {filtered.map((opt) => {
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
                    </div>
                    {value.length > 0 && (
                        <div className="flex justify-end p-2 border-t">
                            <Button variant="ghost" size="sm" onClick={clear}>Clear</Button>
                        </div>
                    )}
                </Command>
            </PopoverContent>
        </Popover>
    );
};

MultiSelect.displayName = "MultiSelect";


