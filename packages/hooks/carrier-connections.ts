import { useCarrierConnections } from "./user-connection";
import { useSystemConnections } from "./system-connection";
import React from "react";

export function useConnections() {
  const [carrierOptions, setCarrierOptions] = React.useState<
    Record<string, string[]>
  >({});
  const {
    query: { isFetched: isUserFetched },
    user_connections,
  } = useCarrierConnections();
  const {
    query: { isFetched: isSystemFetched },
    system_connections,
  } = useSystemConnections();

  const memoizedUserConnections = React.useMemo(() => user_connections, [JSON.stringify(user_connections)]);
  const memoizedSystemConnections = React.useMemo(() => system_connections, [JSON.stringify(system_connections)]);

  React.useEffect(() => {
    if (!isUserFetched || !isSystemFetched) {
      return;
    }

    const newCarrierOptions = [...memoizedUserConnections, ...memoizedSystemConnections]
      .filter((_) => _.active && (_.config?.shipping_options || []).length > 0)
      .reduce(
        (acc, _) => ({
          ...acc,
          [_.carrier_name]: [
            ...(new Set<string>([
              ...((acc[_.carrier_name] as string[]) || []),
              ...(_.config?.shipping_options || []),
            ]) as any),
          ],
        }),
        {} as Record<string, string[]>
      );

    setCarrierOptions(newCarrierOptions);
  }, [isUserFetched, isSystemFetched, memoizedUserConnections, memoizedSystemConnections]);

  return {
    carrierOptions,
  };
}
