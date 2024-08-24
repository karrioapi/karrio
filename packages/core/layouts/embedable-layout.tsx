import "@fortawesome/fontawesome-free/css/all.min.css";
import "highlight.js/styles/stackoverflow-light.css";
import "@/styles/theme.scss";
import "@/styles/dashboard.scss";
import { loadMetadata } from "@karrio/core/context/main";
import { Providers } from "@karrio/hooks/providers";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { metadata } = await loadMetadata();
  const pageProps = { ...metadata };

  return (
    <>
      <Providers {...pageProps}>{children}</Providers>
    </>
  );
}
