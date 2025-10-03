import React from 'react';
import { useKarrio } from '../../provider/karrio-provider';

// Props with optional className for styling
type CarrierConnectProps = {
  className?: string;
  onConnect?: () => void;
};

// Base component
function BaseCarrierConnect({
  className = '',
  carrier = 'Generic',
  onConnect
}: CarrierConnectProps & { carrier: string }) {
  const { theme } = useKarrio();

  return (
    <div className={`p-4 border rounded-md ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} ${className}`}>
      <h3 className="text-lg font-medium mb-2">Connect to {carrier}</h3>
      <p className={`mb-4 text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-500'}`}>
        Connect your {carrier} account to start creating shipments.
      </p>
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        onClick={onConnect}
      >
        Connect
      </button>
    </div>
  );
}

// Named exports for specific carriers
export const CarrierConnect = {
  DHL: (props: CarrierConnectProps) => <BaseCarrierConnect {...props} carrier="DHL" />,
  UPS: (props: CarrierConnectProps) => <BaseCarrierConnect {...props} carrier="UPS" />,
  USPS: (props: CarrierConnectProps) => <BaseCarrierConnect {...props} carrier="USPS" />,
  FedEx: (props: CarrierConnectProps) => <BaseCarrierConnect {...props} carrier="FedEx" />,
};
