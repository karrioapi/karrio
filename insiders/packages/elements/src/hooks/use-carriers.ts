import { useState } from 'react';

type Carrier = {
  id: string;
  name: string;
  isConnected: boolean;
};

export function useCarriers() {
  // This is a mock implementation that would later be connected to the API
  const [carriers, setCarriers] = useState<Carrier[]>([
    { id: 'dhl', name: 'DHL', isConnected: false },
    { id: 'ups', name: 'UPS', isConnected: false },
    { id: 'usps', name: 'USPS', isConnected: false },
    { id: 'fedex', name: 'FedEx', isConnected: false },
  ]);

  const connectCarrier = (carrierId: string) => {
    setCarriers(carriers.map(c =>
      c.id === carrierId ? { ...c, isConnected: true } : c
    ));
    return Promise.resolve({ success: true });
  };

  const disconnectCarrier = (carrierId: string) => {
    setCarriers(carriers.map(c =>
      c.id === carrierId ? { ...c, isConnected: false } : c
    ));
    return Promise.resolve({ success: true });
  };

  return {
    carriers,
    connectCarrier,
    disconnectCarrier,
  };
}
