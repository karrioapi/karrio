import {
  Shield,
  Network,
  Boxes,
  Building,
} from "lucide-react";
import { FeatureShowcase } from "@karrio/console/components/feature-showcase";
import { BookDemoButton } from "@karrio/console/components/book-demo-button";
import { CTASection } from "@/components/cta-section";

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
              <span className="text-[#79e5dd] font-medium">Enterprise Solutions</span>
            </div>

            {/* Title */}
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 max-w-4xl mx-auto">
              Streamline Global Shipping at Enterprise Scale
            </h1>

            {/* Description */}
            <p className="text-xl text-white/80 mb-10 max-w-3xl mx-auto">
              Enhance your shipping operations with a robust, scalable solution designed for complex enterprise requirements and high-volume needs.
            </p>

            {/* CTA Buttons */}
            <div className="flex justify-center">
              <BookDemoButton
                size="lg"
                className="bg-[#5722cc] hover:bg-[#5722cc]/90"
                calLink="karrio/enterprise"
              >
                Contact Sales
              </BookDemoButton>
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
                Enterprises face unique challenges when implementing shipping solutions.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white/5 rounded-xl p-4 md:p-6 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-4 md:mb-6">
                  <Shield className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-2 md:mb-3">Stringent Regulatory Standards</h3>
                <p className="text-white/70">
                  Industries like healthcare or high-value freight rely on secure, compliant shipping processes.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-4 md:p-6 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-4 md:mb-6">
                  <Network className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-2 md:mb-3">Tailored Workflows & Branding</h3>
                <p className="text-white/70">
                  Standard out-of-the-box solutions rarely meet unique enterprise processes or brand requirements.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-4 md:p-6 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-4 md:mb-6">
                  <Boxes className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-2 md:mb-3">Complex System Integrations</h3>
                <p className="text-white/70">
                  Must seamlessly fit into existing ERP, WMS, or other enterprise software.
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
                Our enterprise-grade platform provides complete control and security for your shipping operations.
              </p>
            </div>

            <div className="space-y-12">
              <FeatureShowcase
                title="Single Integration, Multiple Carriers"
                description="Connect to our unified API once and unlock access to all major global carriers. Eliminate the complexity of managing multiple carrier systems and APIs."
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
                            <span className="text-white/80">One integration for 100+ carrier connections</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Reduced development time and resources</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Simplified carrier onboarding process</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />

              <FeatureShowcase
                title="Intelligent Shipping Optimization"
                description="Automatically select the optimal carrier and service based on your business rules, package characteristics, and delivery requirements."
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
                            <span className="text-white/80">Rule-based carrier selection</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Cost and delivery time optimization</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Automated routing decisions</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />

              <FeatureShowcase
                title="Enterprise-Grade Performance"
                description="Handle millions of shipments with a platform designed for high-volume operations. Our architecture delivers consistent performance even during peak periods."
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
                            <span className="text-white/80">High-throughput shipment processing</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Horizontal scaling capability</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Reliable performance at enterprise scale</span>
                          </li>
                        </ul>
                      </div>
                    ),
                  }
                ]}
              />

              <FeatureShowcase
                title="Customizable to Your Brand"
                description="Deliver a seamless, branded experience to your customers. Our white-label solution allows you to maintain brand consistency across every touchpoint."
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
                            <span className="text-white/80">Brand-consistent shipping portal</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Customizable tracking interfaces</span>
                          </li>
                          <li className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
                              <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                            </div>
                            <span className="text-white/80">Branded notification emails</span>
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
                See how Karrio integrates with your enterprise systems while maintaining security and compliance.
              </p>
            </div>

            <div className="bg-white/5 rounded-xl p-2 md:p-6 backdrop-blur-sm border border-white/10 max-w-4xl mx-auto">
              <div className="relative rounded-lg overflow-hidden aspect-video bg-black/40">
                <div className="absolute inset-0 flex items-center justify-center">
                  <svg width="100%" height="100%" viewBox="0 0 1200 675" fill="none" xmlns="http://www.w3.org/2000/svg">
                    {/* Clean Background */}
                    <rect width="1200" height="675" fill="#080215" />

                    {/* Enterprise Systems Section */}
                    <g>
                      <rect x="100" y="200" width="250" height="275" rx="15" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="225" y="170" fill="white" fontSize="24" fontWeight="bold" textAnchor="middle">Enterprise Systems</text>

                      {/* Enterprise System Components */}
                      <rect x="130" y="230" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="225" y="262" fill="white" fontSize="16" textAnchor="middle">ERP System</text>

                      <rect x="130" y="300" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="225" y="332" fill="white" fontSize="16" textAnchor="middle">WMS</text>

                      <rect x="130" y="370" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="225" y="402" fill="white" fontSize="16" textAnchor="middle">Order Management</text>
                    </g>

                    {/* Karrio Platform Section */}
                    <g>
                      <rect x="475" y="150" width="250" height="375" rx="15" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.15)" />
                      <text x="600" y="120" fill="white" fontSize="24" fontWeight="bold" textAnchor="middle">Karrio Platform</text>

                      {/* Security Layer */}
                      <rect x="475" y="150" width="250" height="60" rx="15" stroke="#5722cc" strokeWidth="0" fill="rgba(87, 34, 204, 0.3)" />
                      <text x="600" y="185" fill="white" fontSize="16" textAnchor="middle">Security & Compliance Layer</text>
                      <circle cx="510" y="180" r="10" fill="#30D9B7" fillOpacity="0.6" />
                      <path d="M505 180 L510 185 L515 175" stroke="white" strokeWidth="2" />
                      <circle cx="690" y="180" r="10" fill="#30D9B7" fillOpacity="0.6" />
                      <path d="M685 180 L690 185 L695 175" stroke="white" strokeWidth="2" />

                      {/* Platform Components */}
                      <rect x="505" y="230" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="600" y="262" fill="white" fontSize="16" textAnchor="middle">API Gateway</text>

                      <rect x="505" y="300" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="600" y="332" fill="white" fontSize="16" textAnchor="middle">Carrier Integrations</text>

                      <rect x="505" y="370" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="600" y="402" fill="white" fontSize="16" textAnchor="middle">Rate Management</text>

                      <rect x="505" y="440" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.1)" />
                      <text x="600" y="472" fill="white" fontSize="16" textAnchor="middle">Analytics Engine</text>
                    </g>

                    {/* Supply Chain Network Section */}
                    <g>
                      <rect x="850" y="200" width="250" height="275" rx="15" stroke="#5722cc" strokeWidth="2" fill="rgba(87, 34, 204, 0.1)" />
                      <text x="975" y="170" fill="white" fontSize="24" fontWeight="bold" textAnchor="middle">Supply Chain Network</text>

                      {/* Supply Chain Components */}
                      <rect x="880" y="230" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="975" y="262" fill="white" fontSize="16" textAnchor="middle">Carrier APIs</text>

                      <rect x="880" y="300" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="975" y="332" fill="white" fontSize="16" textAnchor="middle">Fulfillment Centers</text>

                      <rect x="880" y="370" width="190" height="50" rx="8" stroke="#30D9B7" strokeWidth="1.5" fill="rgba(48, 217, 183, 0.05)" />
                      <text x="975" y="402" fill="white" fontSize="16" textAnchor="middle">Last-Mile Delivery</text>
                    </g>

                    {/* Data Flow Arrows */}
                    {/* Enterprise to Karrio */}
                    <path d="M350 270 C400 270, 425 270, 475 270" stroke="#5722cc" strokeWidth="3" strokeDasharray="none" />
                    <path d="M465 265 L475 270 L465 275" fill="none" stroke="#5722cc" strokeWidth="3" />

                    <path d="M350 330 C400 330, 425 330, 475 330" stroke="#5722cc" strokeWidth="3" strokeDasharray="none" />
                    <path d="M465 325 L475 330 L465 335" fill="none" stroke="#5722cc" strokeWidth="3" />

                    <path d="M350 390 C400 390, 425 390, 475 390" stroke="#5722cc" strokeWidth="3" strokeDasharray="none" />
                    <path d="M465 385 L475 390 L465 395" fill="none" stroke="#5722cc" strokeWidth="3" />

                    {/* Karrio to Supply Chain */}
                    <path d="M725 270 C775 270, 800 270, 850 270" stroke="#30D9B7" strokeWidth="3" strokeDasharray="none" />
                    <path d="M840 265 L850 270 L840 275" fill="none" stroke="#30D9B7" strokeWidth="3" />

                    <path d="M725 330 C775 330, 800 330, 850 330" stroke="#30D9B7" strokeWidth="3" strokeDasharray="none" />
                    <path d="M840 325 L850 330 L840 335" fill="none" stroke="#30D9B7" strokeWidth="3" />

                    <path d="M725 390 C775 390, 800 390, 850 390" stroke="#30D9B7" strokeWidth="3" strokeDasharray="none" />
                    <path d="M840 385 L850 390 L840 395" fill="none" stroke="#30D9B7" strokeWidth="3" />

                    {/* Return Data Flow */}
                    <path d="M850 310 C800 310, 775 310, 725 310" stroke="#30D9B7" strokeWidth="1.5" strokeDasharray="5,5" />
                    <path d="M735 315 L725 310 L735 305" fill="none" stroke="#30D9B7" strokeWidth="1.5" />

                    <path d="M475 310 C425 310, 400 310, 350 310" stroke="#5722cc" strokeWidth="1.5" strokeDasharray="5,5" />
                    <path d="M360 315 L350 310 L360 305" fill="none" stroke="#5722cc" strokeWidth="1.5" />
                  </svg>
                </div>
              </div>
              <div className="mt-6 md:mt-8 text-center text-white/80 p-2">
                <p className="text-lg font-medium mb-2">Enterprise System {'->'} Karrio Platform {'->'} Supply Chain Network</p>
                <p>Unify and optimize your shipping logistics within your existing enterprise architecture.</p>
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
                Unlock enterprise-grade shipping capabilities with Karrio.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white/5 rounded-xl p-4 md:p-6 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-4 md:mb-6">
                  <Shield className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-2 md:mb-3">Enhanced Security & Compliance</h3>
                <p className="text-white/70">
                  Maintain full control over data hosting and meet strict industry requirements.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-4 md:p-6 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-4 md:mb-6">
                  <Boxes className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-2 md:mb-3">Seamless Integration</h3>
                <p className="text-white/70">
                  Connect Karrio to internal systems for real-time visibility and automation.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-4 md:p-6 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-4 md:mb-6">
                  <Building className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-2 md:mb-3">Brand Consistency</h3>
                <p className="text-white/70">
                  Present a shipping experience fully aligned with your corporate identity.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <CTASection
          title="Ready to secure your logistics infrastructure?"
          description="Join leading enterprises who trust Karrio for their most sensitive shipping operations."
        />
      </div>
    </>
  );
}
