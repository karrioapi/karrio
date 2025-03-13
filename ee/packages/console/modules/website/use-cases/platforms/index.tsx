import {
  Box,
  DollarSign,
  Users,
  Truck,
  PanelLeft,
  Globe,
  Code,
} from "lucide-react";
import { FeatureShowcase } from "@karrio/console/components/feature-showcase";
import { BookDemoButton } from "@karrio/console/components/book-demo-button";
import { CTASection } from "@karrio/console/components/cta-section";
import { Button } from "@karrio/insiders/components/ui/button";
import Image from "next/image";
import Link from "next/link";

export default async function Page() {
  return (
    <>
      {/* Main content */}
      <div className="py-20 relative">
        {/* Hero Section */}
        <div className="relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,#5722cc20,transparent_50%)]" />
          <div className="container mx-auto px-4 pt-8 pb-20 text-center max-w-[95%] xl:max-w-[1280px] relative">
            {/* Tag line */}
            <div className="inline-block bg-white/5 backdrop-blur-sm px-4 py-2 rounded-full mb-6">
              <span className="text-[#79e5dd] font-medium">Platforms & Marketplaces</span>
            </div>

            {/* Title */}
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 max-w-4xl mx-auto">
              Embed Shipping Capabilities into Your Platform
            </h1>

            {/* Description */}
            <p className="text-xl text-white/80 mb-10 max-w-3xl mx-auto">
              Add powerful shipping functionality to your marketplace, SaaS platform, or e-commerce solution with minimal development effort.
            </p>

            {/* CTA Buttons */}
            <div className="flex justify-center space-x-4">
              <Button size="lg" className="bg-[#5722cc] hover:bg-[#5722cc]/90">
                <Link href="/#pricing">Get Started</Link>
              </Button>
              <BookDemoButton variant="outline" className="border-white/20 hover:bg-white/10" />
            </div>
          </div>
        </div>

        {/* Key Challenges Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
          <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Key Challenges</h2>
              <p className="text-xl text-white/80 max-w-2xl mx-auto">
                Platforms and marketplaces face unique obstacles when incorporating shipping features.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <PanelLeft className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Seamless End-to-End Experience</h3>
                <p className="text-white/70">
                  Your users expect streamlined shipping workflows without stepping out of your platform.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <DollarSign className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Scalable Monetization</h3>
                <p className="text-white/70">
                  Monetize shipping as a value-added service—without heavy engineering overhead.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Globe className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Global Carrier Footprint</h3>
                <p className="text-white/70">
                  Onboard your user base's preferred carriers, from local couriers to global freight.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Platform Solution Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,#5722cc0d,transparent_50%)]" />
          <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Karrio Platform Solution</h2>
              <p className="text-xl text-white/80 max-w-2xl mx-auto">
                Enhance your platform with seamlessly integrated shipping capabilities that drive user retention and revenue.
              </p>
            </div>

            <div className="space-y-12">
              <FeatureShowcase
                title="One API, All Major Carriers"
                description="Integrate once with Karrio and instantly offer your platform users access to a comprehensive network of global and regional carriers."
                learnMoreHref=""
                tabs={[
                  {
                    label: "Overview",
                    value: "overview",
                    content: (
                      <div>
                        <ul className="space-y-3">
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Over 100 carrier integrations available</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Single API for all shipping functionality</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Continuous carrier updates and maintenance</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />

              <FeatureShowcase
                title="Native Shipping Experience"
                description="Provide a seamless, branded shipping experience directly within your platform. Let your users ship without ever leaving your environment."
                learnMoreHref=""
                tabs={[
                  {
                    label: "Overview",
                    value: "overview",
                    content: (
                      <div>
                        <ul className="space-y-3">
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">White-labeled shipping interface</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Embedded rating, label generation, and tracking</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Customizable shipping workflows</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />

              <FeatureShowcase
                title="Built for Developers"
                description="Our platform is designed with developers in mind, featuring clear documentation, robust SDKs, and a responsive support team to ensure successful integration."
                learnMoreHref=""
                tabs={[
                  {
                    label: "Overview",
                    value: "overview",
                    content: (
                      <div>
                        <ul className="space-y-3">
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Comprehensive API documentation</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Client libraries in multiple languages</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Developer-friendly sandbox environment</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />

              <FeatureShowcase
                title="New Revenue Streams"
                description="Create additional revenue streams by offering premium shipping services, negotiated rates, or custom carrier integrations to your platform users."
                learnMoreHref=""
                tabs={[
                  {
                    label: "Overview",
                    value: "overview",
                    content: (
                      <div>
                        <ul className="space-y-3">
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Markup capabilities on shipping rates</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Premium shipping service tiers</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Revenue sharing on transaction volume</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />
            </div>
          </div>
        </section>

        {/* Example Workflow Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
          <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Example Workflow</h2>
              <p className="text-xl text-white/80 max-w-2xl mx-auto">
                See how Karrio integrates with your platform to provide seamless shipping experiences.
              </p>
            </div>

            <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 max-w-4xl mx-auto">
              <div className="relative rounded-lg overflow-hidden aspect-video bg-black/40">
                <div className="absolute inset-0 flex items-center justify-center">
                  <svg width="100%" height="100%" viewBox="0 0 1200 675" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
                    {/* Clean Background with Minimal Gradient */}
                    <rect width="1200" height="675" fill="#080215" />

                    {/* Simple Large Gradient Shapes */}
                    <circle cx="300" cy="337" r="300" fill="url(#purpleGlowPlatform)" opacity="0.12" />
                    <circle cx="900" cy="337" r="300" fill="url(#tealGlowPlatform)" opacity="0.1" />

                    {/* Platform/Marketplace Section (Left) */}
                    <g>
                      <rect x="120" y="232" width="230" height="210" rx="12" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="235" y="200" fill="white" fontSize="22" fontWeight="bold" textAnchor="middle">Your Platform</text>

                      {/* Platform Components */}
                      <rect x="150" y="262" width="170" height="45" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="235" y="290" fill="white" fontSize="16" textAnchor="middle">User Interface</text>

                      <rect x="150" y="317" width="170" height="45" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="235" y="345" fill="white" fontSize="16" textAnchor="middle">Backend Services</text>

                      <rect x="150" y="372" width="170" height="45" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="235" y="400" fill="white" fontSize="16" textAnchor="middle">Platform Users</text>
                    </g>

                    {/* Karrio API Section (Middle) */}
                    <g>
                      <rect x="480" y="182" width="250" height="310" rx="12" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.15)" />
                      <text x="605" y="150" fill="white" fontSize="22" fontWeight="bold" textAnchor="middle">Karrio API</text>

                      {/* API Components */}
                      <rect x="510" y="212" width="190" height="50" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="605" y="243" fill="white" fontSize="16" textAnchor="middle">Authentication</text>

                      <rect x="510" y="277" width="190" height="50" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="605" y="308" fill="white" fontSize="16" textAnchor="middle">Shipping Services</text>

                      <rect x="510" y="342" width="190" height="50" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="605" y="373" fill="white" fontSize="16" textAnchor="middle">Rate Management</text>

                      <rect x="510" y="407" width="190" height="50" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="605" y="438" fill="white" fontSize="16" textAnchor="middle">Tracking & Analytics</text>
                    </g>

                    {/* Multiple Carriers Section (Right) */}
                    <g>
                      {/* Major Carriers */}
                      <rect x="850" y="187" width="220" height="80" rx="10" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="960" y="222" fill="white" fontSize="18" fontWeight="600" textAnchor="middle">Major Carriers</text>
                      <text x="960" y="247" fill="white" fontSize="13" opacity="0.7" textAnchor="middle">Global Shipping Networks</text>

                      {/* Regional Carriers */}
                      <rect x="850" y="287" width="220" height="80" rx="10" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="960" y="322" fill="white" fontSize="18" fontWeight="600" textAnchor="middle">Regional Carriers</text>
                      <text x="960" y="347" fill="white" fontSize="13" opacity="0.7" textAnchor="middle">Local Delivery Services</text>

                      {/* Specialty Services */}
                      <rect x="850" y="387" width="220" height="80" rx="10" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="960" y="422" fill="white" fontSize="18" fontWeight="600" textAnchor="middle">Specialty Services</text>
                      <text x="960" y="447" fill="white" fontSize="13" opacity="0.7" textAnchor="middle">Custom Shipping Options</text>
                    </g>

                    {/* Data Flow Arrows - Platform to API */}
                    <path d="M350 280 C400 280, 430 280, 480 280" stroke="#5722cc" strokeWidth="2.5" />
                    <path d="M472 275 L480 280 L472 285" fill="none" stroke="#5722cc" strokeWidth="2.5" />

                    <path d="M350 335 C400 335, 430 335, 480 335" stroke="#5722cc" strokeWidth="2.5" />
                    <path d="M472 330 L480 335 L472 340" fill="none" stroke="#5722cc" strokeWidth="2.5" />

                    <path d="M350 390 C400 390, 430 390, 480 390" stroke="#5722cc" strokeWidth="2.5" />
                    <path d="M472 385 L480 390 L472 395" fill="none" stroke="#5722cc" strokeWidth="2.5" />

                    {/* API to Carriers */}
                    <path d="M730 227 H850" stroke="#30D9B7" strokeWidth="2.5" />
                    <path d="M842 222 L850 227 L842 232" fill="none" stroke="#30D9B7" strokeWidth="2.5" />

                    <path d="M730 327 H850" stroke="#30D9B7" strokeWidth="2.5" />
                    <path d="M842 322 L850 327 L842 332" fill="none" stroke="#30D9B7" strokeWidth="2.5" />

                    <path d="M730 427 H850" stroke="#30D9B7" strokeWidth="2.5" />
                    <path d="M842 422 L850 427 L842 432" fill="none" stroke="#30D9B7" strokeWidth="2.5" />

                    {/* Return Data Flow */}
                    <path d="M850 260 C800 260, 770 260, 730 260" stroke="#30D9B7" strokeWidth="1.5" stroke-dasharray="5,3" />
                    <path d="M738 265 L730 260 L738 255" fill="none" stroke="#30D9B7" strokeWidth="1.5" />

                    <path d="M480 370 C430 370, 400 370, 350 370" stroke="#5722cc" strokeWidth="1.5" stroke-dasharray="5,3" />
                    <path d="M358 375 L350 370 L358 365" fill="none" stroke="#5722cc" strokeWidth="1.5" />

                    {/* Enhanced Gradients Definitions */}
                    <defs>
                      <radialGradient id="purpleGlowPlatform" cx="0.5" cy="0.5" r="0.5" fx="0.5" fy="0.5">
                        <stop offset="0%" stopColor="#5722cc" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#5722cc" stopOpacity="0" />
                      </radialGradient>

                      <radialGradient id="tealGlowPlatform" cx="0.5" cy="0.5" r="0.5" fx="0.5" fy="0.5">
                        <stop offset="0%" stopColor="#30D9B7" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#30D9B7" stopOpacity="0" />
                      </radialGradient>
                    </defs>
                  </svg>
                </div>
              </div>
              <div className="mt-8 text-center text-white/80">
                <p className="text-lg font-medium mb-2">Your Platform {'->'} Karrio API {'->'} Multiple Carriers</p>
                <p>Provide comprehensive shipping capabilities to your users with minimal development effort.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Business Outcomes Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,#5722cc0d,transparent_50%)]" />
          <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Business Outcomes</h2>
              <p className="text-xl text-white/80 max-w-2xl mx-auto">
                Add value to your platform with integrated shipping capabilities.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Box className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Accelerated Product Roadmap</h3>
                <p className="text-white/70">
                  Launch integrated shipping features faster, without complex development cycles.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <DollarSign className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Increased Revenue Streams</h3>
                <p className="text-white/70">
                  Offer shipping as a built-in service, capturing additional transaction-based revenue.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Users className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Better User Retention</h3>
                <p className="text-white/70">
                  Keep users on your platform with an all-in-one solution for order, fulfillment, and delivery.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Why Karrio Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
          <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Why Karrio?</h2>
              <p className="text-xl text-white/80 max-w-2xl mx-auto">
                Choose the shipping infrastructure built for modern platforms.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Truck className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Shipping Expertise</h3>
                <p className="text-white/70">
                  We specialize in multi-carrier logistics, just like Stripe leads in online payments.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Code className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Open-Source Innovation</h3>
                <p className="text-white/70">
                  Our platform is built on open standards, ensuring flexibility and vendor independence.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Users className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Dedicated Services</h3>
                <p className="text-white/70">
                  From custom carrier integrations to private deployments, our expert team supports you every step of the way.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <CTASection
          title="Ready to elevate your platform with shipping capabilities?"
          description="Join innovative platforms that trust Karrio for their shipping infrastructure."
        />
      </div>
    </>
  );
}
