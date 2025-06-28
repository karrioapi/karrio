"use client";

import React, { useState } from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@karrio/ui/components/ui/dialog";
import { Sheet, SheetContent } from "@karrio/ui/components/ui/sheet";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Trash2, Plus, Copy, Settings, Eye, EyeOff, Globe, Key, Edit3, Loader2 } from "lucide-react";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { formatDateTimeLong } from "@karrio/lib";
import { useAppStore, useAppMutations } from "@karrio/hooks";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useForm } from "@tanstack/react-form";
import { OAuthAppConfig } from "@karrio/developers/components/oauth-app-config";

export function AppsView() {
  const { toast } = useToast();
  const { setLoading } = useLoader();
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [selectedAppId, setSelectedAppId] = useState<string | null>(null);
  const [newlyCreatedApp, setNewlyCreatedApp] = useState<any>(null);
  const [showClientSecret, setShowClientSecret] = useState(false);
  const [deleteAppId, setDeleteAppId] = useState<string | null>(null);
  const [deleteAppName, setDeleteAppName] = useState<string>("");

  const { oauth: oauthApps } = useAppStore();
  const { createOAuthApp, deleteOAuthApp } = useAppMutations();
  const myApps = oauthApps.query.data?.oauth_apps?.edges?.map(edge => edge.node) || [];
  const isLoading = oauthApps.query.isLoading;

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

  const confirmDeleteApp = async () => {
    if (!deleteAppId) return;
    try {
      setLoading(true);
      await deleteOAuthApp.mutateAsync({ id: deleteAppId });
      toast({ title: "OAuth app deleted successfully" });
      setDeleteAppId(null);
    } catch (error: any) {
      toast({
        title: "Error deleting OAuth app",
        description: error.message || "An unexpected error occurred",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast({ title: `${label} copied to clipboard!` });
  };

  const selectedApp = myApps.find(app => app.id === selectedAppId);

  return (
    <div className="h-full flex flex-col">
      <div className="px-4 py-3 border-b border-slate-200">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold">OAuth Apps</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Manage OAuth applications and integrations
            </p>
          </div>
          <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
            <DialogTrigger asChild>
              <Button size="sm">
                <Plus className="h-4 w-4 mr-2" />
                Create OAuth App
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-lg p-4 pb-8">
              <DialogHeader>
                <DialogTitle>Create OAuth App</DialogTitle>
                <DialogDescription>
                  Create a new OAuth application for third-party integrations.
                </DialogDescription>
              </DialogHeader>
              <form
                onSubmit={(e) => { e.preventDefault(); e.stopPropagation(); createAppForm.handleSubmit(); }}
                className="space-y-4 pt-4"
              >
                <createAppForm.Field
                  name="display_name"
                  children={(field) => (
                    <div className="space-y-2">
                      <Label htmlFor={field.name}>App Name</Label>
                      <Input id={field.name} name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} placeholder="Enter app name" required />
                    </div>
                  )}
                />
                <createAppForm.Field
                  name="description"
                  children={(field) => (
                    <div className="space-y-2">
                      <Label htmlFor={field.name}>Description</Label>
                      <Textarea id={field.name} name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} placeholder="Describe your OAuth application" rows={3} />
                    </div>
                  )}
                />
                <createAppForm.Field
                  name="launch_url"
                  children={(field) => (
                    <div className="space-y-2">
                      <Label htmlFor={field.name}>Launch URL</Label>
                      <Input id={field.name} name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} placeholder="https://example.com" required />
                    </div>
                  )}
                />
                <createAppForm.Field
                  name="redirect_uris"
                  children={(field) => (
                    <div className="space-y-2">
                      <Label htmlFor={field.name}>Redirect URIs</Label>
                      <Textarea id={field.name} name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} placeholder="https://example.com/callback&#10;https://example.com/auth/callback" rows={3} required />
                      <p className="text-xs text-slate-500">Enter one redirect URI per line</p>
                    </div>
                  )}
                />
                <DialogFooter className="pt-4">
                  <Button type="button" variant="outline" onClick={() => setShowCreateDialog(false)}>Cancel</Button>
                  <Button type="submit" disabled={createOAuthApp.isLoading}>
                    {createOAuthApp.isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                    Create App
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-4">
        {isLoading ? (
          <div className="flex justify-center items-center h-full"><Loader2 className="h-8 w-8 animate-spin" /></div>
        ) : myApps.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-slate-400 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-slate-900 mb-2">No OAuth apps</h3>
            <p className="text-slate-500 mb-4">Create your first OAuth application to enable third-party integrations.</p>
            <Button onClick={() => setShowCreateDialog(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create OAuth App
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {myApps.map((app) => (
              <Card key={app.id}>
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <CardTitle className="text-base flex items-center gap-2">
                        <Globe className="h-4 w-4 flex-shrink-0" />
                        <span className="truncate">{app.display_name}</span>
                      </CardTitle>
                      <CardDescription className="mt-1 truncate">
                        {app.description || "No description provided"}
                      </CardDescription>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <Button variant="ghost" size="sm" onClick={() => setSelectedAppId(app.id)}>
                        <Edit3 className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm" onClick={() => { setDeleteAppId(app.id); setDeleteAppName(app.display_name); }} className="text-red-600 hover:text-red-700">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <Label className="text-xs text-slate-600 flex items-center gap-1"><Key className="h-3 w-3" />Client ID</Label>
                      <div className="flex items-center gap-2 mt-1">
                        <code className="flex-1 text-sm bg-slate-50 px-3 py-2 rounded font-mono truncate">{app.client_id}</code>
                        <Button variant="ghost" size="sm" onClick={() => copyToClipboard(app.client_id, "Client ID")}><Copy className="h-4 w-4" /></Button>
                      </div>
                    </div>
                    <div className="text-xs text-slate-500 pt-2 border-t">
                      Created {formatDateTimeLong(app.created_at)}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      <Sheet open={!!selectedAppId} onOpenChange={(open) => !open && setSelectedAppId(null)}>
        <SheetContent className="w-full sm:w-[500px] sm:max-w-[500px] p-0 shadow-none">
          {selectedApp && <OAuthAppConfig app={selectedApp} onClose={() => setSelectedAppId(null)} onSave={() => oauthApps.query.refetch()} />}
        </SheetContent>
      </Sheet>

      <Dialog open={showClientSecret} onOpenChange={setShowClientSecret}>
        <DialogContent className="sm:max-w-[525px] p-4 pb-8">
          <DialogHeader>
            <DialogTitle>OAuth App Created Successfully</DialogTitle>
            <DialogDescription>
              Your OAuth app has been created. Please copy and securely store your client secret now - it will not be shown again.
            </DialogDescription>
          </DialogHeader>
          {newlyCreatedApp && (
            <div className="space-y-4 py-4">
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5"><span className="text-red-600 text-sm font-bold">!</span></div>
                  <div>
                    <h4 className="text-sm font-semibold text-red-900 mb-1">Important Security Notice</h4>
                    <p className="text-sm text-red-800">This is the only time your client secret will be displayed. Copy it now and store it securely.</p>
                  </div>
                </div>
              </div>
              <div className="space-y-3">
                <div>
                  <Label className="text-sm font-medium text-slate-700">Client ID</Label>
                  <div className="flex gap-2 mt-1">
                    <Input value={newlyCreatedApp.client_id} readOnly className="font-mono text-sm bg-slate-50" />
                    <Button size="sm" variant="outline" onClick={() => copyToClipboard(newlyCreatedApp.client_id, "Client ID")}><Copy className="w-4 w-4" /></Button>
                  </div>
                </div>
                <div>
                  <Label className="text-sm font-medium text-slate-700">Client Secret</Label>
                  <div className="flex gap-2 mt-1">
                    <Input value={newlyCreatedApp.client_secret} readOnly className="font-mono text-sm bg-slate-50" />
                    <Button size="sm" variant="outline" onClick={() => copyToClipboard(newlyCreatedApp.client_secret, "Client Secret")}><Copy className="w-4 w-4" /></Button>
                  </div>
                </div>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button onClick={() => { setShowClientSecret(false); setNewlyCreatedApp(null); }}>I've Saved My Credentials</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={!!deleteAppId} onOpenChange={() => setDeleteAppId(null)}>
        <DialogContent className="p-4 pb-8">
          <DialogHeader>
            <DialogTitle>Delete OAuth App</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{deleteAppName}"? This action cannot be undone and will revoke all existing tokens.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="pt-4">
            <Button variant="outline" onClick={() => setDeleteAppId(null)}>Cancel</Button>
            <Button variant="destructive" onClick={confirmDeleteApp} disabled={deleteOAuthApp.isLoading}>
              {deleteOAuthApp.isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              Delete App
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
