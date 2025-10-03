import { notFound } from 'next/navigation';
import fs from 'fs/promises';
import path from 'path';
import { LinkIcon } from 'lucide-react';

export async function generateStaticParams() {
  try {
    const integrationsPath = path.join(process.cwd(), 'public', 'carrier-integrations.json');
    const integrationsData = await fs.readFile(integrationsPath, 'utf8');
    const integrations = JSON.parse(integrationsData);

    return integrations.map((integration) => ({
      carrier_id: integration.id,
    }));
  } catch (error) {
    console.error('Error generating static params:', error);
    return [];
  }
}

export default async function CarrierIntegrationPage({ params }: { params: Promise<{ carrier_id: string }> }) {
  try {
    const args = await params;
    // Read carrier-integrations.json from the public directory
    const integrationsPath = path.join(process.cwd(), 'public', 'carrier-integrations.json');
    const integrationsData = await fs.readFile(integrationsPath, 'utf8');
    const integrations = JSON.parse(integrationsData);

    // Find the integration by ID
    const integration = integrations.find((i) => i.id === args?.carrier_id);

    if (!integration) {
      return notFound();
    }

    // Map capabilities to features with capitalized first letter
    const features = integration.capabilities?.map(
      (capability) => capability.charAt(0).toUpperCase() + capability.slice(1)
    ) || [];

    return (
      <div className="py-8 max-w-5xl mx-auto space-y-8">
        {/* Header and Overview Card */}
        <div className="bg-background rounded-lg overflow-hidden border border-gray-200 dark:border-gray-800">
          {/* Gradient Header */}
          <div className="relative w-full h-40 bg-gradient-to-br from-[#4a1db0] to-[#47a3ff] dark:from-[#5722cc] dark:to-[#2364e7] overflow-hidden flex items-center justify-center">
            <div className="text-center z-10">
              <p className="text-lg text-white !text-white opacity-90">API Integration</p>
              <h1 className="text-2xl md:text-3xl font-bold text-white mb-1 !text-white">{integration.display_name}</h1>
            </div>
            <div className="absolute inset-0 opacity-20">
              <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <pattern id="dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                    <circle fill="white" cx="4" cy="4" r="1"></circle>
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#dots)"></rect>
              </svg>
            </div>
          </div>

          {/* Overview Content */}
          <div className="p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-base font-medium text-foreground">{integration.id}</span>
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${integration.integration_status === 'production'
                ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                }`}>
                {integration.integration_status}
              </span>
            </div>

            <p className="text-sm text-muted-foreground mb-3">
              {integration.description || "No description available."}
            </p>

            {/* Features */}
            <div className="flex flex-wrap gap-1.5 mb-3">
              {features.map((feature, idx) => (
                <span
                  key={idx}
                  className="px-2 py-0.5 bg-muted text-muted-foreground rounded-full text-xs font-medium"
                >
                  {feature}
                </span>
              ))}
            </div>

            {/* Resources */}
            {(integration.website || integration.documentation) && (
              <div className="flex flex-wrap gap-4 pt-3 border-t border-gray-200 dark:border-gray-800">
                {integration.website && (
                  <a
                    href={integration.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 text-sm"
                  >
                    <span>Carrier Website</span>
                    <LinkIcon className="w-3.5 h-3.5 ml-1" />
                  </a>
                )}
                {integration.documentation && (
                  <a
                    href={integration.documentation}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 text-sm"
                  >
                    <span>API Documentation</span>
                    <LinkIcon className="w-3.5 h-3.5 ml-1" />
                  </a>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Connection Requirements Section */}
        {integration.connection_fields && Object.keys(integration.connection_fields).length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-bold text-foreground mb-3 pb-2 border-b border-gray-200 dark:border-gray-800">
              Connection Requirements
            </h2>

            <table className="w-full min-w-full text-sm border-separate border-spacing-0 rounded-md overflow-hidden">
              <thead className="bg-muted">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800">Field</th>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800">Type</th>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800 w-24">Required</th>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800 hidden md:table-cell">Description</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(integration.connection_fields).map(([key, field]: [string, any], index) => (
                  <tr key={key} className={`${index % 2 === 1 ? 'bg-muted/50' : 'bg-background'}`}>
                    <td className="py-3 px-4 font-mono text-xs text-foreground border-b border-gray-200 dark:border-gray-800">{field.name}</td>
                    <td className="py-3 px-4 text-muted-foreground text-xs border-b border-gray-200 dark:border-gray-800">{field.type}</td>
                    <td className="py-3 px-4 border-b border-gray-200 dark:border-gray-800">
                      {field.required ? (
                        <span className="inline-block w-4 h-4 rounded-full bg-red-500"></span>
                      ) : (
                        <span className="inline-block w-4 h-4 rounded-full bg-muted-foreground/20"></span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-muted-foreground text-xs hidden md:table-cell border-b border-gray-200 dark:border-gray-800">
                      {field.description || `The ${field.name} field for carrier connection.`}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Carrier Configuration Section */}
        {integration.config_fields && Object.keys(integration.config_fields).length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-bold text-foreground mb-3 pb-2 border-b border-gray-200 dark:border-gray-800">
              Carrier Configuration
            </h2>

            <table className="w-full min-w-full text-sm border-separate border-spacing-0 rounded-md overflow-hidden">
              <thead className="bg-muted">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800">Field</th>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800">Type</th>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800 hidden md:table-cell">Description</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(integration.config_fields).map(([key, config]: [string, any], index) => (
                  <tr key={key} className={`${index % 2 === 1 ? 'bg-muted/50' : 'bg-background'}`}>
                    <td className="py-3 px-4 font-mono text-xs text-foreground border-b border-gray-200 dark:border-gray-800">
                      {key}
                      {config.enum && (
                        <div className="mt-1 flex flex-wrap gap-1 max-w-[200px]">
                          {config.enum.map((value: string, idx: number) => (
                            <span key={idx} className="text-[10px] bg-purple-100/30 dark:bg-purple-900/30 px-1.5 py-0.5 rounded text-purple-700 dark:text-purple-300 border border-purple-200/50 dark:border-purple-800/50 inline-block">
                              {value}
                            </span>
                          ))}
                        </div>
                      )}
                    </td>
                    <td className="py-3 px-4 text-muted-foreground text-xs border-b border-gray-200 dark:border-gray-800">{config.type}</td>
                    <td className="py-3 px-4 text-muted-foreground text-xs hidden md:table-cell border-b border-gray-200 dark:border-gray-800">
                      {config.description || `Configuration option for ${key}.`}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Shipping Services Section */}
        {integration.shipping_services && Object.keys(integration.shipping_services).length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-bold text-foreground mb-3 pb-2 border-b border-gray-200 dark:border-gray-800">
              Available Services
            </h2>

            <table className="w-full min-w-full text-sm border-separate border-spacing-0 rounded-md overflow-hidden">
              <thead className="bg-muted">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800">Service Name</th>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800">Service Code</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(integration.shipping_services).map(([code, name], index) => (
                  <tr key={code} className={`${index % 2 === 1 ? 'bg-muted/50' : 'bg-background'}`}>
                    <td className="py-3 px-4 text-foreground text-xs border-b border-gray-200 dark:border-gray-800">{name as string}</td>
                    <td className="py-3 px-4 font-mono text-xs text-purple-600 dark:text-purple-400 border-b border-gray-200 dark:border-gray-800">{code}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Shipping Options Section */}
        {integration.shipping_options && Object.keys(integration.shipping_options).length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-bold text-foreground mb-3 pb-2 border-b border-gray-200 dark:border-gray-800">
              Shipping Options
            </h2>

            <table className="w-full min-w-full text-sm border-separate border-spacing-0 rounded-md overflow-hidden">
              <thead className="bg-muted">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800">Option</th>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800">Code</th>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground border-b border-gray-200 dark:border-gray-800">Type</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(integration.shipping_options).map(([key, option]: [string, any], index) => (
                  <tr key={key} className={`${index % 2 === 1 ? 'bg-muted/50' : 'bg-background'}`}>
                    <td className="py-3 px-4 text-foreground text-xs border-b border-gray-200 dark:border-gray-800">{key}</td>
                    <td className="py-3 px-4 font-mono text-xs text-purple-600 dark:text-purple-400 border-b border-gray-200 dark:border-gray-800">{option.code}</td>
                    <td className="py-3 px-4 font-mono text-xs text-muted-foreground border-b border-gray-200 dark:border-gray-800">{option.type}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    );
  } catch (error) {
    console.error('Error in CarrierIntegrationPage:', error);
    return notFound();
  }
}
