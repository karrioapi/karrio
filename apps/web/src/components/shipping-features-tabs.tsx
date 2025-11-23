"use client";

import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from "@karrio/ui/components/ui/tabs";
import { useMediaQuery } from "@karrio/ui/hooks/use-media-query";
import {
  Globe,
  Zap,
  Users,
  Shield,
  Network,
  Settings,
  Truck,
  BarChart3,
  CheckCircle
} from "lucide-react";
import Image from "next/image";
import { useState } from "react";

interface ShippingFeature {
  icon: React.ReactNode;
  title: string;
  description: string;
}

interface ShippingTab {
  id: string;
  label: string;
  title: string;
  description: string;
  features: ShippingFeature[];
  demo: React.ReactNode;
  codeExample: {
    comment: string;
    code: string;
  };
}

interface ShippingFeaturesTabsProps {
  title?: string;
  subtitle?: string;
}

export function ShippingFeaturesTab({
  title = "Comprehensive shipping features when you need them",
  subtitle = "Built for platforms and marketplaces"
}: ShippingFeaturesTabsProps) {
  const [activeTab, setActiveTab] = useState("multi-carrier");
  const isMobile = useMediaQuery("(max-width: 768px)");

  const tabs: ShippingTab[] = [
    {
      id: "multi-carrier",
      label: "Multi-carrier connections",
      title: "Multi-carrier connections management",
      description: "Enable merchants to connect and manage multiple carrier accounts from a unified interface with secure credential handling and real-time monitoring.",
      features: [
        {
          icon: <Globe className="w-5 h-5 text-[#79e5dd]" />,
          title: "Enable merchants to connect multiple carriers",
          description: "Provide a unified interface for merchants to manage connections with FedEx, UPS, DHL, USPS, and regional carriers."
        },
        {
          icon: <Shield className="w-5 h-5 text-[#79e5dd]" />,
          title: "Secure credential management",
          description: "Handle carrier API credentials securely with encrypted storage and automatic token refresh."
        },
        {
          icon: <Network className="w-5 h-5 text-[#79e5dd]" />,
          title: "Real-time connection monitoring",
          description: "Monitor carrier API health and connection status with automatic failover and retry logic."
        }
      ],
      demo: (
        <div className="aspect-video bg-black/40 rounded-lg relative overflow-hidden">
          <Image
            src="/placeholder.svg"
            alt="Multi-carrier connections management"
            width={600}
            height={400}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <div className="absolute bottom-4 left-4 right-4">
            <div className="text-white/90 text-sm font-medium">
              Carrier Management Dashboard
            </div>
          </div>
        </div>
      ),
      codeExample: {
        comment: "// Enable merchant carrier connections",
        code: `const connection = await karrio.carriers.connect({
  merchant_id: "merchant_123",
  carrier: "fedex",
  credentials: merchant.fedex_api_key
});`
      }
    },
    {
      id: "fulfillment",
      label: "Automate fulfillment",
      title: "Automate fulfillment and label purchase",
      description: "Streamline order processing with intelligent rate shopping, automated label generation, and real-time tracking across all carrier networks.",
      features: [
        {
          icon: <Zap className="w-5 h-5 text-[#79e5dd]" />,
          title: "Intelligent rate shopping",
          description: "Automatically compare rates across all connected carriers to find the best shipping options for each order."
        },
        {
          icon: <Truck className="w-5 h-5 text-[#79e5dd]" />,
          title: "Automated label generation",
          description: "Generate shipping labels instantly with customizable templates and automated customs documentation."
        },
        {
          icon: <BarChart3 className="w-5 h-5 text-[#79e5dd]" />,
          title: "Real-time tracking integration",
          description: "Provide customers with live tracking updates and delivery notifications across all carriers."
        }
      ],
      demo: (
        <div className="aspect-video bg-black/40 rounded-lg relative overflow-hidden">
          <Image
            src="/placeholder.svg"
            alt="Automated fulfillment workflow"
            width={600}
            height={400}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <div className="absolute bottom-4 left-4 right-4">
            <div className="text-white/90 text-sm font-medium">
              Automated Fulfillment Pipeline
            </div>
          </div>
        </div>
      ),
      codeExample: {
        comment: "// Automate fulfillment process",
        code: `const shipment = await karrio.shipments.create({
  merchant_id: "merchant_123",
  auto_rate_shop: true,
  service_preference: "fastest",
  auto_purchase: true
});`
      }
    },
    {
      id: "merchant-linking",
      label: "Merchant account linking",
      title: "Merchant account linking",
      description: "Allow merchants to seamlessly connect their existing carrier accounts or set up new ones through your platform with guided onboarding flows.",
      features: [
        {
          icon: <Users className="w-5 h-5 text-[#79e5dd]" />,
          title: "Guided carrier onboarding",
          description: "Step-by-step setup process for merchants to connect their carrier accounts with validation and testing."
        },
        {
          icon: <Settings className="w-5 h-5 text-[#79e5dd]" />,
          title: "Custom shipping rules",
          description: "Enable merchants to configure their own shipping rules, zones, and pricing strategies within your platform."
        },
        {
          icon: <CheckCircle className="w-5 h-5 text-[#79e5dd]" />,
          title: "Account verification",
          description: "Automated verification of carrier credentials with fallback options and troubleshooting guidance."
        }
      ],
      demo: (
        <div className="aspect-video bg-black/40 rounded-lg relative overflow-hidden">
          <Image
            src="/placeholder.svg"
            alt="Merchant account linking interface"
            width={600}
            height={400}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <div className="absolute bottom-4 left-4 right-4">
            <div className="text-white/90 text-sm font-medium">
              Merchant Carrier Setup
            </div>
          </div>
        </div>
      ),
      codeExample: {
        comment: "// Guide merchant through carrier setup",
        code: `const setup = await karrio.merchants.setupCarrier({
  merchant_id: "merchant_123",
  carrier: "ups",
  guided_flow: true,
  verify_credentials: true
});`
      }
    }
  ];

  const currentTab = tabs.find(tab => tab.id === activeTab) || tabs[0];

  return (
    <section className="py-20 relative">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,#5722cc0d,transparent_50%)]" />
      <div className="container mx-auto relative px-4 sm:px-6 lg:px-2 max-w-6xl">
        <div className="bg-white/5 rounded-xl p-8 backdrop-blur-sm border border-white/10">
          {/* Header */}
          <div className="text-center mb-12">
            <h3 className="text-2xl md:text-3xl font-bold mb-3 bg-gradient-to-r from-white via-[#79e5dd] to-white bg-clip-text text-transparent">
              {title}
            </h3>
            <p className="text-white/70 text-lg">{subtitle}</p>
            <div className="mt-6 h-px w-24 mx-auto bg-gradient-to-r from-transparent via-[#79e5dd] to-transparent" />
          </div>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            {/* Enhanced Tab Headers */}
            <div className="flex justify-center mb-12">
              <TabsList className="bg-black/30 backdrop-blur-sm border border-white/10 rounded-2xl p-2 gap-2 h-auto">
                {tabs.map((tab) => (
                  <TabsTrigger
                    key={tab.id}
                    value={tab.id}
                    className="relative px-6 py-4 rounded-xl font-medium transition-all duration-200 data-[state=active]:bg-gradient-to-r data-[state=active]:from-[#5722cc] data-[state=active]:to-[#7c3aed] data-[state=active]:text-white data-[state=active]:shadow-lg data-[state=active]:scale-105 text-white/70 hover:text-white hover:bg-white/5 flex-col gap-1 min-w-[140px] text-center"
                  >
                    <div className="text-sm whitespace-nowrap">{tab.label}</div>
                    {activeTab === tab.id && (
                      <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-[#79e5dd] rounded-full animate-pulse" />
                    )}
                  </TabsTrigger>
                ))}
              </TabsList>
            </div>

            {/* Tab Content */}
            {tabs.map((tab) => (
              <TabsContent key={tab.id} value={tab.id} className="space-y-8">
                {/* Content Grid */}
                <div className="grid lg:grid-cols-2 gap-12 items-start">
                  {/* Left Content */}
                  <div className="space-y-6">
                    <div>
                      <h4 className="text-2xl font-bold text-white mb-4">{tab.title}</h4>
                      <p className="text-white/80 text-lg leading-relaxed">{tab.description}</p>
                    </div>

                    <div className="space-y-6">
                      {tab.features.map((feature, index) => (
                        <div key={index} className="flex items-start gap-4 group">
                          <div className="flex-shrink-0 p-2 rounded-lg bg-[#79e5dd]/10 group-hover:bg-[#79e5dd]/20 transition-colors">
                            {feature.icon}
                          </div>
                          <div>
                            <h5 className="font-semibold text-white mb-2 group-hover:text-[#79e5dd] transition-colors">
                              {feature.title}
                            </h5>
                            <p className="text-white/70 text-sm leading-relaxed">
                              {feature.description}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Right Demo */}
                  <div className="relative">
                    {tab.demo}
                  </div>
                </div>

                {/* Code Example */}
                <div className="bg-black/40 rounded-xl p-6 border border-white/5">
                  <div className="font-mono text-sm">
                    <div className="text-green-400 mb-3">{tab.codeExample.comment}</div>
                    <pre className="text-white leading-relaxed">
                      <code>{tab.codeExample.code}</code>
                    </pre>
                  </div>
                </div>
              </TabsContent>
            ))}
          </Tabs>
        </div>
      </div>
    </section>
  );
}