import { OrderComponent } from '@/modules/Orders/order';
import { useLocation } from '@/lib/helper';
import React, { useState } from 'react';

type OrderPreviewContextType = {
  previewOrder: (orderId: string) => void,
};

interface OrderPreviewComponent { }

export const OrderPreviewContext = React.createContext<OrderPreviewContextType>({} as OrderPreviewContextType);

const OrderPreview: React.FC<OrderPreviewComponent> = ({ children }) => {
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`order-${Date.now()}`);
  const [orderId, setOrderId] = useState<string>();

  const previewOrder = (orderId: string) => {
    setOrderId(orderId);
    setIsActive(true);
    setKey(`order-${Date.now()}`);
    addUrlParam('modal', orderId);
  };
  const dismiss = (_?: any) => {
    setOrderId(undefined);
    setIsActive(false);
    setKey(`order-${Date.now()}`);
    removeUrlParam('modal');
  };

  return (
    <>
      <OrderPreviewContext.Provider value={{ previewOrder }}>
        {children}
      </OrderPreviewContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background" onClick={dismiss}></div>

        {isActive && <div className="modal-card is-medium-modal">
          <section className="modal-card-body px-5 pt-0 pb-6">

            <OrderComponent orderId={orderId} />

          </section>
        </div>}

        <button className="modal-close is-large has-background-dark" aria-label="close" onClick={dismiss}></button>

      </div>
    </>
  )
};

export default OrderPreview;
