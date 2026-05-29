// TrackerSheet.tsx — right-drawer detail view for a tracker (C3).
import { useState } from "react";
import { Sheet } from "~/components/ui/Sheet";
import { KV, KVGrid, Section, Timeline, type TimelineEvent } from "~/components/ui/detail";
import { StatusPill } from "~/components/ui/primitives";
import { CARRIERS, CarrierLogo } from "~/components/ui/CarrierLogo";
import { carrierKey } from "~/lib/karrio/display";
import type { Tracker } from "~/lib/karrio/types";

export function TrackerSheet({ tracker, onClose }: { tracker: Tracker | null; onClose: () => void }) {
  const [fullscreen, setFullscreen] = useState(false);
  if (!tracker) return null;

  const carrier = CARRIERS[carrierKey(tracker.carrier_name)]?.name ?? tracker.carrier_name ?? "—";
  const events: TimelineEvent[] = (tracker.events ?? []).map((e, i) => ({
    what: e.description ?? "Event",
    where: e.location,
    when: [e.date, e.time].filter(Boolean).join(" "),
    done: i > 0 || tracker.status === "delivered",
  }));

  return (
    <Sheet
      open={!!tracker}
      onClose={onClose}
      size="md"
      fullscreen={fullscreen}
      onToggleFullscreen={() => setFullscreen((v) => !v)}
      crumb="Trackers"
      title={tracker.tracking_number}
      id={tracker.id}
      headRight={<StatusPill status={tracker.status} />}
    >
      <div className="sheet-body-pad" data-testid="tracker-sheet-body">
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
          <CarrierLogo carrier={carrierKey(tracker.carrier_name)} size="lg" />
          <div>
            <div style={{ fontSize: 18, fontWeight: 600, fontFamily: "var(--font-mono)" }}>{tracker.tracking_number}</div>
            <div className="muted" style={{ fontSize: 12 }}>{carrier}</div>
          </div>
        </div>

        <Section title="Details">
          <KVGrid>
            <KV label="Tracking #" mono>{tracker.tracking_number}</KV>
            <KV label="Carrier">{carrier}</KV>
            <KV label="Estimated delivery">{tracker.estimated_delivery ?? "—"}</KV>
            <KV label="Tracker ID" mono>{tracker.id}</KV>
          </KVGrid>
        </Section>

        <Section title="Tracking timeline">
          <Timeline events={events} />
        </Section>
      </div>
    </Sheet>
  );
}
