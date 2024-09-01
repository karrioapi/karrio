import { loadMetadata } from "@karrio/core/context/main";
import { Metadata, ResolvingMetadata } from "next";
import { PageProps } from "@karrio/types";

export function dynamicMetadata(pageName: string) {
  return async (
    pageProps: PageProps,
    parent: ResolvingMetadata,
  ): Promise<Metadata> => {
    // fetch metadata
    const { metadata } = await loadMetadata();

    return {
      title: `${pageName} - ${metadata?.APP_NAME}`,
    };
  };
}
