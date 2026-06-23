// TenantsScreen.tsx — Govern › Tenants (E2). Multi-tenant accounts are an
// Enterprise/Platform feature (no `accounts` field in the OSS admin GraphQL),
// so this renders an honest "not available" state.
import { PageHeader } from "~/components/ui/primitives";
import { NotAvailableNotice } from "~/components/ui/NotAvailable";
import { useTenants } from "~/lib/karrio/hooks";

export function TenantsScreen() {
  useTenants(); // exercises the data layer; resolves empty on OSS
  return (
    <div className="page" data-testid="screen-tenants">
      <PageHeader title="Tenants" />
      <NotAvailableNotice
        feature="Multi-tenant accounts"
        detail="Tenant/account management is part of Karrio Platform. The open-source admin API doesn’t expose tenant accounts."
      />
    </div>
  );
}
