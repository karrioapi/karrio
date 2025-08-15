"use client";
import React, { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { signIn, getSession } from "next-auth/react";
import { useForm } from "@tanstack/react-form";
import { useSearchParams } from "next/navigation";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { getCookie, isNone } from "@karrio/lib";
import { p } from "@karrio/lib";
import { FieldInfo } from "@karrio/ui/core/components/field-info";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";

// Inner component that uses useSearchParams
function SignInPage(pageProps: any) {
  const { metadata } = useAPIMetadata();
  const searchParams = useSearchParams();
  const [authError, setAuthError] = useState<string | null>(null);
  const form = useForm({
    defaultValues: {
      email: searchParams.get("email") || "",
      password: "",
    },
    onSubmit: async ({ value }) => {
      const orgId = getCookie("orgId");
      const response: any = await signIn("credentials", {
        redirect: false,
        email: value.email,
        password: value.password,
        ...(!!orgId ? { orgId } : {}),
      });

      // Prefer error branch first: NextAuth may return ok=true with an error
      if (response?.error) {
        // Normalize common NextAuth credential errors
        const message =
          response.error === "CredentialsSignin"
            ? "Invalid username or password"
            : String(response.error);
        setAuthError(message);
        try {
          // Persist error in URL so it survives any reloads
          const url = new URL(window.location.href);
          url.searchParams.set("error", "CredentialsSignin");
          window.history.replaceState({}, "", url.toString());
        } catch { }
      } else if (response?.ok) {
        // Clear any persisted error state
        setAuthError(null);
        try {
          const url = new URL(window.location.href);
          url.searchParams.delete("error");
          window.history.replaceState({}, "", url.toString());
        } catch { }

        // Ensure session is ready before navigating to avoid redirect loop
        try {
          let tries = 0;
          while (tries < 10) {
            const session = await getSession();
            if ((session as any)?.accessToken) break;
            await new Promise((r) => setTimeout(r, 100));
            tries += 1;
          }
        } catch { }

        const nextUrl = searchParams.get("next");
        const target = nextUrl ? p`${nextUrl}` : response.url || "/";
        window.location.replace(target);
      } else {
        setAuthError("Unable to sign in. Please try again.");
      }
    },
  });

  // Capture NextAuth error from query string in case of reload/redirect
  useEffect(() => {
    const errParam = searchParams.get("error");
    const message = errParam === "CredentialsSignin" ? "Invalid username or password" : errParam || null;
    if (message) setAuthError(message);
    // Strip error from URL so it doesn't reappear on rerender
    if (errParam) {
      try {
        const url = new URL(window.location.href);
        url.searchParams.delete("error");
        window.history.replaceState({}, "", url.toString());
      } catch { }
    }
  }, [searchParams]);

  return (
    <>
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8">
            <h2 className="mb-4 text-center text-xl font-semibold md:text-2xl">Sign in to your account</h2>

            {authError && (
              <Alert variant="destructive" className="mb-4">
                <AlertDescription>{authError}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2 py-4">
              {/* @ts-ignore */}
              <form.Field
                name="email"
                validators={{
                  onChange: ({ value }) => (!value ? "An email is required" : undefined),
                }}
              >
                {(field) => (
                  <div className="space-y-2 py-1">
                    <Label htmlFor={field.name}>Email</Label>
                    <Input
                      id={field.name}
                      name={field.name}
                      value={field.state.value}
                      onBlur={field.handleBlur}
                      disabled={!isNone(searchParams.get("email"))}
                      onChange={(e) => {
                        if (authError) setAuthError(null);
                        field.handleChange(e.target.value);
                      }}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          e.preventDefault();
                          e.stopPropagation();
                          form.handleSubmit();
                        }
                      }}
                      required
                    />
                    <div className="text-sm text-red-500">
                      <FieldInfo field={field} />
                    </div>
                  </div>
                )}
              </form.Field>

              {/* @ts-ignore */}
              <form.Field
                name="password"
                validators={{
                  onChange: ({ value }) => (!value ? "A password is required" : undefined),
                }}
              >
                {(field) => (
                  <div className="space-y-2 pt-1 pb-4">
                    <div className="flex items-center justify-between">
                      <Label htmlFor={field.name}>Password</Label>
                      <Link href="/password/reset/request" className="text-sm text-primary hover:underline" tabIndex={-1}>
                        Forgot your password?
                      </Link>
                    </div>
                    <Input
                      id={field.name}
                      name={field.name}
                      value={field.state.value}
                      onBlur={field.handleBlur}
                      onChange={(e) => {
                        if (authError) setAuthError(null);
                        field.handleChange(e.target.value);
                      }}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          e.preventDefault();
                          e.stopPropagation();
                          form.handleSubmit();
                        }
                      }}
                      type="password"
                      placeholder="Password"
                      required
                    />
                    <div className="text-sm text-red-500">
                      <FieldInfo field={field} />
                    </div>
                  </div>
                )}
              </form.Field>

              {/* @ts-ignore */}
              <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting]}>
                {([canSubmit, isSubmitting]) => (
                  <Button
                    type="button"
                    className="w-full"
                    disabled={!canSubmit}
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      form.handleSubmit();
                    }}
                  >
                    {isSubmitting ? "Signing in..." : "Sign in"}
                  </Button>
                )}
              </form.Subscribe>
            </div>
          </CardContent>
        </Card>
      </div>

      {metadata?.ALLOW_SIGNUP && (
        <div className="my-4 text-center text-sm">
          Don't have an account? <Link href="/signup" className="font-semibold text-primary hover:underline">Sign Up</Link>
        </div>
      )}
    </>
  );
}

// Exported component with Suspense
export default function Page(pageProps: any) {
  return (
    <Suspense fallback={
      <div className="card isolated-card">
        <div className="card-content has-text-centered">
          <p className="subtitle">Loading...</p>
        </div>
      </div>
    }>
      <SignInPage {...pageProps} />
    </Suspense>
  );
}
