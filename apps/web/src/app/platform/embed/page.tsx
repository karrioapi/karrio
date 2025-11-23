"use client";

import {
  Shield,
  Network,
  Boxes,
  Building,
  Users,
  Globe,
  Zap,
  Plus,
  Minus,
} from "lucide-react";
import { BookDemoButton } from "@karrio/console/components/book-demo-button";
import { CTASection } from "@/components/cta-section";
import { Button } from "@karrio/ui/components/ui/button";
import { ShippingFeaturesTab } from "@/components/shipping-features-tabs";
import Image from "next/image";
import { useState } from "react";

// FAQ Component
function FAQItem({ question, answer, isOpen, onToggle }: {
  question: string;
  answer: string;
  isOpen: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="border border-white/10 rounded-lg bg-white/5 backdrop-blur-sm">
      <button
        className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-white/5 transition-colors"
        onClick={onToggle}
      >
        <span className="font-medium text-white">{question}</span>
        {isOpen ? (
          <Minus className="w-5 h-5 text-[#79e5dd] flex-shrink-0" />
        ) : (
          <Plus className="w-5 h-5 text-[#79e5dd] flex-shrink-0" />
        )}
      </button>
      {isOpen && (
        <div className="px-6 pb-4">
          <p className="text-white/70">{answer}</p>
        </div>
      )}
    </div>
  );
}

