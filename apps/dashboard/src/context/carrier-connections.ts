import { useCarrierConnections } from "@/context/user-connection";
import React from 'react';

export function useConnections() {
  const [carrierOptions, setCarrierOptions] = React.useState<string[]>([]);
  const { query: { data: { user_connections = []} = {} } } = useCarrierConnections();

  React.useEffect(() => {
    const _options: string[][] = (user_connections || []).map(
      (_: any) => (_.active ? _.config?.shipping_options || [] : []) as string[],
      [],
    );

    setCarrierOptions(([] as string[]).concat(..._options));
  }, [user_connections]);

  return {
    carrierOptions
  };
}
