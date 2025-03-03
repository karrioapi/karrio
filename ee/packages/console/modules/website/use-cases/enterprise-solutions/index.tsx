import {
  Code,
  Route,
  BarChart2,
  Layers,
  Shield,
  Network,
  Boxes,
  Building,
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
            <div className="flex justify-center space-x-4">
              <Button size="lg" className="bg-[#5722cc] hover:bg-[#5722cc]/90">
                <Link href="/enterprise-contact">Contact Sales</Link>
              </Button>
              <Button variant="outline" size="lg">
                <Link href="https://calendly.com/karrio/enterprise-demo">Schedule a Demo</Link>
              </Button>
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
              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Shield className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Stringent Regulatory Standards</h3>
                <p className="text-white/70">
                  Industries like healthcare or high-value freight rely on secure, compliant shipping processes.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Network className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Tailored Workflows & Branding</h3>
                <p className="text-white/70">
                  Standard out-of-the-box solutions rarely meet unique enterprise processes or brand requirements.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Boxes className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Complex System Integrations</h3>
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

            <FeatureTabs
              tabs={[
                {
                  label: "Unified API",
                  value: "unified-api",
                  icon: <Code />,
                  title: "Single Integration, Multiple Carriers",
                  description: "Connect to our unified API once and unlock access to all major global carriers. Eliminate the complexity of managing multiple carrier systems and APIs.",
                  features: [
                    "One integration for 100+ carrier connections",
                    "Reduced development time and resources",
                    "Simplified carrier onboarding process"
                  ],
                  demo: (
                    <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                      <Image
                        src="/placeholder.svg"
                        width={800}
                        height={400}
                        alt="Unified API illustration"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )
                },
                {
                  label: "Smart Routing",
                  value: "smart-routing",
                  icon: <Route />,
                  title: "Intelligent Shipping Optimization",
                  description: "Automatically select the optimal carrier and service based on your business rules, package characteristics, and delivery requirements.",
                  features: [
                    "Rule-based carrier selection",
                    "Cost and delivery time optimization",
                    "Automated routing decisions"
                  ],
                  demo: (
                    <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                      <Image
                        src="/placeholder.svg"
                        width={800}
                        height={400}
                        alt="Smart Routing illustration"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )
                },
                {
                  label: "Built for Scale",
                  value: "scale",
                  icon: <BarChart2 />,
                  title: "Enterprise-Grade Performance",
                  description: "Handle millions of shipments with a platform designed for high-volume operations. Our architecture delivers consistent performance even during peak periods.",
                  features: [
                    "High-throughput shipment processing",
                    "Horizontal scaling capability",
                    "Reliable performance at enterprise scale"
                  ],
                  demo: (
                    <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                      <Image
                        src="/placeholder.svg"
                        width={800}
                        height={400}
                        alt="Built for Scale illustration"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )
                },
                {
                  label: "White-Label Ready",
                  value: "white-label",
                  icon: <Layers />,
                  title: "Customizable to Your Brand",
                  description: "Deliver a seamless, branded experience to your customers. Our white-label solution allows you to maintain brand consistency across every touchpoint.",
                  features: [
                    "Brand-consistent shipping portal",
                    "Customizable tracking interfaces",
                    "Branded notification emails"
                  ],
                  demo: (
                    <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                      <Image
                        src="/placeholder.svg"
                        width={800}
                        height={400}
                        alt="White-Label Ready illustration"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )
                },
              ]}
            />
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

            <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 max-w-4xl mx-auto">
              <div className="relative rounded-lg overflow-hidden aspect-video">
                <Image
                  src="/placeholder.svg"
                  width={1200}
                  height={675}
                  alt="Enterprise Workflow Diagram"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="mt-8 text-center text-white/80">
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
              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Shield className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Enhanced Security & Compliance</h3>
                <p className="text-white/70">
                  Maintain full control over data hosting and meet strict industry requirements.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Boxes className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Seamless Integration</h3>
                <p className="text-white/70">
                  Connect Karrio to internal systems for real-time visibility and automation.
                </p>
              </div>

              <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="w-12 h-12 rounded-lg bg-[#79e5dd]/10 flex items-center justify-center mb-6">
                  <Building className="w-6 h-6 text-[#79e5dd]" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Brand Consistency</h3>
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
          primaryButtonText="Get Started"
          primaryButtonHref="/signin"
          secondaryButtonText="Contact Sales"
          secondaryButtonHref="#"
        />
      </div>
    </>
  );
}
