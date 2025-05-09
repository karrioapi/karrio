import { MessageType, RequestError } from "@karrio/types";
import { formatMessage } from "./notifier";
import React from "react";

interface MessagesDescriptionComponent {
  messages?: RequestError | MessageType[];
}

export const MessagesDescription = ({
  messages,
}: MessagesDescriptionComponent): JSX.Element => {
  return (
    <React.Fragment key={Date()}>
      {formatMessage(messages as any)}
    </React.Fragment>
  );
};
