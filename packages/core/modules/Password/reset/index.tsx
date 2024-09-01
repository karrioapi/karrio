"use client";
import React, { FormEvent, useContext, useEffect, useReducer } from "react";
import { LoadingProvider, Loading } from "@karrio/ui/components/loader";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { ConfirmPasswordResetMutationInput } from "@karrio/types";
import { ButtonField } from "@karrio/ui/components/button-field";
import { InputField } from "@karrio/ui/components/input-field";
import { useUserMutation } from "@karrio/hooks/user";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";

export const generateMetadata = dynamicMetadata("Password Reset");

const DEFAULT_VALUE: Partial<ConfirmPasswordResetMutationInput> = {
  new_password1: "",
  new_password2: "",
};

function reducer(
  state: Partial<ConfirmPasswordResetMutationInput>,
  { name, value }: { name: string; value: string | object },
) {
  switch (name) {
    case "full":
      return { ...(value as object) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}

const Component: React.FC<{}> = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [uidb64, token] = [
    searchParams.get("uidb64") as string,
    searchParams.get("token") as string,
  ];
  const { loading, setLoading } = useContext(Loading);
  const [data, dispatch] = useReducer(
    reducer,
    DEFAULT_VALUE,
    () => DEFAULT_VALUE,
  );
  const {
    confirmPasswordReset: { error, mutateAsync },
  } = useUserMutation();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value: string = event.target.value;
    const name: string = event.target.name;

    dispatch({ name, value });
  };
  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      setLoading(true);
      await mutateAsync(data as ConfirmPasswordResetMutationInput);
      router.push("/password/reset/done");
    } catch (error: any) {
      console.log(error);
    }
    setLoading(false);
  };
  const renderFieldError = (check: CallableFunction, errorData: any) => {
    const validation = (errorData?.data?.errors || [])[0]?.validation || {};
    return (
      <>
        {Object.entries(validation)
          .filter(([key, _]) => check(key))
          .map(([_, messages]: any) =>
            messages.map((message: string, index: number) => (
              <p key={index} className="has-text-danger is-size-7 my-1">
                {message}
              </p>
            )),
          )}
      </>
    );
  };

  useEffect(() => {
    dispatch({ name: "partial", value: { uid: uidb64, token } });
  }, [uidb64, token]);

  return (
    <>
      <div className="card isolated-card">
        <div className="card-content">
          <p className="subtitle has-text-centered mb-4">New Password</p>
          <p className="has-text-centered mb-4">
            Enter your new email and password.
          </p>

          {((error as any)?.data?.errors || []).map((_: any, index: number) => (
            <>
              <p key={index} className="has-text-danger is-size-7 my-1">
                {_.message}
              </p>
            </>
          ))}

          <form method="post" onSubmit={onSubmit}>
            <InputField
              label="Password"
              name="new_password1"
              type="password"
              placeholder="New Password"
              wrapperClass="mt-3"
              onChange={handleChange}
              value={data.new_password1}
              required
            >
              {renderFieldError((_: string) => _ === "new_password1", error)}
            </InputField>

            <InputField
              label="Confirm Password"
              name="new_password2"
              type="password"
              placeholder="Confirm Password"
              wrapperClass="mt-3"
              onChange={handleChange}
              value={data.new_password2}
              required
            >
              {renderFieldError((_: string) => _ === "new_password2", error)}
            </InputField>

            <ButtonField
              type="submit"
              disabled={loading}
              className={`is-primary is-fullwidth mt-6`}
              controlClass="has-text-centered"
            >
              <span>Change my password</span>
            </ButtonField>
          </form>
        </div>
      </div>

      <div className="has-text-centered my-4 is-size-6">
        <span>
          Return to{" "}
          <Link legacyBehavior href="/signin">
            Sign in
          </Link>
        </span>
      </div>
    </>
  );
};

export default function Page(pageProps: any) {
  return (
    <>
      <LoadingProvider>
        <Component />
      </LoadingProvider>
    </>
  );
}
