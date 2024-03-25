import { useSystemCarrierConnections } from "./admin/connections";
import { useCarrierConnections } from "./user-connection";
import React from 'react';

export function useConnections() {
  const [carrierOptions, setCarrierOptions] = React.useState<Record<string, string[]>>({});
  const { query: { data: { user_connections = [] } = {}, ...userQuery } } = useCarrierConnections();
  const { query: { data: { system_connections = [] } = {}, ...systemQuery } } = useSystemCarrierConnections();

  React.useEffect(() => {
    if (!userQuery.isFetched) { return; }
    if (!systemQuery.isFetched) { return; }

    setCarrierOptions(
      ([...(user_connections || []), ...(system_connections || [])])
        .filter(_ => _.active && (_.config?.shipping_options || []).length > 0)
        .reduce(
          (acc, _) => ({
            ...acc,
            [_.carrier_name]: [...(new Set<string>([
              ...(acc[_.carrier_name] as string[] || []),
              ...(_.config?.shipping_options || [])
            ])) as any]
          }),
          {} as Record<string, string[]>,
        )
    );
  }, [user_connections, userQuery.isFetched, systemQuery.isFetched]);

  return {
    carrierOptions
  };
}
