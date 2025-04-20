import fs from 'fs/promises';
import path from 'path';

export default async function Carriers() {
  // Read carrier-integrations.json from the public directory
  const integrationsPath = path.join(process.cwd(), 'public', 'carrier-integrations.json');
  const integrationsData = await fs.readFile(integrationsPath, 'utf8');
  const integrations = JSON.parse(integrationsData);

  return (
    <div className="py-10">
      <h1>Karrio Carriers</h1>

      <p>Karrio allows you to access a network of shipping carriers and integrate with any additional logistics provider.</p>

      <h2 className="mt-6">Carriers Connections</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        {integrations.map((integration, key) => (
          <a
            key={key}
            href={`/docs/carriers/${integration.id}`}
            className="group no-underline"
          >
            <div className="docs-card relative flex flex-col h-full rounded-lg border p-4 shadow-sm transition-all duration-200 hover:shadow-md">
              <div className="flex items-center justify-between mb-4">
                <span className="text-base font-medium text-gray-900 dark:text-gray-100 py-3">
                  {integration.display_name}
                </span>
                <span
                  className={`px-2 py-0.5 rounded-full text-xs font-medium ${integration.integration_status === 'production'
                    ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                    : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                    }`}
                >
                  {integration.integration_status}
                </span>
              </div>

              <div className="flex flex-wrap gap-2 mb-3">
                {integration.capabilities?.map((capability, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 rounded-full text-xs font-medium"
                  >
                    {capability.charAt(0).toUpperCase() + capability.slice(1)}
                  </span>
                ))}
              </div>

              <span className="text-sm font-light text-gray-500 dark:text-gray-400">
                {integration.description || ""}
              </span>
            </div>
          </a>
        ))}
      </div>

      <h2 className="mt-8">Missing a carrier?</h2>

      <p>You can get your shipping providers added to Karrio:</p>

      <ul className="list-disc pl-6 mt-2">
        <li><a href="https://github.com/karrioapi/karrio/discussions" className="text-blue-600 dark:text-blue-400 hover:underline">Sponsor an Issue</a></li>
        <li><a href="https://github.com/karrioapi/karrio" className="text-blue-600 dark:text-blue-400 hover:underline">Submit a PR</a></li>
        <li><a href="/docs/developing/extension" className="text-blue-600 dark:text-blue-400 hover:underline">Carrier integration guide</a></li>
      </ul>
    </div>
  );
}
