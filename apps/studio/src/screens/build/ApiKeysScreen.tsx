// ApiKeysScreen.tsx — Build › API keys (D7).
import { useMemo } from "react";
import { Icon } from "~/components/ui/icons";
import { PageHeader, StateRow, TableFooter } from "~/components/ui/primitives";
import { useApiKeys } from "~/lib/karrio/hooks";

export function ApiKeysScreen() {
  const { data, isLoading, isError, error } = useApiKeys();
  const rows = useMemo(() => data?.results ?? [], [data]);

  return (
    <div className="page" data-testid="screen-apikeys">
      <PageHeader title="API keys" actions={<button className="btn btn-primary"><Icon.Plus size={14} /> Generate key</button>} />
      <div className="card card-scroll">
        <table className="table">
          <thead><tr><th>Label</th><th>Key</th><th>Mode</th><th>Created</th><th className="actions-cell" /></tr></thead>
          <tbody>
            {isLoading && <StateRow colSpan={5} kind="loading" message="Loading API keys…" />}
            {isError && !isLoading && <StateRow colSpan={5} kind="error" message={(error as Error)?.message ?? "Failed to load"} />}
            {!isLoading && !isError && rows.length === 0 && <StateRow colSpan={5} kind="empty" message="No API keys yet." />}
            {rows.map((k) => (
              <tr key={k.id} data-testid={`apikey-row-${k.id}`}>
                <td className="recipient-name">{k.label ?? "Default"}</td>
                <td className="mono" style={{ fontSize: 12 }}>{k.key}</td>
                <td><span className={"pill " + (k.test_mode ? "draft" : "purchased")}>{k.test_mode ? "test" : "live"}</span></td>
                <td className="muted" style={{ fontSize: 12 }}>{k.created ?? "—"}</td>
                <td className="actions-cell"><span className="icon-action"><Icon.Dots size={14} /></span></td>
              </tr>
            ))}
          </tbody>
        </table>
        <TableFooter shown={rows.length} total={data?.count ?? rows.length} noun="keys" />
      </div>
    </div>
  );
}
