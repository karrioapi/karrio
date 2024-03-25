import { DocumentTemplateType, OrderType, OrderStatusEnum } from '@karrio/types';
import { useDocumentTemplates } from '@karrio/hooks/document-template';
import { ConfirmModalContext } from '../modals/confirm-modal';
import React, { useState, useRef, useContext } from 'react';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { useRouter } from 'next/dist/client/router';
import { useOrderMutation } from '@karrio/hooks/order';
import { useAppMode } from '@karrio/hooks/app-mode';
import { AppLink } from './app-link';
import { url$ } from '@karrio/lib';


interface OrderMenuComponent extends React.InputHTMLAttributes<HTMLDivElement> {
  order: OrderType;
  templates?: DocumentTemplateType[];
  isViewing?: boolean;
}

export const OrderMenu: React.FC<OrderMenuComponent> = ({ order, isViewing }) => {
  const router = useRouter();
  const { basePath } = useAppMode();
  const { references } = useAPIMetadata();
  const mutation = useOrderMutation();
  const trigger = useRef<HTMLDivElement>(null);
  const [isActive, setIsActive] = useState(false);
  const { confirm: confirmCancellation } = useContext(ConfirmModalContext);
  const { query: { data: { document_templates } = {} } } = useDocumentTemplates({
    related_object: "order",
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
  const displayDetails = (_: React.MouseEvent) => {
    router.push(basePath + '/orders/' + order.id);
  };
  const cancelOrder = (order: OrderType) => async () => {
    await mutation.cancelOrder.mutateAsync(order);
  };
  const computeShipmentId = (order: OrderType) => {
    return order.shipments.find(s => s.status === "draft")?.id || 'new';
  };

  return (
    <div className={`dropdown is-right ${isActive ? 'is-active' : ''}`} key={`menu-${order.id}`}>

      <div className="dropdown-trigger" onClick={handleOnClick} ref={trigger}>
        <a className="button is-white is-small p-3">
          <i className={`fas fa-ellipsis-h`} aria-hidden="true"></i>
        </a>
      </div>

      <div className="dropdown-menu" id={`order-menu-${order.id}`} role="menu">
        <div className="dropdown-content">

          {["unfulfilled", "partial"].includes(order?.status) && <>
            <AppLink className="dropdown-item" href={`/orders/create_label?shipment_id=${computeShipmentId(order)}&order_id=${order?.id}`}>
              <span>Create label</span>
            </AppLink>
          </>}

          {(order.shipments.filter(s => !["cancelled", "draft"].includes(s.status)).length > 0) && <>
            <a
              href={url$`${references.HOST}/documents/orders/label.${order.shipments.filter(s => !["cancelled", "draft"].includes(s.status))[0].label_type}?orders=${order.id}`}
              className={`dropdown-item`} target="_blank" rel="noreferrer">
              <span>{`Print Label${(order.shipments.filter(s => !["cancelled", "draft"].includes(s.status)).length > 1) ? 's' : ''}`}</span>
            </a>
          </>}

          {!isViewing && <a className="dropdown-item" onClick={displayDetails}>
            <span>View order</span>
          </a>}

          {(order.source === "draft" && order.shipments.length === 0) && <>
            <AppLink className="dropdown-item" href={`/draft_orders/${order?.id}`}>
              <span>Edit order</span>
            </AppLink>
            <a className="dropdown-item" onClick={() => confirmCancellation({
              identifier: order.id as string, label: `Delete order`, action: 'Submit',
              onConfirm: () => mutation.deleteOrder.mutateAsync({ id: order.id }),
            })}>
              <span>Delete order</span>
            </a>
          </>}

          {order.status === OrderStatusEnum.Unfulfilled && <>
            <a className="dropdown-item" onClick={() => confirmCancellation({
              identifier: order.id as string, label: `Cancel order`, action: 'Submit',
              onConfirm: cancelOrder(order),
            })}>
              <span>Cancel order</span>
            </a>
          </>}

          {((document_templates?.edges || []).length > 0 && !["fulfilled", "partial", "delivered", "cancelled"].includes(order?.status)) && <>
            <hr className="my-1" style={{ height: '1px' }} />
          </>}

          {(document_templates?.edges || []).map(({ node: template }) =>
            <a href={url$`${references.HOST}/documents/templates/${template.id}.${template.slug}?orders=${order.id}`}
              className="dropdown-item" target="_blank" rel="noreferrer" key={template.id}>
              <span>Download {template.name}</span>
            </a>
          )}
        </div>
      </div>

    </div>
  );
};
