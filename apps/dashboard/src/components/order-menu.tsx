import { useDocumentTemplates } from '@/context/document-template';
import { ConfirmModalContext } from '@/components/confirm-modal';
import { DocumentTemplateType, OrderType } from '@/lib/types';
import React, { useState, useRef, useContext } from 'react';
import { useAPIMetadata } from '@/context/api-metadata';
import { useRouter } from 'next/dist/client/router';
import { useOrderMutation } from '@/context/order';
import { useAppMode } from '@/context/app-mode';
import { OrderStatusEnum } from '@karrio/rest';
import AppLink from '@/components/app-link';
import { url$ } from '@/lib/helper';


interface OrderMenuComponent extends React.InputHTMLAttributes<HTMLDivElement> {
  order: OrderType;
  templates?: DocumentTemplateType[];
  isViewing?: boolean;
}

const OrderMenu: React.FC<OrderMenuComponent> = ({ order, isViewing }) => {
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

  return (
    <div className={`dropdown is-right ${isActive ? 'is-active' : ''}`} key={`menu-${order.id}`}>

      <div className="dropdown-trigger" onClick={handleOnClick} ref={trigger}>
        <a className="button is-white is-small p-3">
          <i className={`fas fa-ellipsis-h`} aria-hidden="true"></i>
        </a>
      </div>

      <div className="dropdown-menu" id={`order-menu-${order.id}`} role="menu">
        <div className="dropdown-content">

          {["unfulfilled", "partial"].includes(order?.status) &&
            <AppLink className="dropdown-item"
              href={`/orders/create_shipment?shipment_id=new&order_id=${order?.id}`}>
              <span>Create shipment</span>
            </AppLink>}

          {!isViewing &&
            <a className="dropdown-item" onClick={displayDetails}>View Order</a>}

          {order.status === OrderStatusEnum.Unfulfilled &&
            <a className="dropdown-item" onClick={() => confirmCancellation({
              identifier: order.id as string,
              label: `Cancel Order`,
              action: 'Submit',
              onConfirm: cancelOrder(order),
            })}>Cancel Order</a>}

          {((document_templates?.edges || []).length > 0 && !["fulfilled", "delivered", "cancelled"].includes(order?.status)) &&
            <hr className="my-1" style={{ height: '1px' }} />}

          {(document_templates?.edges || []).map(({ node: template }) =>
            <a href={url$`${references.HOST}/documents/${template.id}.${template.slug}?orders=${order.id}`}
              className="dropdown-item" target="_blank" rel="noreferrer" key={template.id}>
              Download {template.name}
            </a>
          )}
        </div>
      </div>

    </div>
  );
};

export default OrderMenu;
