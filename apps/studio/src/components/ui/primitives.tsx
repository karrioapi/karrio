// primitives.tsx — small, reusable UI building blocks shared across screens.
import type { ReactNode } from "react";
import { Icon } from "~/components/ui/icons";
import { statusClass, statusLabel } from "~/lib/karrio/display";

/* ---------- Page header ---------- */
export function PageHeader({ title, actions }: { title: string; actions?: ReactNode }) {
  return (
    <div className="page-header">
      <h1 className="page-title">{title}</h1>
      {actions && <div className="page-actions">{actions}</div>}
    </div>
  );
}

/* ---------- Status pill ---------- */
export function StatusPill({ status }: { status?: string }) {
  return <span className={"pill " + statusClass(status)}>{statusLabel(status)}</span>;
}

/* ---------- Tabs (with counts) ---------- */
export type TabDef = { id: string; label: string; count?: number };

export function Tabs({
  tabs,
  value,
  onChange,
}: {
  tabs: TabDef[];
  value: string;
  onChange: (id: string) => void;
}) {
  return (
    <div className="tabs" role="tablist">
      {tabs.map((t) => (
        <button
          key={t.id}
          role="tab"
          aria-selected={value === t.id}
          className={"tab" + (value === t.id ? " active" : "")}
          onClick={() => onChange(t.id)}
          data-testid={`tab-${t.id}`}
        >
          {t.label}
          {t.count != null && <span className="count">{t.count}</span>}
        </button>
      ))}
    </div>
  );
}

/* ---------- Filter toolbar ---------- */
export function FilterToolbar({ children }: { children: ReactNode }) {
  return <div className="table-toolbar">{children}</div>;
}

export function FilterPill({ children }: { children: ReactNode }) {
  return <button className="filter-pill">{children}</button>;
}

/* ---------- Checkbox ---------- */
export function Checkbox({
  checked,
  onChange,
  testid,
}: {
  checked: boolean;
  onChange: () => void;
  testid?: string;
}) {
  return (
    <span
      className={"checkbox" + (checked ? " checked" : "")}
      onClick={(e) => {
        e.stopPropagation();
        onChange();
      }}
      data-testid={testid}
    >
      {checked && <Icon.Check size={12} style={{ color: "white" }} />}
    </span>
  );
}

/* ---------- Table state rows (loading / error / empty) ---------- */
export function StateRow({
  colSpan,
  kind,
  message,
}: {
  colSpan: number;
  kind: "loading" | "error" | "empty";
  message: string;
}) {
  return (
    <tr>
      <td colSpan={colSpan}>
        <div className="state-row" data-testid={`state-${kind}`}>
          {message}
        </div>
      </td>
    </tr>
  );
}

/* ---------- Table footer (pagination) ---------- */
export function TableFooter({
  shown,
  total,
  noun,
  onPrev,
  onNext,
  hasPrev,
  hasNext,
}: {
  shown: number;
  total: number;
  noun: string;
  onPrev?: () => void;
  onNext?: () => void;
  hasPrev?: boolean;
  hasNext?: boolean;
}) {
  return (
    <div className="table-footer">
      <span>
        Viewing 1–{shown} of {total} {noun}
      </span>
      <div className="right">
        <button className="btn btn-sm" disabled={!hasPrev} onClick={onPrev}>
          <Icon.ChevronL size={12} /> Previous
        </button>
        <button className="btn btn-sm" disabled={!hasNext} onClick={onNext}>
          Next <Icon.ChevronR size={12} />
        </button>
      </div>
    </div>
  );
}
