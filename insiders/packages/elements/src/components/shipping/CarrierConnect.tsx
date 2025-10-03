import * as React from 'react';

interface CarrierConnectProps {
    className?: string;
    onConnect?: () => void;
}

/**
 * DHL carrier connection component
 */
function DHL({ className, onConnect }: CarrierConnectProps) {
    return (
        <div className={`p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow ${className}`}>
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-medium text-gray-900">DHL</h3>
                    <p className="text-sm text-gray-500">Connect your DHL account</p>
                </div>
                <div className="w-12 h-12 bg-yellow-400 rounded-full flex items-center justify-center text-white font-bold">
                    DHL
                </div>
            </div>
            <button
                onClick={onConnect}
                className="mt-4 w-full bg-yellow-400 hover:bg-yellow-500 text-white py-2 px-4 rounded-md transition-colors"
            >
                Connect
            </button>
        </div>
    );
}

/**
 * UPS carrier connection component
 */
function UPS({ className, onConnect }: CarrierConnectProps) {
    return (
        <div className={`p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow ${className}`}>
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-medium text-gray-900">UPS</h3>
                    <p className="text-sm text-gray-500">Connect your UPS account</p>
                </div>
                <div className="w-12 h-12 bg-[#351c15] rounded-full flex items-center justify-center text-white font-bold">
                    UPS
                </div>
            </div>
            <button
                onClick={onConnect}
                className="mt-4 w-full bg-[#351c15] hover:bg-[#4a2a20] text-white py-2 px-4 rounded-md transition-colors"
            >
                Connect
            </button>
        </div>
    );
}

/**
 * FedEx carrier connection component
 */
function FedEx({ className, onConnect }: CarrierConnectProps) {
    return (
        <div className={`p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow ${className}`}>
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-medium text-gray-900">FedEx</h3>
                    <p className="text-sm text-gray-500">Connect your FedEx account</p>
                </div>
                <div className="w-12 h-12 bg-[#4d148c] rounded-full flex items-center justify-center text-white font-bold">
                    FDX
                </div>
            </div>
            <button
                onClick={onConnect}
                className="mt-4 w-full bg-[#4d148c] hover:bg-[#5b1ba6] text-white py-2 px-4 rounded-md transition-colors"
            >
                Connect
            </button>
        </div>
    );
}

/**
 * USPS carrier connection component
 */
function USPS({ className, onConnect }: CarrierConnectProps) {
    return (
        <div className={`p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow ${className}`}>
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-medium text-gray-900">USPS</h3>
                    <p className="text-sm text-gray-500">Connect your USPS account</p>
                </div>
                <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                    USPS
                </div>
            </div>
            <button
                onClick={onConnect}
                className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md transition-colors"
            >
                Connect
            </button>
        </div>
    );
}

// Export all carrier components as properties of CarrierConnect
export const CarrierConnect = {
    DHL,
    UPS,
    FedEx,
    USPS
};
