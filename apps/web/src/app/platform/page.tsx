import {
  ArrowRight,
  Code,
  Globe,
  Layers,
  Bell,
  Settings,
  Maximize2,
} from "lucide-react";
import { FeatureShowcase } from "@/components/feature-showcase";
import { BookDemoButton } from "@/components/book-demo-button";
import { RoadmapSection } from "@/components/roadmap-section";
import { PricingSection } from "@/components/pricing-section";
import { Button } from "@karrio/ui/components/ui/button";
import { CodePreview } from "@/components/code-preview";
import { FeatureTabs } from "@/components/feature-tabs";
import { CTASection } from "@/components/cta-section";
import Image from "next/image";
import Link from "next/link";

export default async function LandingPage() {
  return (
    <>
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-24 pb-16">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,#5722cc1a,transparent_50%),radial-gradient(circle_at_bottom_left,#79e5dd1a,transparent_50%)]" />
        <div className="absolute inset-0 bg-[conic-gradient(from_90deg_at_50%_50%,#0f082600,#5722cc0d,#79e5dd0d,#ff48000d,#0f082600)]" />
        <div className="absolute inset-0 backdrop-blur-[100px]" />
        <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
          <div className="text-center space-y-8">
            <div className="inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1 text-sm backdrop-blur-sm">
              <span className="rounded-full bg-[#ff4800] px-1.5 py-0.5 text-xs font-medium text-white mr-2">
                New
              </span>
              {'Karrio 2025.5 is here'}
            </div>
            <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-white via-[#79e5dd] to-[#ff4800] bg-clip-text text-transparent pb-2">
              Modern Logistics, Redefined.
            </h1>
            <p className="text-lg md:text-xl text-white/80 max-w-2xl mx-auto">
              Empowering engineers, logistics providers, and enterprises with
              a modern shipping infrastructure. Karrio is your platform for smarter
              integrations, streamlined operations, and scalable logistics.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <BookDemoButton />
              <Button
                size="lg"
                variant="outline"
                className="border-white/20 text-white/80 hover:bg-white/10"
              >
                <Link href="/docs/self-hosting">Deploy Open Source</Link>
              </Button>
            </div>
          </div>

          {/* Feature Tabs */}
          <div className="mt-16 py-16">
            <div className="mx-auto relative w-full">
              <FeatureTabs
                tabs={[
                  {
                    icon: <Globe className="h-5 w-5" />,
                    label: "Logistics Network",
                    value: "logistics-network",
                    title: "Extensible carrier network",
                    description:
                      "Manage and connect with multiple carriers through a single, unified platform with advanced connection management capabilities.",
                    features: [
                      "Centralized carrier connection management",
                      "Automated carrier credential handling",
                      "Carrier-specific configuration APIs",
                      "Easy onboarding for new carriers",
                    ],
                    demo: (
                      <div className="aspect-[3/1] relative flex justify-center items-center">
                        <Image
                          src="/carrier-connection-illustration.svg"
                          alt="Tracking API interface demo"
                          width={1200}
                          height={400}
                          className="object-cover rounded-lg"
                        />
                      </div>
                    ),
                  },
                  {
                    icon: <Code className="h-5 w-5" />,
                    label: "Shipping Integration",
                    value: "shipping-integration",
                    title: "Unified shipping API",
                    description:
                      "Access a powerful set of APIs for end-to-end shipping operations, from rate comparison to label generation and shipment management.",
                    features: [
                      "Real-time multi-carrier rate fetching API",
                      "Efficient label generation API with customization options",
                      "Complete shipment lifecycle management API",
                      "Seamless integration with major carriers worldwide",
                    ],
                    demo: (
                      <div className="aspect-[3/1] relative flex justify-center items-center">
                        <Image
                          src="/carrier-integration-illustration.svg"
                          alt="Shipping integration illustration"
                          width={1200}
                          height={400}
                          className="object-cover rounded-lg"
                        />
                      </div>
                    ),
                  },
                  {
                    icon: <Bell className="h-5 w-5" />,
                    label: "Real-time Visibility",
                    value: "real-time-visibility",
                    title: "End-to-end data visibility",
                    description:
                      "Stay informed with comprehensive data visibility and automated updates for all your shipments across carriers.",
                    features: [
                      "Unified tracking API for all carriers",
                      "Automated background tracking updates",
                      "Real-time webhook notifications",
                      "Detailed event and API logs",
                    ],
                    demo: (
                      <div className="aspect-[3/1] relative flex justify-center items-center">
                        <Image
                          src="/live-data-illustration.svg"
                          alt="Live data visibility illustration"
                          width={1200}
                          height={400}
                          className="object-cover rounded-lg"
                        />
                      </div>
                    ),
                  },
                  {
                    icon: <Layers className="h-5 w-5" />,
                    label: "Document Generation",
                    value: "document-generation",
                    title: "Customizable document generation",
                    description:
                      "Create and customize shipping documents with a powerful templating engine that supports various document types and formats.",
                    features: [
                      "Custom document generation API",
                      "Advanced label design templating",
                      "GS1-compliant shipping document generation",
                      "Flexible invoice and customs documentation",
                    ],
                    demo: (
                      <div className="aspect-[3/1] relative flex justify-center items-center">
                        <Image
                          src="/document-generation-illustration.svg"
                          alt="Document Generation illustration"
                          width={1200}
                          height={400}
                          className="object-cover rounded-lg"
                        />
                      </div>
                    ),
                  },
                  {
                    icon: <Settings className="h-5 w-5" />,
                    label: "Automation",
                    value: "automation",
                    title: "Logistics automation",
                    description:
                      "Automate your logistics operations with intelligent shipping rules and customizable fulfillment workflows.",
                    features: [
                      "Customizable shipping rules engine",
                      "Automated fulfillment workflows",
                      "Smart carrier selection",
                      "Conditional routing and processing",
                    ],
                    demo: (
                      <div className="aspect-[3/1] relative flex justify-center items-center">
                        <Image
                          src="/automation-illustration.svg"
                          alt="Logistics Automation illustration"
                          width={1200}
                          height={400}
                          className="object-cover rounded-lg"
                        />
                      </div>
                    ),
                  },
                ]}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Value Proposition Section */}
      <section className="py-24 relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,#5722cc0d,transparent_50%)]" />
        <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
        <div className="absolute inset-0 backdrop-blur-[100px]" />
        <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12">
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center">
                <ArrowRight className="w-5 h-5 text-[#79e5dd]" />
              </div>
              <h3 className="text-lg font-semibold">Launch in days</h3>
              <p className="text-sm text-white/60 leading-relaxed">
                Use Karrio's hosted or embedded functionality to go live faster,
                and avoid the up-front costs and development time usually
                required for shipping integration.
              </p>
            </div>
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center">
                <Maximize2 className="w-5 h-5 text-[#79e5dd]" />
              </div>
              <h3 className="text-lg font-semibold">
                Manage shipping at scale
              </h3>
              <p className="text-sm text-white/60 leading-relaxed">
                Use tooling and services from Karrio so you don't have to
                dedicate extra resources to carrier integration, rate
                optimization, or compliance management.
              </p>
            </div>
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center">
                <Globe className="w-5 h-5 text-[#79e5dd]" />
              </div>
              <h3 className="text-lg font-semibold">Ship globally</h3>
              <p className="text-sm text-white/60 leading-relaxed">
                Help your users reach more customers worldwide with local
                carrier integrations and the ability to easily calculate duties,
                taxes, and customs documentation.
              </p>
            </div>
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center">
                <Layers className="w-5 h-5 text-[#79e5dd]" />
              </div>
              <h3 className="text-lg font-semibold">
                Build new revenue streams
              </h3>
              <p className="text-sm text-white/60 leading-relaxed">
                Optimize shipping revenue by collecting fees on each
                transaction. Monetize Karrio's capabilities by enabling premium
                features, automated workflows, and value-added services.
              </p>
            </div>
          </div>
          <div className="mt-20 text-center space-y-3">
            <div className="text-[#79e5dd] text-base font-medium">
              Ship with confidence
            </div>
            <h2 className="text-3xl md:text-4xl font-bold">
              Build a foundation for any logistics business
            </h2>
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_right,#ff48001a,transparent_70%)]" />
        <div className="absolute inset-0 bg-[conic-gradient(from_270deg_at_50%_50%,#0f082600,#5722cc0d,#79e5dd0d,#0f082600)]" />
        <div className="absolute inset-0 backdrop-blur-[100px]" />
        <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
          <div className="mb-16">
            <div className="text-[#79e5dd] mb-4">Use Cases</div>
            <h2 className="text-3xl md:text-5xl font-bold mb-4">
              Tailored solutions for specialized shipping needs
            </h2>
            <p className="text-white/60 max-w-3xl">
              From marketplaces to enterprise logistics, Karrio provides a customizable platform to meet the unique requirements of different business models and industries.
            </p>
          </div>
          <div className="space-y-12">
            <FeatureShowcase
              title="Scale Your Logistics Network"
              description="Build stronger partnerships and expand your network with our comprehensive logistics solutions designed for carriers and LSPs."
              learnMoreHref="/use-cases/logistics-providers"
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
                          <span className="text-white/80">Expand your carrier network through a single integration</span>
                        </li>
                        <li className="flex items-start gap-3">
                          <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                            <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                          </div>
                          <span className="text-white/80">Streamline cross-border shipping with automated documentation</span>
                        </li>
                        <li className="flex items-start gap-3">
                          <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                            <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                          </div>
                          <span className="text-white/80">Enhance operational efficiency with real-time tracking and visibility</span>
                        </li>
                        <li className="flex items-start gap-3">
                          <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                            <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                          </div>
                          <span className="text-white/80">Improve partner collaboration with advanced integration tools</span>
                        </li>
                      </ul>
                    </div>
                  ),
                }
              ]}
            />
            <FeatureShowcase
              title="Embed Shipping Into Your Platform"
              description="Empower your merchants with a robust network of fulfillment carriers, streamlining operations and enhancing customer satisfaction."
              learnMoreHref="/use-cases/platforms"
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
                          <span className="text-white/80">Embedded shipping capabilities for marketplaces and platforms</span>
                        </li>
                        <li className="flex items-start gap-3">
                          <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                            <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                          </div>
                          <span className="text-white/80">Offer multi-carrier shipping options with automated best-rate selection</span>
                        </li>
                        <li className="flex items-start gap-3">
                          <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                            <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                          </div>
                          <span className="text-white/80">White-labeled shipping portal with your branding</span>
                        </li>
                        <li className="flex items-start gap-3">
                          <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                            <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                          </div>
                          <span className="text-white/80">Comprehensive analytics and reporting for merchant insights</span>
                        </li>
                      </ul>
                    </div>
                  ),
                }
              ]}
            />
            <FeatureShowcase
              title="Enterprise-Grade Shipping Solutions"
              description="Specialized shipping solutions for government agencies, healthcare providers, and high-value shipment handlers requiring enhanced security and compliance."
              learnMoreHref="/use-cases/enterprise-solutions"
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
                          <span className="text-white/80">Enterprise-grade security with advanced compliance controls</span>
                        </li>
                        <li className="flex items-start gap-3">
                          <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                            <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                          </div>
                          <span className="text-white/80">Specialized workflows for sensitive and high-value shipments</span>
                        </li>
                        <li className="flex items-start gap-3">
                          <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                            <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                          </div>
                          <span className="text-white/80">Configurable approval processes and role-based permissions</span>
                        </li>
                        <li className="flex items-start gap-3">
                          <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                            <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                          </div>
                          <span className="text-white/80">Priority support with dedicated account management</span>
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

      {/* Developers Section */}
      <section className="py-24 relative overflow-x-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,#5722cc1a,transparent_70%)]" />
        <div className="absolute inset-0 bg-[conic-gradient(from_0deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
        <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl relative">
          <div className="text-center mb-12">
            <div className="text-[#79e5dd] mb-4 text-center">Developer-first design</div>
            <h2 className="text-3xl md:text-5xl font-bold mb-4">
              A unified platform with modern APIs
            </h2>
            <p className="text-white/60 max-w-2xl mx-auto">
              Karrio provides a single, elegant interface that abstracts dozens
              of carrier integrations.
            </p>
          </div>

          <div className="grid lg:grid-cols-[1fr,1.5fr] gap-12 mt-16">
            {/* Features Column */}
            <div className="space-y-8">
              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-lg bg-white/5 flex items-center justify-center">
                    <Code className="w-6 h-6 text-[#79e5dd]" />
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">
                    RESTful APIs, JSON responses
                  </h3>
                  <p className="text-white/60">
                    Modern API design with predictable resource-oriented URLs
                    and JSON responses.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-lg bg-white/5 flex items-center justify-center">
                    <ArrowRight className="w-6 h-6 text-[#79e5dd]" />
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">
                    Seamless dashboard integration
                  </h3>
                  <p className="text-white/60">
                    Integrate Karrio into your application with our ready-to-use
                    components.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-lg bg-white/5 flex items-center justify-center">
                    <Bell className="w-6 h-6 text-[#79e5dd]" />
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">
                    Real-time webhook events
                  </h3>
                  <p className="text-white/60">
                    Get instant updates for shipment status changes and tracking
                    events.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-lg bg-white/5 flex items-center justify-center">
                    <Globe className="w-6 h-6 text-[#79e5dd]" />
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">
                    Multi-carrier support
                  </h3>
                  <p className="text-white/60">
                    Connect with 30+ carriers through a single integration
                    point.
                  </p>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row items-start gap-4 pt-4">
                <Button
                  variant="outline"
                  className="bg-[#79e5dd] text-white hover:bg-[#79e5dd]/90"
                  asChild
                >
                  <Link href="/docs">Read the docs</Link>
                </Button>
                <Button
                  variant="outline"
                  className="border-white/20 hover:bg-white/10"
                  asChild
                >
                  <Link href="/platform#pricing">Get your API key</Link>
                </Button>
              </div>
            </div>

            {/* Code Example Column */}
            <div className="overflow-hidden p-0">
              <CodePreview
                languages={[
                  {
                    label: "Node.js",
                    value: "nodejs",
                    code: `// Get a shipment rate and create a label
import { Karrio } from '@karrio/sdk';

const karrio = new Karrio('sk_test_123456789');

const shipment = await karrio.shipments.create({
  service: "usps_priority",
  shipper: {
    postal_code: "V6M2V9",
    country_code: "CA",
  },
  recipient: {
    postal_code: "27401",
    country_code: "US",
  },
  parcels: [{
    weight: 1,
    width: 10,
    height: 10,
    length: 10,
  }]
});`,
                    response: `{
  "id": "shp_f8f8f8f8f8f8f8f8",
  "status": "created",
  "tracking_number": "9400100000000000000000",
  "label_url": "https://api.karrio.io/v1/labels/shp_f8f8f8f8",
  "tracking_url": "https://track.karrio.io/shp_f8f8f8f8",
  "created_at": "2024-01-01T00:00:00Z"
}`
                  },
                  {
                    label: "Python",
                    value: "python",
                    code: `# Get a shipment rate and create a label
from karrio.sdk import Karrio

karrio = Karrio('sk_test_123456789')

shipment = karrio.shipments.create({
    "service": "usps_priority",
    "shipper": {
        "postal_code": "V6M2V9",
        "country_code": "CA",
    },
    "recipient": {
        "postal_code": "27401",
        "country_code": "US",
    },
    "parcels": [{
        "weight": 1,
        "width": 10,
        "height": 10,
        "length": 10,
    }]
})`,
                    response: `{
  "id": "shp_f8f8f8f8f8f8f8f8",
  "status": "created",
  "tracking_number": "9400100000000000000000",
  "label_url": "https://api.karrio.io/v1/labels/shp_f8f8f8f8",
  "tracking_url": "https://track.karrio.io/shp_f8f8f8f8",
  "created_at": "2024-01-01T00:00:00Z"
}`
                  }
                ]}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Roadmap Section */}
      <RoadmapSection />

      {/* FAQ Section */}
      <section className="py-24 relative">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,#5722cc1a,transparent_70%)]" />
        <div className="absolute inset-0 bg-[conic-gradient(from_270deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
        <div className="absolute inset-0 backdrop-blur-[100px]" />
        <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
          <div className="text-center mb-16">
            <div className="text-[#79e5dd] mb-4">FAQ</div>
            <h2 className="text-3xl md:text-5xl font-bold mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-white/60 max-w-2xl mx-auto">
              Everything you need to know about Karrio and our services.
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="space-y-6">
              <div className="bg-white/5 rounded-lg p-6 backdrop-blur-sm border border-white/10">
                <h3 className="text-lg font-semibold mb-2">What is Karrio?</h3>
                <p className="text-white/60">
                  Karrio is an open-source shipping infrastructure for modern logistics. Our mission is to simplify shipping for developers and businesses of all sizes. We're open source, API-first, and self-serve.
                </p>
              </div>
              <div className="bg-white/5 rounded-lg p-6 backdrop-blur-sm border border-white/10">
                <h3 className="text-lg font-semibold mb-2">How is Karrio different from other shipping APIs?</h3>
                <p className="text-white/60">
                  1. We are API-first and built for developers. 2. We are open source, giving you full control and transparency. 3. We are designed for scale, from startups to enterprise. 4. Our unified data model abstracts away the complexity of individual carriers.
                </p>
              </div>
              <div className="bg-white/5 rounded-lg p-6 backdrop-blur-sm border border-white/10">
                <h3 className="text-lg font-semibold mb-2">Can I embed Karrio into my platform?</h3>
                <p className="text-white/60">
                  Yes! Our commercial license allows you to white-label Karrio and embed it directly into your platform. This includes custom branding, domain support, and unlimited usage starting at $50,000/year.
                </p>
              </div>
            </div>
            <div className="space-y-6">
              <div className="bg-white/5 rounded-lg p-6 backdrop-blur-sm border border-white/10">
                <h3 className="text-lg font-semibold mb-2">How much does Karrio cost?</h3>
                <p className="text-white/60">
                  Karrio is free to use if you self-host our open-source version. Our managed Scale platform starts at $499/month with pay-as-you-go pricing. For embedding into your platform, our commercial license starts at $50,000/year.
                </p>
              </div>
              <div className="bg-white/5 rounded-lg p-6 backdrop-blur-sm border border-white/10">
                <h3 className="text-lg font-semibold mb-2">What kind of support do you offer?</h3>
                <p className="text-white/60">
                  We offer community support via GitHub. Scale platform customers get email and Slack support. Enterprise and commercial license customers get dedicated account management, priority support with SLA, and one-on-one developer calls.
                </p>
              </div>
              <div className="bg-white/5 rounded-lg p-6 backdrop-blur-sm border border-white/10">
                <h3 className="text-lg font-semibold mb-2">Do I need my own carrier accounts?</h3>
                <p className="text-white/60">
                  Yes. Karrio is a universal API that plugs into your existing carrier accounts. This puts you in control of your rates and relationships. Think of it as your own white-label shipping platform, built on an open, modern infrastructure.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <CTASection
        title="Ready to Transform Your Shipping Operations?"
        description="Join hundreds of businesses that trust Karrio to power their shipping infrastructure."
      />
    </>
  );
}
