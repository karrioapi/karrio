import {
  useCarrierConnectionMutation,
  useCarrierConnections,
} from "@karrio/hooks/user-connection";
import {
  UpdateCarrierConnectionMutationInput,
  NotificationType,
} from "@karrio/types";
import { ConnectProviderModalContext } from "../modals/connect-provider-modal";
import { useLabelTemplateModal } from "../modals/label-template-edit-modal";
import { CarrierNameBadge } from "../components/carrier-name-badge";
import { ConfirmModalContext } from "../modals/confirm-modal";
import { CopiableLink } from "../components/copiable-link";
import React, { useContext, useEffect, useState } from "react";
import { isNoneOrEmpty, jsonify } from "@karrio/lib";
import { supportsRateSheets as checkRateSheetSupport } from "@karrio/lib/carrier-utils";
import { useAppMode } from "@karrio/hooks/app-mode";
import { useSearchParams } from "next/navigation";
import { Notify } from "../components/notifier";
import { Spinner } from "../components/spinner";
import { Loading } from "../components/loader";
import { RateSheetEditor } from "@karrio/ui/components/rate-sheet-editor";
import { useRateSheet, useRateSheetMutation } from "@karrio/hooks/rate-sheet";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

type ConnectionUpdateType = Partial<UpdateCarrierConnectionMutationInput> & {
  id: string;
  carrier_name: string;
};
interface UserConnectionListView { }

