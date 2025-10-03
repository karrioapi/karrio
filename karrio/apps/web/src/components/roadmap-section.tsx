"use client"

import { useState } from "react";
import { ChevronRight, Check } from "lucide-react";

interface RoadmapSubItem {
  title: string;
  status: "planned" | "in_progress" | "preview" | "completed";
}

interface RoadmapItem {
  title: string;
  status: "planned" | "in_progress" | "preview" | "completed";
  description: string;
  items: RoadmapSubItem[];
}

const ROADMAP_ITEMS: RoadmapItem[] = [
  {
    title: "Admin Dashboard",
    status: "completed",
    description: "Comprehensive admin tools for platform and carrier management",
    items: [
      { title: "Platform API", status: "completed" },
      { title: "System Carrier Management & Rate sheets", status: "completed" },
      { title: "Connected Account Management", status: "completed" },
      { title: "Markups Management", status: "completed" },
      { title: "Docs", status: "completed" }
    ]
  },
  {
    title: "Karrio Automation",
    status: "preview",
    description: "Advanced automation tools for shipping workflows and integrations",
    items: [
      { title: "Finalize Connections Management", status: "completed" },
      { title: "Shipping Rules Dashboard", status: "completed" },
      { title: "Finalize Cron Job support", status: "preview" },
      { title: "Shipping Rules API", status: "preview" },
      { title: "Docs", status: "in_progress" }
    ]
  },
  {
    title: "Karrio CLI",
    status: "preview",
    description: "Command-line tools for developers and integrations",
    items: [
      { title: "Finalize API reader", status: "completed" },
      { title: "Finalize Carrier integration cli", status: "preview" }
    ]
  },
  {
    title: "Customizable Shipper Dashboard",
    status: "in_progress",
    description: "Flexible and customizable dashboard solutions for shippers",
    items: [
      { title: "Portal app template", status: "planned" },
      { title: "Reusable Elements", status: "in_progress" }
    ]
  },
  {
    title: "Karrio Dashboard Apps",
    status: "in_progress",
    description: "Extensible app ecosystem for the Karrio platform",
    items: [
      { title: "Embedded apps toolkit", status: "in_progress" },
      { title: "Shopify app", status: "in_progress" },
      { title: "Custom app store", status: "in_progress" },
    ]
  },
  {
    title: "Carrier On-boarding Dev tool",
    status: "planned",
    description: "AI-powered tools for carrier integration",
    items: [
      { title: "AI assisted carrier integration", status: "planned" },
      { title: "Onboarding Lifecycle management", status: "planned" }
    ]
  },
  {
    title: "Karrio Enterprise Features",
    status: "planned",
    description: "Advanced features for enterprise customers",
    items: [
      { title: "Advanced Analytics", status: "planned" },
      { title: "SSO", status: "planned" },
      { title: "Audit Log (API + Management UI)", status: "planned" },
      { title: "Compliance Check: SOC2, HIPAA", status: "planned" }
    ]
  },
  {
    title: "Carrier Dashboard Mode",
    status: "planned",
    description: "Advanced carrier management and customization tools",
    items: [
      { title: "Advanced Rate sheets management", status: "preview" },
      { title: "Generic carrier hooks", status: "planned" },
      { title: "Custom Tracking Event API", status: "planned" },
      { title: "Custom Tracking Event mapping", status: "planned" },
      { title: "Advanced Label designer", status: "in_progress" }
    ]
  }
];

function StatusIndicator({ status }: { status: RoadmapSubItem["status"] }) {
  if (status === "completed") {
    return (
      <div className="w-6 h-6 rounded-full bg-emerald-500/20 flex items-center justify-center flex-shrink-0">
        <Check className="w-3.5 h-3.5 text-emerald-400" />
      </div>
    );
  }

  if (status === "in_progress") {
    return (
      <div className="w-6 h-6 rounded-full bg-amber-500/20 flex items-center justify-center flex-shrink-0">
        <div className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse" />
      </div>
    );
  }

  if (status === "preview") {
    return (
      <div className="w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center flex-shrink-0">
        <div className="w-2 h-2 rounded-full bg-purple-400" />
      </div>
    );
  }

  return (
    <div className="w-6 h-6 rounded-full bg-slate-500/10 flex items-center justify-center flex-shrink-0">
      <div className="w-2 h-2 rounded-full bg-slate-400/60" />
    </div>
  );
}

export function RoadmapSection() {
  const [selectedItem, setSelectedItem] = useState<RoadmapItem | null>(ROADMAP_ITEMS[0]);

  return (
    <section className="py-24 relative">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_left,#8b5cf61a,transparent_70%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,#10b98115,transparent_60%)]" />
      <div className="absolute inset-0 bg-[conic-gradient(from_90deg_at_50%_50%,#0f082600,#f59e0b0a,#8b5cf60a,#10b9810a,#0f082600)]" />
      <div className="absolute inset-0 backdrop-blur-[100px]" />
      <div className="container mx-auto px-2 relative max-w-6xl">
        <div className="text-center mb-16">
          <div className="text-transparent bg-gradient-to-r from-purple-400 via-amber-400 to-emerald-400 bg-clip-text font-semibold mb-4">Product Roadmap</div>
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
                  ? "bg-white/10 border-l-2 border-purple-400"
                  : "hover:bg-white/5"
                  }`}
                onClick={() => setSelectedItem(item)}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${item.status === "completed"
                    ? "bg-emerald-400"
                    : item.status === "in_progress"
                      ? "bg-amber-400 animate-pulse"
                      : item.status === "preview"
                        ? "bg-purple-400"
                        : "bg-slate-400/60"
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
              <div className="bg-white/5 rounded-lg p-4 backdrop-blur-sm border border-white/10">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className={`px-3 py-1 rounded-full text-sm font-medium ${selectedItem.status === "completed"
                      ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                      : selectedItem.status === "in_progress"
                        ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                        : selectedItem.status === "preview"
                          ? "bg-purple-500/20 text-purple-400 border border-purple-500/30"
                          : "bg-slate-500/10 text-slate-400 border border-slate-500/20"
                      }`}>
                      {selectedItem.status === "completed"
                        ? "Completed"
                        : selectedItem.status === "in_progress"
                          ? "In Progress"
                          : selectedItem.status === "preview"
                            ? "Preview"
                            : "Planned"}
                    </div>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-white/60">
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-emerald-400" />
                      <span>
                        {selectedItem.items.filter(i => i.status === "completed").length} completed
                      </span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-purple-400" />
                      <span>
                        {selectedItem.items.filter(i => i.status === "preview").length} preview
                      </span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-amber-400" />
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
                          className={`bg-white/5 rounded-lg p-4 border transition-all duration-200 hover:bg-white/[0.07] ${item.status === "completed"
                            ? "border-emerald-500/30 shadow-emerald-500/5 shadow-sm"
                            : item.status === "in_progress"
                              ? "border-amber-500/30 shadow-amber-500/5 shadow-sm"
                              : item.status === "preview"
                                ? "border-purple-500/30 shadow-purple-500/5 shadow-sm"
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
