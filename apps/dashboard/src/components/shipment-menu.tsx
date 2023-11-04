import { ManualShipmentStatusEnum, ShipmentStatusEnum } from 'karrio/graphql';
import { useDocumentTemplates } from '@/context/document-template';
import { DocumentTemplateType, ShipmentType } from '@/lib/types';
import { ConfirmModalContext } from '@/components/confirm-modal';
import React, { useState, useRef, useContext } from 'react';
import { useShipmentMutation } from '@/context/shipment';
import { useAPIMetadata } from '@/context/api-metadata';
import { useRouter } from 'next/dist/client/router';
import { useAppMode } from '@/context/app-mode';
import { isNone, url$ } from '@/lib/helper';


interface ShipmentMenuComponent extends React.InputHTMLAttributes<HTMLDivElement> {
  shipment: ShipmentType;
  templates?: DocumentTemplateType[];
  isViewing?: boolean;
}


const ShipmentMenu: React.FC<ShipmentMenuComponent> = ({ shipment, isViewing }) => {
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
    router.push(basePath + '/create_label?shipment_id=' + shipment.id);
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
            !(shipment!.carrier_name in (references.carriers || {})) &&
            ![ShipmentStatusEnum.cancelled, ShipmentStatusEnum.delivered].includes(shipment.status as any)
          ) && <>
              <hr className="my-1" style={{ height: '1px' }} />

              {(shipment.status === ShipmentStatusEnum.purchased) &&
                <a className="dropdown-item" onClick={() => confirmCancellation({
                  identifier: shipment.id as string,
                  label: `Mark shipment as ${ManualShipmentStatusEnum.in_transit}`,
                  action: 'Apply',
                  onConfirm: changeStatus(shipment, ManualShipmentStatusEnum.in_transit),
                })}>Mark as {ManualShipmentStatusEnum.in_transit}</a>}

              {([ShipmentStatusEnum.purchased, ShipmentStatusEnum.in_transit].includes(shipment.status as any)) &&
                <a className="dropdown-item" onClick={() => confirmCancellation({
                  identifier: shipment.id as string,
                  label: `Mark shipment as ${ManualShipmentStatusEnum.delivered}`,
                  action: 'Save',
                  onConfirm: changeStatus(shipment, ManualShipmentStatusEnum.delivered),
                })}>Mark as {ManualShipmentStatusEnum.delivered}</a>}

            </>}

          {(document_templates?.edges || []).length > 0 &&
            <hr className="my-1" style={{ height: '1px' }} />}

          {(document_templates?.edges || []).map(({ node: template }) =>
            <a href={url$`${references.HOST}/documents/${template.id}.${template.slug}?shipments=${shipment.id}`}
              className="dropdown-item" target="_blank" rel="noreferrer" key={template.id}>
              Download {template.name}
            </a>
          )}
        </div>
      </div>

    </div>
  );
};

export default ShipmentMenu;
