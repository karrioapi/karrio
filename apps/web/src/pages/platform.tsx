import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import TailwindWrapper from '../components/TailwindWrapper';
import KarrioLayout from '../components/KarrioLayout';

export default function Platform(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();

  return (
    <TailwindWrapper>
      <KarrioLayout>
        {/* Hero Section */}
        <div className="bg-gradient-to-b from-purple-50 to-white dark:from-gray-900 dark:to-gray-800 pt-20">
          <div className="container mx-auto px-4 py-16 md:py-24">
            <div className="text-center max-w-4xl mx-auto mb-16">
              <h1 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900 dark:text-white">
                Karrio Platform
              </h1>
              <p className="text-lg md:text-xl mb-8 text-gray-700 dark:text-gray-300">
                A fully-managed, multi-tenant shipping platform for platforms, 3PLs, and logistics providers.
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <Link
                  to="https://app.karrio.io/signup"
                  className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-md transition-colors font-medium">
                  Get Started
                </Link>
                <Link
                  to="https://calendly.com/karrio/demo"
                  className="bg-white hover:bg-gray-50 text-purple-600 border border-purple-600 px-6 py-3 rounded-md transition-colors font-medium">
                  Request Demo
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-16">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">Platform Features</h2>
              <p className="mt-4 text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Everything you need to build a powerful shipping solution for your customers.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">Multi-tenant Architecture</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Support multiple merchants, each with their own configuration, carriers, and shipping profiles.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">White-label Dashboard</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Customize the shipping dashboard with your branding, colors, and logo for a seamless customer experience.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">Carrier Management</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Manage carrier credentials, services, and settings for your customers centrally or delegate control.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">Analytics & Reporting</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Gain insights into shipping volumes, costs, and performance across your customer base.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">Role-based Access</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Control who has access to what with granular permission settings for teams and customers.
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4">API & Webhooks</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Integrate with your existing systems using our comprehensive API and webhook system.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Pricing Section */}
        <div className="bg-gray-50 dark:bg-gray-900 py-16">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">Pricing</h2>
              <p className="mt-4 text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Transparent pricing that scales with your business.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="text-purple-600 font-semibold mb-2">Starter</div>
                <h3 className="text-3xl font-bold mb-2">$99/mo</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-6">For small platforms and businesses</p>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Up to 10 merchants
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    500 monthly shipments
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Basic white-labeling
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Email support
                  </li>
                </ul>
                <Link
                  to="https://app.karrio.io/signup"
                  className="block w-full text-center bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-md transition-colors font-medium">
                  Get Started
                </Link>
              </div>
              <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg border-2 border-purple-500 dark:border-purple-400 relative">
                <div className="absolute top-0 right-0 bg-purple-600 text-white px-4 py-1 rounded-bl-lg rounded-tr-lg font-medium">Popular</div>
                <div className="text-purple-600 font-semibold mb-2">Growth</div>
                <h3 className="text-3xl font-bold mb-2">$299/mo</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-6">For growing platforms</p>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Up to 50 merchants
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    2,500 monthly shipments
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Advanced white-labeling
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Priority support
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Analytics dashboard
                  </li>
                </ul>
                <Link
                  to="https://app.karrio.io/signup"
                  className="block w-full text-center bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-md transition-colors font-medium">
                  Get Started
                </Link>
              </div>
              <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="text-purple-600 font-semibold mb-2">Enterprise</div>
                <h3 className="text-3xl font-bold mb-2">Custom</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-6">For large platforms and 3PLs</p>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Unlimited merchants
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Custom shipment volume
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Fully custom branding
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Dedicated support
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    SLA guarantees
                  </li>
                </ul>
                <Link
                  to="https://calendly.com/karrio/demo"
                  className="block w-full text-center bg-white hover:bg-gray-50 text-purple-600 border border-purple-600 px-6 py-3 rounded-md transition-colors font-medium">
                  Contact Sales
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="py-16">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">Frequently Asked Questions</h2>
            </div>

            <div className="max-w-3xl mx-auto">
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-2">How does the multi-tenant system work?</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Each of your customers gets their own isolated tenant environment with dedicated carrier connections,
                  shipping profiles, and user accounts, while you maintain central control and visibility.
                </p>
              </div>
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-2">Can I use my own carrier accounts?</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Yes, Karrio Platform supports both your own carrier accounts and your customers' carrier accounts.
                  You can decide which model works best for your business.
                </p>
              </div>
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-2">What customization options are available?</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  You can customize logos, colors, domain names, email templates, and more. Enterprise customers
                  can request fully custom UI and workflow modifications.
                </p>
              </div>
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-2">Do you offer volume discounts?</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Yes, we offer volume-based pricing for customers with high shipping volumes. Contact our sales team
                  for a custom quote based on your expected volume.
                </p>
              </div>
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-2">How does support work?</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  We provide different levels of support based on your plan. Higher tiers include faster response times,
                  dedicated support contacts, and implementation assistance.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="bg-purple-100 dark:bg-gray-800 py-16">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">Ready to get started?</h2>
            <p className="text-xl text-gray-700 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
              Join platforms and logistics providers that are building better shipping experiences with Karrio.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                to="https://app.karrio.io/signup"
                className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-md transition-colors font-medium">
                Sign Up
              </Link>
              <Link
                to="https://calendly.com/karrio/demo"
                className="bg-white hover:bg-gray-50 text-purple-600 border border-purple-600 px-6 py-3 rounded-md transition-colors font-medium">
                Schedule Demo
              </Link>
            </div>
          </div>
        </div>
      </KarrioLayout>
    </TailwindWrapper>
  );
}
