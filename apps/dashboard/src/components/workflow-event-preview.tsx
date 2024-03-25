import { ModalFormProps, useModal } from '@karrio/ui/modals/modal';
import { Component } from '@/modules/Workflows/event';
import React from 'react';

type EventPreviewModalProps = {
  eventId?: string;
};

export const WorkflowPreviewModal: React.FC<ModalFormProps<EventPreviewModalProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const ModalComponent: React.FC<EventPreviewModalProps> = props => {
    const { eventId } = props;

    return (
      <section className="modal-card-body px-5 pt-0 pb-6">
        <Component eventId={eventId} />
      </section>
    )
  };

  return React.cloneElement(trigger, {
    onClick: () => modal.open(
      <ModalComponent {...args} />,
      { className: 'is-medium-modal', backgroundDismiss: true }
    )
  });
};