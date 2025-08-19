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

  React.useEffect(() => {
    if (!isUserFetched || !isSystemFetched) {
      return;
    }

    const newCarrierOptions = [...user_connections, ...system_connections]
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
  }, [isUserFetched, isSystemFetched, user_connections, system_connections]);

  return {
    carrierOptions,
  };
}
