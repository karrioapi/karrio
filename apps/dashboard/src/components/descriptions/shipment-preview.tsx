import { ShipmentComponent } from '@/modules/Shipments/shipment';
import ConfirmModal from '@/components/confirm-modal';
import { useLocation } from '@/lib/helper';
import React, { useState } from 'react';

type ShipmentPreviewContextType = {
  previewShipment: (shipmentId: string) => void,
};

interface ShipmentPreviewComponent { }

export const ShipmentPreviewContext = React.createContext<ShipmentPreviewContextType>({} as ShipmentPreviewContextType);

const ShipmentPreview: React.FC<ShipmentPreviewComponent> = ({ children }) => {
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`shipment-${Date.now()}`);
  const [shipmentId, setShipmentId] = useState<string>();

  const previewShipment = (shipmentId: string) => {
    setShipmentId(shipmentId);
    setIsActive(true);
    setKey(`shipment-${Date.now()}`);
    addUrlParam('modal', shipmentId);
  };
  const dismiss = (_?: any) => {
    setShipmentId(undefined);
    setIsActive(false);
    setKey(`shipment-${Date.now()}`);
    removeUrlParam('modal');
  };

  return (
    <>
      <ShipmentPreviewContext.Provider value={{ previewShipment }}>
        {children}
      </ShipmentPreviewContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background" onClick={dismiss}></div>

        {(isActive && shipmentId) && <div className="modal-card is-medium-modal">
          <section className="modal-card-body px-5 pt-0 pb-6">

            <ConfirmModal>
              <ShipmentComponent shipmentId={shipmentId} />
            </ConfirmModal>

          </section>
        </div>}

        <button className="modal-close is-large has-background-dark" aria-label="close" onClick={dismiss}></button>

      </div>
    </>
  )
};

export default ShipmentPreview;
