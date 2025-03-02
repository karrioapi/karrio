import { WebsiteLayout } from "@karrio/console/layouts/website-layout";

export default function Layout({ children }: { children: React.ReactNode }) {
    return <WebsiteLayout>{children}</WebsiteLayout>;
}
