// detail.tsx — reusable building blocks for Sheet detail views.
import type { ReactNode } from "react";
import { recipientAddr, recipientName } from "~/lib/karrio/display";
import type { Address } from "~/lib/karrio/types";

export function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <>
      <div className="section-head">{title}</div>
      {children}
    </>
  );
}

export function KV({ label, children, mono }: { label: string; children: ReactNode; mono?: boolean }) {
  return (
    <div>
      <div className="kv-label">{label}</div>
      <div className={"kv-value" + (mono ? " mono" : "")}>{children}</div>
    </div>
  );
}

export function KVGrid({ children }: { children: ReactNode }) {
  return <div className="kv-grid">{children}</div>;
}

export function AddressCard({ label, addr }: { label: string; addr?: Address }) {
  return (
    <div className="addr-card">
      <div className="lbl">{label}</div>
      <div className="nm">{recipientName(addr)}</div>
      <div className="ln">{recipientAddr(addr) || "—"}</div>
      {addr?.postal_code && <div className="ln">{addr.postal_code}</div>}
    </div>
  );
}

export type TimelineEvent = { what: string; where?: string; when?: string; done?: boolean };

export function Timeline({ events }: { events: TimelineEvent[] }) {
  if (events.length === 0) {
    return <div className="muted" style={{ fontSize: 12.5 }}>No tracking events yet.</div>;
  }
  return (
    <div className="timeline" data-testid="timeline">
      {events.map((ev, i) => (
        <div key={i} className={"ev" + (ev.done ? " done" : "")}>
          <div className="dot" />
          <div>
            <div className="what">{ev.what}</div>
            {ev.where && <div className="where">{ev.where}</div>}
          </div>
          {ev.when && <div className="when">{ev.when}</div>}
        </div>
      ))}
    </div>
  );
}
