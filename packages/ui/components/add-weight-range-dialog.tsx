"use client";

import React, { useState } from "react";
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogCancel,
  AlertDialogAction,
} from "@karrio/ui/components/ui/alert-dialog";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";

export interface WeightRange {
  min_weight: number;
  max_weight: number;
}

interface AddWeightRangeDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  existingRanges: WeightRange[];
  weightUnit: string;
  onAdd: (minWeight: number, maxWeight: number) => void;
  isLoading?: boolean;
}

export function AddWeightRangeDialog({
  open,
  onOpenChange,
  existingRanges,
  weightUnit,
  onAdd,
  isLoading = false,
}: AddWeightRangeDialogProps) {
  const [maxWeight, setMaxWeight] = useState("");
  const [error, setError] = useState<string | null>(null);

  const suggestedMin = 0;
  const derivedMinWeight = suggestedMin;

  const handleSubmit = () => {
    setError(null);
    const max = parseFloat(maxWeight);

    if (isNaN(max) || max <= 0) {
      setError("Max weight must be a positive number");
      return;
    }

    if (max <= derivedMinWeight) {
      setError(
        `Max weight must be greater than ${derivedMinWeight} ${weightUnit}`
      );
      return;
    }

    const overlapping = existingRanges.some(
      (r) => derivedMinWeight < r.max_weight && max > r.min_weight
    );
    if (overlapping) {
      setError("This weight range overlaps with an existing range");
      return;
    }

    onAdd(derivedMinWeight, max);
    setMaxWeight("");
    setError(null);
    onOpenChange(false);
  };

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Add Weight Range</AlertDialogTitle>
          <AlertDialogDescription>
            Add a new weight bracket to the rate grid. Rates will be initialized
            to 0 for all service-zone combinations.
          </AlertDialogDescription>
        </AlertDialogHeader>

        <div className="space-y-4 py-2">
          <div>
            <Label>Min Weight ({weightUnit})</Label>
            <Input value={derivedMinWeight} disabled className="mt-1" />
            <p className="text-xs text-muted-foreground mt-1">
              Auto-derived from the previous range
            </p>
          </div>

          <div>
            <Label>Max Weight ({weightUnit})</Label>
            <Input
              type="number"
              step="any"
              min={derivedMinWeight + 0.01}
              value={maxWeight}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setMaxWeight(e.target.value)
              }
              onKeyDown={(e: React.KeyboardEvent) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
              placeholder={`e.g., ${derivedMinWeight + 5}`}
              className="mt-1"
              autoFocus
            />
            {error && (
              <p className="text-xs text-destructive mt-1">{error}</p>
            )}
          </div>
        </div>

        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={handleSubmit}
            disabled={isLoading || !maxWeight}
          >
            {isLoading ? "Adding..." : "Add Range"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

export default AddWeightRangeDialog;
