import {
  Network,
  Settings,
  Globe,
  Plug,
} from "lucide-react";
import { FeatureTabs } from "@karrio/console/components/feature-tabs";
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
              <span className="text-[#79e5dd] font-medium">Logistics Service Providers</span>
            </div>

            {/* Title */}
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 max-w-4xl mx-auto">
              Scale Your Logistics Operations with a Network of Partners
            </h1>

            {/* Description */}
            <p className="text-xl text-white/80 mb-10 max-w-3xl mx-auto">
              Drive operational efficiency and enhance your customer experience by integrating with a network of carriers through a single platform.
            </p>

            {/* CTA Buttons */}
            <div className="flex justify-center space-x-4">
              <Button size="lg" className="bg-[#5722cc] hover:bg-[#5722cc]/90">
                <Link href="/signup">Get Started</Link>
              </Button>
              <Button variant="outline" size="lg">
                <Link href="https://calendly.com/karrio/demo">Schedule a Demo</Link>
              </Button>
            </div>
          </div>
        </div>

        {/* Key Challenges Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,#5722cc0d,transparent_50%)]" />
          <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
            {/* Section Header */}
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Key Challenges for Logistics Service Providers
              </h2>
              <p className="text-white/80 text-lg">
                Modern LSPs face evolving challenges in a rapidly changing industry landscape.
              </p>
            </div>

            {/* Challenges Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Challenge 1 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
                <h3 className="text-xl font-semibold mb-4">Carrier Integration Complexity</h3>
                <p className="text-white/80">
                  Maintaining direct integrations with multiple carriers requires significant development resources and ongoing maintenance.
                </p>
              </div>

              {/* Challenge 2 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
                <h3 className="text-xl font-semibold mb-4">Client-Specific Requirements</h3>
                <p className="text-white/80">
                  Each client has unique shipping needs, requiring customized workflows and carrier selections that are difficult to scale.
                </p>
              </div>

              {/* Challenge 3 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
                <h3 className="text-xl font-semibold mb-4">Technology Stack Limitations</h3>
                <p className="text-white/80">
                  Legacy systems often struggle to adapt to changing carrier APIs and new shipping requirements.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Platform Solutions Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
          <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
            {/* Section Header */}
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                How Karrio Powers Logistics Service Providers
              </h2>
              <p className="text-white/80 text-lg">
                Our platform provides the flexibility and carrier diversity needed to streamline operations and serve clients more effectively.
              </p>
            </div>

            {/* Feature Tabs */}
            <div className="mb-20">
              <FeatureTabs
                tabs={[
                  {
                    label: "Network of Carriers",
                    value: "carriers",
                    icon: <Network />,
                    title: "Access a Global Carrier Ecosystem",
                    description: "Leverage out-of-the-box integrations with domestic and international carriers. No need to reinvent the wheel—your team can focus on innovating, not building carrier connections.",
                    features: [
                      "Pre-built integrations with major carriers",
                      "Continuous updates as carrier APIs evolve",
                      "Global coverage across multiple regions"
                    ],
                    demo: (
                      <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                        <Image
                          src="/placeholder.svg"
                          width={800}
                          height={400}
                          alt="Network of Carriers illustration"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    )
                  },
                  {
                    label: "Configurable Connections",
                    value: "connections",
                    icon: <Settings />,
                    title: "Quickly Customize Shipping Flows",
                    description: "Fine-tune shipping flows for each client. Configure service levels, packaging options, and shipping rules through a single platform.",
                    features: [
                      "Client-specific shipping rules and workflows",
                      "Custom service level management",
                      "Flexible packaging and label customization"
                    ],
                    demo: (
                      <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                        <Image
                          src="/placeholder.svg"
                          width={800}
                          height={400}
                          alt="Configurable Connections illustration"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    )
                  },
                  {
                    label: "Augment Solutions",
                    value: "augment",
                    icon: <Plug />,
                    title: "Plug Into Your Existing Stack",
                    description: "Seamlessly integrate Karrio into your existing operational stack and let us handle the intricate carrier complexities. Save thousands of development hours and costly maintenance overhead.",
                    features: [
                      "Flexible API integration with your systems",
                      "Reduce development and maintenance costs",
                      "Focus on your core business capabilities"
                    ],
                    demo: (
                      <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                        <Image
                          src="/placeholder.svg"
                          width={800}
                          height={400}
                          alt="Augment Solutions illustration"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    )
                  },
                  {
                    label: "Open Ecosystem",
                    value: "ecosystem",
                    icon: <Globe />,
                    title: "Open-Source Solution with Full Support",
                    description: "As an open-source solution, Karrio seamlessly integrates with proprietary systems and offers complete extensibility. When you need specialized carriers or custom workflows, our team provides full carrier onboarding and advanced integration services.",
                    features: [
                      "Open-source codebase for complete control",
                      "Expert services for custom integrations",
                      "Dedicated support for specialized workflows"
                    ],
                    demo: (
                      <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                        <Image
                          src="/placeholder.svg"
                          width={800}
                          height={400}
                          alt="Open Ecosystem illustration"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    )
                  },
                ]}
              />
            </div>
          </div>
        </section>

        {/* Example Workflow Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,#5722cc0d,transparent_50%)]" />
          <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
            {/* Section Header */}
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Example Workflow
              </h2>
              <p className="text-white/80 text-lg">
                How Karrio streamlines logistics operations for service providers
              </p>
            </div>

            {/* Workflow Diagram */}
            <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10 max-w-4xl mx-auto">
              <Image
                src="/placeholder.svg"
                width={1000}
                height={400}
                alt="LSP Workflow Diagram"
                className="w-full h-auto"
              />
              <div className="mt-8 text-center text-white/80">
                <p className="text-lg font-medium mb-2">Your LSP System {'->'} Karrio Platform {'->'} Multiple Carriers</p>
                <p>Streamline your shipping operations by connecting your existing systems to multiple carriers through a single integration.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Business Outcomes Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#5722cc0d,#0f082600)]" />
          <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
            {/* Section Header */}
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Business Outcomes
              </h2>
              <p className="text-white/80 text-lg">
                Tangible results for logistics service providers using Karrio
              </p>
            </div>

            {/* Outcomes Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              {/* Outcome 1 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
                <h3 className="text-xl font-semibold mb-4">40% Reduction in Integration Costs</h3>
                <p className="text-white/80">
                  Eliminate the need for custom carrier integrations and ongoing maintenance, significantly reducing your development costs.
                </p>
              </div>

              {/* Outcome 2 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
                <h3 className="text-xl font-semibold mb-4">60% Faster Onboarding</h3>
                <p className="text-white/80">
                  Rapidly onboard new clients with pre-built carrier integrations and customizable workflows, reducing time-to-value.
                </p>
              </div>

              {/* Outcome 3 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
                <h3 className="text-xl font-semibold mb-4">25% Improved Operational Efficiency</h3>
                <p className="text-white/80">
                  Streamline shipping operations with automated processes and reduced manual intervention, boosting overall productivity.
                </p>
              </div>

              {/* Outcome 4 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
                <h3 className="text-xl font-semibold mb-4">Enhanced Service Offering</h3>
                <p className="text-white/80">
                  Provide clients with more carrier options and service levels, strengthening your competitive advantage in the market.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <CTASection
          title="Ready to Transform Your Logistics Services?"
          description="Start offering more carrier options and optimized shipping flows to your clients."
          primaryButtonText="Get Started"
          primaryButtonHref="/signup"
          secondaryButtonText="Schedule a Demo"
          secondaryButtonHref="https://calendly.com/karrio/demo"
        />
      </div>
    </>
  );
}
