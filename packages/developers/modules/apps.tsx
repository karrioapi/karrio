"use client";
import { useEffect, useState } from "react";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { useLoader } from "@karrio/ui/core/components/loader";
import { Button } from "@karrio/ui/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@karrio/ui/components/ui/tabs";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@karrio/ui/components/ui/dialog";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Separator } from "@karrio/ui/components/ui/separator";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { Copy, Eye, EyeOff, Plus, Edit3, Trash2, ExternalLink, Settings } from "lucide-react";

export default function AppsPage() {
  const Component = (): JSX.Element => {
    const { setLoading } = useLoader();
    const { toast } = useToast();
    const [activeTab, setActiveTab] = useState("marketplace");
    const [showCreateDialog, setShowCreateDialog] = useState(false);
    const [selectedApp, setSelectedApp] = useState<any>(null);
    const [revealedSecrets, setRevealedSecrets] = useState<Record<string, boolean>>({});

    // Mock data - replace with actual GraphQL queries
    const marketplaceApps = [
      {
        id: "1",
        display_name: "ShipStation Integration",
        developer_name: "ShipStation",
        description: "Connect your ShipStation account to manage orders and shipments",
        features: ["Orders", "Shipments", "Tracking"],
        is_public: true,
        is_published: true,
        installation: null,
      },
      {
        id: "2",
        display_name: "WooCommerce Connector",
        developer_name: "WooCommerce",
        description: "Sync orders from your WooCommerce store",
        features: ["Orders", "Products", "Customers"],
        is_public: true,
        is_published: true,
        installation: { id: "inst_1", access_scopes: ["read:orders", "write:shipments"] },
      },
    ];

    const privateApps = [
      {
        id: "3",
        display_name: "My Custom App",
        developer_name: "John Doe",
        description: "Custom integration for my business",
        features: ["Custom API", "Webhooks"],
        client_id: "app_123456789",
        client_secret: "sk_test_123456789abcdef",
        redirect_uris: "https://myapp.com/callback",
        is_public: false,
        created_at: "2024-01-15T10:30:00Z",
      },
    ];

    const copyToClipboard = (text: string, label: string) => {
      navigator.clipboard.writeText(text);
      toast({ title: `${label} copied to clipboard` });
    };

    const toggleSecretVisibility = (appId: string) => {
      setRevealedSecrets(prev => ({
        ...prev,
        [appId]: !prev[appId]
      }));
    };

    return (
      <div className="tailwind-only">
        {/* Header */}
        <header className="px-0 pb-0 pt-4 flex justify-between items-center">
          <span className="title is-4">Developers</span>
        </header>

        {/* Navigation Tabs - keeping Bulma style for consistency */}
        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers" shallow={false} prefetch={false}>
                <span>Overview</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/apikeys" shallow={false} prefetch={false}>
                <span>API Keys</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/webhooks" shallow={false} prefetch={false}>
                <span>Webhooks</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/developers/apps" shallow={false} prefetch={false}>
                <span>Apps</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/events" shallow={false} prefetch={false}>
                <span>Events</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/logs" shallow={false} prefetch={false}>
                <span>Logs</span>
              </AppLink>
            </li>
          </ul>
        </div>

        {/* Main Content */}
        <div className="mt-6">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="marketplace">App Marketplace</TabsTrigger>
              <TabsTrigger value="installed">Installed Apps</TabsTrigger>
              <TabsTrigger value="developer">My Apps</TabsTrigger>
            </TabsList>

            {/* App Marketplace */}
            <TabsContent value="marketplace" className="space-y-4">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold">App Marketplace</h3>
                  <p className="text-sm text-muted-foreground">
                    Discover and install apps to extend your Karrio experience
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {marketplaceApps.map((app) => (
                  <Card key={app.id} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-base">{app.display_name}</CardTitle>
                          <CardDescription>by {app.developer_name}</CardDescription>
                        </div>
                        {app.installation && (
                          <Badge variant="default" className="text-xs">Installed</Badge>
                        )}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground mb-3">
                        {app.description}
                      </p>
                      <div className="flex flex-wrap gap-1 mb-4">
                        {app.features.map((feature) => (
                          <Badge key={feature} variant="secondary" className="text-xs">
                            {feature}
                          </Badge>
                        ))}
                      </div>
                      <div className="flex gap-2">
                        {app.installation ? (
                          <>
                            <Button size="sm" variant="outline" className="flex-1">
                              <Settings className="w-4 h-4 mr-2" />
                              Configure
                            </Button>
                            <Button size="sm" variant="destructive" className="flex-1">
                              Uninstall
                            </Button>
                          </>
                        ) : (
                          <Button size="sm" className="flex-1">
                            <Plus className="w-4 h-4 mr-2" />
                            Install
                          </Button>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* Installed Apps */}
            <TabsContent value="installed" className="space-y-4">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold">Installed Apps</h3>
                  <p className="text-sm text-muted-foreground">
                    Manage your installed applications and their permissions
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                {marketplaceApps
                  .filter(app => app.installation)
                  .map((app) => (
                    <Card key={app.id}>
                      <CardHeader>
                        <div className="flex justify-between items-start">
                          <div>
                            <CardTitle className="text-base">{app.display_name}</CardTitle>
                            <CardDescription>by {app.developer_name}</CardDescription>
                          </div>
                          <div className="flex gap-2">
                            <Button size="sm" variant="outline">
                              <ExternalLink className="w-4 h-4 mr-2" />
                              Launch
                            </Button>
                            <Button size="sm" variant="outline">
                              <Settings className="w-4 h-4 mr-2" />
                              Configure
                            </Button>
                            <Button size="sm" variant="destructive">
                              <Trash2 className="w-4 h-4 mr-2" />
                              Uninstall
                            </Button>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div>
                            <Label className="text-sm font-medium">Permissions</Label>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {app.installation?.access_scopes.map((scope: string) => (
                                <Badge key={scope} variant="outline" className="text-xs">
                                  {scope}
                                </Badge>
                              ))}
                            </div>
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {app.features.map((feature) => (
                              <Badge key={feature} variant="secondary" className="text-xs">
                                {feature}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
              </div>
            </TabsContent>

            {/* Developer Portal */}
            <TabsContent value="developer" className="space-y-4">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold">My Apps</h3>
                  <p className="text-sm text-muted-foreground">
                    Create and manage OAuth applications for API access
                  </p>
                </div>
                <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
                  <DialogTrigger asChild>
                    <Button>
                      <Plus className="w-4 h-4 mr-2" />
                      Create App
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[525px]">
                    <DialogHeader>
                      <DialogTitle>Create New App</DialogTitle>
                      <DialogDescription>
                        Create a new OAuth application to access Karrio APIs.
                      </DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                      <div className="grid gap-2">
                        <Label htmlFor="name">App Name</Label>
                        <Input
                          id="name"
                          placeholder="My Integration App"
                        />
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="developer">Developer Name</Label>
                        <Input
                          id="developer"
                          placeholder="Your Company Name"
                        />
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="description">Description</Label>
                        <Textarea
                          id="description"
                          placeholder="Brief description of your app..."
                        />
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="redirect_uri">Redirect URI</Label>
                        <Input
                          id="redirect_uri"
                          placeholder="https://yourapp.com/auth/callback"
                        />
                      </div>
                      <div className="flex items-center space-x-2">
                        <Switch id="is_public" />
                        <Label htmlFor="is_public">Make this app public</Label>
                      </div>
                    </div>
                    <div className="flex justify-end gap-2">
                      <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
                        Cancel
                      </Button>
                      <Button onClick={() => setShowCreateDialog(false)}>
                        Create App
                      </Button>
                    </div>
                  </DialogContent>
                </Dialog>
              </div>

              <div className="space-y-4">
                {privateApps.map((app) => (
                  <Card key={app.id}>
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-base">{app.display_name}</CardTitle>
                          <CardDescription>Created on {new Date(app.created_at).toLocaleDateString()}</CardDescription>
                        </div>
                        <div className="flex gap-2">
                          <Button size="sm" variant="outline">
                            <Edit3 className="w-4 h-4 mr-2" />
                            Edit
                          </Button>
                          <Button size="sm" variant="destructive">
                            <Trash2 className="w-4 h-4 mr-2" />
                            Delete
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {/* Client ID */}
                        <div>
                          <Label className="text-sm font-medium">Client ID</Label>
                          <div className="flex gap-2 mt-1">
                            <Input
                              value={app.client_id}
                              readOnly
                              className="font-mono text-sm"
                            />
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => copyToClipboard(app.client_id, "Client ID")}
                            >
                              <Copy className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>

                        {/* Client Secret */}
                        <div>
                          <Label className="text-sm font-medium">Client Secret</Label>
                          <div className="flex gap-2 mt-1">
                            <Input
                              type={revealedSecrets[app.id] ? "text" : "password"}
                              value={revealedSecrets[app.id] ? app.client_secret : "••••••••••••••••••••••••••••••••"}
                              readOnly
                              className="font-mono text-sm"
                            />
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => copyToClipboard(app.client_secret, "Client Secret")}
                              disabled={!revealedSecrets[app.id]}
                            >
                              <Copy className="w-4 h-4" />
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => toggleSecretVisibility(app.id)}
                            >
                              {revealedSecrets[app.id] ? (
                                <EyeOff className="w-4 h-4" />
                              ) : (
                                <Eye className="w-4 h-4" />
                              )}
                            </Button>
                          </div>
                          <p className="text-xs text-muted-foreground mt-1">
                            Keep this secret secure and never expose it in client-side code
                          </p>
                        </div>

                        {/* Redirect URI */}
                        <div>
                          <Label className="text-sm font-medium">Redirect URI</Label>
                          <Input
                            value={app.redirect_uris}
                            readOnly
                            className="mt-1"
                          />
                        </div>

                        <Separator />

                        {/* Features */}
                        <div>
                          <Label className="text-sm font-medium">Features</Label>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {app.features.map((feature) => (
                              <Badge key={feature} variant="secondary" className="text-xs">
                                {feature}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    );
  };

  return <Component />;
}
