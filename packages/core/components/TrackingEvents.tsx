// components/TrackingEvents.tsx
import { TrackingEvent, TrackingStatus } from "@karrio/types/rest/api";
import { formatDayDate } from "@karrio/lib";
import { TrackerType } from "@karrio/types";

type DayEvents = { [k: string]: TrackingEvent[] };

const computeEvents = (tracker: TrackingStatus): DayEvents => {
  const days: DayEvents = {};

  (tracker?.events || []).forEach((event: TrackingEvent) => {
    const daydate = formatDayDate(event.date as string);

    if (!days[daydate]) {
      days[daydate] = [];
    }

    days[daydate].push(event);
  });

  return days;
};


const TrackingEvents: React.FC<{ tracker: TrackerType }> = ({ tracker }) => {
  const eventsByDay = computeEvents(tracker as TrackingStatus);

  return (
    <div className="my-6">
      <aside className="menu">
        <ul className="menu-list mb-5" style={{ maxWidth: "28rem" }}>
          {Object.entries(eventsByDay).map(([day, events], index) => (
            <li key={index}>
              <p className="menu-label is-size-6 is-capitalized">{day}</p>
              {events.map((event, index) => (
                <ul key={index}>
                  <li className="my-2">
                    <code>{event.time}</code>
                    <span className="is-subtitle is-size-7 my-1 has-text-weight-semibold">
                      {event.location}
                    </span>
                  </li>
                  <li className="my-2">
                    <span className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                      {event.description}
                    </span>
                  </li>
                </ul>
              ))}
            </li>
          ))}
        </ul>
      </aside>
    </div>
  );
};

export default TrackingEvents;
