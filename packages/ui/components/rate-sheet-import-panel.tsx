"use client";

import React, { useRef, useState } from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { cn } from "@karrio/ui/lib/utils";
import { Loader2, UploadCloud, FileSpreadsheet, AlertCircle, CheckCircle2 } from "lucide-react";

// ─── Types ───────────────────────────────────────────────────────────────────

export interface ImportValidationError {
  sheet: string;
  row: number;
  field: string;
  message: string;
}

export interface ImportDiffRow {
  /** Flat-format field names (preferred) */
  service_code: string;
  zone_label: string;
  shipment_type: string;
  min_weight: number;
  max_weight: number;
  old_rate: number | null;
  new_rate: number | null;
  change: "added" | "updated" | "removed" | "unchanged";
  /** Legacy aliases — present for backward-compat; equal to service_code / zone_label */
  service_id?: string;
  zone_id?: string;
}

export interface ImportDiff {
  summary: {
    added: number;
    updated: number;
    removed: number;
    unchanged: number;
  };
  rows: ImportDiffRow[];
}

export interface DryRunResult {
  dry_run: true;
  errors: ImportValidationError[];
  diff: ImportDiff;
  rate_sheet: {
    name: string;
    slug: string;
    carrier_name: string;
  };
}

interface RateSheetImportPanelProps {
  /** Existing rate sheet slug or id — used to tag the import (optional for new sheets) */
  rateSheetId?: string;
  /** Called with the confirmed diff when the user clicks "Confirm Import" */
  onConfirm: (file: File) => Promise<void>;
  /** Called to validate without writing — returns DryRunResult or throws */
  onDryRun: (file: File) => Promise<DryRunResult>;
  /** Called when user cancels import mode */
  onCancel: () => void;
  isConfirming?: boolean;
}

type Step = "pick" | "validating" | "errors" | "preview" | "confirming";

// ─── Component ───────────────────────────────────────────────────────────────

