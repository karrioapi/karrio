import { ModalFormProps, useModal } from "@karrio/ui/modals/modal";
import { Component } from "@karrio/core/modules/Workflows/event";
import React from "react";

type EventPreviewModalProps = {
  eventId: string;
};

export const WorkflowPreviewModal = ({
  trigger,
  ...args
}: ModalFormProps<EventPreviewModalProps>): JSX.Element => {
  const modal = useModal();

  const ModalComponent = ({ eventId }: EventPreviewModalProps): JSX.Element => {
    return (
      <section className="modal-card-body px-5 pt-0 pb-6">
        <Component eventId={eventId} isPreview />
      </section>
    );
  };

  return React.cloneElement(
    trigger as React.ReactElement,
    {
      onClick: () =>
        modal.open(<ModalComponent {...args} />, {
          className: "is-medium-modal",
          backgroundDismiss: true,
        }),
    } as any,
  );
};
