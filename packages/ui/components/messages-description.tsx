import { MessageType, RequestError } from '@karrio/types';
import { formatMessage } from './notifier';
import React from 'react';

interface MessagesDescriptionComponent {
  messages?: RequestError | MessageType[];
}

export const MessagesDescription: React.FC<MessagesDescriptionComponent> = ({ messages }) => {
  return (
    <React.Fragment key={Date()}>
      {formatMessage(messages as any)}
    </React.Fragment>
  );
};
