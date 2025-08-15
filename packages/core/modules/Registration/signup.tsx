"use client";
import React, { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useForm } from "@tanstack/react-form";
import { useUserMutation } from "@karrio/hooks/user";
import { p, isNoneOrEmpty } from "@karrio/lib";
import {
  RegisterUserMutationInput,
  register_user_register_user_errors,
} from "@karrio/types";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { FieldInfo } from "@karrio/ui/core/components/field-info";

const DEFAULT_VALUE: Partial<RegisterUserMutationInput> = {
  email: "",
  full_name: "",
  password1: "",
  password2: "",
};

// Inner component that uses useSearchParams
const SignUpForm = (): JSX.Element => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const emailParam = (searchParams.get("email") as string) || "";
  const mutation = useUserMutation();
  const [errors, setErrors] = useState<register_user_register_user_errors[]>([]);

  const form = useForm<RegisterUserMutationInput>({
    defaultValues: {
      email: emailParam || DEFAULT_VALUE.email!,
      full_name: DEFAULT_VALUE.full_name!,
      password1: DEFAULT_VALUE.password1!,
      password2: DEFAULT_VALUE.password2!,
      redirect_url: "",
    },
    onSubmit: async ({ value }) => {
      try {
        setErrors([]);
        await mutation.registerUser.mutateAsync({
          email: value.email,
          full_name: value.full_name,
          password1: value.password1,
          password2: value.password2,
          redirect_url: location.origin + p`/email`,
        });
        router.push(p`/signup/success`);
      } catch (error: any) {
        setErrors(Array.isArray(error) ? error : [error]);
      }
    },
  });

  useEffect(() => {
    if (!isNoneOrEmpty(emailParam)) {
      // No-op: default value is already set; disable input via prop
    }
  }, [emailParam]);

  return (
    <>
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8">
            <h2 className="mb-4 text-center text-xl font-semibold md:text-2xl">Create your account</h2>

            {(errors as any[])
              .filter((error) => !error.field)
              .map(({ message }, index) => (
                <Alert key={index} variant="destructive" className="mb-4">
                  <AlertDescription>{message}</AlertDescription>
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
                name="email"
                validators={{
                  onChange: ({ value }) => (!value ? "Email is required" : undefined),
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
                      onChange={(e) => field.handleChange(e.target.value)}
                      disabled={!isNoneOrEmpty(emailParam)}
                      required
                    />
                    {/* Client-side validation errors */}
                    <div className="text-sm text-red-500">
                      <FieldInfo field={field} />
                    </div>
                    {/* Server field errors */}
                    {errors
                      .filter((error) => error.field === "email")
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
              <form.Field
                name="full_name"
                validators={{
                  onChange: ({ value }) => (!value ? "Full name is required" : undefined),
                }}
              >
                {(field) => (
                  <div className="space-y-2 py-1">
                    <Label htmlFor={field.name}>Full Name</Label>
                    <Input
                      id={field.name}
                      name={field.name}
                      value={field.state.value as string}
                      onBlur={field.handleBlur}
                      onChange={(e) => field.handleChange(e.target.value)}
                      required
                    />
                    {/* Client-side validation errors */}
                    <div className="text-sm text-red-500">
                      <FieldInfo field={field} />
                    </div>
                    {errors
                      .filter((error) => error.field === "full_name")
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
              <form.Field
                name="password1"
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
                  <div className="space-y-2 py-1">
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
                    {/* Client-side validation errors */}
                    <div className="text-sm text-red-500">
                      <FieldInfo field={field} />
                    </div>
                    {errors
                      .filter((error) => error.field === "password1")
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
              <form.Field
                name="password2"
                validators={{
                  onChange: ({ value }) =>
                    !value
                      ? "Please confirm your password"
                      : value !== (form.state.values as any).password1
                        ? "Passwords do not match"
                        : undefined,
                }}
              >
                {(field) => (
                  <div className="space-y-2 pt-1 pb-4">
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
                    {/* Client-side validation errors */}
                    <div className="text-sm text-red-500">
                      <FieldInfo field={field} />
                    </div>
                    {/* Live mismatch indicator even if field not touched */}
                    {/* @ts-ignore */}
                    <form.Subscribe selector={(state) => [state.values.password1, state.values.password2]}>
                      {([p1, p2]) => (
                        p1 && p2 && p1 !== p2 ? (
                          <div className="text-sm text-red-500">Passwords do not match</div>
                        ) : null
                      )}
                    </form.Subscribe>
                    {errors
                      .filter((error) => error.field === "password2")
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
                  <div className="space-y-2">
                    {!canSubmit && !isSubmitting && (
                      <Alert variant="destructive">
                        <AlertDescription>
                          Please fix the errors above before continuing.
                        </AlertDescription>
                      </Alert>
                    )}
                    <Button type="submit" className="w-full" disabled={!canSubmit}>
                      {isSubmitting ? "Creating account..." : "Sign up"}
                    </Button>
                  </div>
                )}
              </form.Subscribe>
            </form>
          </CardContent>
        </Card>
      </div>

      <div className="my-4 text-center text-sm">
        Have an account? <Link href="/signin" className="font-semibold text-primary hover:underline">Sign in</Link>
      </div>
    </>
  );
};

// Exported component with Suspense
export default function SignUp(pageProps: any) {
  return (
    <Suspense fallback={
      <Card className="mx-auto mt-6 w-full max-w-md"><CardContent className="pt-6"><p className="text-center">Loading...</p></CardContent></Card>
    }>
      <SignUpForm />
    </Suspense>
  );
}
