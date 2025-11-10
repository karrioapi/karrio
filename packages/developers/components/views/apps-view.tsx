"use client";

import React, { useState } from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger, DialogPortal } from "@karrio/ui/components/ui/dialog";
import { Sheet, SheetContent, SheetPortal } from "@karrio/ui/components/ui/sheet";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Trash2, Plus, Copy, Settings, Eye, EyeOff, Globe, Key, Edit3, Loader2, MoreHorizontal } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@karrio/ui/components/ui/table";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger, DropdownMenuPortal } from "@karrio/ui/components/ui/dropdown-menu";
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
    <div className="h-full flex flex-col bg-background">
      <div className="px-4 py-3 border-b border-border">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">OAuth Apps</h2>
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
            <DialogPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
              <DialogContent className="devtools-theme dark max-w-lg bg-popover border-border text-foreground">
                <DialogHeader className="bg-popover border-b border-border px-4 py-3 text-foreground">
                  <DialogTitle className="text-foreground">Create OAuth App</DialogTitle>
                  <DialogDescription className="text-muted-foreground">
                    Create a new OAuth application for third-party integrations.
                  </DialogDescription>
                </DialogHeader>
                <form
                  onSubmit={(e) => { e.preventDefault(); e.stopPropagation(); createAppForm.handleSubmit(); }}
                  className="space-y-4 pt-4 p-4 pb-8"
                >
                  <createAppForm.Field
                    name="display_name"
                    children={(field) => (
                      <div className="space-y-2">
                        <Label htmlFor={field.name} className="text-muted-foreground">App Name</Label>
                        <Input id={field.name} name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} placeholder="Enter app name" required className="bg-input border-border text-foreground placeholder:text-muted-foreground" />
                      </div>
                    )}
                  />
                  <createAppForm.Field
                    name="description"
                    children={(field) => (
                      <div className="space-y-2">
                        <Label htmlFor={field.name} className="text-muted-foreground">Description</Label>
                        <Textarea id={field.name} name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} placeholder="Describe your OAuth application" rows={3} className="bg-input border-border text-foreground placeholder:text-muted-foreground" />
                      </div>
                    )}
                  />
                  <createAppForm.Field
                    name="launch_url"
                    children={(field) => (
                      <div className="space-y-2">
                        <Label htmlFor={field.name} className="text-muted-foreground">Launch URL</Label>
                        <Input id={field.name} name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} placeholder="https://example.com" required className="bg-input border-border text-foreground placeholder:text-muted-foreground" />
                      </div>
                    )}
                  />
                  <createAppForm.Field
                    name="redirect_uris"
                    children={(field) => (
                      <div className="space-y-2">
                        <Label htmlFor={field.name} className="text-muted-foreground">Redirect URIs</Label>
                        <Textarea id={field.name} name={field.name} value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} placeholder={`https://example.com/callback\nhttps://example.com/auth/callback`} rows={3} required className="bg-input border-border text-foreground placeholder:text-muted-foreground" />
                        <p className="text-xs text-muted-foreground">Enter one redirect URI per line</p>
                      </div>
                    )}
                  />
                  <DialogFooter className="pt-4 bg-popover border-t border-border">
                    <Button type="button" variant="outline" onClick={() => setShowCreateDialog(false)} className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!border-primary hover:!text-primary">Cancel</Button>
                    <Button type="submit" disabled={createOAuthApp.isLoading}>
                      {createOAuthApp.isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                      Create App
                    </Button>
                  </DialogFooter>
                </form>
              </DialogContent>
            </DialogPortal>
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
            <h3 className="text-lg font-medium text-slate-300 mb-2">No OAuth apps</h3>
            <p className="text-slate-500 mb-4">Create your first OAuth application to enable third-party integrations.</p>
            <Button onClick={() => setShowCreateDialog(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create OAuth App
            </Button>
          </div>
        ) : (
          <div className="border-b border-border overflow-x-auto sm:overflow-x-visible" style={{ touchAction: 'pan-x', WebkitOverflowScrolling: 'touch', overscrollBehaviorX: 'contain' }}>
            <div className="inline-block w-full min-w-[900px] sm:min-w-0 align-top">
              <Table className="w-full table-auto">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-foreground">App Name</TableHead>
                    <TableHead className="text-foreground">Description</TableHead>
                    <TableHead className="text-foreground">Client ID</TableHead>
                    <TableHead className="text-foreground">Created</TableHead>
                    <TableHead className="w-12"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {myApps.map((app) => (
                    <TableRow key={app.id}>
                      <TableCell className="font-medium">
                        <div className="flex items-center gap-2">
                          <Globe className="h-4 w-4 text-primary" />
                          <span className="text-foreground">{app.display_name}</span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="max-w-md">
                          <p className="text-sm text-muted-foreground truncate">
                            {app.description || "No description provided"}
                          </p>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <code className="text-sm bg-muted border border-border px-2 py-1 rounded font-mono text-foreground">
                            {app.client_id.substring(0, 8)}...
                          </code>
                          <Button variant="ghost" size="sm" onClick={() => copyToClipboard(app.client_id, "Client ID")}>
                            <Copy className="h-4 w-4 text-muted-foreground" />
                          </Button>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm text-muted-foreground">
                          {formatDateTimeLong(app.created_at)}
                        </div>
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon" className="h-8 w-8 p-0">
                              <MoreHorizontal className="h-4 w-4 text-muted-foreground" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
                            <DropdownMenuContent align="end" className="devtools-theme dark bg-popover text-foreground border-border">
                              <DropdownMenuItem onClick={() => setSelectedAppId(app.id)} className="text-foreground focus:bg-primary/20 focus:text-foreground">
                                <Edit3 className="h-4 w-4 mr-2" />
                                Configure
                              </DropdownMenuItem>
                              <DropdownMenuItem onClick={() => copyToClipboard(app.client_id, "Client ID")} className="text-foreground focus:bg-primary/20 focus:text-foreground">
                                <Copy className="h-4 w-4 mr-2" />
                                Copy Client ID
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => { setDeleteAppId(app.id); setDeleteAppName(app.display_name); }}
                                className="text-destructive"
                              >
                                <Trash2 className="h-4 w-4 mr-2" />
                                Delete
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenuPortal>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        )}
      </div>

      <Sheet open={!!selectedAppId} onOpenChange={(open) => !open && setSelectedAppId(null)}>
        <SheetPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
          <SheetContent className="devtools-theme dark w-full sm:w-[500px] sm:max-w-[500px] p-0 shadow-none">
            {selectedApp && <OAuthAppConfig app={selectedApp} onClose={() => setSelectedAppId(null)} onSave={() => oauthApps.query.refetch()} />}
          </SheetContent>
        </SheetPortal>
      </Sheet>

      <Dialog open={showClientSecret} onOpenChange={setShowClientSecret}>
        <DialogPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
          <DialogContent className="devtools-theme dark sm:max-w-[525px] bg-popover border-border text-foreground">
            <DialogHeader className="bg-popover border-b border-border px-4 py-3">
              <DialogTitle className="text-foreground">OAuth App Created Successfully</DialogTitle>
              <DialogDescription className="text-muted-foreground">
                Your OAuth app has been created. Please copy and securely store your client secret now - it will not be shown again.
              </DialogDescription>
            </DialogHeader>
            {newlyCreatedApp && (
              <div className="space-y-4 py-4 p-4 pb-8">
                <div className="p-4 bg-red-900/20 border border-red-900/40 rounded-lg">
                  <div className="flex items-start gap-3">
                    <div className="w-6 h-6 bg-red-800/50 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5"><span className="text-red-300 text-sm font-bold">!</span></div>
                    <div>
                      <h4 className="text-sm font-semibold text-red-200 mb-1">Important Security Notice</h4>
                      <p className="text-sm text-red-300">This is the only time your client secret will be displayed. Copy it now and store it securely.</p>
                    </div>
                  </div>
                </div>
                <div className="space-y-3">
                  <div>
                    <Label className="text-sm font-medium text-muted-foreground">Client ID</Label>
                    <div className="flex gap-2 mt-1">
                      <Input value={newlyCreatedApp.client_id} readOnly className="font-mono text-sm bg-input border-border text-foreground" />
                      <Button size="sm" variant="outline" onClick={() => copyToClipboard(newlyCreatedApp.client_id, "Client ID")} className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!border-primary hover:!text-primary"><Copy className="w-4 w-4" /></Button>
                    </div>
                  </div>
                  <div>
                    <Label className="text-sm font-medium text-muted-foreground">Client Secret</Label>
                    <div className="flex gap-2 mt-1">
                      <Input value={newlyCreatedApp.client_secret} readOnly className="font-mono text-sm bg-input border-border text-foreground" />
                      <Button size="sm" variant="outline" onClick={() => copyToClipboard(newlyCreatedApp.client_secret, "Client Secret")} className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!border-primary hover:!text-primary"><Copy className="w-4 w-4" /></Button>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <DialogFooter className="bg-popover border-t border-border">
              <Button onClick={() => { setShowClientSecret(false); setNewlyCreatedApp(null); }} className="text-foreground border-border hover:bg-primary/10">I've Saved My Credentials</Button>
            </DialogFooter>
          </DialogContent>
        </DialogPortal>
      </Dialog>

      <Dialog open={!!deleteAppId} onOpenChange={() => setDeleteAppId(null)}>
        <DialogPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
          <DialogContent className="devtools-theme dark bg-popover border-border text-foreground">
            <DialogHeader className="bg-popover border-b border-border">
              <DialogTitle className="text-foreground">Delete OAuth App</DialogTitle>
              <DialogDescription className="text-muted-foreground">
                Are you sure you want to delete "{deleteAppName}"? This action cannot be undone and will revoke all existing tokens.
              </DialogDescription>
            </DialogHeader>
            <DialogFooter className="pt-4 bg-popover border-t border-border">
              <Button variant="outline" onClick={() => setDeleteAppId(null)} className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!border-primary hover:!text-primary">Cancel</Button>
              <Button variant="destructive" onClick={confirmDeleteApp} disabled={deleteOAuthApp.isLoading}>
                {deleteOAuthApp.isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                Delete App
              </Button>
            </DialogFooter>
          </DialogContent>
        </DialogPortal>
      </Dialog>
    </div>
  );
}