// FAQ Section Component
function FAQSection() {
  const [openItems, setOpenItems] = useState<Set<number>>(new Set());

  const toggleItem = (index: number) => {
    const newOpenItems = new Set(openItems);
    if (newOpenItems.has(index)) {
      newOpenItems.delete(index);
    } else {
      newOpenItems.add(index);
    }
    setOpenItems(newOpenItems);
  };

  const faqItems = [
    {
      question: "How do I know I need an embed license?",
      answer: "You need an embed license if you want to white-label Karrio and integrate it directly into your platform. This allows you to offer shipping capabilities to your users under your own branding and domain."
    },
    {
      question: "How much does an embed license cost?",
      answer: "Our embed license starts at $50,000 USD per year. This includes white-labeling rights, custom branding support, and unlimited usage within your platform. Contact our sales team for detailed pricing based on your specific requirements."
    },
    {
      question: "Do you offer support with your license?",
      answer: "Yes! Embed license customers receive priority support with dedicated account management, one-on-one developer calls, and priority bug fixes. We also provide implementation assistance and technical guidance."
    },
    {
      question: "What do I get with the embed license?",
      answer: "The embed license includes: full white-labeling rights, custom domain support, branded UI components, priority support, commercial usage rights, and the ability to resell shipping services to your customers."
    },
    {
      question: "What are the usage restrictions?",
      answer: "With the embed license, there are no volume restrictions on shipments or API calls. You can scale without worrying about usage limits. The license is tied to your organization and covers all your platforms and products."
    },
    {
      question: "How do I get started?",
      answer: "Contact our sales team to discuss your requirements. We'll provide a demo, custom proposal, and implementation timeline. Most customers are up and running within 2-4 weeks of signing."
    }
  ];

  return (
    <section className="py-20 relative">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,#5722cc0d,transparent_50%)]" />
      <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-4xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Frequently Asked Questions</h2>
          <p className="text-xl text-white/80">
            Everything you need to know about Karrio embed solutions
          </p>
        </div>

        <div className="space-y-4">
          {faqItems.map((item, index) => (
            <FAQItem
              key={index}
              question={item.question}
              answer={item.answer}
              isOpen={openItems.has(index)}
              onToggle={() => toggleItem(index)}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Page() {
  return (
    <>
      {/* Main content */}
      <div className="py-20 relative">
        {/* Hero Section */}
        <div className="relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,#5722cc20,transparent_50%)]" />
          <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl pt-8 pb-20 relative">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              {/* Left Column - Content */}
              <div className="space-y-8">
                {/* Tag line */}
                <div className="inline-block bg-white/5 backdrop-blur-sm px-4 py-2 rounded-full">
                  <span className="text-[#79e5dd] font-medium">Embed Solutions</span>
                </div>

                {/* Title */}
                <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold max-w-4xl">
                  Native shipping integrations inside your platform
                </h1>

                {/* Description */}
                <p className="text-xl text-white/80 max-w-2xl">
                  Embed multi-carrier shipping capabilities into your platform. Let your merchants connect their shipping accounts, automate fulfillment, and purchase labels directly within your ecosystem.
                </p>

                {/* CTA Buttons */}
                <div className="flex gap-4">
                  <BookDemoButton
                    size="lg"
                    className="bg-[#ff4800] hover:bg-[#ff4800]/90"
                    calLink="karrio/embed"
                  >
                    Contact Sales
                  </BookDemoButton>
                  <Button
                    size="lg"
                    variant="outline"
                    className="border-white/20 text-white/80 hover:bg-white/10"
                  >
                    GitHub
                  </Button>
                </div>
              </div>

              {/* Right Column - Workflow Illustration */}
              <div className="relative">
                <div className="bg-white/5 rounded-xl p-6 backdrop-blur-sm border border-white/10">
                  <div className="space-y-4">
                    {/* Workflow Steps */}
                    <div className="flex items-center gap-3 p-3 bg-white/10 rounded-lg">
                      <div className="w-8 h-8 bg-green-500/20 rounded flex items-center justify-center">
                        <Users className="w-4 h-4 text-green-400" />
                      </div>
                      <span className="text-sm text-white/80">Merchant Onboarding</span>
                      <div className="text-xs text-white/60">Link shipping accounts</div>
                    </div>

                    <div className="flex items-center gap-3 p-3 bg-white/10 rounded-lg">
                      <div className="w-8 h-8 bg-blue-500/20 rounded flex items-center justify-center">
                        <Globe className="w-4 h-4 text-blue-400" />
                      </div>
                      <span className="text-sm text-white/80">Multi-Carrier Management</span>
                      <div className="text-xs text-white/60">Unified carrier connections</div>
                    </div>

                    <div className="flex items-center gap-3 p-3 bg-white/10 rounded-lg">
                      <div className="w-8 h-8 bg-purple-500/20 rounded flex items-center justify-center">
                        <Zap className="w-4 h-4 text-purple-400" />
                      </div>
                      <span className="text-sm text-white/80">Automated Fulfillment</span>
                      <div className="text-xs text-white/60">Label purchase & tracking</div>
                    </div>

                    <div className="flex items-center gap-3 p-3 bg-white/10 rounded-lg">
                      <div className="w-8 h-8 bg-[#79e5dd]/20 rounded flex items-center justify-center">
                        <Network className="w-4 h-4 text-[#79e5dd]" />
                      </div>
                      <span className="text-sm text-white/80">Your Platform</span>
                      <div className="text-xs text-white/60">Branded shipping experience</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Company Logos Section */}
        <section className="py-16 relative">
          <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
            <div className="text-center">
              <p className="text-white/80 text-lg mb-8">
                The world's most popular shipping infrastructure platform for platforms and marketplaces including
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8 items-center justify-items-center">
                {/* Company Logos Placeholders */}
                <div className="bg-white/10 rounded-lg p-6 h-16 w-32 flex items-center justify-center">
                  <span className="text-white/80 font-semibold">Teleship</span>
                </div>
                <div className="bg-white/10 rounded-lg p-6 h-16 w-32 flex items-center justify-center">
                  <span className="text-white/80 font-semibold">JTL</span>
                </div>
                <div className="bg-white/10 rounded-lg p-6 h-16 w-32 flex items-center justify-center">
                  <span className="text-white/80 font-semibold">DTDC</span>
                </div>
                <div className="bg-white/10 rounded-lg p-6 h-16 w-32 flex items-center justify-center">
                  <span className="text-white/80 font-semibold">Ameripharma</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* How it Works Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
          <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
            <div className="text-center mb-16">
              <div className="text-[#ff4800] text-base font-medium mb-4">How it works</div>
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Make it yours</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Implement shipping features */}
              <div className="bg-white/5 rounded-xl p-6 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="aspect-video bg-black/40 rounded-lg mb-6 relative overflow-hidden">
                  <Image
                    src="/placeholder.svg"
                    alt="Implement shipping features illustration"
                    width={400}
                    height={300}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4">
                    <div className="text-white/90 font-mono text-sm">
                      {`npm install @karrio/embed`}
                    </div>
                  </div>
                </div>
                <h3 className="text-xl font-semibold mb-3">Implement our shipping components</h3>
                <p className="text-white/70">
                  Embed carrier connection management, rate comparison, and label generation directly into your platform. Deploy across web, mobile, or API endpoints.
                </p>
              </div>

              {/* Style to match your branding */}
              <div className="bg-white/5 rounded-xl p-6 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="aspect-video bg-black/40 rounded-lg mb-6 relative overflow-hidden">
                  <Image
                    src="/placeholder.svg"
                    alt="Style customization illustration"
                    width={400}
                    height={300}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4">
                    <div className="w-12 h-3 bg-[#79e5dd] rounded mb-2"></div>
                    <div className="w-8 h-3 bg-[#ff4800] rounded"></div>
                  </div>
                </div>
                <h3 className="text-xl font-semibold mb-3">Style it to match your platform branding</h3>
                <p className="text-white/70">
                  Complete white-label solution with your colors, logo, and domain. The shipping interface feels native to your platform while powered by Karrio.
                </p>
              </div>

              {/* Allow merchants to connect carriers */}
              <div className="bg-white/5 rounded-xl p-6 backdrop-blur-sm border border-white/10 hover:border-[#79e5dd]/30 transition-all">
                <div className="aspect-video bg-black/40 rounded-lg mb-6 relative overflow-hidden">
                  <Image
                    src="/placeholder.svg"
                    alt="Merchant carrier connections illustration"
                    width={400}
                    height={300}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <div className="absolute top-4 left-4 w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                    <Users className="w-6 h-6 text-white" />
                  </div>
                </div>
                <h3 className="text-xl font-semibold mb-3">Allow merchants to link their shipping accounts</h3>
                <p className="text-white/70">
                  Enable your merchants to connect their own carrier accounts, manage shipping rules, and automate fulfillment processes directly within your ecosystem.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Comprehensive Shipping Features Section */}
        <ShippingFeaturesTab />

        {/* Integrations Showcase Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,#5722cc0d,transparent_50%)]" />
          <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Stand out from the competition and get stickier customers
              </h2>
            </div>

            <div className="grid md:grid-cols-3 gap-8 text-center mb-16">
              <div className="space-y-4">
                <h3 className="text-xl font-semibold">Connect to any carrier</h3>
                <p className="text-white/70">
                  ✓ 30+ carrier integrations plus custom connectors for regional providers.
                  Enable your merchants to use their preferred shipping partners.
                </p>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold">Let your merchants ship themselves</h3>
                <p className="text-white/70">
                  Empower merchants with self-service shipping tools. They can connect carriers, set up shipping rules, and manage fulfillment without leaving your platform.
                </p>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold">Extensive partner network</h3>
                <p className="text-white/70">
                  Access major carriers like FedEx, UPS, DHL, and USPS, plus regional providers and last-mile delivery services worldwide.
                </p>
              </div>
            </div>

            {/* Integration Preview */}
            <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10 max-w-4xl mx-auto">
              <div className="aspect-video bg-black/40 rounded-lg relative overflow-hidden">
                <Image
                  src="/placeholder.svg"
                  alt="Carrier integrations showcase"
                  width={800}
                  height={400}
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                <div className="absolute inset-4 flex flex-wrap gap-3 items-center justify-center">
                  {/* Carrier Icons/Names */}
                  {['FedEx', 'UPS', 'DHL', 'USPS', 'TNT', 'Aramex', 'Canada Post', 'Purolator'].map((carrier) => (
                    <div key={carrier} className="bg-white/10 backdrop-blur-sm px-3 py-2 rounded-lg text-sm text-white/80">
                      {carrier}
                    </div>
                  ))}
                  <div className="bg-[#79e5dd]/20 backdrop-blur-sm px-3 py-2 rounded-lg text-sm text-[#79e5dd]">
                    +22 more
                  </div>
                </div>
              </div>
              <div className="mt-6 text-center">
                <p className="text-white/80">
                  The world's most popular shipping infrastructure platform for platforms and marketplaces
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Scale Your Operations Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-[conic-gradient(from_180deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
          <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
            <div className="bg-gradient-to-r from-[#5722cc]/20 to-[#79e5dd]/20 rounded-xl p-8 md:p-12 backdrop-blur-sm border border-white/10 text-center">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Scale your company's operations with our advanced on-prem or cloud shipping automation
              </h2>
              <div className="mt-8">
                <BookDemoButton
                  size="lg"
                  className="bg-[#4A90E2] hover:bg-[#4A90E2]/90"
                  calLink="karrio/enterprise"
                >
                  Contact Sales
                </BookDemoButton>
              </div>
            </div>
          </div>
        </section>

        {/* There's Nothing You Can't Automate Section */}
        <section className="py-20 relative">
          <div className="absolute inset-0 bg-gradient-to-b from-[#ff4800]/10 via-transparent to-transparent" />
          <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
            <div className="bg-gradient-to-r from-[#ff4800]/20 to-[#5722cc]/20 rounded-xl p-8 md:p-12 backdrop-blur-sm border border-white/10 text-center">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                There's no shipping challenge you can't solve with Karrio
              </h2>
              <p className="text-xl text-white/80 mb-8 max-w-2xl mx-auto">
                Our platform customers' words, not ours. Skeptical?{' '}
                <span className="text-[#ff4800] font-semibold">Try it out</span>{' '}
                and see how your merchants ship faster.
              </p>
              <div className="mt-8">
                <BookDemoButton
                  size="lg"
                  className="bg-[#ff4800] hover:bg-[#ff4800]/90"
                  calLink="karrio/embed"
                >
                  Start building
                </BookDemoButton>
              </div>
            </div>
          </div>
        </section>


        {/* FAQ Section */}
        <FAQSection />

        {/* CTA Section */}
        <CTASection
          title="Ready to embed shipping into your platform?"
          description="Join the companies using Karrio to power their shipping infrastructure and deliver exceptional customer experiences."
        />
      </div>
    </>
  );
}
