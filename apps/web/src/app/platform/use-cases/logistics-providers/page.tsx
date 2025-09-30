import { FeatureShowcase } from "@karrio/console/components/feature-showcase";
import { BookDemoButton } from "@karrio/console/components/book-demo-button";
import { Button } from "@karrio/ui/components/ui/button";
import { CTASection } from "@/components/cta-section";
import Link from "next/link";

export default async function Page() {
  return (
    <>
      {/* Main content */}
      <div className="py-20 relative">
        {/* Hero Section */}
        <div className="relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,#5722cc20,transparent_50%)]" />
          <div className="container mx-auto px-4 pt-8 pb-20 text-center max-w-6xl relative">
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
                <Link href="/#pricing">Get Started</Link>
              </Button>
              <BookDemoButton variant="outline" className="border-white/20 hover:bg-white/10" />
            </div>
          </div>
        </div>

        {/* Key Challenges Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,#5722cc0d,transparent_50%)]" />
          <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
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
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 md:p-6 border border-white/10">
                <h3 className="text-xl font-semibold mb-3 md:mb-4">Carrier Integration Complexity</h3>
                <p className="text-white/80">
                  Maintaining direct integrations with multiple carriers requires significant development resources and ongoing maintenance.
                </p>
              </div>

              {/* Challenge 2 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 md:p-6 border border-white/10">
                <h3 className="text-xl font-semibold mb-3 md:mb-4">Client-Specific Requirements</h3>
                <p className="text-white/80">
                  Each client has unique shipping needs, requiring customized workflows and carrier selections that are difficult to scale.
                </p>
              </div>

              {/* Challenge 3 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 md:p-6 border border-white/10">
                <h3 className="text-xl font-semibold mb-3 md:mb-4">Technology Stack Limitations</h3>
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
          <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
            {/* Section Header */}
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                How Karrio Powers Logistics Service Providers
              </h2>
              <p className="text-white/80 text-lg">
                Our platform provides the flexibility and carrier diversity needed to streamline operations and serve clients more effectively.
              </p>
            </div>

            {/* Feature Showcases */}
            <div className="space-y-12">
              <FeatureShowcase
                title="Access a Global Carrier Ecosystem"
                description="Leverage out-of-the-box integrations with domestic and international carriers. No need to reinvent the wheel—your team can focus on innovating, not building carrier connections."
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
                            <span className="text-white/80">Pre-built integrations with major carriers</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Continuous updates as carrier APIs evolve</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Global coverage across multiple regions</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />

              <FeatureShowcase
                title="Quickly Customize Shipping Flows"
                description="Fine-tune shipping flows for each client. Configure service levels, packaging options, and shipping rules through a single platform."
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
                            <span className="text-white/80">Client-specific shipping rules and workflows</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Custom service level management</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Flexible packaging and label customization</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />

              <FeatureShowcase
                title="Plug Into Your Existing Stack"
                description="Seamlessly integrate Karrio into your existing operational stack and let us handle the intricate carrier complexities. Save thousands of development hours and costly maintenance overhead."
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
                            <span className="text-white/80">Flexible API integration with your systems</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Reduce development and maintenance costs</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Focus on your core business capabilities</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />

              <FeatureShowcase
                title="Open-Source Solution with Full Support"
                description="As an open-source solution, Karrio seamlessly integrates with proprietary systems and offers complete extensibility. When you need specialized carriers or custom workflows, our team provides full carrier onboarding and advanced integration services."
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
                            <span className="text-white/80">Open-source codebase for complete control</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Expert services for custom integrations</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Dedicated support for specialized workflows</span>
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
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,#5722cc0d,transparent_50%)]" />
          <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
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
            <div className="bg-white/5 backdrop-blur-sm rounded-lg p-2 border border-white/10 max-w-4xl mx-auto">
              <div className="relative rounded-lg overflow-hidden bg-black/40" style={{ aspectRatio: '16/9' }}>
                <div className="absolute inset-0 flex items-center justify-center">
                  <svg width="100%" height="100%" viewBox="0 0 1200 675" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
                    {/* Clean Background with Minimal Gradient */}
                    <rect width="1200" height="675" fill="#080215" />

                    {/* Simple Large Gradient Shapes - Keeping these but simplified */}
                    <circle cx="300" cy="337" r="300" fill="url(#purpleGlowLSP)" opacity="0.12" />
                    <circle cx="900" cy="337" r="300" fill="url(#tealGlowLSP)" opacity="0.1" />

                    {/* LSP System Section (Left) */}
                    <g>
                      <rect x="120" y="232" width="230" height="210" rx="12" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="235" y="200" fill="white" fontSize="22" fontWeight="bold" textAnchor="middle">Logistics Service Provider</text>

                      {/* LSP Components */}
                      <rect x="150" y="262" width="170" height="45" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="235" y="290" fill="white" fontSize="16" textAnchor="middle">Order Management</text>

                      <rect x="150" y="317" width="170" height="45" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="235" y="345" fill="white" fontSize="16" textAnchor="middle">TMS</text>

                      <rect x="150" y="372" width="170" height="45" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="235" y="400" fill="white" fontSize="16" textAnchor="middle">Customer Portal</text>
                    </g>

                    {/* Karrio Platform Section (Middle) */}
                    <g>
                      <rect x="480" y="182" width="250" height="310" rx="12" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.15)" />
                      <text x="605" y="150" fill="white" fontSize="22" fontWeight="bold" textAnchor="middle">Karrio Platform</text>

                      {/* Platform Components */}
                      <rect x="510" y="212" width="190" height="50" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="605" y="243" fill="white" fontSize="16" textAnchor="middle">API Management</text>

                      <rect x="510" y="277" width="190" height="50" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="605" y="308" fill="white" fontSize="16" textAnchor="middle">Carrier Integrations</text>

                      <rect x="510" y="342" width="190" height="50" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="605" y="373" fill="white" fontSize="16" textAnchor="middle">Routing Optimization</text>

                      <rect x="510" y="407" width="190" height="50" rx="6" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="605" y="438" fill="white" fontSize="16" textAnchor="middle">Real-time Tracking</text>
                    </g>

                    {/* Multiple Carriers Section (Right) */}
                    <g>
                      {/* First Mile */}
                      <rect x="850" y="187" width="220" height="80" rx="10" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="960" y="222" fill="white" fontSize="18" fontWeight="600" textAnchor="middle">First Mile Carriers</text>
                      <text x="960" y="247" fill="white" fontSize="13" opacity="0.7" textAnchor="middle">Collection & Transportation</text>

                      {/* Freight Forwarders */}
                      <rect x="850" y="287" width="220" height="80" rx="10" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="960" y="322" fill="white" fontSize="18" fontWeight="600" textAnchor="middle">Freight Forwarders</text>
                      <text x="960" y="347" fill="white" fontSize="13" opacity="0.7" textAnchor="middle">International Shipping</text>

                      {/* Last Mile */}
                      <rect x="850" y="387" width="220" height="80" rx="10" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="960" y="422" fill="white" fontSize="18" fontWeight="600" textAnchor="middle">Last Mile Carriers</text>
                      <text x="960" y="447" fill="white" fontSize="13" opacity="0.7" textAnchor="middle">Final Delivery</text>

                      {/* Parcel Carriers */}
                      <rect x="900" y="487" width="190" height="40" rx="10" stroke="#5722cc" strokeWidth="1.5" strokeDasharray="4 2" fill="rgba(87, 34, 204, 0.05)" />
                      <text x="995" y="512" fill="white" fontSize="16" fontWeight="normal" textAnchor="middle">Parcel Networks</text>
                      <path d="M800 467 L870 487" stroke="#30D9B7" strokeWidth="1.5" strokeDasharray="3 2" />
                    </g>

                    {/* Data Flow Arrows - Main Flows */}
                    {/* LSP to Karrio Platform */}
                    <path d="M350 280 C400 280, 430 280, 480 280" stroke="#5722cc" strokeWidth="2.5" />
                    <path d="M472 275 L480 280 L472 285" fill="none" stroke="#5722cc" strokeWidth="2.5" />

                    <path d="M350 335 C400 335, 430 335, 480 335" stroke="#5722cc" strokeWidth="2.5" />
                    <path d="M472 330 L480 335 L472 340" fill="none" stroke="#5722cc" strokeWidth="2.5" />

                    <path d="M350 390 C400 390, 430 390, 480 390" stroke="#5722cc" strokeWidth="2.5" />
                    <path d="M472 385 L480 390 L472 395" fill="none" stroke="#5722cc" strokeWidth="2.5" />

                    {/* Karrio to Carriers */}
                    <path d="M730 227 H850" stroke="#30D9B7" strokeWidth="2.5" />
                    <path d="M842 222 L850 227 L842 232" fill="none" stroke="#30D9B7" strokeWidth="2.5" />

                    <path d="M730 327 H850" stroke="#30D9B7" strokeWidth="2.5" />
                    <path d="M842 322 L850 327 L842 332" fill="none" stroke="#30D9B7" strokeWidth="2.5" />

                    <path d="M730 427 H850" stroke="#30D9B7" strokeWidth="2.5" />
                    <path d="M842 422 L850 427 L842 432" fill="none" stroke="#30D9B7" strokeWidth="2.5" />

                    {/* Return Data Flow - Keeping these as they're important for the flow */}
                    <path d="M850 260 C800 260, 770 260, 730 260" stroke="#30D9B7" strokeWidth="1.5" strokeDasharray="5,3" />
                    <path d="M738 265 L730 260 L738 255" fill="none" stroke="#30D9B7" strokeWidth="1.5" />

                    <path d="M480 370 C430 370, 400 370, 350 370" stroke="#5722cc" strokeWidth="1.5" strokeDasharray="5,3" />
                    <path d="M358 375 L350 370 L358 365" fill="none" stroke="#5722cc" strokeWidth="1.5" />

                    {/* Enhanced Gradients Definitions - Simplified */}
                    <defs>
                      <radialGradient id="purpleGlowLSP" cx="0.5" cy="0.5" r="0.5" fx="0.5" fy="0.5">
                        <stop offset="0%" stopColor="#5722cc" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#5722cc" stopOpacity="0" />
                      </radialGradient>

                      <radialGradient id="tealGlowLSP" cx="0.5" cy="0.5" r="0.5" fx="0.5" fy="0.5">
                        <stop offset="0%" stopColor="#30D9B7" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#30D9B7" stopOpacity="0" />
                      </radialGradient>
                    </defs>
                  </svg>
                </div>
              </div>
              <div className="mt-6 md:mt-8 text-center text-white/80 p-2">
                <p className="text-lg font-medium mb-2">Your LSP System {'->'} Karrio Platform {'->'} Multiple Carriers</p>
                <p>Streamline your shipping operations by connecting your existing systems to multiple carriers through a single integration.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Business Outcomes Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#5722cc0d,#0f082600)]" />
          <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
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
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 md:p-6 border border-white/10">
                <h3 className="text-xl font-semibold mb-3 md:mb-4">40% Reduction in Integration Costs</h3>
                <p className="text-white/80">
                  Eliminate the need for custom carrier integrations and ongoing maintenance, significantly reducing your development costs.
                </p>
              </div>

              {/* Outcome 2 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 md:p-6 border border-white/10">
                <h3 className="text-xl font-semibold mb-3 md:mb-4">60% Faster Onboarding</h3>
                <p className="text-white/80">
                  Rapidly onboard new clients with pre-built carrier integrations and customizable workflows, reducing time-to-value.
                </p>
              </div>

              {/* Outcome 3 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 md:p-6 border border-white/10">
                <h3 className="text-xl font-semibold mb-3 md:mb-4">25% Improved Operational Efficiency</h3>
                <p className="text-white/80">
                  Streamline shipping operations with automated processes and reduced manual intervention, boosting overall productivity.
                </p>
              </div>

              {/* Outcome 4 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 md:p-6 border border-white/10">
                <h3 className="text-xl font-semibold mb-3 md:mb-4">Enhanced Service Offering</h3>
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
        />
      </div>
    </>
  );
}
