"use client";
import {
  ActionNodeInput,
  AutomationActionType,
  AutomationAuthType,
  AutomationEventStatus,
  AutomationTriggerType,
} from "@karrio/types/graphql/ee";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@karrio/ui/components/ui/collapsible";
import { ConnectionModalEditor } from "@karrio/ui/core/modals/workflow-connection-edit-modal";
import { ActionModalEditor } from "@karrio/ui/core/modals/workflow-action-edit-modal";
import { TextAreaField } from "@karrio/ui/core/components/textarea-field";
import { TabStateProvider, Tabs } from "@karrio/ui/core/components/tabs";
import { ConfirmModalWrapper } from "@karrio/ui/core/modals/form-modals";
import { CopiableLink } from "@karrio/ui/core/components/copiable-link";
import { WorkflowActionType } from "@karrio/hooks/workflow-actions";
import { InputField } from "@karrio/ui/core/components/input-field";
import { isEqual, isNone, isNoneOrEmpty, url$ } from "@karrio/lib";
import { useLoader } from "@karrio/ui/core/components/loader";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useWorkflowForm } from "@karrio/hooks/workflows";
import { SelectField } from "@karrio/ui/core/components";
import django from "highlight.js/lib/languages/django";
import { parseWorkflowEventRecordData } from "./event";
import { bundleContexts } from "@karrio/hooks/utils";
import { jsonLanguage } from "@codemirror/lang-json";
import { htmlLanguage } from "@codemirror/lang-html";
import json from "highlight.js/lib/languages/json";
import CodeMirror from "@uiw/react-codemirror";
import { WorkflowEventList } from "./events";
import React, { useState } from "react";
import hljs from "highlight.js";
import moment from "moment";

const ContextProviders = bundleContexts([ModalProvider]);
hljs.registerLanguage("django", django);
hljs.registerLanguage("json", json);

export default function Page({ params }: { params: Promise<{ id: string }> }) {
  const Component = (): JSX.Element => {
    const [id, setId] = React.useState<string>();

    React.useEffect(() => {
      params.then(query => {
        setId(query.id);
      });
    }, []);

    if (!id) return <></>;

    return (
      <>
        <WorkflowComponent workflowId={id} />
      </>
    );
  };

  return <Component />;
}

