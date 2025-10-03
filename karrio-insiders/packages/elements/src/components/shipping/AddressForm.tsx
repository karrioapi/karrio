import * as React from 'react';

interface AddressFormProps {
    className?: string;
    onSave?: (address: any) => void;
}

/**
 * Address form component for collecting shipping/billing address information
 */
export function AddressForm({ className, onSave }: AddressFormProps) {
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (onSave) {
            onSave({
                name: "John Doe",
                company: "Example Corp",
                street1: "123 Main St",
                street2: "Suite 100",
                city: "New York",
                state: "NY",
                postal_code: "10001",
                country: "US",
                phone: "+1 555-555-5555",
                email: "john@example.com"
            });
        }
    };

    return (
        <div className={`p-4 border rounded-lg shadow-sm ${className}`}>
            <h3 className="text-lg font-medium mb-4">Shipping Address</h3>
            <form onSubmit={handleSubmit}>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div className="col-span-2">
                        <label className="block text-sm font-medium text-gray-700">Full Name</label>
                        <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="John Doe" />
                    </div>

                    <div className="col-span-2">
                        <label className="block text-sm font-medium text-gray-700">Company (Optional)</label>
                        <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="Example Corp" />
                    </div>

                    <div className="col-span-2">
                        <label className="block text-sm font-medium text-gray-700">Street Address</label>
                        <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="123 Main St" />
                    </div>

                    <div className="col-span-2">
                        <label className="block text-sm font-medium text-gray-700">Apartment, suite, etc.</label>
                        <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="Apt 4B" />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">City</label>
                        <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="New York" />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">State / Province</label>
                        <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="NY" />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Postal Code</label>
                        <input type="text" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="10001" />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Country</label>
                        <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                            <option value="US">United States</option>
                            <option value="CA">Canada</option>
                            <option value="MX">Mexico</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Phone</label>
                        <input type="tel" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="+1 555-555-5555" />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="john@example.com" />
                    </div>
                </div>

                <div className="mt-4">
                    <button type="submit" className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Save Address
                    </button>
                </div>
            </form>
        </div>
    );
}
