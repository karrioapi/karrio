"use client";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@karrio/ui/components/ui/dialog";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Sheet, SheetContent } from "@karrio/ui/components/ui/sheet";
import { Copy, Plus, Edit3, Trash2, Loader2 } from "lucide-react";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { useAppStore, useAppMutations } from "@karrio/hooks";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useForm } from "@tanstack/react-form";
import { OAuthAppConfig } from "../components/oauth-app-config";
import { useState } from "react";


export default function AppsPage() {
  const Component = (): JSX.Element => {
    const { setLoading } = useLoader();
    const { toast } = useToast();
    const { metadata } = useAPIMetadata();
    const [showCreateDialog, setShowCreateDialog] = useState(false);
    const [selectedAppId, setSelectedAppId] = useState<string | null>(null);
    const [newlyCreatedApp, setNewlyCreatedApp] = useState<any>(null);
    const [showClientSecret, setShowClientSecret] = useState(false);
    const [deleteAppId, setDeleteAppId] = useState<string | null>(null);
    const [deleteAppName, setDeleteAppName] = useState<string>("");

    // Use OAuth apps instead of private apps
    const { oauth: oauthApps } = useAppStore();
    const { createOAuthApp, updateOAuthApp, deleteOAuthApp } = useAppMutations();

    const myApps = oauthApps.query.data?.oauth_apps?.edges?.map(edge => edge.node) || [];

    // Loading states
    const isLoadingOAuth = oauthApps.query.isLoading;

    // Form for creating new OAuth app
    const createAppForm = useForm({
      defaultValues: {
        display_name: "",
        description: "",
        launch_url: "",
        redirect_uris: "",
      },
      onSubmit: async ({ value }) => {
        try {
          setLoading(true);
          const result = await createOAuthApp.mutateAsync({
            display_name: value.display_name,
            description: value.description,
            launch_url: value.launch_url,
            redirect_uris: value.redirect_uris,
            features: [],
            metadata: {},
          });

          if (result.create_oauth_app?.errors?.length) {
            const error = result.create_oauth_app.errors[0];
            toast({
              title: "Error creating OAuth app",
              description: error.messages?.join(", "),
              variant: "destructive",
            });
          } else {
            toast({
              title: "OAuth app created successfully",
              description: `${value.display_name} has been created`,
            });
            setShowCreateDialog(false);
            createAppForm.reset();
            setNewlyCreatedApp(result.create_oauth_app?.oauth_app);
            setShowClientSecret(true);
          }
        } catch (error: any) {
          toast({
            title: "Error creating OAuth app",
            description: error.message || "An unexpected error occurred",
            variant: "destructive",
          });
        } finally {
          setLoading(false);
        }
      },
    });

    const copyToClipboard = (text: string, label: string) => {
      navigator.clipboard.writeText(text);
      toast({ title: `${label} copied to clipboard` });
    };

    const handleDeleteApp = async (appId: string, appName: string) => {
      setDeleteAppId(appId);
      setDeleteAppName(appName);
    };

    const confirmDeleteApp = async () => {
      if (!deleteAppId) return;

      try {
        setLoading(true);
        const result = await deleteOAuthApp.mutateAsync({
          id: deleteAppId,
        });

        if (result.delete_oauth_app?.errors?.length) {
          const error = result.delete_oauth_app.errors[0];
          toast({
            title: "Error deleting OAuth app",
            description: error.messages?.join(", "),
            variant: "destructive",
          });
        } else {
          toast({
            title: "OAuth app deleted successfully",
            description: "The OAuth app has been permanently deleted",
          });
        }
      } catch (error: any) {
        toast({
          title: "Error deleting OAuth app",
          description: error.message || "An unexpected error occurred",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
        setDeleteAppId(null);
        setDeleteAppName("");
      }
    };

    const handleConfigureApp = (appId: string) => {
      setSelectedAppId(appId);
    };

    const handleFormSave = () => {
      // Refetch the OAuth apps data
      oauthApps.query.refetch();
    };

    const selectedApp = myApps.find(app => app.id === selectedAppId);

    return (
      <div className="tailwind-only">
        {/* Header */}
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Developers</span>
          <div>
            <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="w-4 h-4 mr-2" />
                  Create OAuth App
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[525px]">
                <DialogHeader>
                  <DialogTitle>Create New OAuth App</DialogTitle>
                  <DialogDescription>
                    Create a new OAuth application to access Karrio APIs.
                  </DialogDescription>
                </DialogHeader>
                <form
                  className="p-4 pb-8"
                  onSubmit={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    createAppForm.handleSubmit();
                  }}
                >
                  <div className="grid gap-4 py-4">
                    <createAppForm.Field
                      name="display_name"
                      validators={{
                        onChange: ({ value }) =>
                          !value ? "App name is required" : undefined,
                      }}
                      children={(field) => (
                        <div className="grid gap-2">
                          <Label htmlFor={field.name}>App Name</Label>
                          <Input
                            id={field.name}
                            name={field.name}
                            value={field.state.value}
                            onBlur={field.handleBlur}
                            onChange={(e) => field.handleChange(e.target.value)}
                            placeholder="My Integration App"
                          />
                          {field.state.meta.errors && (
                            <span className="text-sm text-red-500">
                              {field.state.meta.errors}
                            </span>
                          )}
                        </div>
                      )}
                    />

                    <createAppForm.Field
                      name="description"
                      children={(field) => (
                        <div className="grid gap-2">
                          <Label htmlFor={field.name}>Description</Label>
                          <Textarea
                            id={field.name}
                            name={field.name}
                            value={field.state.value}
                            onBlur={field.handleBlur}
                            onChange={(e) => field.handleChange(e.target.value)}
                            placeholder="Brief description of your app..."
                          />
                        </div>
                      )}
                    />
                    <createAppForm.Field
                      name="launch_url"
                      validators={{
                        onChange: ({ value }) =>
                          !value ? "Launch URL is required" : undefined,
                      }}
                      children={(field) => (
                        <div className="grid gap-2">
                          <Label htmlFor={field.name}>Launch URL</Label>
                          <Input
                            id={field.name}
                            name={field.name}
                            value={field.state.value}
                            onBlur={field.handleBlur}
                            onChange={(e) => field.handleChange(e.target.value)}
                            placeholder="https://yourapp.com"
                          />
                          {field.state.meta.errors && (
                            <span className="text-sm text-red-500">
                              {field.state.meta.errors}
                            </span>
                          )}
                        </div>
                      )}
                    />
                    <createAppForm.Field
                      name="redirect_uris"
                      validators={{
                        onChange: ({ value }) =>
                          !value ? "Redirect URI is required" : undefined,
                      }}
                      children={(field) => (
                        <div className="grid gap-2">
                          <Label htmlFor={field.name}>Redirect URI</Label>
                          <Input
                            id={field.name}
                            name={field.name}
                            value={field.state.value}
                            onBlur={field.handleBlur}
                            onChange={(e) => field.handleChange(e.target.value)}
                            placeholder="https://yourapp.com/auth/callback"
                          />
                          {field.state.meta.errors && (
                            <span className="text-sm text-red-500">
                              {field.state.meta.errors}
                            </span>
                          )}
                        </div>
                      )}
                    />
                  </div>
                  <div className="flex justify-end gap-2">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => setShowCreateDialog(false)}
                    >
                      Cancel
                    </Button>
                    <Button
                      type="submit"
                      disabled={createOAuthApp.isLoading}
                    >
                      {createOAuthApp.isLoading && (
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      )}
                      Create OAuth App
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </Dialog>
          </div>
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
              <AppLink
                href="/developers/apikeys"
                shallow={false}
                prefetch={false}
              >
                <span>API Keys</span>
              </AppLink>
            </li>
            {metadata?.APPS_MANAGEMENT && (
              <li className={`is-capitalized has-text-weight-semibold is-active`}>
                <AppLink
                  href="/developers/apps"
                  shallow={false}
                  prefetch={false}
                >
                  <span>Apps</span>
                </AppLink>
              </li>
            )}
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/developers/webhooks"
                shallow={false}
                prefetch={false}
              >
                <span>Webhooks</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/developers/events"
                shallow={false}
                prefetch={false}
              >
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

        {/* Main Content - My OAuth Apps */}
        <div className="mt-6">
          {isLoadingOAuth ? (
            <div className="flex justify-center items-center py-8">
              <Loader2 className="w-8 h-8 animate-spin" />
            </div>
          ) : (
            <div className="tailwind-only">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {myApps.map((app) => (
                  <Card key={app.id} className="hover:shadow-md transition-shadow">
                    <CardHeader className="pb-4 pt-6 px-6">
                      <div className="flex items-start gap-4">
                        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-lg font-semibold flex-shrink-0">
                          {app.display_name?.charAt(0) || 'A'}
                        </div>
                        <div className="flex-1 min-w-0">
                          <CardTitle className="text-base font-semibold leading-tight mb-2">
                            {app.display_name}
                          </CardTitle>
                          <CardDescription className="text-sm text-muted-foreground">
                            OAuth Application
                          </CardDescription>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="pt-0 pb-6 px-6">
                      <p className="text-sm text-muted-foreground mb-6 line-clamp-3 leading-relaxed">
                        {app.description || 'No description available'}
                      </p>

                      <div className="flex gap-3">
                        <Button
                          size="sm"
                          variant="outline"
                          className="flex-1 text-sm h-9"
                          onClick={() => handleConfigureApp(app.id)}
                        >
                          <Edit3 className="w-4 h-4 mr-2" />
                          Configure
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          className="flex-1 text-sm h-9"
                          onClick={() => handleDeleteApp(app.id, app.display_name)}
                        >
                          <Trash2 className="w-4 h-4 mr-2" />
                          Delete
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
                {myApps.length === 0 && (
                  <div className="col-span-full flex items-center justify-center min-h-[400px]">
                    <div className="text-center">
                      <p className="text-muted-foreground text-lg mb-2">
                        No OAuth apps created yet
                      </p>
                      <p className="text-muted-foreground text-sm">
                        Create your first OAuth app to get started
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* OAuth App Configuration Sheet */}
        <Sheet open={!!selectedAppId} onOpenChange={(open) => {
          if (!open) {
            setSelectedAppId(null);
          }
        }}>
          <SheetContent className="w-full sm:w-[500px] sm:max-w-[500px] p-0 shadow-none">
            {selectedApp && (
              <OAuthAppConfig
                app={selectedApp}
                onClose={() => setSelectedAppId(null)}
                onSave={handleFormSave}
              />
            )}
          </SheetContent>
        </Sheet>

        {/* Client Secret Display Dialog */}
        <Dialog open={showClientSecret} onOpenChange={setShowClientSecret}>
          <DialogContent className="sm:max-w-[525px]">
            <DialogHeader>
              <DialogTitle>OAuth App Created Successfully</DialogTitle>
              <DialogDescription>
                Your OAuth app has been created. Please copy and securely store your client secret now - it will not be shown again.
              </DialogDescription>
            </DialogHeader>

            {newlyCreatedApp && (
              <div className="space-y-4 p-4 pb-8">
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-red-600 text-sm font-bold">!</span>
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-red-900 mb-1">Important Security Notice</h4>
                      <p className="text-sm text-red-800">
                        This is the only time your client secret will be displayed. Copy it now and store it securely.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <Label className="text-sm font-medium text-slate-700">Client ID</Label>
                    <div className="flex gap-2 mt-1">
                      <Input
                        value={newlyCreatedApp.client_id}
                        readOnly
                        className="font-mono text-sm bg-slate-50"
                      />
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => copyToClipboard(newlyCreatedApp.client_id, "Client ID")}
                      >
                        <Copy className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-slate-700">Client Secret</Label>
                    <div className="flex gap-2 mt-1">
                      <Input
                        value={newlyCreatedApp.client_secret}
                        readOnly
                        className="font-mono text-sm bg-slate-50"
                      />
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => copyToClipboard(newlyCreatedApp.client_secret, "Client Secret")}
                      >
                        <Copy className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div className="flex justify-end gap-2 p-4 pb-8">
              <Button
                onClick={() => {
                  setShowClientSecret(false);
                  setNewlyCreatedApp(null);
                }}
              >
                I've Saved My Credentials
              </Button>
            </div>
          </DialogContent>
        </Dialog>

        {/* Delete Confirmation Dialog */}
        <Dialog open={!!deleteAppId} onOpenChange={(open) => {
          if (!open) {
            setDeleteAppId(null);
            setDeleteAppName("");
          }
        }}>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>Delete OAuth App</DialogTitle>
              <DialogDescription>
                Are you sure you want to delete "{deleteAppName}"? This action cannot be undone.
              </DialogDescription>
            </DialogHeader>

            <div className="py-4 p-4 pb-8">
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-red-600 text-sm font-bold">!</span>
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-red-900 mb-1">Warning</h4>
                    <p className="text-sm text-red-800">
                      This will permanently delete the OAuth app and revoke all associated access tokens.
                      Any applications using this OAuth app will stop working immediately.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex justify-end gap-2 p-4 pb-8">
              <Button
                variant="outline"
                onClick={() => {
                  setDeleteAppId(null);
                  setDeleteAppName("");
                }}
              >
                Cancel
              </Button>
              <Button
                variant="destructive"
                onClick={confirmDeleteApp}
                disabled={deleteOAuthApp.isLoading}
              >
                {deleteOAuthApp.isLoading && (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                )}
                Delete OAuth App
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    );
  };

  return <Component />;
}
