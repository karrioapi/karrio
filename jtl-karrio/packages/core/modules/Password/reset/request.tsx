"use client";
import React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "@tanstack/react-form";
import { useUserMutation } from "@karrio/hooks/user";
import { p } from "@karrio/lib";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Label } from "@karrio/ui/components/ui/label";
import { Input } from "@karrio/ui/components/ui/input";
import { Button } from "@karrio/ui/components/ui/button";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";


export default function Page() {
  const router = useRouter();
  const { requestPasswordReset } = useUserMutation();
  const [topErrors, setTopErrors] = React.useState<string[]>([]);

  const form = useForm<{ email: string }>({
    defaultValues: { email: "" },
    onSubmit: async ({ value }) => {
      try {
        setTopErrors([]);
        await requestPasswordReset.mutateAsync({
          email: value.email,
          redirect_url: location.origin + p`/password/reset`,
        });
        router.push(`/password/reset/sent`);
      } catch (error: any) {
        const apiErrors = error?.data?.errors || error || [];
        const list = (Array.isArray(apiErrors) ? apiErrors : [apiErrors])
          .filter((e: any) => !e.field)
          .map((e: any) => e.message || String(e));
        setTopErrors(list);
      }
    },
  });

  return (
    <>
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8">
            <h2 className="mb-4 text-center text-xl font-semibold md:text-2xl">Forgotten your password?</h2>
            <p className="mb-4 px-4 text-center text-sm text-muted-foreground">
              Enter your email address below, and we’ll email instructions for setting a new one.
            </p>

            {topErrors.map((msg, idx) => (
              <Alert key={idx} variant="destructive" className="mb-3">
                <AlertDescription>{msg}</AlertDescription>
              </Alert>
            ))}

            <form
              onSubmit={(e) => {
                e.preventDefault();
                e.stopPropagation();
                form.handleSubmit();
              }}
              className="space-y-2 py-4"
            >
              {/* @ts-ignore */}
              <form.Field
                name="email"
                validators={{
                  onChange: ({ value }) => (!value ? "Email is required" : undefined),
                }}
              >
                {(field) => (
                  <div className="space-y-2 pb-4">
                    <Label htmlFor={field.name}>Email</Label>
                    <Input
                      id={field.name}
                      name={field.name}
                      type="email"
                      value={field.state.value}
                      onBlur={field.handleBlur}
                      onChange={(e) => field.handleChange(e.target.value)}
                      required
                    />
                  </div>
                )}
              </form.Field>

              {/* @ts-ignore */}
              <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting]}>
                {([canSubmit, isSubmitting]) => (
                  <Button type="submit" className="w-full" disabled={!canSubmit}>
                    {isSubmitting ? "Sending..." : "Reset my password"}
                  </Button>
                )}
              </form.Subscribe>
            </form>
          </CardContent>
        </Card>
      </div>

      <div className="my-4 text-center text-sm">
        Return to <Link href="/signin" className="font-semibold text-primary hover:underline">Sign in</Link>
      </div>
    </>
  );
}
