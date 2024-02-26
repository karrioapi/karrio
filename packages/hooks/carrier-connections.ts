import { useCarrierConnections } from "./user-connection";
import React from 'react';

export function useConnections() {
  const [carrierOptions, setCarrierOptions] = React.useState<Record<string, string[]>>({});
  const { query: { data: { user_connections = [] } = {}, ...query } } = useCarrierConnections();

  React.useEffect(() => {
    if (!query.isFetched) { return; }

    setCarrierOptions(
      (user_connections || [])
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
  }, [user_connections, query.isFetched]);

  return {
    carrierOptions
  };
}
