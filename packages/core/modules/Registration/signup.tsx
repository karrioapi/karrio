"use client";
import {
  RegisterUserMutationInput,
  register_user_register_user_errors,
} from "@karrio/types";
import React, { FormEvent, Suspense, useEffect, useReducer, useState } from "react";
import { LoadingProvider, useLoader } from "@karrio/ui/core/components/loader";
import { ButtonField } from "@karrio/ui/core/components/button-field";
import { InputField } from "@karrio/ui/core/components/input-field";
import { useRouter, useSearchParams } from "next/navigation";
import { useUserMutation } from "@karrio/hooks/user";
import { isNone, isNoneOrEmpty } from "@karrio/lib";
import { p } from "@karrio/lib";
import Link from "next/link";

const DEFAULT_VALUE: Partial<RegisterUserMutationInput> = {
  email: "",
  full_name: "",
  password1: "",
  password2: "",
};

function reducer(
  state: Partial<RegisterUserMutationInput>,
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

// Inner component that uses useSearchParams
const SignUpForm = (): JSX.Element => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const email = searchParams.get("email") as string;
  const mutation = useUserMutation();
  const { loading, setLoading } = useLoader();
  const [user, dispatch] = useReducer(
    reducer,
    DEFAULT_VALUE,
    () => DEFAULT_VALUE,
  );
  const [errors, setErrors] = useState<register_user_register_user_errors[]>(
    [],
  );

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value: string = event.target.value;
    const name: string = event.target.name;

    dispatch({ name, value });
  };
  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      setLoading(true);
      await mutation.registerUser.mutateAsync({
        ...user,
        redirect_url: location.origin + p`/email`,
      } as RegisterUserMutationInput);
      router.push(p`/signup/success`);
    } catch (error: any) {
      setErrors(Array.isArray(error) ? error : [error]);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (!isNoneOrEmpty(email)) {
      dispatch({ name: "email", value: email as string });
    }
  }, [email]);

  return (
    <>
      <div className="card isolated-card">
        <div className="card-content">
          <p className="subtitle has-text-centered mb-6">
            Sign up with credentials
          </p>

          {(errors as any[])
            .filter((error) => isNone(error.field))
            .map(({ message }, index) => (
              <p key={index} className="has-text-danger is-size-7">
                {message}
              </p>
            ))}

          <form method="post" onSubmit={onSubmit}>
            <InputField
              label="Email"
              name="email"
              placeholder="Email"
              wrapperClass="mt-3"
              onChange={handleChange}
              value={user.email}
              disabled={!isNoneOrEmpty(email)}
              required
            >
              {errors
                .filter((error) => error.field === "email")
                .map(({ messages }) =>
                  messages.map((message, index) => (
                    <p key={index} className="has-text-danger is-size-7">
                      {message}
                    </p>
                  )),
                )}
            </InputField>

            <InputField
              label="Full Name"
              name="full_name"
              placeholder="Full Name"
              wrapperClass="mt-3"
              onChange={handleChange}
              value={user.full_name as string}
              required
            >
              {errors
                .filter((error) => error.field === "full_name")
                .map(({ messages }) =>
                  messages.map((message, index) => (
                    <p key={index} className="has-text-danger is-size-7">
                      {message}
                    </p>
                  )),
                )}
            </InputField>

            <InputField
              label="Password"
              name="password1"
              type="password"
              placeholder="Password"
              wrapperClass="mt-3"
              onChange={handleChange}
              value={user.password1}
              required
            >
              {errors
                .filter((error) => error.field === "password1")
                .map(({ messages }) =>
                  messages.map((message, index) => (
                    <p key={index} className="has-text-danger is-size-7">
                      {message}
                    </p>
                  )),
                )}
            </InputField>

            <InputField
              label="Confirm Password"
              name="password2"
              type="password"
              placeholder="Confirm Password"
              wrapperClass="mt-3"
              onChange={handleChange}
              value={user.password2}
              required
            >
              {errors
                .filter((error) => error.field === "password2")
                .map(({ messages }) =>
                  messages.map((message, index) => (
                    <p key={index} className="has-text-danger is-size-7">
                      {message}
                    </p>
                  )),
                )}
            </InputField>

            <ButtonField
              type="submit"
              disabled={loading}
              className={`is-primary is-fullwidth mt-6`}
              controlClass="has-text-centered"
            >
              <span>Create account</span>
            </ButtonField>
          </form>
        </div>
      </div>

      <div className="has-text-centered my-4 is-size-6">
        <span>
          Have an account?{" "}
          <Link legacyBehavior href="/signin">
            Sign in
          </Link>
        </span>
      </div>
    </>
  );
};

// Component with LoadingProvider
const LoadingWrappedForm = () => {
  return (
    <LoadingProvider>
      <SignUpForm />
    </LoadingProvider>
  );
};

// Exported component with Suspense
export default function SignUp(pageProps: any) {
  return (
    <Suspense fallback={
      <div className="card isolated-card">
        <div className="card-content has-text-centered">
          <p className="subtitle">Loading...</p>
        </div>
      </div>
    }>
      <LoadingWrappedForm />
    </Suspense>
  );
}
