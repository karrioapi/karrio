import { ManualShipmentStatusEnum, ShipmentStatusEnum, DocumentTemplateType, ShipmentType } from '@karrio/types';
import { useDocumentTemplates } from '@karrio/hooks/document-template';
import { ConfirmModalContext } from '../modals/confirm-modal';
import React, { useState, useRef, useContext } from 'react';
import { useShipmentMutation } from '@karrio/hooks/shipment';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { useRouter } from 'next/dist/client/router';
import { useAppMode } from '@karrio/hooks/app-mode';
import { formatRef, isNone, isNoneOrEmpty, url$ } from '@karrio/lib';


interface ShipmentMenuComponent extends React.InputHTMLAttributes<HTMLDivElement> {
  shipment: ShipmentType;
  templates?: DocumentTemplateType[];
  isViewing?: boolean;
}


export const ShipmentMenu: React.FC<ShipmentMenuComponent> = ({ shipment, isViewing }) => {
  const router = useRouter();
  const { basePath } = useAppMode();
  const { references } = useAPIMetadata();
  const mutation = useShipmentMutation();
  const trigger = useRef<HTMLDivElement>(null);
  const [isActive, setIsActive] = useState(false);
  const { confirm: confirmCancellation } = useContext(ConfirmModalContext);
  const { query: { data: { document_templates } = {} } } = useDocumentTemplates({
    related_object: "shipment",
    active: true,
  } as any);

  const handleOnClick = (e: React.MouseEvent) => {
    setIsActive(!isActive);
    if (!isActive) { document.addEventListener('click', onBodyClick); }
    else { document.removeEventListener('click', onBodyClick); }
  };
  const onBodyClick = (e: MouseEvent) => {
    if (!trigger.current?.contains(e.target as Node)) {
      setIsActive(false);
      document.removeEventListener('click', onBodyClick);
    }
  };
  const createLabel = (_: React.MouseEvent) => {
    if (!!shipment.meta?.orders) {
      router.push(`${basePath}/orders/create_label?shipment_id=${shipment.id}&order_id=${shipment.meta.orders}`)
    }
    else {
      router.push(`${basePath}/create_label?shipment_id=${shipment.id}`)
    }
  };
  const displayDetails = (_: React.MouseEvent) => {
    router.push(basePath + '/shipments/' + shipment.id);
  };
  const cancelShipment = (shipment: ShipmentType) => async () => {
    await mutation.voidLabel.mutateAsync(shipment);
  };
  const changeStatus = ({ id }: ShipmentType, status: ManualShipmentStatusEnum) => async () => {
    await mutation.changeStatus.mutateAsync({ id: shipment.id, status });
  };

  return (
    <div className={`dropdown is-right ${isActive ? 'is-active' : ''}`} key={`menu-${shipment.id}`}>

      <div className="dropdown-trigger" onClick={handleOnClick} ref={trigger}>
        <a className="button is-white is-small p-3">
          <i className={`fas fa-ellipsis-h`} aria-hidden="true"></i>
        </a>
      </div>

      <div className="dropdown-menu" id={`shipment-menu-${shipment.id}`} role="menu">
        <div className="dropdown-content">
          {isNone(shipment.label_url) && shipment.status === ShipmentStatusEnum.draft &&
            <a className="dropdown-item" onClick={createLabel}>
              <span>Buy Label</span>
            </a>}

          {!isNone(shipment.label_url) &&
            <a className="dropdown-item" href={url$`${references.HOST}/${shipment?.label_url}`}
              target="_blank" rel="noreferrer">
              <span>Print Label</span>
            </a>}

          {!isViewing &&
            <a className="dropdown-item" onClick={displayDetails}>View Shipment</a>}

          {![ShipmentStatusEnum.cancelled, ShipmentStatusEnum.delivered].includes(shipment.status as any) &&
            <a className="dropdown-item" onClick={() => confirmCancellation({
              identifier: shipment.id as string,
              label: `Cancel Shipment`,
              action: 'Submit',
              onConfirm: cancelShipment(shipment),
            })}>Cancel Shipment</a>}

          {!isNone(shipment.invoice_url) &&
            <a className="dropdown-item" href={url$`${references.HOST}/${shipment.invoice_url}`}
              target="_blank" rel="noreferrer">Print Invoice</a>}

          {(
            shipment.carrier_name &&
            isNoneOrEmpty(shipment.tracker_id) &&
            ![ShipmentStatusEnum.cancelled, ShipmentStatusEnum.delivered, ManualShipmentStatusEnum.delivery_failed].includes(shipment.status as any)
          ) && <>
              <hr className="my-1" style={{ height: '1px' }} />

              {(shipment.status === ShipmentStatusEnum.purchased) &&
                <a className="dropdown-item" onClick={() => confirmCancellation({
                  identifier: shipment.id as string,
                  label: `Mark shipment as ${formatRef(ManualShipmentStatusEnum.in_transit.toString())}`,
                  action: 'Apply',
                  onConfirm: changeStatus(shipment, ManualShipmentStatusEnum.in_transit),
                })}>Mark as {formatRef(ManualShipmentStatusEnum.in_transit.toString())}</a>}

              {([ShipmentStatusEnum.purchased, ShipmentStatusEnum.in_transit].includes(shipment.status as any)) &&
                <a className="dropdown-item" onClick={() => confirmCancellation({
                  identifier: shipment.id as string,
                  label: `Mark shipment as ${formatRef(ManualShipmentStatusEnum.needs_attention.toString())}`,
                  action: 'Save',
                  onConfirm: changeStatus(shipment, ManualShipmentStatusEnum.needs_attention),
                })}>Mark as {formatRef(ManualShipmentStatusEnum.needs_attention.toString())}</a>}

              {([ShipmentStatusEnum.purchased, ShipmentStatusEnum.in_transit, ShipmentStatusEnum.needs_attention].includes(shipment.status as any)) &&
                <a className="dropdown-item" onClick={() => confirmCancellation({
                  identifier: shipment.id as string,
                  label: `Mark shipment as ${formatRef(ManualShipmentStatusEnum.delivery_failed.toString())}`,
                  action: 'Save',
                  onConfirm: changeStatus(shipment, ManualShipmentStatusEnum.delivery_failed),
                })}>Mark as {formatRef(ManualShipmentStatusEnum.delivery_failed.toString())}</a>}

              {([ShipmentStatusEnum.purchased, ShipmentStatusEnum.in_transit, ShipmentStatusEnum.needs_attention].includes(shipment.status as any)) &&
                <a className="dropdown-item" onClick={() => confirmCancellation({
                  identifier: shipment.id as string,
                  label: `Mark shipment as ${formatRef(ManualShipmentStatusEnum.delivered.toString())}`,
                  action: 'Save',
                  onConfirm: changeStatus(shipment, ManualShipmentStatusEnum.delivered),
                })}>Mark as {formatRef(ManualShipmentStatusEnum.delivered.toString())}</a>}

            </>}

          {(document_templates?.edges || []).length > 0 &&
            <hr className="my-1" style={{ height: '1px' }} />}

          {(document_templates?.edges || []).map(({ node: template }) =>
            <a href={url$`${references.HOST}/documents/templates/${template.id}.${template.slug}?shipments=${shipment.id}`}
              className="dropdown-item" target="_blank" rel="noreferrer" key={template.id}>
              Download {template.name}
            </a>
          )}
        </div>
      </div>

    </div>
  );
};
