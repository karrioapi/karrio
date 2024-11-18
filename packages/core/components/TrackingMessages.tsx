import React from "react";
import { TrackerType } from "@karrio/types";

interface TrackingMessagesProps {
  messages: (TrackerType["messages"] extends (infer U)[] ? U : never)[]; // Allow flexibility for undefined/null
}

const TrackingMessages: React.FC<TrackingMessagesProps> = ({ messages }) => {
  if (!messages || messages.length === 0) return null;

  return (
    <div className="notification is-warning">
      {messages.map((msg, index) => (
        <p
          key={index}
          className="is-size-7 my-1 has-text-weight-semibold has-text-grey"
        >
          {msg?.message ?? "No message available"}{" "}
          {/* Handle undefined/null message */}
        </p>
      ))}
    </div>
  );
};

export default TrackingMessages;
