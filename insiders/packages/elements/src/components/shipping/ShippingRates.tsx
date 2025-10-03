import * as React from 'react';

interface Rate {
  id: string;
  carrier: string;
  service: string;
  price: number;
  currency: string;
  delivery_time: string;
}

interface ShippingRatesProps {
  rates?: Rate[];
  className?: string;
  onSelect?: (rate: Rate) => void;
}

/**
 * Shipping rates display component for showing available shipping rates
 */
export function ShippingRates({
  rates = [],
  className,
  onSelect
}: ShippingRatesProps) {
  return (
    <div className={`p-4 border rounded-lg shadow-sm ${className}`}>
      <h3 className="text-lg font-medium mb-4">Available Shipping Rates</h3>
      {rates.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No shipping rates available. Please calculate rates first.
        </div>
      ) : (
        <div className="space-y-3">
          {rates.map((rate) => (
            <div
              key={rate.id}
              className="border rounded-md p-3 hover:border-indigo-500 cursor-pointer transition-colors"
              onClick={() => onSelect && onSelect(rate)}
            >
              <div className="flex justify-between">
                <div>
                  <div className="font-medium">{rate.carrier}</div>
                  <div className="text-sm text-gray-500">{rate.service}</div>
                </div>
                <div className="text-right">
                  <div className="font-medium">
                    {rate.price.toFixed(2)} {rate.currency}
                  </div>
                  <div className="text-sm text-gray-500">{rate.delivery_time}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
