import * as React from 'react';

interface ShippingRateCalculatorProps {
  className?: string;
  onCalculate?: (data: any) => void;
}

/**
 * Shipping rate calculator component for calculating shipping rates
 */
export function ShippingRateCalculator({ className, onCalculate }: ShippingRateCalculatorProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onCalculate) {
      onCalculate({
        origin: {
          postal_code: "10001",
          country: "US"
        },
        destination: {
          postal_code: "94107",
          country: "US"
        },
        package: {
          weight: 2,
          dimensions: {
            length: 10,
            width: 8,
            height: 6
          }
        }
      });
    }
  };

  return (
    <div className={`p-4 border rounded-lg shadow-sm ${className}`}>
      <h3 className="text-lg font-medium mb-4">Calculate Shipping Rates</h3>
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="border-b pb-4">
            <h4 className="font-medium text-gray-700 mb-2">Origin</h4>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700">Country</label>
                <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                  <option value="US">United States</option>
                  <option value="CA">Canada</option>
                  <option value="MX">Mexico</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Postal Code</label>
                <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="10001" />
              </div>
            </div>
          </div>

          <div className="border-b pb-4">
            <h4 className="font-medium text-gray-700 mb-2">Destination</h4>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700">Country</label>
                <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                  <option value="US">United States</option>
                  <option value="CA">Canada</option>
                  <option value="MX">Mexico</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Postal Code</label>
                <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="94107" />
              </div>
            </div>
          </div>

          <div className="col-span-full">
            <h4 className="font-medium text-gray-700 mb-2">Package Details</h4>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700">Weight (lbs)</label>
                <input type="number" min="0.1" step="0.1" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="2" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Package Type</label>
                <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                  <option value="box">Box</option>
                  <option value="envelope">Envelope</option>
                  <option value="tube">Tube</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Length (in)</label>
                <input type="number" min="0.1" step="0.1" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="10" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Width (in)</label>
                <input type="number" min="0.1" step="0.1" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="8" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Height (in)</label>
                <input type="number" min="0.1" step="0.1" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="6" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Insurance Value ($)</label>
                <input type="number" min="0" step="0.01" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="0.00" />
              </div>
            </div>
          </div>
        </div>

        <div className="mt-4">
          <button type="submit" className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Calculate Rates
          </button>
        </div>
      </form>
    </div>
  );
}
