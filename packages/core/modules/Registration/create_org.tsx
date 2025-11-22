"use client";
import { create_organization_create_organization_errors } from "@karrio/types/graphql/ee/types";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { useOrganizationMutation } from "@karrio/hooks/organization";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { FieldInfo } from "@karrio/ui/core/components/field-info";
import React, { Suspense, useState, useEffect } from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { useForm } from "@tanstack/react-form";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { p } from "@karrio/lib";

const CreateOrgForm = (): JSX.Element => {
  const router = useRouter();
  const { data: session, update } = useSession();
  const { metadata } = useAPIMetadata();
  const { createOrganization } = useOrganizationMutation();
  const [errors, setErrors] = useState<create_organization_create_organization_errors[]>([]);

  // Initialize form hook before any conditional returns
  const form = useForm({
    defaultValues: { name: "" },
    onSubmit: async ({ value }) => {
      try {
        setErrors([]);
        const result = await createOrganization.mutateAsync({ name: value.name });

        if (result?.create_organization?.organization?.id) {
          const orgId = result.create_organization.organization.id;

          // Update session with new orgId
          await update({ orgId });

          // Give the session update a moment to propagate
          await new Promise(resolve => setTimeout(resolve, 500));

          // Force a hard refresh to ensure session is fully updated
          window.location.href = p`/`;
        } else if (result?.create_organization?.errors) {
          setErrors(result.create_organization.errors);
        }
      } catch (error: any) {
        console.error("Organization creation error:", error);
        const parsedErrors: create_organization_create_organization_errors[] = [];

        if (error.data?.create_organization?.errors) {
          parsedErrors.push(...error.data.create_organization.errors);
        } else if (error.response?.data?.errors) {
          parsedErrors.push(...error.response.data.errors);
        } else if (error.message) {
          parsedErrors.push({
            field: "",
            messages: [error.message]
          });
        } else {
          parsedErrors.push({
            field: "",
            messages: ["Failed to create organization. Please try again."]
          });
        }

        setErrors(parsedErrors);
      }
    },
  });

  // Guard: redirect if MULTI_ORGANIZATIONS is disabled (open source mode)
  useEffect(() => {
    if (metadata && !metadata.MULTI_ORGANIZATIONS) {
      router.replace(p`/`);
    }
  }, [metadata, router]);

  // Show loading state while metadata loads or if MULTI_ORGANIZATIONS is disabled
  if (!metadata || !metadata.MULTI_ORGANIZATIONS) {
    return (
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md">
          <CardContent className="pt-6">
            <p className="text-center">Loading...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <>
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8">
            <h2 className="mb-4 text-center text-xl font-semibold md:text-2xl">Create Your Organization</h2>
            <p className="mb-6 text-center text-sm text-muted-foreground">
              Set up your organization to start using Karrio
            </p>

            {(errors as any[])
              .filter((error) => !error.field)
              .map(({ messages }, index) => (
                <Alert key={index} variant="destructive" className="mb-4">
                  <AlertDescription>
                    {messages.map((msg: string, idx: number) => (
                      <p key={idx}>{msg}</p>
                    ))}
                  </AlertDescription>
                </Alert>
              ))}

            <form
              method="post"
              onSubmit={(e) => {
                e.preventDefault();
                e.stopPropagation();
                form.handleSubmit();
              }}
              className="space-y-2 py-4"
            >
              {/* @ts-ignore */}
              <form.Field
                name="name"
                validators={{
                  onChange: ({ value }) => (!value ? "Organization name is required" : undefined),
                }}
              >
                {(field) => (
                  <div className="space-y-2 py-1">
                    <Label htmlFor={field.name}>Organization Name</Label>
                    <Input
                      id={field.name}
                      name={field.name}
                      value={field.state.value}
                      onBlur={field.handleBlur}
                      onChange={(e) => {
                        if (errors.length > 0) setErrors([]);
                        field.handleChange(e.target.value);
                      }}
                      placeholder="Acme Inc"
                      required
                    />
                    <div className="text-sm text-red-500">
                      <FieldInfo field={field} />
                    </div>
                    {errors
                      .filter((error) => error.field === "name")
                      .map(({ messages }, idx) => (
                        <div key={idx} className="text-sm text-red-500">
                          {messages.map((m, i) => (
                            <p key={i}>{m}</p>
                          ))}
                        </div>
                      ))}
                  </div>
                )}
              </form.Field>

              {/* @ts-ignore */}
              <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting]}>
                {([canSubmit, isSubmitting]) => (
                  <div className="space-y-2 pt-4">
                    <Button type="submit" className="w-full" disabled={!canSubmit || isSubmitting}>
                      {isSubmitting ? "Creating organization..." : "Create Organization"}
                    </Button>
                  </div>
                )}
              </form.Subscribe>
            </form>
          </CardContent>
        </Card>
      </div>
    </>
  );
};

export default function CreateOrganization() {
  return (
    <Suspense fallback={
      <Card className="mx-auto mt-6 w-full max-w-md"><CardContent className="pt-6"><p className="text-center">Loading...</p></CardContent></Card>
    }>
      <CreateOrgForm />
    </Suspense>
  );
}