export const RateSheetImportPanel: React.FC<RateSheetImportPanelProps> = ({
  rateSheetId,
  onConfirm,
  onDryRun,
  onCancel,
  isConfirming = false,
}) => {
  const [step, setStep] = useState<Step>("pick");
  const [file, setFile] = useState<File | null>(null);
  const [errors, setErrors] = useState<ImportValidationError[]>([]);
  const [diff, setDiff] = useState<ImportDiff | null>(null);
  const [dryRunMeta, setDryRunMeta] = useState<DryRunResult["rate_sheet"] | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (f: File) => {
    setFile(f);
    setErrors([]);
    setDiff(null);
    setStep("validating");
    try {
      const result = await onDryRun(f);
      if (result.errors && result.errors.length > 0) {
        setErrors(result.errors);
        setStep("errors");
      } else {
        setDiff(result.diff);
        setDryRunMeta(result.rate_sheet ?? null);
        setStep("preview");
      }
    } catch (err: any) {
      setErrors([{ sheet: "", row: 0, field: "", message: err?.message || "Unknown error" }]);
      setStep("errors");
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files?.[0];
    if (f) handleFile(f);
  };

  const handleConfirm = async () => {
    if (!file) return;
    setStep("confirming");
    await onConfirm(file);
  };

  const handleReset = () => {
    setStep("pick");
    setFile(null);
    setErrors([]);
    setDiff(null);
    setDryRunMeta(null);
  };

  return (
    <div className="flex flex-col gap-4 p-4 h-full">
      {/* ── Step 1: File picker ── */}
      {(step === "pick") && (
        <FilePicker
          dragOver={dragOver}
          onDragOver={() => setDragOver(true)}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onFileChange={(f) => handleFile(f)}
          fileInputRef={fileInputRef}
          onCancel={onCancel}
        />
      )}

      {/* ── Validating spinner ── */}
      {step === "validating" && (
        <div className="flex flex-col items-center justify-center gap-3 py-16 text-muted-foreground">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm font-medium">Validating {file?.name}…</p>
        </div>
      )}

      {/* ── Validation errors ── */}
      {step === "errors" && (
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-2 text-destructive">
            <AlertCircle className="h-5 w-5 flex-shrink-0" />
            <span className="font-semibold text-sm">
              {errors.length} validation error{errors.length !== 1 ? "s" : ""} found — no data was written
            </span>
          </div>
          <div className="rounded-md border border-destructive/30 bg-destructive/5 p-3 max-h-80 overflow-y-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="text-muted-foreground border-b">
                  <th className="pb-1 pr-2 text-left font-medium">Sheet</th>
                  <th className="pb-1 pr-2 text-left font-medium">Row</th>
                  <th className="pb-1 pr-2 text-left font-medium">Field</th>
                  <th className="pb-1 text-left font-medium">Message</th>
                </tr>
              </thead>
              <tbody>
                {errors.map((e, i) => (
                  <tr key={i} className="border-b border-border/40 last:border-0">
                    <td className="py-1 pr-2 font-mono text-muted-foreground">{e.sheet || "—"}</td>
                    <td className="py-1 pr-2 text-right text-muted-foreground">{e.row || "—"}</td>
                    <td className="py-1 pr-2 font-mono text-orange-600">{e.field || "—"}</td>
                    <td className="py-1 text-foreground">{e.message}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={handleReset}>
              Try a different file
            </Button>
            <Button size="sm" variant="ghost" onClick={onCancel}>
              Cancel
            </Button>
          </div>
        </div>
      )}

      {/* ── Step 2: Diff preview ── */}
      {(step === "preview" || step === "confirming") && diff && (
        <DiffPreview
          diff={diff}
          meta={dryRunMeta}
          fileName={file?.name}
          onConfirm={handleConfirm}
          onCancel={onCancel}
          isConfirming={step === "confirming" || isConfirming}
        />
      )}
    </div>
  );
};

// ─── Sub-components ───────────────────────────────────────────────────────────

interface FilePickerProps {
  dragOver: boolean;
  onDragOver: () => void;
  onDragLeave: () => void;
  onDrop: (e: React.DragEvent) => void;
  onFileChange: (f: File) => void;
  fileInputRef: React.RefObject<HTMLInputElement>;
  onCancel: () => void;
}

const FilePicker: React.FC<FilePickerProps> = ({
  dragOver,
  onDragOver,
  onDragLeave,
  onDrop,
  onFileChange,
  fileInputRef,
  onCancel,
}) => (
  <div className="flex flex-col gap-4">
    <div>
      <h3 className="text-sm font-semibold mb-0.5">Import Rate Sheet</h3>
      <p className="text-xs text-muted-foreground">
        Upload an Excel (.xlsx) or CSV file. One file = one rate sheet. Upload will validate before writing.
      </p>
    </div>
    <div
      className={cn(
        "relative flex flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed p-10 text-center transition-colors",
        dragOver
          ? "border-primary bg-primary/5"
          : "border-border hover:border-primary/50 hover:bg-accent/30"
      )}
      onDragOver={(e) => { e.preventDefault(); onDragOver(); }}
      onDragLeave={onDragLeave}
      onDrop={onDrop}
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-muted">
        <UploadCloud className="h-6 w-6 text-muted-foreground" />
      </div>
      <div>
        <p className="text-sm font-medium">Drop your file here, or{" "}
          <button
            type="button"
            className="text-primary underline underline-offset-2 hover:no-underline"
            onClick={() => fileInputRef.current?.click()}
          >
            browse
          </button>
        </p>
        <p className="mt-0.5 text-xs text-muted-foreground">.xlsx or .csv — max 10 MB</p>
      </div>
      <input
        ref={fileInputRef}
        type="file"
        accept=".xlsx,.xls,.csv"
        className="hidden"
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) onFileChange(f);
          // reset so same file can be re-uploaded
          e.target.value = "";
        }}
      />
    </div>
    <div className="flex items-center gap-2 text-xs text-muted-foreground">
      <FileSpreadsheet className="h-4 w-4 flex-shrink-0" />
      <span>
        Need the template?{" "}
        <a
          href="/templates/rate-sheet-template.xlsx"
          download
          className="text-primary underline underline-offset-2 hover:no-underline"
        >
          Download blank template
        </a>
        {" "}·{" "}
        <a
          href="/templates/rate-sheet-sample.xlsx"
          download
          className="text-primary underline underline-offset-2 hover:no-underline"
        >
          Download sample (DHL Parcel DE)
        </a>
      </span>
    </div>
    <Button size="sm" variant="ghost" className="self-start" onClick={onCancel}>
      Cancel
    </Button>
  </div>
);

// ─── Diff Preview ─────────────────────────────────────────────────────────────

interface DiffPreviewProps {
  diff: ImportDiff;
  meta: DryRunResult["rate_sheet"] | null;
  fileName?: string;
  onConfirm: () => void;
  onCancel: () => void;
  isConfirming: boolean;
}

const CHANGE_STYLES: Record<string, string> = {
  added: "bg-green-50 text-green-800 dark:bg-green-950/30 dark:text-green-300",
  updated: "bg-amber-50 text-amber-800 dark:bg-amber-950/30 dark:text-amber-300",
  removed: "bg-red-50 text-red-800 dark:bg-red-950/30 dark:text-red-300",
  unchanged: "",
};

const CHANGE_BADGE: Record<string, string> = {
  added: "bg-green-100 text-green-700 dark:bg-green-900/40",
  updated: "bg-amber-100 text-amber-700 dark:bg-amber-900/40",
  removed: "bg-red-100 text-red-700 dark:bg-red-900/40",
  unchanged: "bg-muted text-muted-foreground",
};

const CHANGE_ICON: Record<string, string> = {
  added: "+",
  updated: "↑",
  removed: "−",
  unchanged: "=",
};

const DiffPreview: React.FC<DiffPreviewProps> = ({
  diff,
  meta,
  fileName,
  onConfirm,
  onCancel,
  isConfirming,
}) => {
  const { added, updated, removed, unchanged } = diff.summary;
  const hasChanges = added + updated + removed > 0;

  // Show changed rows first, then unchanged
  const sorted = [...diff.rows].sort((a, b) => {
    const order = { added: 0, updated: 1, removed: 2, unchanged: 3 };
    return (order[a.change] ?? 4) - (order[b.change] ?? 4);
  });

  return (
    <div className="flex flex-col gap-3 h-full">
      {/* Header */}
      <div className="flex items-center gap-2">
        <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0" />
        <div>
          <p className="text-sm font-semibold">
            {fileName} validated successfully
          </p>
          {meta && (
            <p className="text-xs text-muted-foreground">
              {meta.name} · {meta.carrier_name} · slug: {meta.slug}
            </p>
          )}
        </div>
      </div>

      {/* Summary badges */}
      <div className="flex flex-wrap gap-2">
        {[
          { label: "added", count: added, key: "added" },
          { label: "updated", count: updated, key: "updated" },
          { label: "removed", count: removed, key: "removed" },
          { label: "unchanged", count: unchanged, key: "unchanged" },
        ].map(({ label, count, key }) => (
          <span
            key={key}
            className={cn("inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium", CHANGE_BADGE[key])}
          >
            <span className="font-bold">{CHANGE_ICON[key]}</span>
            {count} {label}
          </span>
        ))}
      </div>

      {/* Diff table */}
      <div className="flex-1 rounded-md border overflow-auto max-h-[400px]">
        <table className="w-full text-xs">
          <thead className="sticky top-0 bg-muted/80 backdrop-blur-sm z-10">
            <tr>
              <th className="px-2 py-1.5 text-left font-medium text-muted-foreground w-6"></th>
              <th className="px-2 py-1.5 text-left font-medium text-muted-foreground">Service</th>
              <th className="px-2 py-1.5 text-left font-medium text-muted-foreground">Zone</th>
              <th className="px-2 py-1.5 text-left font-medium text-muted-foreground">Shipment Type</th>
              <th className="px-2 py-1.5 text-right font-medium text-muted-foreground">Weight</th>
              <th className="px-2 py-1.5 text-right font-medium text-muted-foreground">Old Rate</th>
              <th className="px-2 py-1.5 text-right font-medium text-muted-foreground">New Rate</th>
              <th className="px-2 py-1.5 text-left font-medium text-muted-foreground">Status</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((row, i) => (
              <tr
                key={i}
                className={cn(
                  "border-b border-border/40 last:border-0",
                  CHANGE_STYLES[row.change]
                )}
              >
                <td className="px-2 py-1 text-center font-bold">{CHANGE_ICON[row.change]}</td>
                <td className="px-2 py-1 font-mono truncate max-w-[120px]">
                  {row.service_code ?? row.service_id}
                </td>
                <td className="px-2 py-1 font-mono truncate max-w-[100px]">
                  {row.zone_label ?? row.zone_id}
                </td>
                <td className="px-2 py-1 text-muted-foreground">{row.shipment_type}</td>
                <td className="px-2 py-1 text-right text-muted-foreground whitespace-nowrap">
                  {row.min_weight}–{row.max_weight} kg
                </td>
                <td className="px-2 py-1 text-right">
                  {row.old_rate != null ? row.old_rate.toFixed(2) : "—"}
                </td>
                <td className="px-2 py-1 text-right font-semibold">
                  {row.new_rate != null ? row.new_rate.toFixed(2) : "—"}
                </td>
                <td className="px-2 py-1">
                  <span className={cn(
                    "inline-flex rounded-full px-1.5 py-0.5 text-[10px] font-medium",
                    CHANGE_BADGE[row.change],
                  )}>
                    {row.change}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {!hasChanges && (
        <p className="text-xs text-muted-foreground italic">
          No rate changes detected — file matches the current rate sheet exactly.
        </p>
      )}

      {/* Action buttons */}
      <div className="flex items-center gap-2">
        <Button
          size="sm"
          onClick={onConfirm}
          disabled={isConfirming}
        >
          {isConfirming ? (
            <><Loader2 className="mr-2 h-3.5 w-3.5 animate-spin" />Importing…</>
          ) : (
            "Confirm Import"
          )}
        </Button>
        <Button size="sm" variant="outline" onClick={onCancel} disabled={isConfirming}>
          Cancel
        </Button>
      </div>
    </div>
  );
};
