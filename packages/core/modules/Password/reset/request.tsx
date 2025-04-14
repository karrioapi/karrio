"use client";
import { LoadingProvider, useLoader } from "@karrio/ui/core/components/loader";
import { ButtonField } from "@karrio/ui/core/components/button-field";
import { useUserMutation } from "@karrio/hooks/user";
import { useRouter } from "next/navigation";
import React, { FormEvent, useRef } from "react";
import { p, isNone } from "@karrio/lib";
import Link from "next/link";


export default function Page() {
  const Component = (): JSX.Element => {
    const router = useRouter();
    const email = useRef<HTMLInputElement>(null);
    const [errors, setErrors] = React.useState<any[]>([]);
    const { loading, setLoading } = useLoader();
    const { requestPasswordReset } = useUserMutation();

    const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      try {
        setLoading(true);
        await requestPasswordReset.mutateAsync({
          email: email.current?.value as string,
          redirect_url: location.origin + p`/password/reset`,
        });
        router.push(`/password/reset/sent`);
      } catch (error: any) {
        const _error = error.data?.errors || error;
        setErrors(Array.isArray(_error) ? _error : [_error]);
      }
      setLoading(false);
    };

    return (
      <>
        <div className="card isolated-card">
          <div className="card-content">
            <p className="subtitle has-text-centered mb-4">
              Forgotten your password?
            </p>
            <p className="has-text-centered mb-4">
              Enter your email address below, and we’ll email instructions for
              setting a new one.
            </p>

            {(errors as any[])
              .filter((error) => isNone(error.field))
              .map(({ message }, index) => (
                <p
                  key={index}
                  className="has-text-danger has-text-centered is-size-7"
                >
                  {message}
                </p>
              ))}

            <form method="post" onSubmit={onSubmit}>
              <div className="field mt-6">
                <div className="control">
                  <input
                    className="input"
                    id="id_email"
                    name="email"
                    type="email"
                    placeholder="Email"
                    ref={email}
                    required
                  />
                </div>
              </div>

              {errors
                .filter((error) => error.field === "email")
                .map(({ messages }) =>
                  messages.map((message: any, index: number) => (
                    <p key={index} className="has-text-danger is-size-7">
                      {message}
                    </p>
                  )),
                )}

              <ButtonField
                type="submit"
                disabled={loading}
                className={`is-primary is-fullwidth mt-6`}
                controlClass="has-text-centered"
              >
                <span>Reset my password</span>
              </ButtonField>
            </form>
          </div>
        </div>

        <div className="has-text-centered my-4 is-size-6">
          <span>
            Return to <Link href="/signin">Sign in</Link>
          </span>
        </div>
      </>
    );
  };

  return (
    <>
      <LoadingProvider>
        <Component />
      </LoadingProvider>
    </>
  );
}
