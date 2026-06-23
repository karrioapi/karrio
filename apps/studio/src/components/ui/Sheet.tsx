// Sheet.tsx — the workhorse right drawer. Build ALL detail/create/edit views on
// this. sm/md/lg widths, fullscreen, ESC/backdrop close, and accessible focus
// management: focus moves in on open, is trapped while open, restored on close,
// and the closed sheet is `inert` so it's not tab-reachable.
import { useEffect, useRef, type ReactNode } from "react";
import { Icon } from "~/components/ui/icons";

const FOCUSABLE =
  'button:not([disabled]),[href],input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

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
  const ref = useRef<HTMLElement>(null);
  const restoreTo = useRef<HTMLElement | null>(null);

  // ESC to close.
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  // Focus management + inert.
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (open) {
      restoreTo.current = (document.activeElement as HTMLElement) ?? null;
      el.inert = false;
      const focusables = el.querySelectorAll<HTMLElement>(FOCUSABLE);
      (focusables[0] ?? el).focus({ preventScroll: true });
    } else {
      el.inert = true;
      restoreTo.current?.focus?.({ preventScroll: true });
    }
  }, [open]);

  const onKeyDownTrap = (e: React.KeyboardEvent) => {
    if (e.key !== "Tab" || !ref.current) return;
    const f = Array.from(ref.current.querySelectorAll<HTMLElement>(FOCUSABLE)).filter(
      (n) => n.offsetParent !== null,
    );
    if (f.length === 0) return;
    const first = f[0];
    const last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  };

  return (
    <>
      <div
        className={"sheet-backdrop" + (open ? " open" : "")}
        style={{ pointerEvents: open ? "auto" : "none" }}
        onClick={onClose}
        data-testid="sheet-backdrop"
        aria-hidden="true"
      />
      <aside
        ref={ref}
        className={
          "sheet" +
          (size ? " " + size : "") +
          (fullscreen ? " fullscreen" : "") +
          (open ? " open" : "")
        }
        role="dialog"
        aria-modal="true"
        aria-label={typeof title === "string" ? title : crumb}
        onKeyDown={onKeyDownTrap}
        data-testid="sheet"
        tabIndex={-1}
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
              <button className="icon-btn" title="Expand" aria-label="Toggle fullscreen" onClick={onToggleFullscreen}>
                <Icon.Workspace size={14} />
              </button>
            )}
            <button className="icon-btn" title="Close" aria-label="Close" onClick={onClose} data-testid="sheet-close">
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

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      {children}
    </label>
  );
}
