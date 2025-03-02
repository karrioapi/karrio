import {
  ChevronRight,
  Github,
  Box,
  Code,
  Bell,
  Grid,
  BarChart3,
  Settings,
  Globe,
  Layers,
  Store,
  DollarSign,
  Users,
  PanelLeft,
  Truck,
  ArrowRight,
  Boxes,
  Building,
  Network,
  Plug,
  Route,
  Shield,
  ShoppingCart,
} from "lucide-react";
import { FeatureShowcase } from "@karrio/console/components/feature-showcase";
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
                <Link href="/platform-signup">Get Started</Link>
              </Button>
              <Button variant="outline" size="lg">
                <Link href="https://calendly.com/karrio/platform-demo">Schedule a Demo</Link>
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

            <FeatureTabs
              tabs={[
                {
                  label: "Multi-Carrier Integration",
                  value: "multi-carrier",
                  icon: <Truck />,
                  title: "One API, All Major Carriers",
                  description: "Integrate once with Karrio and instantly offer your platform users access to a comprehensive network of global and regional carriers.",
                  features: [
                    "Over 100 carrier integrations available",
                    "Single API for all shipping functionality",
                    "Continuous carrier updates and maintenance"
                  ],
                  demo: (
                    <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                      <Image
                        src="/placeholder.svg"
                        width={800}
                        height={400}
                        alt="Multi-Carrier Integration illustration"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )
                },
                {
                  label: "Embedded Shipping",
                  value: "embedded",
                  icon: <ShoppingCart />,
                  title: "Native Shipping Experience",
                  description: "Provide a seamless, branded shipping experience directly within your platform. Let your users ship without ever leaving your environment.",
                  features: [
                    "White-labeled shipping interface",
                    "Embedded rating, label generation, and tracking",
                    "Customizable shipping workflows"
                  ],
                  demo: (
                    <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                      <Image
                        src="/placeholder.svg"
                        width={800}
                        height={400}
                        alt="Embedded Shipping illustration"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )
                },
                {
                  label: "Developer Experience",
                  value: "dev-experience",
                  icon: <Code />,
                  title: "Built for Developers",
                  description: "Our platform is designed with developers in mind, featuring clear documentation, robust SDKs, and a responsive support team to ensure successful integration.",
                  features: [
                    "Comprehensive API documentation",
                    "Client libraries in multiple languages",
                    "Developer-friendly sandbox environment"
                  ],
                  demo: (
                    <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                      <Image
                        src="/placeholder.svg"
                        width={800}
                        height={400}
                        alt="Developer Experience illustration"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )
                },
                {
                  label: "Revenue Opportunities",
                  value: "revenue",
                  icon: <Building />,
                  title: "New Revenue Streams",
                  description: "Create additional revenue streams by offering premium shipping services, negotiated rates, or custom carrier integrations to your platform users.",
                  features: [
                    "Markup capabilities on shipping rates",
                    "Premium shipping service tiers",
                    "Revenue sharing on transaction volume"
                  ],
                  demo: (
                    <div className="bg-black/20 aspect-video rounded-lg overflow-hidden">
                      <Image
                        src="/placeholder.svg"
                        width={800}
                        height={400}
                        alt="Revenue Opportunities illustration"
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
                See how Karrio integrates with your platform to provide seamless shipping experiences.
              </p>
            </div>

            <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 max-w-4xl mx-auto">
              <div className="relative rounded-lg overflow-hidden aspect-video">
                <Image
                  src="/placeholder.svg"
                  width={1200}
                  height={675}
                  alt="Platform Workflow Diagram"
                  className="w-full h-full object-cover"
                />
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
          primaryButtonText="Get Started"
          primaryButtonHref="/signin"
          secondaryButtonText="Contact Sales"
          secondaryButtonHref="#"
        />
      </div>
    </>
  );
}
