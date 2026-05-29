// AppsScreen.tsx — Build › Apps (D1). Commerce/integration apps as tiles.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, Tabs, type TabDef } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { useApps } from "~/lib/karrio/hooks";
import type { App } from "~/lib/karrio/types";

export function AppsScreen() {
  const [tab, setTab] = useState("all");
  const [preview, setPreview] = useState<App | null>(null);
  const { data, isLoading, isError, error } = useApps();
  const all = useMemo(() => data?.results ?? [], [data]);
  const rows = useMemo(
    () => (tab === "installed" ? all.filter((a) => a.installed) : tab === "available" ? all.filter((a) => !a.installed) : all),
    [all, tab],
  );
  const tabs: TabDef[] = [
    { id: "all", label: "All", count: all.length },
    { id: "installed", label: "Installed", count: all.filter((a) => a.installed).length },
    { id: "available", label: "Available", count: all.filter((a) => !a.installed).length },
  ];

  return (
    <div className="page" data-testid="screen-apps">
      <PageHeader title="Apps" actions={<button className="btn"><Icon.External size={14} /> Browse marketplace</button>} />
      <Tabs tabs={tabs} value={tab} onChange={setTab} />
      {isLoading && <div className="state-row" data-testid="state-loading">Loading apps…</div>}
      {isError && !isLoading && <div className="state-row" data-testid="state-error">{(error as Error)?.message ?? "Failed to load"}</div>}
      {!isLoading && !isError && rows.length === 0 && <div className="state-row" data-testid="state-empty">No apps.</div>}
      <div className="tile-grid">
        {rows.map((a) => (
          <button key={a.id} className="tile" onClick={() => setPreview(a)} data-testid={`app-tile-${a.id}`}>
            <div className="tile-head">
              <div className="tile-logo">{a.name.charAt(0)}</div>
              <div style={{ flex: 1 }}>
                <div className="tile-name">{a.name}</div>
                <div className="tile-vendor">{a.vendor ?? ""}</div>
              </div>
              {a.installed ? <span className="tag installed">installed</span> : a.badge ? <span className={`tag ${a.badge}`}>{a.badge}</span> : null}
            </div>
            <div className="tile-desc">{a.description}</div>
            <div className="tile-foot">{a.status ?? (a.installed ? "connected" : "not installed")}</div>
          </button>
        ))}
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Apps" title={preview.name} id={preview.id}
          footer={<><div style={{ flex: 1 }} /><button className="btn btn-primary">{preview.installed ? "Configure" : "Install"}</button></>}>
          <div className="sheet-body-pad" data-testid="app-sheet-body">
            <Section title="About">
              <p className="muted" style={{ fontSize: 12.5 }}>{preview.description}</p>
              <KVGrid>
                <KV label="Vendor">{preview.vendor ?? "—"}</KV>
                <KV label="Status">{preview.status ?? (preview.installed ? "connected" : "not installed")}</KV>
              </KVGrid>
            </Section>
          </div>
        </Sheet>
      )}
    </div>
  );
}
