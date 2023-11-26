import { MessageType, RequestError } from '@karrio/types';
import { formatMessage } from './notifier';
import React from 'react';

interface MessagesDescriptionComponent {
  messages?: RequestError | MessageType[];
}

export const MessagesDescription: React.FC<MessagesDescriptionComponent> = ({ messages }) => {
  return (
    <>
      {formatMessage(messages as any)}
    </>
  );
};
