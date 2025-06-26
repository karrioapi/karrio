import React from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Separator } from "./ui/separator";
import { User, Mail, Lock, Save, X } from "lucide-react";
import { useUser } from "@karrio/hooks/user";
import { useUserMutation } from "@karrio/hooks/user";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { NotificationType } from "@karrio/types";

interface EmailChangeDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

function EmailChangeDialog({ open, onOpenChange }: EmailChangeDialogProps) {
  const mutation = useUserMutation();
  const { notify } = useNotifier();
  const [loading, setLoading] = React.useState(false);
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [errors, setErrors] = React.useState<any[]>([]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setErrors([]);

    try {
      await mutation.requestEmailChange.mutateAsync({
        email,
        password,
        redirect_url: `${location.origin}/email/change`,
      });
      notify({
        type: NotificationType.success,
        message: "Email change request sent! Check your inbox."
      });
      onOpenChange(false);
      setEmail("");
      setPassword("");
    } catch (error: any) {
      setErrors(Array.isArray(error) ? error : [error]);
    } finally {
      setLoading(false);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm">
      <div className="fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 sm:rounded-lg">
        <div className="space-y-4">
          <div className="space-y-2">
            <h2 className="text-lg font-semibold">Change Email Address</h2>
            <p className="text-sm text-muted-foreground">
              We'll send a confirmation link to your new email address.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="new-email">New Email Address</Label>
              <Input
                id="new-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter new email address"
                required
              />
              {errors.filter(error => error.field === "email").map(({ messages }, index) =>
                messages.map((message: string, msgIndex: number) => (
                  <p key={`${index}-${msgIndex}`} className="text-sm text-destructive">
                    {message}
                  </p>
                ))
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="current-password">Current Password</Label>
              <Input
                id="current-password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter current password"
                required
              />
              {errors.filter(error => error.field === "password").map(({ messages }, index) =>
                messages.map((message: string, msgIndex: number) => (
                  <p key={`${index}-${msgIndex}`} className="text-sm text-destructive">
                    {message}
                  </p>
                ))
              )}
            </div>

            <div className="flex justify-end gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => onOpenChange(false)}
                disabled={loading}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={loading}
              >
                {loading ? "Sending..." : "Send Confirmation"}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

interface PasswordChangeFormProps {
  onSuccess?: () => void;
}

function PasswordChangeForm({ onSuccess }: PasswordChangeFormProps) {
  const mutation = useUserMutation();
  const { notify } = useNotifier();
  const [loading, setLoading] = React.useState(false);
  const [passwords, setPasswords] = React.useState({
    old_password: "",
    new_password1: "",
    new_password2: "",
  });
  const [errors, setErrors] = React.useState<any>({});

  const handleChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setPasswords(prev => ({ ...prev, [field]: e.target.value }));
    if (errors[field]) {
      setErrors((prev: any) => ({ ...prev, [field]: undefined }));
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setErrors({});

    try {
      await mutation.changePassword.mutateAsync(passwords);
      notify({
        type: NotificationType.success,
        message: "Password changed successfully"
      });
      setPasswords({
        old_password: "",
        new_password1: "",
        new_password2: "",
      });
      onSuccess?.();
    } catch (error: any) {
      setErrors(error);
    } finally {
      setLoading(false);
    }
  };

  const isDisabled = !passwords.old_password || !passwords.new_password1 || !passwords.new_password2;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="old-password">Current Password</Label>
        <Input
          id="old-password"
          type="password"
          value={passwords.old_password}
          onChange={handleChange("old_password")}
          placeholder="Enter current password"
          required
        />
        {errors.old_password && (
          <p className="text-sm text-destructive">{errors.old_password}</p>
        )}
      </div>

      <Separator />

      <div className="space-y-2">
        <Label htmlFor="new-password1">New Password</Label>
        <Input
          id="new-password1"
          type="password"
          value={passwords.new_password1}
          onChange={handleChange("new_password1")}
          placeholder="Enter new password"
          required
        />
        {errors.new_password1 && (
          <p className="text-sm text-destructive">{errors.new_password1}</p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="new-password2">Confirm New Password</Label>
        <Input
          id="new-password2"
          type="password"
          value={passwords.new_password2}
          onChange={handleChange("new_password2")}
          placeholder="Confirm new password"
          required
        />
        {errors.new_password2 && (
          <p className="text-sm text-destructive">{errors.new_password2}</p>
        )}
      </div>

      <Button
        type="submit"
        disabled={isDisabled || loading}
      >
        <Lock className="h-4 w-4 mr-2" />
        {loading ? "Changing Password..." : "Change Password"}
      </Button>
    </form>
  );
}

interface ProfileUpdateFieldProps {
  label: string;
  value: string;
  onSave: (value: string) => Promise<void>;
  placeholder?: string;
  type?: string;
}

function ProfileUpdateField({ label, value, onSave, placeholder, type = "text" }: ProfileUpdateFieldProps) {
  const [editing, setEditing] = React.useState(false);
  const [inputValue, setInputValue] = React.useState(value);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    setInputValue(value);
  }, [value]);

  const handleSave = async () => {
    setLoading(true);
    try {
      await onSave(inputValue);
      setEditing(false);
    } catch (error) {
      // Error handled by parent
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setInputValue(value);
    setEditing(false);
  };

  if (editing) {
    return (
      <div className="space-y-2">
        <Label>{label}</Label>
        <div className="flex gap-2">
          <Input
            type={type}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={placeholder}
            className="flex-1"
          />
          <Button
            size="sm"
            variant="outline"
            onClick={handleCancel}
            disabled={loading}
          >
            <X className="h-3 w-3" />
          </Button>
          <Button
            size="sm"
            onClick={handleSave}
            disabled={loading}
          >
            <Save className="h-3 w-3" />
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      <div className="flex items-center gap-2">
        <div className="flex-1 px-3 py-2 border border-input rounded-md bg-background text-sm">
          {value || <span className="text-muted-foreground">{placeholder}</span>}
        </div>
        <Button
          size="sm"
          variant="outline"
          onClick={() => setEditing(true)}
        >
          Edit
        </Button>
      </div>
    </div>
  );
}

export function ProfileSettings() {
  const { references } = useAPIMetadata();
  const { notify } = useNotifier();
  const mutation = useUserMutation();
  const { query: { data: { user } = {} } } = useUser();

  const [emailDialogOpen, setEmailDialogOpen] = React.useState(false);

  const updateProfile = async (field: string, value: string) => {
    try {
      await mutation.updateUser.mutateAsync({ [field]: value });
      notify({
        type: NotificationType.success,
        message: "Profile updated successfully"
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || "Failed to update profile"
      });
      throw error;
    }
  };

  return (
    <div className="space-y-6">
      {/* Profile Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            Profile Information
          </CardTitle>
          <CardDescription>
            Your personal information used on {references?.APP_NAME}.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="max-w-md space-y-6">
            <div className="space-y-2">
              <Label>Email Address</Label>
              <div className="flex items-center gap-2">
                <div className="flex-1 px-3 py-2 border border-input rounded-md bg-background text-sm">
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4 text-muted-foreground" />
                    {user?.email}
                  </div>
                </div>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setEmailDialogOpen(true)}
                >
                  Change Email
                </Button>
              </div>
              <p className="text-xs text-muted-foreground">
                Your email address is your identity on {references?.APP_NAME} and is used to log in.
              </p>
            </div>

            <ProfileUpdateField
              label="Full Name"
              value={user?.full_name || ""}
              onSave={(value) => updateProfile("full_name", value)}
              placeholder="Enter your full name (optional)"
            />
          </div>
        </CardContent>
      </Card>

      {/* Password Management */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lock className="h-5 w-5" />
            Password & Security
          </CardTitle>
          <CardDescription>
            Manage your account password and security settings.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-w-md">
            <PasswordChangeForm />
          </div>
        </CardContent>
      </Card>

      <EmailChangeDialog
        open={emailDialogOpen}
        onOpenChange={setEmailDialogOpen}
      />
    </div>
  );
}
