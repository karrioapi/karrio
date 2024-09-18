// components/TrackingEvents.tsx
import { TrackingEvent, TrackingStatus } from "@karrio/types/rest/api";
import { formatDayDate } from "@karrio/lib";

type DayEvents = { [k: string]: TrackingEvent[] };

const computeEvents = (tracker: TrackingStatus): DayEvents => {
  return (tracker?.events || []).reduce((days, event: TrackingEvent) => {
    const daydate = formatDayDate(event.date as string);
    return { ...days, [daydate]: [...(days[daydate] || []), event] };
  }, {} as DayEvents);
};

const TrackingEvents: React.FC<{ tracker: TrackingStatus }> = ({ tracker }) => {
  const eventsByDay = computeEvents(tracker);

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
