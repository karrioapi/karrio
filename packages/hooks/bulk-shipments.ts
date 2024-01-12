import { NotificationType, ShipmentType } from "@karrio/types";
import { useBatchOperationMutation } from "./batch-operations";
import { useNotifier } from "@karrio/ui/components/notifier";
import { BatchShipmentData, ShipmentData } from "@karrio/types/rest/api";
import { useLoader } from "@karrio/ui/components/loader";
import { useLabelDataMutation } from "./label-data";
import { onError, useLocation } from "@karrio/lib";
import { useQuery } from "@tanstack/react-query";
import { useAppMode } from "./app-mode";
import React from "react";


// -----------------------------------------------------------
// Bulk shipments hook
// -----------------------------------------------------------
//#region

type ChangeType = {
  deleted?: boolean,
  created?: boolean,
  manuallyUpdated?: boolean,
  forcelocalUpdate?: boolean,
};
const DEFAULT_STATE = { shipments: [] } as BatchShipmentData;

function reducer(state: Partial<BatchShipmentData>, { name, value }: { name: string, value: Partial<BatchShipmentData> }): BatchShipmentData {
  switch (name) {
    case 'full':
      return { ...(value as BatchShipmentData) };
    default:
      let newState = { ...state, ...(value as Partial<BatchShipmentData>) } as BatchShipmentData;
      return { ...state, ...(newState as BatchShipmentData) };
  }
}

export function useBulkShipmentForm(shipments: ((ShipmentType | ShipmentData) & { id?: string })[] = []) {
  const loader = useLoader();
  const router = useLocation();
  const notifier = useNotifier();
  const { basePath } = useAppMode();
  const mutation = useBatchOperationMutation();
  const [batch, dispatch] = React.useReducer(reducer, DEFAULT_STATE, () => DEFAULT_STATE);
  const [mutations, setMutations] = React.useState<Record<number, ReturnType<typeof useLabelDataMutation>>>(shipments.reduce(
    (_, shipment, index) => {
      const _mutation = useLabelDataMutation(shipment.id || "new", shipment as ShipmentType);

      return ({ ..._, [index]: _mutation });
    },
    {},
  ));

  // Queries
  const query = useQuery({
    queryKey: ['batch-operations', 'new'],
    queryFn: () => Promise.resolve(
      batch.shipments.length > 0 ? batch : { shipments } as BatchShipmentData
    ),
    enabled: shipments.length > 0,
    onError,
  });

  // updates
  const updateBatch = async (changes: Partial<BatchShipmentData>, change: ChangeType = { manuallyUpdated: false, forcelocalUpdate: false }) => {
    const updateLocalState = (
      change.forcelocalUpdate ||
      // only update local state first if it is not a draft and no new object is created or deleted.
      (!change.created && !change.deleted && !change.manuallyUpdated)
    );

    if (updateLocalState) {
      dispatch({ name: "partial", value: { ...batch, ...changes } });
    }
  }
  const removeShipment = (shipment_index: number) => async () => {
    setMutations(Object.entries(mutations).reduce(
      (_, [index, mutation]) => {
        if (parseInt(index) === shipment_index) return _;
        return ({ ..._, [index]: mutation });
      },
      {},
    ));
    const update = {
      shipments: batch.shipments.filter((_, index) => index !== shipment_index)
    };

    updateBatch(update, { deleted: true });
  }

  // Requests
  const buyLabels = async () => {
    try {
      loader.setLoading(true);
      await mutation.createShipments.mutateAsync(batch);
      notifier.notify({ type: NotificationType.success, message: `Batch shipments created.` });
      // router.push(`${basePath}/orders`);
    } catch (error: any) {
      notifier.notify({ type: NotificationType.error, message: error });
      loader.setLoading(false);
    }
  }

  // Effects
  // React.useEffect(() => {
  //   if (!query.isFetched) return;

  //   const [shipments, isLoading] = Object.values(mutations).reduce(
  //     ([shipments, isLoading], mutation) => [
  //       [...shipments, mutation.state.shipment as BatchShipmentData['shipments'][0]],
  //       isLoading || mutation.state.query.isLoading
  //     ],
  //     [[] as BatchShipmentData['shipments'], false],
  //   );
  //   console.log({ shipments, isLoading });
  //   if (isLoading) return;

  //   dispatch({ name: "full", value: { shipments } });
  // }, [Object.values(mutations).map(_ => _.state.shipment)]);

  return {
    batch,
    mutations,
    buyLabels,
    removeShipment,
  }
}

//#endregion
