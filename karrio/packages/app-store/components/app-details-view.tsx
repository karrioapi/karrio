"use client";
import { getAppLogo, getAppScreenshots, loadAppReadme } from "../lib/assets";
import { SheetHeader, SheetTitle } from "@karrio/ui/components/ui/sheet";
import { Globe, Mail, Check, X, FileText, Image } from "lucide-react";
import { Button } from "@karrio/ui/components/ui/button";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { MarkdownRenderer, AppErrorBoundary } from "@karrio/core";
import React, { useState, useEffect } from "react";

interface PhysicalApp {
  id: string;
  manifest: any;
  isInstalled: boolean;
  installation?: any;
}

interface AppDetailsFormProps {
  app: PhysicalApp;
  onClose: () => void;
}

export function AppDetailsForm({ app, onClose }: AppDetailsFormProps) {
  const [readmeContent, setReadmeContent] = useState<string | null>(null);
  const [readmeLoading, setReadmeLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'screenshots' | 'readme'>('overview');

  const appLogo = getAppLogo(app.manifest);
  const screenshots = getAppScreenshots(app.manifest);

  // Load README content
  useEffect(() => {
    const loadReadme = async () => {
      setReadmeLoading(true);
      try {
        const content = await loadAppReadme(app.manifest);
        setReadmeContent(content);
      } catch (error) {
        console.warn('Failed to load README:', error);
      } finally {
        setReadmeLoading(false);
      }
    };

    if (activeTab === 'readme') {
      loadReadme();
    }
  }, [activeTab, app.manifest]);

  return (
    <AppErrorBoundary
      context="App Details View"
      showDetails={process.env.NODE_ENV === 'development'}
    >
      <div className="h-full flex flex-col">
        <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">

          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <div className="w-16 h-16 rounded-lg flex items-center justify-center flex-shrink-0 overflow-hidden">
                <img
                  src={appLogo}
                  alt={`${app.manifest.name} logo`}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    // Fallback to letter avatar if image fails to load
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                    target.parentElement!.innerHTML = `
                    <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-xl font-semibold">
                      ${app.manifest.name?.charAt(0) || 'A'}
                    </div>
                  `;
                  }}
                />
              </div>
              <div className="flex-1 min-w-0">
                <h2 className="text-xl font-semibold text-slate-900 mb-1">
                  {app.manifest.name}
                </h2>
                <p className="text-sm text-slate-600 mb-2">
                  by {app.manifest.developer?.name || 'Unknown Developer'}
                </p>
                {app.isInstalled && (
                  <Badge variant="default" className="text-xs">
                    <Check className="w-3 h-3 mr-1" />
                    Installed
                  </Badge>
                )}
              </div>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <SheetTitle className="text-lg font-semibold">
              App Details
            </SheetTitle>
            <div>
              <Button variant="ghost" size="sm" onClick={onClose} className="p-0 rounded-full">
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </SheetHeader>

        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-6 pb-32">
          {/* App Header */}

          {/* Tab Navigation */}
          <div className="space-y-4">
            <div className="border-b border-slate-200">
              <nav className="flex space-x-8">
                <button
                  onClick={() => setActiveTab('overview')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${activeTab === 'overview'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                    }`}
                >
                  Overview
                </button>
                {screenshots.length > 0 && (
                  <button
                    onClick={() => setActiveTab('screenshots')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-1 ${activeTab === 'screenshots'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                      }`}
                  >
                    <Image className="w-4 h-4" />
                    Screenshots ({screenshots.length})
                  </button>
                )}
                {app.manifest.assets?.readme && (
                  <button
                    onClick={() => setActiveTab('readme')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-1 ${activeTab === 'readme'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                      }`}
                  >
                    <FileText className="w-4 h-4" />
                    Documentation
                  </button>
                )}
              </nav>
            </div>
          </div>

          {/* Tab Content */}
          {activeTab === 'overview' && (
            <>
              {/* Description */}
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">Description</h3>
                  <p className="text-sm text-slate-700 leading-relaxed">
                    {app.manifest.description || 'No description available.'}
                  </p>
                </div>
              </div>

              {/* App Information */}
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-semibold text-slate-900 mb-4">App Information</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-slate-50 rounded-md border">
                      <div>
                        <Label className="text-xs text-slate-700">Version</Label>
                        <p className="text-xs text-slate-500">{app.manifest.version || '1.0.0'}</p>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        v{app.manifest.version || '1.0.0'}
                      </Badge>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-slate-50 rounded-md border">
                      <div>
                        <Label className="text-xs text-slate-700">Category</Label>
                        <p className="text-xs text-slate-500">{app.manifest.category || 'General'}</p>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {app.manifest.category || 'General'}
                      </Badge>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-slate-50 rounded-md border">
                      <div>
                        <Label className="text-xs text-slate-700">Type</Label>
                        <p className="text-xs text-slate-500">{app.manifest.type || 'Integration'}</p>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {app.manifest.type || 'Integration'}
                      </Badge>
                    </div>
                  </div>
                </div>
              </div>

              {/* Features */}
              {app.manifest.features && app.manifest.features.length > 0 && (
                <div className="space-y-4">
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900 mb-2">Features</h3>
                    <div className="flex flex-wrap gap-2">
                      {app.manifest.features.map((feature: string) => (
                        <Badge key={feature} variant="secondary" className="text-xs">
                          {feature}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Pricing */}
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">Pricing</h3>
                  <div className="p-3 bg-slate-50 rounded-md border">
                    <p className="text-sm font-medium text-slate-900">
                      {app.manifest.pricing || 'Free'}
                    </p>
                  </div>
                </div>
              </div>

              {/* Contact Information */}
              {(app.manifest.developer?.website || app.manifest.developer?.email) && (
                <div className="space-y-4">
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900 mb-2">Contact</h3>
                    <div className="space-y-2">
                      {app.manifest.developer?.website && (
                        <div className="flex items-center gap-2 text-sm text-slate-600">
                          <Globe className="w-4 h-4" />
                          <a
                            href={app.manifest.developer.website}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hover:text-slate-900 hover:underline"
                          >
                            {app.manifest.developer.website}
                          </a>
                        </div>
                      )}
                      {app.manifest.developer?.email && (
                        <div className="flex items-center gap-2 text-sm text-slate-600">
                          <Mail className="w-4 h-4" />
                          <a
                            href={`mailto:${app.manifest.developer.email}`}
                            className="hover:text-slate-900 hover:underline"
                          >
                            {app.manifest.developer.email}
                          </a>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Disclaimer */}
              <div className="space-y-4">
                <div className="p-3 bg-slate-50 rounded-md border">
                  <p className="text-xs text-slate-500 leading-relaxed">
                    Every app published on the Karrio App Store is open source and thoroughly tested via
                    peer reviews. Nevertheless, Karrio, Inc. does not endorse or certify these apps unless
                    they are published by Karrio. If you encounter inappropriate content or behaviour
                    please report it.
                  </p>
                  <button className="text-xs text-red-600 hover:text-red-700 mt-2 flex items-center gap-1">
                    🚩 Report app
                  </button>
                </div>
              </div>
            </>
          )}

          {/* Screenshots Tab */}
          {activeTab === 'screenshots' && (
            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-slate-900 mb-4">Screenshots</h3>
              {screenshots.length > 0 ? (
                <div className="grid grid-cols-1 gap-4">
                  {screenshots.map((screenshot, index) => (
                    <div key={index} className="border rounded-lg overflow-hidden">
                      <img
                        src={screenshot}
                        alt={`Screenshot ${index + 1}`}
                        className="w-full h-auto"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.style.display = 'none';
                          target.parentElement!.innerHTML = `
                          <div class="w-full h-32 bg-slate-100 flex items-center justify-center text-slate-500">
                            <span>Screenshot not available</span>
                          </div>
                        `;
                        }}
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-slate-500">
                  <Image className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>No screenshots available</p>
                </div>
              )}
            </div>
          )}

          {/* README Tab */}
          {activeTab === 'readme' && (
            <div className="space-y-4">
              {readmeLoading ? (
                <div className="text-center py-8 text-slate-500">
                  <div className="animate-spin w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-2"></div>
                  <p>Loading documentation...</p>
                </div>
              ) : readmeContent ? (
                <div className="prose prose-sm max-w-none">
                  <AppErrorBoundary
                    context="App README Markdown"
                    showDetails={process.env.NODE_ENV === 'development'}
                    fallback={
                      <div className="text-center py-8 text-slate-500">
                        <FileText className="w-12 h-12 mx-auto mb-2 opacity-50" />
                        <p>Failed to render documentation</p>
                      </div>
                    }
                  >
                    <MarkdownRenderer content={readmeContent} />
                  </AppErrorBoundary>
                </div>
              ) : (
                <div className="text-center py-8 text-slate-500">
                  <FileText className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>No documentation available</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </AppErrorBoundary>
  );
}
