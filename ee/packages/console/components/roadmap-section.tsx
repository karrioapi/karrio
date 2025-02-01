"use client"

import { useState } from "react";
import { ChevronRight, Check } from "lucide-react";

interface RoadmapSubItem {
  title: string;
  status: "completed" | "in_progress" | "planned";
}

interface RoadmapItem {
  title: string;
  status: "in_progress" | "planned" | "completed";
  description: string;
  items: RoadmapSubItem[];
}

const ROADMAP_ITEMS: RoadmapItem[] = [
  {
    title: "Admin Dashboard",
    status: "in_progress",
    description: "Comprehensive admin tools for platform and carrier management",
    items: [
      { title: "Platform API", status: "completed" },
      { title: "System Carrier Management & Rate sheets", status: "in_progress" },
      { title: "Connected Account Management", status: "in_progress" },
      { title: "Markups Management", status: "planned" },
      { title: "Docs", status: "planned" }
    ]
  },
  {
    title: "Karrio Automation",
    status: "in_progress",
    description: "Advanced automation tools for shipping workflows and integrations",
    items: [
      { title: "Finalize Cron Job support", status: "completed" },
      { title: "Shipping Rules API", status: "in_progress" },
      { title: "Shipping Rules Dashboard", status: "in_progress" },
      { title: "Finalize Connections Management", status: "planned" },
      { title: "Finalize Integration Presets Management", status: "planned" },
      { title: "Docs", status: "planned" }
    ]
  },
  {
    title: "Customizable Shipper Dashboard",
    status: "planned",
    description: "Flexible and customizable dashboard solutions for shippers",
    items: [
      { title: "Portal app template", status: "planned" },
      { title: "Reusable Elements", status: "planned" }
    ]
  },
  {
    title: "Karrio CLI",
    status: "planned",
    description: "Command-line tools for developers and integrations",
    items: [
      { title: "Finalize API reader", status: "planned" },
      { title: "Finalize Carrier integration cli", status: "planned" }
    ]
  },
  {
    title: "Karrio Enterprise Features",
    status: "planned",
    description: "Advanced features for enterprise customers",
    items: [
      { title: "SSO", status: "planned" },
      { title: "Audit Log (API + Management UI)", status: "planned" },
      { title: "Advanced Analytics", status: "planned" },
      { title: "Compliance Check", status: "planned" }
    ]
  },
  {
    title: "Karrio Dashboard Apps",
    status: "planned",
    description: "Extensible app ecosystem for the Karrio platform",
    items: [
      { title: "Embedded apps toolkit", status: "planned" },
      { title: "Billing reconciliation app", status: "planned" },
      { title: "Pickup management app", status: "planned" }
    ]
  },
  {
    title: "Carrier On-boarding Dev tool",
    status: "planned",
    description: "AI-powered tools for carrier integration",
    items: [
      { title: "AI assisted carrier integration", status: "planned" },
      { title: "Onboard Lifecycle management", status: "planned" }
    ]
  },
  {
    title: "Carrier Dashboard Mode",
    status: "planned",
    description: "Advanced carrier management and customization tools",
    items: [
      { title: "Generic carrier hooks", status: "planned" },
      { title: "Custom Tracking Event mapping", status: "planned" },
      { title: "Advanced Label designer", status: "planned" }
    ]
  }
];

function StatusIndicator({ status }: { status: RoadmapSubItem["status"] }) {
  if (status === "completed") {
    return (
      <div className="w-6 h-6 rounded-full bg-[#79e5dd]/20 flex items-center justify-center flex-shrink-0">
        <Check className="w-3.5 h-3.5 text-[#79e5dd]" />
      </div>
    );
  }

  return (
    <div className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center flex-shrink-0">
      <div className={`w-2 h-2 rounded-full ${status === "in_progress" ? "bg-[#ff4800]" : "bg-white/40"
        }`} />
    </div>
  );
}

export function RoadmapSection() {
  const [selectedItem, setSelectedItem] = useState<RoadmapItem | null>(ROADMAP_ITEMS[0]);

  return (
    <section className="py-24 relative">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_left,#5722cc1a,transparent_70%)]" />
      <div className="absolute inset-0 bg-[conic-gradient(from_90deg_at_50%_50%,#0f082600,#79e5dd0d,#0f082600)]" />
      <div className="absolute inset-0 backdrop-blur-[100px]" />
      <div className="container mx-auto px-4 relative max-w-[95%] xl:max-w-[1280px]">
        <div className="text-center mb-16">
          <div className="text-[#79e5dd] mb-4">Product Roadmap</div>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Building the future of logistics
          </h2>
          <p className="text-white/60 max-w-2xl mx-auto">
            Our vision for revolutionizing the shipping and logistics industry through continuous innovation and development.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 space-y-1">
            {ROADMAP_ITEMS.map((item) => (
              <div
                key={item.title}
                className={`group flex items-center justify-between px-4 py-3 rounded-lg cursor-pointer transition-all duration-200 ${selectedItem?.title === item.title
                  ? "bg-white/10 border-l-2 border-[#79e5dd]"
                  : "hover:bg-white/5"
                  }`}
                onClick={() => setSelectedItem(item)}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${item.status === "in_progress"
                    ? "bg-[#ff4800]"
                    : item.status === "completed"
                      ? "bg-[#79e5dd]"
                      : "bg-white/40"
                    }`} />
                  <h3 className={`text-base ${selectedItem?.title === item.title
                    ? "text-white font-medium"
                    : "text-white/60"
                    }`}>
                    {item.title}
                  </h3>
                </div>
                <ChevronRight className={`w-4 h-4 transition-transform ${selectedItem?.title === item.title
                  ? "text-white rotate-90"
                  : "text-white/40 group-hover:text-white/60"
                  }`} />
              </div>
            ))}
          </div>

          <div className="lg:col-span-2 h-fit">
            {selectedItem && (
              <div className="bg-white/5 rounded-lg p-8 backdrop-blur-sm border border-white/10">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className={`px-3 py-1 rounded-full text-sm ${selectedItem.status === "in_progress"
                      ? "bg-[#ff4800]/20 text-[#ff4800]"
                      : selectedItem.status === "completed"
                        ? "bg-[#79e5dd]/20 text-[#79e5dd]"
                        : "bg-white/10 text-white/60"
                      }`}>
                      {selectedItem.status === "in_progress"
                        ? "In Progress"
                        : selectedItem.status === "completed"
                          ? "Completed"
                          : "Planned"}
                    </div>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-white/60">
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-[#79e5dd]" />
                      <span>
                        {selectedItem.items.filter(i => i.status === "completed").length} completed
                      </span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-[#ff4800]" />
                      <span>
                        {selectedItem.items.filter(i => i.status === "in_progress").length} in progress
                      </span>
                    </div>
                  </div>
                </div>

                <h3 className="text-2xl font-bold mb-4">{selectedItem.title}</h3>
                <p className="text-white/60 text-lg mb-8">{selectedItem.description}</p>

                <div className="space-y-6">
                  <div>
                    <h4 className="text-lg font-semibold mb-4">Features</h4>
                    <div className="grid gap-4">
                      {selectedItem.items.map((item, index) => (
                        <div
                          key={index}
                          className={`bg-white/5 rounded-lg p-4 border transition-colors ${item.status === "completed"
                            ? "border-[#79e5dd]/20"
                            : item.status === "in_progress"
                              ? "border-[#ff4800]/20"
                              : "border-white/10"
                            }`}
                        >
                          <div className="flex items-start gap-3">
                            <StatusIndicator status={item.status} />
                            <div>
                              <p className="text-white/80">{item.title}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