export const UserConnectionList = (): JSX.Element => {
  const searchParams = useSearchParams();
  const modal = searchParams.get("modal") as string;
  const { testMode } = useAppMode();
  const { notify } = useContext(Notify);
  const labelModal = useLabelTemplateModal();
  const { setLoading } = useContext(Loading);
  const { confirm: confirmDeletion } = useContext(ConfirmModalContext);
  const { editConnection } = useContext(ConnectProviderModalContext);
  const mutation = useCarrierConnectionMutation();
  const { query, user_connections } = useCarrierConnections();
  const [rateSheetEditorOpen, setRateSheetEditorOpen] = useState(false);
  const [selectedConnection, setSelectedConnection] = useState<any>(null);
  const { metadata, references } = useAPIMetadata();
  const [carrierMetadata, setCarrierMetadata] = useState<any[]>([]);

  // Fetch detailed carrier metadata
  useEffect(() => {
    if (metadata?.HOST) {
      fetch(`${metadata.HOST}/v1/carriers`)
        .then(res => res.json())
        .then(setCarrierMetadata)
        .catch(console.error);
    }
  }, [metadata?.HOST]);

  // Use centralized utility to check if carrier supports rate sheets
  const supportsRateSheets = (connection: any) => {
    return checkRateSheetSupport(connection, references);
  };

  const update =
    ({ carrier_name, ...changes }: ConnectionUpdateType) =>
      async () => {
        try {
          await mutation.updateCarrierConnection.mutateAsync(changes);
          notify({
            type: NotificationType.success,
            message: `carrier connection updated!`,
          });
        } catch (message: any) {
          notify({ type: NotificationType.error, message });
        }
      };
  const onDelete = (id: string) => async () => {
    try {
      await mutation.deleteCarrierConnection.mutateAsync({ id });
      notify({
        type: NotificationType.success,
        message: `carrier connection deleted!`,
      });
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
  };

  useEffect(() => {
    setLoading(query.isFetching);
  });
  useEffect(() => {
    if (labelModal.isActive) {
      const connection = (user_connections || []).find(
        (c: any) => c.id === labelModal.operation?.connection.id,
      );
      connection &&
        labelModal.editLabelTemplate({
          connection: connection as any,
          onSubmit: (label_template) =>
            update({
              id: connection.id,
              carrier_name: connection.carrier_name,
              label_template,
            } as any)(),
        });
    }
  }, [user_connections]);
  useEffect(() => {
    if (query.isFetching && !isNoneOrEmpty(modal)) {
      const connection = (user_connections || []).find(
        (c: any) => c.id === modal,
      );
      connection &&
        editConnection({
          connection,
          update: mutation.updateCarrierConnection.mutateAsync,
        });
    }
  }, [modal, user_connections]);

  return (
    <>
      {query.isFetching && !query.isFetched && <Spinner />}

      {query.isFetched && (user_connections || []).length > 0 && (
        <>
          <div className="table-container">
            <table className="table is-fullwidth">
              <tbody className="connections-table">
                <tr>
                  <td className="is-size-7" colSpan={testMode ? 4 : 3}>
                    ACCOUNTS
                  </td>
                  <td className="action"></td>
                </tr>

                {(user_connections || []).map((connection: any) => (
                  <tr key={`${connection.id}-${Date.now()}`}>
                    <td className="carrier is-vcentered pl-1">
                      <CarrierNameBadge
                        carrier_name={connection.carrier_name}
                        display_name={connection.display_name}
                        className="box p-3 has-text-weight-bold"
                        customTheme={
                          !!connection.config?.brand_color ? "plain" : undefined
                        }
                        style={JSON.parse(
                          jsonify({
                            backgroundColor: connection.config?.brand_color,
                            color: connection.config?.text_color,
                          }),
                        )}
                      />
                    </td>
                    {testMode && (
                      <td className="mode is-vcentered">
                        <span className="tag is-warning is-centered">Test</span>
                      </td>
                    )}
                    <td className="active is-vcentered">
                      <button
                        className="button is-white is-large"
                        onClick={update({
                          id: connection.id,
                          carrier_name: connection.carrier_name,
                          active: !connection.active,
                        } as any)}
                      >
                        <span
                          className={`icon is-medium ${connection.active ? "has-text-success" : "has-text-grey"}`}
                        >
                          <i
                            className={`fas fa-${connection.active ? "toggle-on" : "toggle-off"} fa-lg`}
                          ></i>
                        </span>
                      </button>
                    </td>
                    <td className="details">
                      <div className="content is-small">
                        <ul>
                          <li>
                            <span className="is-size-7 my-1 has-text-weight-semibold">
                              carrier_name:{" "}
                              {(connection as any).custom_carrier_name ||
                                connection.carrier_name}
                            </span>
                          </li>
                          <li>
                            <span className="is-size-7 my-1 has-text-weight-semibold">
                              carrier_id:{" "}
                              <CopiableLink
                                className="button is-white is-small"
                                text={connection.carrier_id}
                              />
                            </span>
                          </li>
                        </ul>
                      </div>
                    </td>
                    <td className="action is-vcentered pr-0">
                      <div className="buttons is-justify-content-end">
                        {!isNoneOrEmpty(
                          (connection as any).custom_carrier_name,
                        ) && (
                            <button
                              title="edit label"
                              className="button is-white"
                              onClick={() =>
                                labelModal.editLabelTemplate({
                                  connection: connection as any,
                                  onSubmit: (label_template) =>
                                    update({
                                      id: connection.id,
                                      carrier_name: connection.carrier_name,
                                      label_template,
                                    } as any)(),
                                })
                              }
                            >
                              <span className="icon is-small">
                                <i className="fas fa-sticky-note"></i>
                              </span>
                            </button>
                          )}
                        {(supportsRateSheets(connection) ||
                          !isNoneOrEmpty((connection as any).rate_sheet_id)) && (
                            <button
                              title="manage rate sheet"
                              className="button is-white"
                              onClick={() => {
                                setSelectedConnection(connection);
                                setRateSheetEditorOpen(true);
                              }}
                            >
                              <span className="icon is-small">
                                <i className="fas fa-table"></i>
                              </span>
                            </button>
                          )}
                        <button
                          title="edit account"
                          className="button is-white"
                          onClick={() =>
                            editConnection({
                              connection,
                              update:
                                mutation.updateCarrierConnection.mutateAsync,
                            })
                          }
                        >
                          <span className="icon is-small">
                            <i className="fas fa-pen"></i>
                          </span>
                        </button>
                        <button
                          title="discard connection"
                          className="button is-white"
                          onClick={() =>
                            confirmDeletion({
                              identifier: connection.id,
                              label: `Delete Carrier connection`,
                              onConfirm: onDelete(connection.id),
                            })
                          }
                        >
                          <span className="icon is-small">
                            <i className="fas fa-trash"></i>
                          </span>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {query.isFetched && (user_connections || []).length == 0 && (
        <div className="card my-6">
          <div className="card-content has-text-centered">
            <p>No carriers connected yet.</p>
            <p>
              Use the <strong>Register a Carrier</strong> button above to add a
              new connection
            </p>
          </div>
        </div>
      )}

      {/* Rate Sheet Editor */}
      {rateSheetEditorOpen && selectedConnection && (
        <RateSheetEditor
          rateSheetId={selectedConnection.rate_sheet?.id || 'new'}
          preloadCarrier={selectedConnection.rate_sheet?.id ? undefined : selectedConnection.carrier_name}
          linkConnectionId={selectedConnection.id}
          onClose={() => {
            setRateSheetEditorOpen(false);
            setSelectedConnection(null);
          }}
          isAdmin={false}
          useRateSheet={useRateSheet}
          useRateSheetMutation={useRateSheetMutation}
        />
      )}
    </>
  );
};
