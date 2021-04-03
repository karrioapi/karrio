import React, { useContext, useEffect } from 'react';
import { View } from '@/library/types';
import CarrierBadge from '@/components/carrier-badge';
import { TrackingEvent, TrackingStatus } from '@/api';
import TrackShipmentModal from '@/components/track-shipment-modal';
import { isNone } from '@/library/helper';
import { Trackers } from '@/components/data/trackers-query';
import TrackerMutation from '@/components/data/tracker-mutation';
import { Loading } from '@/components/loader';


interface TrackersView extends View {}

const TrackersPage: React.FC<TrackersView> = TrackerMutation<TrackersView>(({ removeTracker }) => {
  const { setLoading } = useContext(Loading);
  const { called, loading, results, load, loadMore, next, previous, refetch } = useContext(Trackers);

  const update = () => refetch && refetch();
  const remove = (tracker: TrackingStatus) => async () => {
    await removeTracker(tracker.id as string);
    update();
  };

  useEffect(() => { !loading && load(); }, []);
  useEffect(() => { setLoading(loading); });

  return (
    <>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Trackers</span>
        {called && <TrackShipmentModal className="button is-success is-pulled-right" onUpdate={update}>
          <span>Track a Shipment</span>
        </TrackShipmentModal>}
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <thead className="trackers-table">
            <tr>
              <th className="tracking-number">Tracking No</th>
              <th className="status">status</th>
              <th className="carrier">Carrier</th>
              <th className="last-event">Last Event</th>
            </tr>
          </thead>

          <tbody>

            {results.map(tracker => (
              <tr key={tracker.id}>
                <td><span className="is-subtitle is-size-6 has-text-weight-semibold has-text-grey">{tracker.tracking_number}</span></td>
                <td>
                  <span className={`tag ${statusColor(tracker)}`}>{formatSatus(tracker)}</span>
                </td>
                <td>
                  <CarrierBadge carrier={tracker.carrier_name} className="tag" />
                </td>
                <td>
                  <span className="is-subtitle is-size-7 has-text-weight-semibold text-wrapped">{formatEventDescription((tracker.events || [])[0])}</span><br/>
                  <span className="is-subtitle is-size-7 has-text-weight-semibold has-text-grey">{formatEventDate((tracker.events || [])[0])}</span>
                </td>
              </tr>
            ))}

          </tbody>

        </table>
      </div>

      {(!loading && results.length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No shipment trackers created yet.</p>
          <p>Use the <strong>API</strong> to track your first shipment.</p>
        </div>

      </div>}

      {loading && <div className="card my-6">

        <div className="card-content has-text-centered">
          <span className="icon has-text-info is-large">
            <i className="fas fa-spinner fa-pulse"></i>
          </span>
        </div>

      </div>}

      <footer className="px-2 py-2 is-vcentered">
        <div className="buttons has-addons is-centered">
          <button className="button is-small" onClick={() => loadMore(previous)} disabled={isNone(previous)}>
            <span>Previous</span>
          </button>
          <button className="button is-small" onClick={() => loadMore(next)} disabled={isNone(next)}>
            <span>Next</span>
          </button>
        </div>
      </footer>

    </>
  );
});

function statusColor(tracker: TrackingStatus): string {
  if (tracker.delivered) return 'is-success';
  return 'is-info';
}

function formatSatus(tracker: TrackingStatus): string {
  if (tracker.delivered) return 'Delivered';
  return 'In Transit';
}

function formatEventDescription(last_event?: TrackingEvent): string {
  return last_event?.description || '';
}

function formatEventDate(last_event?: TrackingEvent): string {
  if (isNone(last_event)) return '';

  return [
    last_event?.date,
    last_event?.time
  ].filter(a => !isNone(a) && a !== "").join(" ");
}

export default TrackersPage;