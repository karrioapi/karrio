"use client";
import { SheetHeader, SheetTitle, SheetDescription } from "@karrio/ui/components/ui/sheet";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Copy, Save, Loader2 } from "lucide-react";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useAppMutations } from "@karrio/hooks";
import { useForm } from "@tanstack/react-form";
import React from "react";

interface OAuthApp {
  id: string;
  display_name: string;
  description?: string | null;
  launch_url: string;
  redirect_uris: string;
  client_id: string;
  client_secret?: string;
}

interface OAuthAppConfigProps {
  app: OAuthApp;
  onClose: () => void;
  onSave: () => void;
}

export function OAuthAppConfig({ app, onClose, onSave }: OAuthAppConfigProps) {
  const { setLoading } = useLoader();
  const { toast } = useToast();
  const { updateOAuthApp } = useAppMutations();

  const updateForm = useForm({
    defaultValues: {
      display_name: app.display_name,
      description: app.description || "",
      launch_url: app.launch_url,
      redirect_uris: app.redirect_uris,
    },
    onSubmit: async ({ value }) => {
      try {
        setLoading(true);
        const result = await updateOAuthApp.mutateAsync({
          id: app.id,
          display_name: value.display_name,
          description: value.description,
          launch_url: value.launch_url,
          redirect_uris: value.redirect_uris,
        });

        if (result.update_oauth_app?.errors?.length) {
          const error = result.update_oauth_app.errors[0];
          toast({
            title: "Error updating OAuth app",
            description: error.messages?.join(", "),
            variant: "destructive",
          });
        } else {
          toast({
            title: "OAuth app updated successfully",
            description: `${value.display_name} has been updated`,
          });
          onSave();
          onClose();
        }
      } catch (error: any) {
        toast({
          title: "Error updating OAuth app",
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

  return (
    <div className="h-full flex flex-col bg-background text-foreground">
      <SheetHeader className="sticky top-0 z-10 bg-popover px-4 py-3 border-b border-border">
        <div className="flex items-center justify-between">
          <SheetTitle className="text-lg font-semibold text-foreground">
            Configure OAuth App
          </SheetTitle>
        </div>
        <SheetDescription className="sr-only">
          Configure and update your OAuth application settings including credentials and endpoints.
        </SheetDescription>
      </SheetHeader>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-6 pb-32">
        {/* App Header */}
        <div className="space-y-4">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-xl font-semibold flex-shrink-0">
              {app.display_name?.charAt(0) || 'A'}
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-xl font-semibold text-foreground mb-1">
                {app.display_name}
              </h2>
              <p className="text-sm text-muted-foreground mb-2">
                OAuth Application
              </p>
            </div>
          </div>
        </div>

        {/* OAuth Credentials */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-foreground mb-4">OAuth Credentials</h3>

          {/* Client ID */}
          <div className="space-y-2">
            <Label className="text-sm font-medium text-muted-foreground">Client ID</Label>
            <div className="flex gap-2">
              <Input
                value={app.client_id}
                readOnly
                className="font-mono text-sm bg-input border-border text-foreground"
              />
              <Button
                size="sm"
                variant="outline"
                onClick={() => copyToClipboard(app.client_id, "Client ID")}
                className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!border-primary hover:!text-primary"
              >
                <Copy className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Client Secret - only show if available */}
          {app.client_secret && (
            <div className="space-y-2">
              <Label className="text-sm font-medium text-muted-foreground">Client Secret</Label>
              <div className="flex gap-2">
                <Input
                  value={app.client_secret}
                  readOnly
                  type="password"
                  className="font-mono text-sm bg-input border-border text-foreground"
                />
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => copyToClipboard(app.client_secret as string, "Client Secret")}
                  className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!border-primary hover:!text-primary"
                >
                  <Copy className="w-4 h-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Warning when client secret is not available */}
          {!app.client_secret && (
            <div className="p-3 bg-amber-900/20 rounded-md border border-amber-900/40">
              <p className="text-xs text-amber-200 leading-relaxed">
                <span className="font-bold text-red-400">Client Secret:</span> The client secret is only displayed once during app creation for security reasons.
                If you need to access it again, you'll need to regenerate your OAuth credentials.
              </p>
            </div>
          )}
        </div>

        {/* Configuration Form */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            e.stopPropagation();
            updateForm.handleSubmit();
          }}
          className="space-y-6"
        >
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-foreground">App Configuration</h3>

            <updateForm.Field
              name="display_name"
              validators={{
                onChange: ({ value }) =>
                  !value ? "App name is required" : undefined,
              }}
              children={(field) => (
                <div className="space-y-2">
                  <Label htmlFor={field.name} className="text-muted-foreground">App Name</Label>
                  <Input
                    id={field.name}
                    name={field.name}
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(e) => field.handleChange(e.target.value)}
                    placeholder="My Integration App"
                    className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                  />
                  {field.state.meta.errors && (
                    <span className="text-sm text-red-400">
                      {field.state.meta.errors}
                    </span>
                  )}
                </div>
              )}
            />

            <updateForm.Field
              name="description"
              children={(field) => (
                <div className="space-y-2">
                  <Label htmlFor={field.name} className="text-muted-foreground">Description</Label>
                  <Textarea
                    id={field.name}
                    name={field.name}
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(e) => field.handleChange(e.target.value)}
                    placeholder="Brief description of your app..."
                    rows={3}
                    className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                  />
                </div>
              )}
            />

            <updateForm.Field
              name="launch_url"
              validators={{
                onChange: ({ value }) =>
                  !value ? "Launch URL is required" : undefined,
              }}
              children={(field) => (
                <div className="space-y-2">
                  <Label htmlFor={field.name} className="text-muted-foreground">Launch URL</Label>
                  <Input
                    id={field.name}
                    name={field.name}
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(e) => field.handleChange(e.target.value)}
                    placeholder="https://yourapp.com"
                    className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                  />
                  {field.state.meta.errors && (
                    <span className="text-sm text-red-400">
                      {field.state.meta.errors}
                    </span>
                  )}
                </div>
              )}
            />

            <updateForm.Field
              name="redirect_uris"
              validators={{
                onChange: ({ value }) =>
                  !value ? "Redirect URI is required" : undefined,
              }}
              children={(field) => (
                <div className="space-y-2">
                  <Label htmlFor={field.name} className="text-muted-foreground">Redirect URI</Label>
                  <Input
                    id={field.name}
                    name={field.name}
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(e) => field.handleChange(e.target.value)}
                    placeholder="https://yourapp.com/auth/callback"
                    className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                  />
                  {field.state.meta.errors && (
                    <span className="text-sm text-red-400">
                      {field.state.meta.errors}
                    </span>
                  )}
                </div>
              )}
            />
          </div>
        </form>

        {/* Security Notice */}
        <div className="space-y-4">
          <div className="p-3 bg-amber-900/20 rounded-md border border-amber-900/40">
            <p className="text-xs text-amber-200 leading-relaxed">
              <span className="font-bold text-red-400">Security Notice:</span> Keep your client secret secure and never expose it in client-side code.
              Only use it in server-to-server communications.
            </p>
          </div>
        </div>
      </div>

      {/* Floating Action Buttons */}
      <div className="sticky bottom-0 z-10 bg-popover border-t border-border px-4 py-4">
        <div className="flex items-center justify-end gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={onClose}
            className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!border-primary hover:!text-primary"
          >
            Cancel
          </Button>
          <Button
            onClick={() => updateForm.handleSubmit()}
            size="sm"
            disabled={updateOAuthApp.isLoading}
          >
            {updateOAuthApp.isLoading && (
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            )}
            <Save className="h-4 w-4 mr-1" />
            Save Changes
          </Button>
        </div>
      </div>
    </div>
  );
}
