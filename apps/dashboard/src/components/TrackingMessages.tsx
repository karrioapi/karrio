// components/TrackingMessages.tsx
import React from "react";
import { TrackerType } from "@karrio/types";

interface TrackingMessagesProps {
  messages: TrackerType["messages"];
}

const TrackingMessages: React.FC<TrackingMessagesProps> = ({ messages }) => {
  if (!messages || messages.length === 0) return null;

  return (
    <div className="notification is-warning">
      <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">
        {messages[0]?.message}
      </p>
    </div>
  );
};

export default TrackingMessages;