function WorkflowComponent({ workflowId }: { workflowId: string }) {
  const loader = useLoader();
  const { references } = useAPIMetadata();
  const [key, setKey] = useState<string>(`workflow-${Date.now()}`);
  const {
    workflow,
    current,
    isNew,
    DEFAULT_STATE,
    query,
    zipActionWithNode,
    debug_event,
    ...mutation
  } = useWorkflowForm({ id: workflowId as string });

  const handleChange = async (changes?: Partial<typeof workflow>) => {
    if (changes === undefined) {
      return;
    }
    await mutation.updateWorkflow({ id: workflowId, ...changes });
    setKey(`${workflowId}-${Date.now()}`);
  };

  const NextIndicator = () => (
    <div className="is-flex is-justify-content-space-around p-2 my-3">
      <span className="icon is-size-6">
        <i className="fas fa-lg fa-arrow-down"></i>
      </span>
    </div>
  );

  return (
    <ContextProviders>
      <TabStateProvider
        tabs={["Editor", "Executions"]}
        setSelectedToURL={true}
      >
        <div className="p-4">
          <header
            className="columns has-background-white"
            style={{
              position: "sticky",
              zIndex: 1,
              top: 0,
              left: 0,
              right: 0,
              borderBottom: "1px solid #ddd",
            }}
          >
            <div className="column is-vcentered">
              <AppLink
                className="button is-small is-white"
                href="/workflows"
                style={{ borderRadius: "50%" }}
              >
                <span className="icon is-large">
                  <i className="fas fa-lg fa-times"></i>
                </span>
              </AppLink>
              <span className="title is-6 has-text-weight-semibold px-2 py-3">
                Edit workflow
              </span>
            </div>
            <div className="column is-flex is-justify-content-end">
              <button
                type="button"
                className="button is-small is-success"
                onClick={() => mutation.save()}
                disabled={
                  loader.loading || isEqual(workflow, current || DEFAULT_STATE)
                }
              >
                Save
              </button>
            </div>
          </header>

          <Tabs
            tabContainerClass="is-centered"
            tabClass="is-capitalized has-text-weight-bold"
            style={{ position: "relative" }}
          >
            <>
              {query.isFetched && !!workflow.actions && (
                <div className="columns m-0">
                  {/* Workflow fields section */}
                  <div className="column px-0 pb-4 is-relative">
                    <InputField
                      label="name"
                      name="name"
                      value={workflow.name as string}
                      onChange={(e) => handleChange({ name: e.target.value })}
                      placeholder="ERP orders sync"
                      className="is-small"
                      required
                    />
                    {/* @ts-ignore */}
                    <TextAreaField
                      label="description"
                      name="description"
                      value={workflow.description as string}
                      onChange={(e) =>
                        handleChange({ description: e.target.value })
                      }
                      placeholder="Automate ERP orders syncing for fulfillment"
                      className="is-small"
                    />
                  </div>

                  <div className="p-3"></div>

                  <div
                    className="column is-9 card has-background-light is-radiusless p-0"
                    style={{ height: "85vh", minHeight: "600px" }}
                  >
                    <div className="columns m-0 is-multiline">
                      {/* Workflow related objects section */}
                      <div
                        className="column is-full p-3"
                        style={{ height: "79vh", overflowY: "auto" }}
                      >
                        {/* Trigger section */}
                        <Collapsible
                          className="card px-0"
                          defaultOpen={true}
                          style={{ maxWidth: "600px", margin: "auto" }}
                        >
                          <CollapsibleTrigger
                            asChild
                            className="p-3 is-flex is-justify-content-space-between is-clickable w-full"
                          >
                            <div className="is-title is-size-6 is-vcentered my-2">
                              <span className="has-text-weight-bold">
                                Trigger
                              </span>
                              <p className="is-size-7 has-text-weight-semibold has-text-grey my-1">
                                How the workflow is tiggered
                              </p>
                            </div>
                          </CollapsibleTrigger>
                          <CollapsibleContent>
                            <hr className="my-1" style={{ height: "1px" }} />

                            <div className="p-3">
                              {/* trigger type */}
                              <SelectField
                                name="trigger_type"
                                required={true}
                                label="Trigger type"
                                className="is-fullwidth"
                                fieldClass="column mb-0 px-0 py-2"
                                value={workflow.trigger?.trigger_type || ""}
                                onChange={(e) =>
                                  handleChange({
                                    trigger: {
                                      ...workflow.trigger,
                                      trigger_type: e.target.value,
                                    },
                                  })
                                }
                              >
                                {Array.from(
                                  new Set(Object.values(AutomationTriggerType)),
                                ).map((unit) => (
                                  <option
                                    key={unit}
                                    value={unit}
                                    disabled={
                                      unit != AutomationTriggerType.manual
                                    }
                                  >
                                    {unit}
                                  </option>
                                ))}
                              </SelectField>

                              {/* trigger schedule */}
                              <div
                                className="column mb-0 p-0"
                                style={{
                                  display: `${workflow.trigger?.trigger_type == AutomationTriggerType.scheduled ? "block" : "none"}`,
                                }}
                              >
                                <InputField
                                  name="schedule"
                                  label="Schedule (cron)"
                                  wrapperClass="px-1 py-2"
                                  fieldClass="column mb-0 p-0"
                                  defaultValue={workflow.trigger?.schedule || ""}
                                  required={
                                    workflow.trigger?.trigger_type ==
                                    AutomationTriggerType.scheduled
                                  }
                                  onChange={(e) =>
                                    handleChange({
                                      trigger: {
                                        ...workflow.trigger,
                                        schedule: e.target.value,
                                      },
                                    })
                                  }
                                />
                              </div>

                              {/* webhook options */}
                              <div
                                className="column mb-0 p-0"
                                style={{
                                  display: `${workflow.trigger?.trigger_type == AutomationTriggerType.webhook ? "block" : "none"}`,
                                }}
                              >
                                <InputField
                                  name="secret"
                                  label="Webhook secret"
                                  wrapperClass="px-1 py-2"
                                  fieldClass="column mb-0 p-0"
                                  defaultValue={workflow.trigger?.secret || ""}
                                  onChange={(e) =>
                                    handleChange({
                                      trigger: {
                                        ...workflow.trigger,
                                        secret: e.target.value,
                                      },
                                    })
                                  }
                                />

                                <InputField
                                  name="secret_key"
                                  label="Webhook secret key"
                                  wrapperClass="px-1 py-2"
                                  fieldClass="column mb-0 p-0"
                                  defaultValue={
                                    workflow.trigger?.secret_key || ""
                                  }
                                  required={
                                    !isNoneOrEmpty(workflow.trigger?.secret_key)
                                  }
                                  onChange={(e) =>
                                    handleChange({
                                      trigger: {
                                        ...workflow.trigger,
                                        secret_key: e.target.value,
                                      },
                                    })
                                  }
                                />
                              </div>
                            </div>

                            <hr className="my-1" style={{ height: "1px" }} />

                            {/* webhook URL */}
                            <InputField
                              label="Webhook URL"
                              className="is-small"
                              wrapperClass="column p-3"
                              fieldClass="mb-0 p-0"
                              controlClass="has-icons-right"
                              value={
                                !!workflow.id && workflow.id !== "new"
                                  ? url$`${references.HOST}/v1/workflows/${workflow.id}/trigger`
                                  : ""
                              }
                              iconRight={
                                <span className="icon is-small is-right">
                                  <i className="fas fa-copy"></i>
                                </span>
                              }
                              readOnly
                            />
                          </CollapsibleContent>
                        </Collapsible>

                        <NextIndicator />

                        {/* Actions section */}
                        {zipActionWithNode(
                          workflow.actions as WorkflowActionType[],
                          workflow.action_nodes as ActionNodeInput[],
                        ).map(([action, node], index) => (
                          <React.Fragment key={index}>
                            <Collapsible
                              className="card px-0"
                              style={{ maxWidth: "600px", margin: "auto" }}
                            >
                              <CollapsibleTrigger
                                asChild
                                className="p-3 is-flex is-justify-content-space-between is-clickable w-full"
                              >
                                <div>
                                  <div className="is-title is-size-6 is-vcentered my-2">
                                    <span className="has-text-weight-bold">
                                      Action
                                    </span>
                                    <p className="is-size-7 has-text-weight-semibold has-text-grey my-1">
                                      {action.name || "An action to perform"}
                                    </p>
                                  </div>
                                  <div>
                                    <ActionModalEditor
                                      action={action}
                                      onSubmit={mutation.updateAction(
                                        index,
                                        action?.id,
                                      )}
                                      trigger={
                                        <button
                                          type="button"
                                          className="button is-white"
                                        >
                                          <span className="icon">
                                            <i className="fas fa-pen"></i>
                                          </span>
                                        </button>
                                      }
                                    />
                                    <ConfirmModalWrapper
                                      onSubmit={mutation.deleteAction(
                                        index,
                                        action?.id,
                                      )}
                                      trigger={
                                        <button
                                          type="button"
                                          className="button is-white"
                                          disabled={index == 0}
                                        >
                                          <span className="icon">
                                            <i className="fas fa-trash"></i>
                                          </span>
                                        </button>
                                      }
                                    />
                                  </div>
                                </div>
                              </CollapsibleTrigger>
                              <CollapsibleContent>
                                <hr className="my-1" style={{ height: "1px" }} />

                                <TabStateProvider
                                  tabs={[
                                    "Template",
                                    "Inputs",
                                    "Outputs",
                                    "Logs",
                                    "Details",
                                  ]}
                                  setSelectedToURL={false}
                                >
                                  <Tabs
                                    tabClass="is-size-7 has-text-weight-bold"
                                    tabContainerClass="mb-0"
                                    className="p-0"
                                    style={{
                                      position: "relative",
                                      height: "300px",
                                      maxHeight: "300px",
                                      overflowY: "auto",
                                    }}
                                  >
                                    <div className="control">
                                      <div className="card is-radiusless">
                                        {/* @ts-ignore */}
                                        <CodeMirror
                                          height="297px"
                                          extensions={[htmlLanguage]}
                                          value={
                                            action.parameters_template ||
                                            ("" as string)
                                          }
                                          onChange={(value) =>
                                            mutation.updateAction(
                                              index,
                                              action?.id,
                                            )({ parameters_template: value })
                                          }
                                        />
                                      </div>
                                    </div>

                                    <div>
                                      {(debug_event?.records || []).filter(
                                        (_) =>
                                          _.meta.workflow_action_slug ===
                                          action.slug &&
                                          _.key === "action-input",
                                      ).length == 0 && (
                                          <div className="notification is-default p-2 is-size-6">
                                            No input data sample...
                                          </div>
                                        )}

                                      {(debug_event?.records || []).length >
                                        0 && (
                                          <>
                                            {debug_event!.records
                                              .filter(
                                                (_) =>
                                                  _.meta.workflow_action_slug ===
                                                  action.slug &&
                                                  _.key === "action-input",
                                              )
                                              .map((trace) => {
                                                return (
                                                  <div
                                                    className="card is-radiusless"
                                                    key={trace.id}
                                                  >
                                                    {/* @ts-ignore */}
                                                    <CodeMirror
                                                      height="297px"
                                                      extensions={[jsonLanguage]}
                                                      value={
                                                        parseWorkflowEventRecordData(
                                                          trace.record.output ||
                                                          trace.record,
                                                        ) || ("{}" as string)
                                                      }
                                                      readOnly={true}
                                                    />
                                                  </div>
                                                );
                                              })}
                                          </>
                                        )}
                                    </div>

                                    <div>
                                      {(debug_event?.records || []).filter(
                                        (_) =>
                                          _.meta.workflow_action_slug ===
                                          action.slug &&
                                          _.key === "action-output",
                                      ).length == 0 && (
                                          <div className="notification is-default p-2 is-size-6">
                                            No output data sample...
                                          </div>
                                        )}

                                      {(debug_event?.records || []).length >
                                        0 && (
                                          <>
                                            {debug_event!.records
                                              .filter(
                                                (_) =>
                                                  _.meta.workflow_action_slug ===
                                                  action.slug &&
                                                  _.key === "action-output",
                                              )
                                              .map((trace) => {
                                                return (
                                                  <div
                                                    className="card is-radiusless"
                                                    key={trace.id}
                                                  >
                                                    {/* @ts-ignore */}
                                                    <CodeMirror
                                                      height="297px"
                                                      extensions={[jsonLanguage]}
                                                      value={
                                                        parseWorkflowEventRecordData(
                                                          trace.record.output ||
                                                          trace.record,
                                                        ) || ("{}" as string)
                                                      }
                                                      readOnly={true}
                                                    />
                                                  </div>
                                                );
                                              })}
                                          </>
                                        )}
                                    </div>

                                    <div>
                                      {(debug_event?.records || []).length ==
                                        0 && (
                                          <div className="notification is-default p-2 is-size-6">
                                            No tracing records...
                                          </div>
                                        )}

                                      {(debug_event?.records || []).length >
                                        0 && (
                                          <>
                                            {debug_event!.records
                                              .filter(
                                                (_) =>
                                                  _.meta.workflow_action_id ==
                                                  action.id,
                                              )
                                              .map((trace) => {
                                                return (
                                                  <div
                                                    className={"card m-4"}
                                                    key={trace.id}
                                                  >
                                                    <div className="p-3 is-size-7 has-text-weight-semibold has-text-grey">
                                                      <p className="my-1">
                                                        <span>
                                                          Record type:{" "}
                                                          <strong>
                                                            {trace.key}
                                                          </strong>
                                                        </span>
                                                      </p>
                                                      {!!trace.record.url && (
                                                        <p className="my-1">
                                                          <span>
                                                            URL:{" "}
                                                            <strong>
                                                              {trace.record.url}
                                                            </strong>
                                                          </span>
                                                        </p>
                                                      )}
                                                      {!!trace.record
                                                        .request_id && (
                                                          <p className="my-1">
                                                            <span>
                                                              Request id:{" "}
                                                              <strong>
                                                                {
                                                                  trace.record
                                                                    .request_id
                                                                }
                                                              </strong>
                                                            </span>
                                                          </p>
                                                        )}
                                                      {trace?.timestamp && (
                                                        <p className="my-1">
                                                          <span>
                                                            Request timestamp:{" "}
                                                            <strong>
                                                              {moment(
                                                                trace.timestamp *
                                                                1000,
                                                              ).format("LTS")}
                                                            </strong>
                                                          </span>
                                                        </p>
                                                      )}
                                                      {!!trace.record.status && (
                                                        <p className="my-1">
                                                          <span>
                                                            Step status:{" "}
                                                            <strong>
                                                              {trace.record.status}
                                                            </strong>
                                                          </span>
                                                        </p>
                                                      )}
                                                    </div>

                                                    <div className="p-0 is-relative">
                                                      <CopiableLink
                                                        text="COPY"
                                                        value={
                                                          trace.record ||
                                                          trace.record?.url ||
                                                          ""
                                                        }
                                                        style={{
                                                          position: "absolute",
                                                          right: 4,
                                                        }}
                                                        className="button is-primary is-small m-1"
                                                      />
                                                      <pre
                                                        className="code p-1"
                                                        style={{
                                                          overflow: "auto",
                                                          minHeight: "40px",
                                                          maxHeight: "30vh",
                                                        }}
                                                      >
                                                        <code
                                                          style={{
                                                            whiteSpace: "pre-wrap",
                                                          }}
                                                          dangerouslySetInnerHTML={{
                                                            __html: hljs.highlight(
                                                              parseWorkflowEventRecordData(
                                                                trace.record
                                                                  .output ||
                                                                trace.record,
                                                              ) ||
                                                              trace.record.url ||
                                                              "",
                                                              {
                                                                language:
                                                                  trace.record
                                                                    ?.format ||
                                                                  "json",
                                                              },
                                                            ).value,
                                                          }}
                                                        />
                                                      </pre>
                                                    </div>
                                                  </div>
                                                );
                                              })}
                                          </>
                                        )}
                                    </div>

                                    <div>
                                      <div className="is-size-7">
                                        {/* action type */}
                                        <div className="columns my-0 px-3">
                                          <div className="column is-4 py-1">
                                            <span className="has-text-weight-bold has-text-grey">
                                              Action type
                                            </span>
                                          </div>
                                          <div className="column is-8 py-1">
                                            <code>{action.action_type}</code>
                                          </div>
                                        </div>

                                        {/* action description */}
                                        {!!action.description && (
                                          <div className="columns my-0 px-3">
                                            <div className="column is-4 py-1">
                                              <span className="has-text-weight-bold has-text-grey">
                                                description
                                              </span>
                                            </div>
                                            <div className="column is-8 py-1">
                                              <code>{action.description}</code>
                                            </div>
                                          </div>
                                        )}

                                        {/* data mapping options */}
                                        {action.action_type ==
                                          AutomationActionType.data_mapping && (
                                            <>
                                              {/* action parameters type */}
                                              <div className="columns my-0 px-3">
                                                <div className="column is-4 py-1">
                                                  <span className="has-text-weight-bold has-text-grey">
                                                    format
                                                  </span>
                                                </div>
                                                <div className="column is-8 py-1">
                                                  <code>{action.content_type}</code>
                                                </div>
                                              </div>
                                            </>
                                          )}

                                        {/* http request options */}
                                        {action.action_type ==
                                          AutomationActionType.http_request && (
                                            <>
                                              {/* action method */}
                                              <div className="columns my-0 px-3">
                                                <div className="column is-4 py-1">
                                                  <span className="has-text-weight-bold has-text-grey">
                                                    Method
                                                  </span>
                                                </div>
                                                <div className="column is-8 py-1">
                                                  <code>
                                                    {action.method?.toLocaleUpperCase()}
                                                  </code>
                                                </div>
                                              </div>

                                              {/* action host */}
                                              <div className="columns my-0 px-3">
                                                <div className="column is-4 py-1">
                                                  <span className="has-text-weight-bold has-text-grey">
                                                    Host
                                                  </span>
                                                </div>
                                                <div className="column is-8 py-1">
                                                  <code>{action.host}</code>
                                                </div>
                                              </div>

                                              {/* host port */}
                                              {!isNone(action.port) && (
                                                <div className="columns my-0 px-3">
                                                  <div className="column is-4 py-1">
                                                    <span className="has-text-weight-bold has-text-grey">
                                                      Port
                                                    </span>
                                                  </div>
                                                  <div className="column is-8 py-1">
                                                    <code>{action.port}</code>
                                                  </div>
                                                </div>
                                              )}

                                              {/* action endpoint */}
                                              {!isNoneOrEmpty(action.endpoint) && (
                                                <div className="columns my-0 px-3">
                                                  <div className="column is-4 py-1">
                                                    <span className="has-text-weight-bold has-text-grey">
                                                      Endpoint
                                                    </span>
                                                  </div>
                                                  <div className="column is-8 py-1">
                                                    <code>{action.endpoint}</code>
                                                  </div>
                                                </div>
                                              )}

                                              {/* action content type */}
                                              <div className="columns my-0 px-3">
                                                <div className="column is-4 py-1">
                                                  <span className="has-text-weight-bold has-text-grey">
                                                    Content Type
                                                  </span>
                                                </div>
                                                <div className="column is-8 py-1">
                                                  <code>{action.content_type}</code>
                                                </div>
                                              </div>

                                              {/* action parameters type */}
                                              <div className="columns my-0 px-3">
                                                <div className="column is-4 py-1">
                                                  <span className="has-text-weight-bold has-text-grey">
                                                    Parameters Type
                                                  </span>
                                                </div>
                                                <div className="column is-8 py-1">
                                                  <code>
                                                    {action.parameters_type}
                                                  </code>
                                                </div>
                                              </div>
                                            </>
                                          )}
                                      </div>

                                      <Collapsible
                                        className="card px-0 m-2"
                                        style={{
                                          maxWidth: "600px",
                                          margin: "auto",
                                        }}
                                      >
                                        <CollapsibleTrigger
                                          asChild
                                          className="p-3 is-flex is-justify-content-space-between is-clickable w-full"
                                        >
                                          <div>
                                            <div className="is-title is-size-6 is-vcentered my-2">
                                              <div className="is-flex is-align-items-center">
                                                <span className="has-text-weight-bold">
                                                  Connection
                                                </span>
                                                {action.connection && (action.connection as any).is_credentials_complete === false && (
                                                  <span className="icon has-text-danger ml-2" title="Credentials incomplete">
                                                    <i className="fas fa-exclamation-triangle"></i>
                                                  </span>
                                                )}
                                                {action.connection && (action.connection as any).is_credentials_complete === true && (
                                                  <span className="icon has-text-success ml-2" title="Credentials complete">
                                                    <i className="fas fa-check-circle"></i>
                                                  </span>
                                                )}
                                              </div>
                                              <p className="is-size-7 has-text-weight-semibold has-text-grey my-1">
                                                {action.connection?.name ||
                                                  "A connection for the action"}
                                                {action.connection && (action.connection as any).is_credentials_complete === false && (
                                                  <span className="has-text-danger ml-1">(Missing credentials)</span>
                                                )}
                                              </p>
                                            </div>
                                            <div>
                                              <ConnectionModalEditor
                                                connection={
                                                  action.connection ||
                                                  ({ auth_type: "basic" } as any)
                                                }
                                                onSubmit={mutation.updateActionConnection(
                                                  index,
                                                  action?.id,
                                                )}
                                                trigger={
                                                  <button
                                                    type="button"
                                                    className="button is-white"
                                                  >
                                                    <span className="icon">
                                                      <i
                                                        className={`fas fa-${!!action.connection ? "pen" : "plus"}`}
                                                      ></i>
                                                    </span>
                                                  </button>
                                                }
                                              />
                                              <ConfirmModalWrapper
                                                onSubmit={mutation.deleteActionConnection(
                                                  index,
                                                  action?.id,
                                                  action.connection?.id,
                                                )}
                                                trigger={
                                                  <button
                                                    type="button"
                                                    className="button is-white"
                                                    disabled={!action.connection}
                                                  >
                                                    <span className="icon">
                                                      <i className="fas fa-trash"></i>
                                                    </span>
                                                  </button>
                                                }
                                              />
                                            </div>
                                          </div>
                                        </CollapsibleTrigger>
                                        <CollapsibleContent>
                                          <hr
                                            className="my-1"
                                            style={{ height: "1px" }}
                                          />

                                          {!action.connection && (
                                            <div className="p-3 is-size-7">
                                              <div className="message p-2 is-size-7 has-text-weight-bold">
                                                <span>
                                                  No connection defined!
                                                </span>
                                              </div>
                                            </div>
                                          )}

                                          {!!action.connection && (
                                            <div className="p-3 is-size-7">
                                              {/* auth type */}
                                              <div className="columns my-0 px-3">
                                                <div className="column is-4 py-1">
                                                  <span className="has-text-weight-bold has-text-grey">
                                                    Auth type
                                                  </span>
                                                </div>
                                                <div className="column is-8 py-1">
                                                  <code>
                                                    {action.connection.auth_type}
                                                  </code>
                                                </div>
                                              </div>

                                              {/* connection description */}
                                              {!!action.connection
                                                .description && (
                                                  <div className="columns my-0 px-3">
                                                    <div className="column is-4 py-1">
                                                      <span className="has-text-weight-bold has-text-grey">
                                                        description
                                                      </span>
                                                    </div>
                                                    <div className="column is-8 py-1">
                                                      <code>
                                                        {
                                                          action.connection
                                                            .description
                                                        }
                                                      </code>
                                                    </div>
                                                  </div>
                                                )}

                                              {/* credentials status */}
                                              <div className="columns my-0 px-3">
                                                <div className="column is-4 py-1">
                                                  <span className="has-text-weight-bold has-text-grey">
                                                    Credentials Status
                                                  </span>
                                                </div>
                                                <div className="column is-8 py-1">
                                                  {(action.connection as any).is_credentials_complete ? (
                                                    <span className="tag is-success is-small">
                                                      <i className="fas fa-check mr-1"></i>
                                                      Complete
                                                    </span>
                                                  ) : (
                                                    <span className="tag is-danger is-small">
                                                      <i className="fas fa-exclamation-triangle mr-1"></i>
                                                      Incomplete
                                                    </span>
                                                  )}
                                                </div>
                                              </div>

                                              {/* required credentials */}
                                              {(action.connection as any).required_credentials && (action.connection as any).required_credentials.length > 0 && (
                                                <div className="columns my-0 px-3">
                                                  <div className="column is-4 py-1">
                                                    <span className="has-text-weight-bold has-text-grey">
                                                      Required
                                                    </span>
                                                  </div>
                                                  <div className="column is-8 py-1">
                                                    <div className="tags">
                                                      {(action.connection as any).required_credentials.map((cred: string) => (
                                                        <span key={cred} className="tag is-light is-small">
                                                          {cred}
                                                        </span>
                                                      ))}
                                                    </div>
                                                  </div>
                                                </div>
                                              )}

                                              {/* http request options */}
                                              {[
                                                AutomationAuthType.oauth2,
                                                AutomationAuthType.jwt,
                                              ].includes(
                                                action.connection
                                                  .auth_type as any,
                                              ) && (
                                                  <>
                                                    {/* connection host */}
                                                    <div className="columns my-0 px-3">
                                                      <div className="column is-4 py-1">
                                                        <span className="has-text-weight-bold has-text-grey">
                                                          Host
                                                        </span>
                                                      </div>
                                                      <div className="column is-8 py-1">
                                                        <code>
                                                          {action.connection.host}
                                                        </code>
                                                      </div>
                                                    </div>

                                                    {/* host port */}
                                                    {!isNone(
                                                      action.connection.port,
                                                    ) && (
                                                        <div className="columns my-0 px-3">
                                                          <div className="column is-4 py-1">
                                                            <span className="has-text-weight-bold has-text-grey">
                                                              Port
                                                            </span>
                                                          </div>
                                                          <div className="column is-8 py-1">
                                                            <code>
                                                              {action.connection.port}
                                                            </code>
                                                          </div>
                                                        </div>
                                                      )}

                                                    {/* endpoint */}
                                                    {!isNoneOrEmpty(
                                                      action.connection.endpoint,
                                                    ) && (
                                                        <div className="columns my-0 px-3">
                                                          <div className="column is-4 py-1">
                                                            <span className="has-text-weight-bold has-text-grey">
                                                              Endpoint
                                                            </span>
                                                          </div>
                                                          <div className="column is-8 py-1">
                                                            <code>
                                                              {
                                                                action.connection
                                                                  .endpoint
                                                              }
                                                            </code>
                                                          </div>
                                                        </div>
                                                      )}
                                                  </>
                                                )}

                                              {/* connection auth template */}
                                              <div className="columns is-multiline my-0 px-3">
                                                <div className="column py-1">
                                                  <span className="has-text-weight-bold has-text-grey">
                                                    Auth template
                                                  </span>
                                                </div>
                                                <div className="column is-12 py-1">
                                                  <pre
                                                    className="code p-1"
                                                    style={{
                                                      maxHeight: "15vh",
                                                      overflowY: "auto",
                                                    }}
                                                  >
                                                    <code
                                                      dangerouslySetInnerHTML={{
                                                        __html: hljs.highlight(
                                                          (action.connection
                                                            .auth_template ||
                                                            "") as string,
                                                          { language: "django" },
                                                        ).value,
                                                      }}
                                                    />
                                                  </pre>
                                                </div>
                                              </div>

                                              {[
                                                AutomationAuthType.oauth2,
                                                AutomationAuthType.jwt,
                                              ].includes(
                                                action.connection
                                                  .auth_type as any,
                                              ) && (
                                                  <>
                                                    {/* parameters template */}
                                                    <div className="columns is-multiline my-0 px-3">
                                                      <div className="column py-1">
                                                        <span className="has-text-weight-bold has-text-grey">
                                                          Template
                                                        </span>
                                                      </div>
                                                      <div className="column is-12 py-1">
                                                        <pre
                                                          className="code p-1"
                                                          style={{
                                                            maxHeight: "15vh",
                                                            overflowY: "auto",
                                                          }}
                                                        >
                                                          <code
                                                            dangerouslySetInnerHTML={{
                                                              __html:
                                                                hljs.highlight(
                                                                  (action.connection
                                                                    .parameters_template ||
                                                                    "{}") as string,
                                                                  {
                                                                    language:
                                                                      "django",
                                                                  },
                                                                ).value,
                                                            }}
                                                          />
                                                        </pre>
                                                      </div>
                                                    </div>
                                                  </>
                                                )}
                                            </div>
                                          )}
                                        </CollapsibleContent>
                                      </Collapsible>
                                    </div>
                                  </Tabs>
                                </TabStateProvider>
                              </CollapsibleContent>
                            </Collapsible>

                            <NextIndicator />
                          </React.Fragment>
                        ))}

                        {/* Add action button */}
                        <ActionModalEditor
                          action={(DEFAULT_STATE.actions || [])[0] as any}
                          onSubmit={mutation.addAction}
                          trigger={
                            <div className="is-flex is-justify-content-space-around p-2">
                              <button
                                type="button"
                                className="button is-small is-default"
                              >
                                Add action
                              </button>
                            </div>
                          }
                        />
                      </div>

                      <div className="column is-full has-text-centered p-3">
                        <button
                          className={`button is-default ${[AutomationEventStatus.running, AutomationEventStatus.pending].includes(debug_event?.status as any) ? "is-loading" : ""}`}
                          type="button"
                          onClick={() => mutation.runWorkflow()}
                        >
                          <span className="icon">
                            <i className="fas fa-play"></i>
                          </span>
                          <span>Exexute workflow</span>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </>

            <>{!!workflowId && <WorkflowEventList defaultFilter={{ keyword: workflowId }} />}</>
          </Tabs>
        </div>
      </TabStateProvider>
    </ContextProviders>
  );
}
