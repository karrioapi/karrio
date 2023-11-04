import { RegisterUserMutationInput, register_user_register_user_errors } from "karrio/graphql";
import React, { FormEvent, useContext, useEffect, useReducer, useState } from "react";
import LoadingProvider, { Loading } from "@/components/loader";
import ButtonField from "@/components/generic/button-field";
import InputField from "@/components/generic/input-field";
import { isNone, isNoneOrEmpty } from "@/lib/helper";
import SectionLayout from "@/layouts/section-layout";
import { useRouter } from "next/dist/client/router";
import { useUserMutation } from "@/context/user";
import { p } from "@/lib/client";
import Head from "next/head";
import Link from "next/link";

export { getServerSideProps } from '@/lib/data-fetching/metadata';

const DEFAULT_VALUE: Partial<RegisterUserMutationInput> = {
  email: "",
  full_name: "",
  password1: "",
  password2: "",
};

function reducer(state: Partial<RegisterUserMutationInput>, { name, value }: { name: string, value: string | object }) {
  switch (name) {
    case "full":
      return { ...(value as object) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}

const Component: React.FC = () => {
  const router = useRouter();
  const { email } = router.query;
  const mutation = useUserMutation();
  const { loading, setLoading } = useContext(Loading);
  const [user, dispatch] = useReducer(reducer, DEFAULT_VALUE, () => DEFAULT_VALUE);
  const [errors, setErrors] = useState<register_user_register_user_errors[]>([]);

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
        ...user, redirect_url: location.origin + p`/email`
      } as RegisterUserMutationInput);
      router.push(p`/signup/success`);
    } catch (error: any) {
      setErrors(Array.isArray(error) ? error : [error]);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (!isNoneOrEmpty(email)) {
      dispatch({ name: 'email', value: email as string });
    }
  }, [email]);

  return (
    <>
      <div className="card isolated-card">
        <div className="card-content">
          <p className="subtitle has-text-centered mb-6">Sign up with credentials</p>

          {(errors as any[]).filter(error => isNone(error.field)).map(({ message }, index) => (
            <p key={index} className="has-text-danger is-size-7">{message}</p>
          ))}

          <form method="post" onSubmit={onSubmit}>

            <InputField
              label="Email"
              name="email"
              placeholder="Email"
              fieldClass="mt-3"
              onChange={handleChange}
              value={user.email}
              disabled={!isNoneOrEmpty(email)}
              required
            >
              {errors.filter(error => error.field === 'email').map(({ messages }) => (
                messages.map((message, index) => <p key={index} className="has-text-danger is-size-7">{message}</p>)
              ))}
            </InputField>

            <InputField
              label="Full Name" name="full_name"
              placeholder="Full Name" fieldClass="mt-3"
              onChange={handleChange} value={user.full_name as string} required>
              {errors.filter(error => error.field === 'full_name').map(({ messages }) => (
                messages.map((message, index) => <p key={index} className="has-text-danger is-size-7">{message}</p>)
              ))}
            </InputField>

            <InputField
              label="Password" name="password1" type="password"
              placeholder="Password" fieldClass="mt-3"
              onChange={handleChange} value={user.password1} required>
              {errors.filter(error => error.field === 'password1').map(({ messages }) => (
                messages.map((message, index) => <p key={index} className="has-text-danger is-size-7">{message}</p>)
              ))}
            </InputField>

            <InputField
              label="Confirm Password" name="password2" type="password"
              placeholder="Confirm Password" fieldClass="mt-3"
              onChange={handleChange} value={user.password2} required>
              {errors.filter(error => error.field === 'password2').map(({ messages }) => (
                messages.map((message, index) => <p key={index} className="has-text-danger is-size-7">{message}</p>)
              ))}
            </InputField>


            <ButtonField type="submit"
              disabled={loading}
              className={`is-primary is-fullwidth mt-6`}
              controlClass="has-text-centered">
              <span>Create account</span>
            </ButtonField>

          </form>

        </div>
      </div>

      <div className="has-text-centered my-4 is-size-6">
        <span>Have an account? <Link legacyBehavior href="/login">Sign in</Link></span>
      </div>
    </>
  )
};

function SignUp(pageProps: any) {
  return (
    <>
      <SectionLayout {...pageProps}>
        <Head><title>{`Sign Up - ${pageProps.metadata?.APP_NAME}`}</title></Head>

        <LoadingProvider>
          <Component />
        </LoadingProvider>

      </SectionLayout>
    </>
  )
};

export default SignUp;
