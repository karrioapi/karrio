import React from "react";
import { LinkIcon } from '@heroicons/react/24/solid';

const references = require("./references.json");

const CarrierIntegrationDetails = ({ id, integration = {} }) => {
  const connectionFields = references.connection_fields?.[id] || {};
  const connectionConfig = references.connection_configs?.[id] || {};
  const services = references.services?.[id] || {};
  const options = references.options?.[id] || {};

  return (
    <div id="tailwind" className="max-w-5xl mx-auto space-y-8">
      {/* Overview Card */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-slate-800">{id}</h2>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            integration.status === 'production' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
          }`}>
            {integration.status}
          </span>
        </div>

        <p className="text-slate-600 mb-6">{integration.description}</p>

        {/* Features */}
        <div className="flex flex-wrap gap-2 mb-6">
          {integration.features?.map((feature, idx) => (
            <span key={idx} className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm">
              {feature}
            </span>
          ))}
        </div>

        {/* Resources */}
        <div className="flex gap-4">
          <a href={integration.website}
             target="_blank"
             rel="noopener noreferrer"
             className="flex items-center text-blue-600 hover:text-blue-800">
            <span>Carrier Website</span>
            <LinkIcon className="w-4 h-4 ml-1" />
          </a>
          <a href={integration.docs}
             target="_blank"
             rel="noopener noreferrer"
             className="flex items-center text-blue-600 hover:text-blue-800">
            <span>API Documentation</span>
            <LinkIcon className="w-4 h-4 ml-1" />
          </a>
        </div>
      </div>

      {/* Connection Requirements */}
      {Object.keys(connectionFields).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-bold text-slate-800 mb-4">Connection Requirements</h2>

          <div className="space-y-4">
            {Object.entries(connectionFields).map(([key, field]) => (
              <div key={key} className="border-b border-slate-200 pb-4">
                <div className="flex items-baseline gap-2 mb-2">
                  <code className="text-sm bg-slate-100 px-2 py-1 rounded text-slate-800">
                    {field.name}
                  </code>
                  <span className="text-slate-500 text-sm">{field.type}</span>
                  {field.required && (
                    <span className="text-red-600 text-sm">required</span>
                  )}
                </div>
                <p className="text-slate-600 text-sm">
                  {field.description || `The ${field.name} field for carrier connection.`}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Carrier Configuration */}
      {Object.keys(connectionConfig).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-bold text-slate-800 mb-4">Carrier Configuration</h2>

          <div className="space-y-4">
            {Object.entries(connectionConfig).map(([key, config]) => (
              <div key={key} className="border-b border-slate-200 pb-4">
                <div className="flex items-baseline gap-2 mb-2">
                  <code className="text-sm bg-slate-100 px-2 py-1 rounded text-slate-800">
                    {config.name}
                  </code>
                  <span className="text-slate-500 text-sm">{config.type}</span>
                </div>
                {config.enum && (
                  <div className="mt-2">
                    <div className="text-sm text-slate-500 mb-2">Allowed values:</div>
                    <div className="flex flex-wrap gap-2">
                      {config.enum.map((value, idx) => (
                        <code key={idx} className="text-xs bg-slate-100 px-2 py-1 rounded text-slate-700">
                          {value}
                        </code>
                      ))}
                    </div>
                  </div>
                )}
                <p className="text-slate-600 text-sm mt-2">
                  {config.description || `Configuration option for ${config.name}.`}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Shipping Services */}
      {Object.keys(services).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-bold text-slate-800 mb-4">Available Services</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="text-left py-2 px-4 text-slate-600">Service Name</th>
                  <th className="text-left py-2 px-4 text-slate-600">Service Code</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(services).map(([code, name]) => (
                  <tr key={code} className="border-b border-slate-100 hover:bg-slate-50">
                    <td className="py-2 px-4">{name}</td>
                    <td className="py-2 px-4 font-mono text-sm text-slate-600">{code}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Shipping Options */}
      {Object.keys(options).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-bold text-slate-800 mb-4">Shipping Options</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="text-left py-3 px-4 text-slate-600">Option</th>
                  <th className="text-left py-3 px-4 text-slate-600">Code</th>
                  <th className="text-left py-3 px-4 text-slate-600">Type</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(options).map(([key, option]) => (
                  <tr key={key} className="border-b border-slate-100 hover:bg-slate-50">
                    <td className="py-3 px-4 font-medium">{key}</td>
                    <td className="py-3 px-4 font-mono text-sm">{option.code}</td>
                    <td className="py-3 px-4 font-mono text-sm">{option.type}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
};

export default CarrierIntegrationDetails;
