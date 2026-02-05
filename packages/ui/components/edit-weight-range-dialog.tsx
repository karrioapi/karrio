"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
  DialogBody,
} from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import type { WeightRange } from "@karrio/ui/components/weight-rate-grid";

interface EditWeightRangeDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  weightRange: WeightRange | null;
  existingRanges: WeightRange[];
  weightUnit: string;
  onSave: (oldMin: number, oldMax: number, newMax: number) => void;
  isLoading?: boolean;
}

export function EditWeightRangeDialog({
  open,
  onOpenChange,
  weightRange,
  existingRanges,
  weightUnit,
  onSave,
  isLoading = false,
}: EditWeightRangeDialogProps) {
  const [maxWeight, setMaxWeight] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (open && weightRange) {
      setMaxWeight(weightRange.max_weight.toString());
      setError(null);
    }
  }, [open, weightRange]);

  if (!weightRange) return null;

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    setError(null);
    const newMax = parseFloat(maxWeight);

    if (isNaN(newMax) || newMax <= 0) {
      setError("Max weight must be a positive number");
      return;
    }

    if (newMax <= weightRange.min_weight) {
      setError(
        `Max weight must be greater than ${weightRange.min_weight} ${weightUnit}`
      );
      return;
    }

    // Check for overlapping with other ranges (excluding current range)
    const otherRanges = existingRanges.filter(
      (r) =>
        !(
          r.min_weight === weightRange.min_weight &&
          r.max_weight === weightRange.max_weight
        )
    );
    const overlapping = otherRanges.some(
      (r) => weightRange.min_weight < r.max_weight && newMax > r.min_weight
    );
    if (overlapping) {
      setError("This weight range would overlap with an existing range");
      return;
    }

    onSave(weightRange.min_weight, weightRange.max_weight, newMax);
    onOpenChange(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-sm">
        <DialogHeader>
          <DialogTitle>Edit Weight Range</DialogTitle>
          <DialogDescription>
            Modify the max weight for this bracket. Existing rates will be
            re-keyed automatically.
          </DialogDescription>
        </DialogHeader>

        <DialogBody>
          <form id="edit-weight-range-form" onSubmit={handleSubmit} className="space-y-4">
            {/* Min weight (read-only) */}
            <div className="space-y-1.5">
              <Label className="text-xs">Min Weight ({weightUnit})</Label>
              <Input
                type="number"
                value={weightRange.min_weight}
                disabled
                className="h-9 bg-muted text-muted-foreground"
              />
            </div>

            {/* Max weight (editable) */}
            <div className="space-y-1.5">
              <Label className="text-xs">Max Weight ({weightUnit})</Label>
              <Input
                type="number"
                step="any"
                min={weightRange.min_weight + 0.01}
                value={maxWeight}
                onChange={(e) => setMaxWeight(e.target.value)}
                onKeyDown={handleKeyDown}
                className="h-9"
                autoFocus
              />
              {error && (
                <p className="text-xs text-destructive mt-1">{error}</p>
              )}
            </div>
          </form>
        </DialogBody>

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => onOpenChange(false)}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            size="sm"
            form="edit-weight-range-form"
            disabled={isLoading || !maxWeight}
          >
            {isLoading ? "Saving..." : "Save"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
