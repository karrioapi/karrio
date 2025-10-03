import React from 'react';
import { useKarrio } from '../../provider/karrio-provider';

type ShippingFormProps = {
  className?: string;
  onSubmit?: (data: any) => void;
};

export function ShippingForm({ className = '', onSubmit }: ShippingFormProps) {
  const { theme } = useKarrio();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit({ success: true, message: 'Form submitted (placeholder)' });
    }
  };

  return (
    <div className={`shipping-form shipping-form-${theme} ${className}`}>
      <h3 className="text-lg font-medium mb-4">Create Shipping Label</h3>
      <form onSubmit={handleSubmit}>
        <div className="space-y-4">
          <div className="form-group">
            <label className="block text-sm font-medium mb-1">Package Type</label>
            <select className="w-full rounded-md border border-gray-300 shadow-sm p-2">
              <option>Small Box</option>
              <option>Medium Box</option>
              <option>Large Box</option>
            </select>
          </div>
          <div className="form-group">
            <label className="block text-sm font-medium mb-1">Service Type</label>
            <select className="w-full rounded-md border border-gray-300 shadow-sm p-2">
              <option>Standard</option>
              <option>Express</option>
              <option>Priority</option>
            </select>
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 text-white rounded-md py-2 px-4 hover:bg-blue-700"
          >
            Create Label
          </button>
        </div>
      </form>
      <p className="mt-4 text-sm text-gray-500">This is a placeholder for the shipping form UI.</p>
    </div>
  );
}
