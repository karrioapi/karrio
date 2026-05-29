// Sheet.tsx — the workhorse right drawer. Build ALL detail/create/edit views
// on this. Supports sm/md/lg widths, fullscreen expand, ESC/backdrop close.
import { useEffect, type ReactNode } from "react";
import { Icon } from "~/components/ui/icons";

export type SheetProps = {
  open: boolean;
  onClose: () => void;
  size?: "sm" | "md" | "lg";
  fullscreen?: boolean;
  onToggleFullscreen?: () => void;
  crumb?: string;
  title?: ReactNode;
  id?: string;
  headRight?: ReactNode;
  footer?: ReactNode;
  children?: ReactNode;
};

export function Sheet({
  open,
  onClose,
  size,
  fullscreen,
  onToggleFullscreen,
  crumb,
  title,
  id,
  headRight,
  footer,
  children,
}: SheetProps) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  return (
    <>
      <div
        className={"sheet-backdrop" + (open ? " open" : "")}
        style={{ pointerEvents: open ? "auto" : "none" }}
        onClick={onClose}
        data-testid="sheet-backdrop"
      />
      <aside
        className={
          "sheet" +
          (size ? " " + size : "") +
          (fullscreen ? " fullscreen" : "") +
          (open ? " open" : "")
        }
        role="dialog"
        aria-modal="true"
        aria-hidden={!open}
        data-testid="sheet"
      >
        <div className="sheet-head">
          <div style={{ minWidth: 0 }}>
            {crumb && <div className="sheet-crumb">{crumb}</div>}
            {title && <div className="sheet-title">{title}</div>}
            {id && <div className="sheet-id">{id}</div>}
          </div>
          <div className="sheet-head-right">
            {headRight}
            {onToggleFullscreen && (
              <button className="icon-btn" title="Expand" onClick={onToggleFullscreen}>
                <Icon.Workspace size={14} />
              </button>
            )}
            <button className="icon-btn" title="Close" onClick={onClose} data-testid="sheet-close">
              <Icon.X size={14} />
            </button>
          </div>
        </div>
        <div className="sheet-body">{children}</div>
        {footer && <div className="sheet-foot">{footer}</div>}
      </aside>
    </>
  );
}

export function Field({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      {children}
    </label>
  );
}
