// CommandPalette.tsx — ⌘K overlay: navigate + run actions.
import { useEffect, useMemo, useRef, useState } from "react";
import { NAV, type Mode } from "~/lib/modes";

export type Command = {
  id: string;
  label: string;
  kind: string;
  run: () => void;
};

export function CommandPalette({
  open,
  onClose,
  onGo,
  onAction,
}: {
  open: boolean;
  onClose: () => void;
  onGo: (route: string) => void;
  onAction: (id: string) => void;
}) {
  const [q, setQ] = useState("");
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const commands = useMemo<Command[]>(() => {
    const navCmds: Command[] = (Object.keys(NAV) as Mode[]).flatMap((mode) =>
      NAV[mode].flatMap((g) =>
        g.items.map((it) => ({
          id: `nav:${it.route}`,
          label: it.label,
          kind: mode,
          run: () => onGo(it.route),
        })),
      ),
    );
    const actions: Command[] = [
      { id: "new-shipment", label: "New shipment", kind: "action", run: () => onAction("shipment") },
      { id: "track", label: "Track a shipment", kind: "action", run: () => onAction("tracker") },
      { id: "toggle-theme", label: "Toggle theme", kind: "action", run: () => onAction("theme") },
      { id: "workbench", label: "Open Workbench", kind: "action", run: () => onAction("workbench") },
    ];
    // De-dupe nav routes that appear in multiple groups by id.
    const seen = new Set<string>();
    return [...navCmds, ...actions].filter((c) => (seen.has(c.id) ? false : (seen.add(c.id), true)));
  }, [onGo, onAction]);

  const filtered = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return commands;
    return commands.filter((c) => c.label.toLowerCase().includes(s) || c.kind.includes(s));
  }, [q, commands]);

  useEffect(() => {
    if (open) {
      setQ("");
      setActive(0);
      requestAnimationFrame(() => inputRef.current?.focus());
    }
  }, [open]);

  useEffect(() => setActive(0), [q]);

  if (!open) return null;

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") return onClose();
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((a) => Math.min(a + 1, filtered.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((a) => Math.max(a - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      filtered[active]?.run();
      onClose();
    }
  };

  return (
    <div className="cp-backdrop" onClick={onClose} data-testid="command-palette">
      <div className="cp" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="Command palette">
        <input
          ref={inputRef}
          className="cp-input"
          placeholder="Search screens and actions…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={onKeyDown}
          data-testid="cp-input"
          aria-label="Command palette search"
        />
        <div className="cp-list" data-testid="cp-list">
          {filtered.length === 0 && <div className="cp-empty">No results</div>}
          {filtered.map((c, i) => (
            <div
              key={c.id}
              className={"cp-item" + (i === active ? " active" : "")}
              onMouseEnter={() => setActive(i)}
              onClick={() => {
                c.run();
                onClose();
              }}
              data-testid={`cp-item-${c.id}`}
            >
              <span>{c.label}</span>
              <span className="cp-kind">{c.kind}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
