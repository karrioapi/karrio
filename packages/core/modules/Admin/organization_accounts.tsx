"use client";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import Head from "next/head";

export const generateMetadata = dynamicMetadata("Platform");

export default function Page(pageProps: any) {
  const { APP_NAME } = (pageProps as any).metadata || {};

  const Component: React.FC = () => {
    return (
      <>
        <header className="px-0 pb-5 pt-1 mb-1">
          <span className="title is-4 has-text-weight-bold">
            Organization accounts
          </span>
        </header>
      </>
    );
  };

  return (
    <>
      <Head>
        <title>{`Organizations - ${APP_NAME}`}</title>
      </Head>

      <Component />
    </>
  );
}
