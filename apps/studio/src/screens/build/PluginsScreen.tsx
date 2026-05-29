// PluginsScreen.tsx — Build › Plugins (D2). Carrier/address/rule plugins as tiles.
import { useMemo, useState } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, Tabs, type TabDef } from "~/components/ui/primitives";
import { KV, KVGrid, Section } from "~/components/ui/detail";
import { Sheet } from "~/components/ui/Sheet";
import { usePlugins } from "~/lib/karrio/hooks";
import type { Plugin } from "~/lib/karrio/types";

export function PluginsScreen() {
  const [tab, setTab] = useState("all");
  const [preview, setPreview] = useState<Plugin | null>(null);
  const { data, isLoading, isError, error } = usePlugins();
  const all = useMemo(() => data?.results ?? [], [data]);
  const has = (p: Plugin, t: string) => (p.tags ?? []).some((x) => x.toLowerCase() === t);
  const rows = useMemo(() => {
    if (tab === "all") return all;
    if (tab === "installed") return all.filter((p) => p.installed);
    return all.filter((p) => has(p, tab));
  }, [all, tab]);
  const tabs: TabDef[] = [
    { id: "all", label: "All", count: all.length },
    { id: "installed", label: "Installed", count: all.filter((p) => p.installed).length },
    { id: "carrier", label: "Carriers", count: all.filter((p) => has(p, "carrier")).length },
    { id: "address", label: "Address", count: all.filter((p) => has(p, "address")).length },
    { id: "rules", label: "Rules", count: all.filter((p) => has(p, "rules")).length },
  ];

  return (
    <div className="page" data-testid="screen-plugins">
      <PageHeader title="Plugins" actions={<button className="btn btn-primary"><Icon.Code size={14} /> Build your own</button>} />
      <Tabs tabs={tabs} value={tab} onChange={setTab} />
      {isLoading && <div className="state-row" data-testid="state-loading">Loading plugins…</div>}
      {isError && !isLoading && <div className="state-row" data-testid="state-error">{(error as Error)?.message ?? "Failed to load"}</div>}
      {!isLoading && !isError && rows.length === 0 && <div className="state-row" data-testid="state-empty">No plugins.</div>}
      <div className="tile-grid">
        {rows.map((p) => (
          <button key={p.id} className="tile" onClick={() => setPreview(p)} data-testid={`plugin-tile-${p.id}`}>
            <div className="tile-head">
              <div className="tile-logo">{p.name.charAt(0)}</div>
              <div style={{ flex: 1 }}>
                <div className="tile-name">{p.name}</div>
                <div className="tile-vendor">{p.vendor ?? ""}</div>
              </div>
              {p.installed ? <span className="tag installed">installed</span> : p.badge ? <span className={`tag ${p.badge}`}>{p.badge}</span> : null}
            </div>
            <div className="tile-desc">{p.description}</div>
            <div className="tile-foot">{(p.tags ?? []).join(" · ")}{p.version ? ` · v${p.version}` : ""}</div>
          </button>
        ))}
      </div>

      {preview && (
        <Sheet open onClose={() => setPreview(null)} size="md" crumb="Plugins" title={preview.name} id={preview.id}
          footer={<><div style={{ flex: 1 }} /><button className="btn btn-primary">{preview.installed ? "Manage" : "Install"}</button></>}>
          <div className="sheet-body-pad" data-testid="plugin-sheet-body">
            <Section title="About">
              <p className="muted" style={{ fontSize: 12.5 }}>{preview.description}</p>
              <KVGrid>
                <KV label="Vendor">{preview.vendor ?? "—"}</KV>
                <KV label="Version" mono>{preview.version ?? "—"}</KV>
              </KVGrid>
            </Section>
            {preview.tags && preview.tags.length > 0 && (
              <Section title="Capabilities">
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {preview.tags.map((t) => <span key={t} className="tag">{t}</span>)}
                </div>
              </Section>
            )}
          </div>
        </Sheet>
      )}
    </div>
  );
}
