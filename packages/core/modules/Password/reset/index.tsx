"use client";
import React, { Suspense, useEffect } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useForm } from "@tanstack/react-form";
import { ConfirmPasswordResetMutationInput } from "@karrio/types";
import { useUserMutation } from "@karrio/hooks/user";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Label } from "@karrio/ui/components/ui/label";
import { Input } from "@karrio/ui/components/ui/input";
import { Button } from "@karrio/ui/components/ui/button";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { FieldInfo } from "@karrio/ui/core/components/field-info";


const DEFAULT_VALUE: Partial<ConfirmPasswordResetMutationInput> = {
  new_password1: "",
  new_password2: "",
};

// Inner component that uses useSearchParams
const PasswordResetForm = (): JSX.Element => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [uidb64, token] = [
    searchParams.get("uidb64") as string,
    searchParams.get("token") as string,
  ];
  const {
    confirmPasswordReset: { error, mutateAsync },
  } = useUserMutation();

  const form = useForm<ConfirmPasswordResetMutationInput>({
    defaultValues: {
      uid: uidb64 || "",
      token: token || "",
      new_password1: DEFAULT_VALUE.new_password1!,
      new_password2: DEFAULT_VALUE.new_password2!,
    },
    onSubmit: async ({ value }) => {
      await mutateAsync(value);
      router.push("/password/reset/done");
    },
  });

  useEffect(() => {
    (form as any).setFieldValue("uid", uidb64 || "");
    (form as any).setFieldValue("token", token || "");
  }, [uidb64, token]);

  const apiErrors = ((error as any)?.data?.errors || []) as any[];
  const validation = (apiErrors[0]?.validation || {}) as Record<string, string[]>;

  return (
    <>
      <Card className="mx-auto mt-6 w-full max-w-md">
        <CardContent className="pt-6">
          <h2 className="mb-2 text-center text-xl font-semibold">New Password</h2>
          <p className="mb-4 text-center text-sm text-muted-foreground">
            Enter your new email and password.
          </p>

          {apiErrors.map((e, i) => (
            <Alert key={i} variant="destructive" className="mb-3">
              <AlertDescription>{e.message}</AlertDescription>
            </Alert>
          ))}

          <form
            onSubmit={(e) => {
              e.preventDefault();
              e.stopPropagation();
              form.handleSubmit();
            }}
            className="space-y-4"
          >
            {/* @ts-ignore */}
            <form.Field
              name="new_password1"
              validators={{
                onChange: ({ value }) =>
                  !value
                    ? "Password is required"
                    : value.length < 8
                    ? "Password must be at least 8 characters"
                    : undefined,
              }}
            >
              {(field) => (
                <div className="space-y-2">
                  <Label htmlFor={field.name}>Password</Label>
                  <Input
                    id={field.name}
                    name={field.name}
                    type="password"
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(e) => field.handleChange(e.target.value)}
                    required
                  />
                  <div className="text-sm text-red-500">
                    <FieldInfo field={field} />
                  </div>
                  {(validation["new_password1"] || []).map((m, i) => (
                    <div key={i} className="text-sm text-red-500">{m}</div>
                  ))}
                </div>
              )}
            </form.Field>

            {/* @ts-ignore */}
            <form.Field
              name="new_password2"
              validators={{
                onChange: ({ value }) =>
                  !value
                    ? "Please confirm your password"
                    : value !== (form.state.values as any).new_password1
                    ? "Passwords do not match"
                    : undefined,
              }}
            >
              {(field) => (
                <div className="space-y-2">
                  <Label htmlFor={field.name}>Confirm Password</Label>
                  <Input
                    id={field.name}
                    name={field.name}
                    type="password"
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(e) => field.handleChange(e.target.value)}
                    required
                  />
                  <div className="text-sm text-red-500">
                    <FieldInfo field={field} />
                  </div>
                  {(validation["new_password2"] || []).map((m, i) => (
                    <div key={i} className="text-sm text-red-500">{m}</div>
                  ))}
                </div>
              )}
            </form.Field>

            {/* @ts-ignore */}
            <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting]}>
              {([canSubmit, isSubmitting]) => (
                <Button type="submit" className="w-full" disabled={!canSubmit}>
                  {isSubmitting ? "Saving..." : "Change my password"}
                </Button>
              )}
            </form.Subscribe>
          </form>
        </CardContent>
      </Card>

      <div className="my-4 text-center text-sm">
        Return to {" "}
        <Link href="/signin" className="font-semibold text-primary hover:underline">
          Sign in
        </Link>
      </div>
    </>
  );
};

// Component with LoadingProvider
const LoadingWrappedComponent = () => {
  return <PasswordResetForm />;
};

// Exported component with Suspense
export default function Page() {
  return (
    <Suspense fallback={
      <Card className="mx-auto mt-6 w-full max-w-md"><CardContent className="pt-6 text-center"><p>Loading...</p></CardContent></Card>
    }>
      <LoadingWrappedComponent />
    </Suspense>
  );
}
