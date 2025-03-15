import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import TailwindWrapper from '../components/TailwindWrapper';
import KarrioLayout from '../components/KarrioLayout';

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();

  return (
    <TailwindWrapper>
      <KarrioLayout>
        {/* Hero Section */}
        <div className="bg-gradient-to-b from-indigo-50 to-white dark:from-gray-900 dark:to-gray-800">
          <div className="container mx-auto px-4 py-16 md:py-24">
            <div className="text-center max-w-4xl mx-auto mb-16">
              <h1 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900 dark:text-white">
                Programmable shipping APIs for platforms
              </h1>
              <p className="text-lg md:text-xl mb-8 text-gray-700 dark:text-gray-300">
                Karrio is the most flexible way to integrate shipping into your platform. Our headless shipping platform enables you to build shipping experiences from live rating, label generation, package tracking, and more.
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <Link
                  to="https://app.karrio.io/signup"
                  className="bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-md transition-colors font-medium">
                  Get Started
                </Link>
                <Link
                  to="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                  className="bg-white hover:bg-gray-50 text-primary border border-primary px-6 py-3 rounded-md transition-colors font-medium">
                  Watch Demo
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Section */}
        <div className="container mx-auto px-4 py-12">
          <div className="flex flex-wrap justify-center gap-12 md:gap-24 text-center">
            <div>
              <div className="text-2xl md:text-3xl font-bold text-primary dark:text-secondary">+30</div>
              <div className="text-gray-600 dark:text-gray-400">Supported Carriers</div>
            </div>
            <div>
              <div className="text-2xl md:text-3xl font-bold text-primary dark:text-secondary">+20K</div>
              <div className="text-gray-600 dark:text-gray-400">OSS Downloads</div>
            </div>
            <div>
              <div className="text-2xl md:text-3xl font-bold text-primary dark:text-secondary">+1M</div>
              <div className="text-gray-600 dark:text-gray-400">Live Transactions</div>
            </div>
          </div>

          {/* Carrier Logos */}
          <div className="mt-20 mb-12">
            <h3 className="text-xl text-center font-semibold mb-8 text-gray-800 dark:text-gray-200">Trusted by businesses shipping with</h3>
            <div className="flex flex-wrap justify-center items-center gap-8">
              <img src="/img/carriers/canadapost_icon.svg" alt="Canada Post" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
              <img src="/img/carriers/usps_icon.svg" alt="USPS" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
              <img src="/img/carriers/fedex_icon.svg" alt="FedEx" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
              <img src="/img/carriers/dhl_universal_icon.svg" alt="DHL" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
              <img src="/img/carriers/ups_icon.svg" alt="UPS" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
              <img src="/img/carriers/purolator_icon.svg" alt="Purolator" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
              <img src="/img/carriers/australiapost_icon.svg" alt="Australia Post" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
              <img src="/img/carriers/royalmail_icon.svg" alt="Royal Mail" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
              <img src="/img/carriers/laposte_icon.svg" alt="La Poste" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
              <img src="/img/carriers/dpd_icon.svg" alt="DPD" className="h-8 md:h-10 grayscale hover:grayscale-0 transition-all duration-300" />
            </div>
          </div>
        </div>

        {/* Problem Section */}
        <div className="bg-gray-50 dark:bg-gray-900 py-16">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h3 className="text-lg font-medium text-primary dark:text-secondary mb-2">The problem</h3>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">Shipping integration is still painful</h2>
              <p className="mt-4 text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Poor developer experience. Long time-to-value. Lack of control.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">For engineers</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Obstacles include arcane technologies, a lack of documentation, multiple and inconsistent APIs, difficult access to accounts and API credentials for development, and more. In short, an overall poor developer experience.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">For brands & retailers</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Seamless shipping is crucial but expensive, with limited options. Developing an in-house shipping system diverts engineering resources and prolongs carrier onboarding. Adopting closed Saas solutions results in a limited ability to create custom logistics processes.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">For Logistics providers</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  After re-inventing the wheel or adopting a closed-source solution, how much profit margins do you have left? Building a custom-branded shipping experience for your merchants doesn't have to result in a lack of control, vendor lock-in and low margins.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Solution Section */}
        <div className="py-16">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h3 className="text-lg font-medium text-primary dark:text-secondary mb-2">The solution</h3>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">Headless shipping platform</h2>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">Universal shipping API</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Feeling the pain or struggling with shipping API integrations? Stop reinventing the wheel and add your carrier accounts on Karrio to start processing shipping transactions.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">Out-of-the-box shipping system</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Karrio's shipping solution offers an API for engineers and a flexible user interface for back-office fulfilment operations. With our composable architecture, you can add carrier extensions and extend Karrio's functionalities.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">More control and security</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Our open-source solution gives you an alternative to the build-or-buy dilemma. With Karrio's transparency, you can regain control and visibility over logistics processes and shipping spending. All while achieving carrier, data and security compliance.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* How it Works Section */}
        <div className="bg-gray-50 dark:bg-gray-900 py-16">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h3 className="text-lg font-medium text-primary dark:text-secondary mb-2">How it works</h3>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">Effortless shipping integration</h2>
            </div>

            <div className="grid md:grid-cols-4 gap-8 max-w-5xl mx-auto">
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <div className="text-2xl font-bold text-primary dark:text-secondary mb-2">1</div>
                <h3 className="text-xl font-semibold mb-4">Manage carrier connections</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Setup accounts and API credentials to enable Karrio's connection to your carriers.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <div className="text-2xl font-bold text-primary dark:text-secondary mb-2">2</div>
                <h3 className="text-xl font-semibold mb-4">Fetch live rates</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Your users can fetch live rates from a network of carriers by submitting shipment details using the user interface or programmatically via API.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <div className="text-2xl font-bold text-primary dark:text-secondary mb-2">3</div>
                <h3 className="text-xl font-semibold mb-4">Generate shipping labels</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Karrio will generate shipping labels based on your preferred shipping service. You can then download and print generated labels.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <div className="text-2xl font-bold text-primary dark:text-secondary mb-2">4</div>
                <h3 className="text-xl font-semibold mb-4">Track packages</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Labels purchased on Karrio are automatically linked with a package tracker to provide real-time delivery status. You can also create trackers for shipments made outside of Karrio.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Developer Section */}
        <div className="py-16">
          <div className="container mx-auto px-4">
            <div className="max-w-5xl mx-auto">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white text-center mb-8">Made for developers</h2>
              <p className="text-xl text-center mb-12 text-gray-700 dark:text-gray-300 max-w-3xl mx-auto">
                <strong>The flexible headless shipping platform</strong>
              </p>
              <p className="text-lg mb-8 text-gray-700 dark:text-gray-300">
                No more painful in-house carrier integrations. No more dependence on 3rd party and Saas vendor lock-in for your logistics automation. We obsess over the right abstractions so your teams don't have to and won't spend months integrating shipping functionalities. Create memorable shipping experiences and powerful extensions through Webhooks, REST and GraphQL API.
              </p>
              <div className="text-center">
                <Link
                  to="/docs"
                  className="bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-md transition-colors font-medium inline-block">
                  Read Docs
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Next Steps Section */}
        <div className="bg-gray-50 dark:bg-gray-900 py-16">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">Next steps</h2>
              <p className="mt-4 text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Karrio provides a modern shipping integration solution, is free to get started, and has an insider sponsorship tier for mission critical and shipping at scale.
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                <h3 className="text-2xl font-bold mb-4">Karrio Platform</h3>
                <p className="text-gray-700 dark:text-gray-300 mb-6">
                  Multi-tenant shipping Platform
                </p>
                <Link
                  to="/platform"
                  className="bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-md transition-colors font-medium inline-block">
                  Learn More
                </Link>
              </div>
              <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                <h3 className="text-2xl font-bold mb-4">Karrio Open Source</h3>
                <p className="text-gray-700 dark:text-gray-300 mb-6">
                  Multi-carrier shipping API
                </p>
                <Link
                  to="/docs/self-hosting/introduction"
                  className="bg-white hover:bg-gray-50 text-primary border border-primary px-6 py-3 rounded-md transition-colors font-medium inline-block">
                  Deploy Open Source
                </Link>
              </div>
            </div>
          </div>
        </div>
      </KarrioLayout>
    </TailwindWrapper>
  );
}
