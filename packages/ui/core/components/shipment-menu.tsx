"use client";
import {
  ManualShipmentStatusEnum,
  ShipmentStatusEnum,
  DocumentTemplateType,
  ShipmentType,
} from "@karrio/types";
import { useDocumentTemplates } from "@karrio/hooks/document-template";
import { useDocumentPrinter, FormatType } from "@karrio/hooks/resource-token";
import { formatRef, isNone, isNoneOrEmpty, p } from "@karrio/lib";
import { ConfirmModalContext } from "../modals/confirm-modal";
import { useShipmentMutation } from "@karrio/hooks/shipment";
import React, { useState, useRef, useContext } from "react";
import { useRouter } from "next/navigation";
import { useAppMode } from "@karrio/hooks/app-mode";

interface ShipmentMenuComponent
  extends React.InputHTMLAttributes<HTMLDivElement> {
  shipment: ShipmentType;
  templates?: DocumentTemplateType[];
  isViewing?: boolean;
}

export const ShipmentMenu = ({
  shipment,
  isViewing,
}: ShipmentMenuComponent): JSX.Element => {
  const router = useRouter();
  const { basePath } = useAppMode();
  const mutation = useShipmentMutation();
  const trigger = useRef<HTMLDivElement>(null);
  const [isActive, setIsActive] = useState(false);
  const { confirm: confirmCancellation } = useContext(ConfirmModalContext);
  const documentPrinter = useDocumentPrinter();
  const {
    query: { data: { document_templates } = {} },
  } = useDocumentTemplates({
    related_object: "shipment",
    active: true,
  } as any);

  const handleOnClick = (e: React.MouseEvent) => {
    setIsActive(!isActive);
    if (!isActive) {
      document.addEventListener("click", onBodyClick);
    } else {
      document.removeEventListener("click", onBodyClick);
    }
  };
  const onBodyClick = (e: MouseEvent) => {
    if (!trigger.current?.contains(e.target as Node)) {
      setIsActive(false);
      document.removeEventListener("click", onBodyClick);
    }
  };
  const createLabel = (_: React.MouseEvent) => {
    if (!!shipment.meta?.orders) {
      router.push(
        p`${basePath}/orders/create_label?shipment_id=${shipment.id}&order_id=${shipment.meta.orders}`,
      );
    } else {
      router.push(p`${basePath}/create_label?shipment_id=${shipment.id}`);
    }
  };
  const displayDetails = (_: React.MouseEvent) => {
    router.push(p`${basePath}/shipments/${shipment.id}`);
  };
  const cancelShipment = (shipment: ShipmentType) => async () => {
    await mutation.voidLabel.mutateAsync(shipment);
  };
  const changeStatus =
    ({ id }: ShipmentType, status: ManualShipmentStatusEnum) =>
      async () => {
        await mutation.changeStatus.mutateAsync({ id, status });
      };
  const duplicateShipment = async (_: React.MouseEvent) => {
    console.log("> duplicating shipment...");
    const duplicatedShipment =
      await mutation.duplicateShipment.mutateAsync(shipment);
    console.log("> shipment duplicate created successfully!");
    router.push(
      p`${basePath}/create_label?shipment_id=${duplicatedShipment.id}`,
    );
  };

  return (
    <div
      className={`dropdown is-right ${isActive ? "is-active" : ""}`}
      key={`menu-${shipment.id}`}
    >
      <div className="dropdown-trigger" onClick={handleOnClick} ref={trigger}>
        <a className="button is-white is-small p-3">
          <i className={`fas fa-ellipsis-h`} aria-hidden="true"></i>
        </a>
      </div>

      <div
        className="dropdown-menu"
        id={`shipment-menu-${shipment.id}`}
        role="menu"
      >
        <div className="dropdown-content">
          {isNone(shipment.label_url) &&
            shipment.status === ShipmentStatusEnum.draft && (
              <a className="dropdown-item" onClick={createLabel}>
                <span>Buy Label</span>
              </a>
            )}

          {!isNone(shipment.label_url) && (
            <a
              className={`dropdown-item ${documentPrinter.isLoading ? 'is-loading' : ''}`}
              onClick={() => documentPrinter.openShipmentLabel(
                shipment.id,
                { format: (shipment.label_type || "pdf").toLowerCase() as FormatType, doc: "label" }
              )}
            >
              <span>Print Label</span>
            </a>
          )}

          {!isNone(shipment.invoice_url) && (
            <a
              className={`dropdown-item ${documentPrinter.isLoading ? 'is-loading' : ''}`}
              onClick={() => documentPrinter.openShipmentLabel(
                shipment.id,
                { format: "pdf", doc: "invoice" }
              )}
            >
              Print Invoice
            </a>
          )}

          {!isViewing && (
            <a className="dropdown-item" onClick={displayDetails}>
              View Shipment
            </a>
          )}

          <a className="dropdown-item" onClick={duplicateShipment}>
            Duplicate Shipment
          </a>

          {![
            ShipmentStatusEnum.cancelled,
            ShipmentStatusEnum.delivered,
          ].includes(shipment.status as any) && (
              <a
                className="dropdown-item"
                onClick={() =>
                  confirmCancellation({
                    identifier: shipment.id as string,
                    label: `Cancel Shipment`,
                    action: "Submit",
                    onConfirm: cancelShipment(shipment),
                  })
                }
              >
                Cancel Shipment
              </a>
            )}

          {shipment.carrier_name &&
            isNoneOrEmpty(shipment.tracker_id) &&
            ![
              ShipmentStatusEnum.cancelled,
              ShipmentStatusEnum.delivered,
              ManualShipmentStatusEnum.delivery_failed,
            ].includes(shipment.status as any) && (
              <>
                <hr className="my-1" style={{ height: "1px" }} />

                {shipment.status === ShipmentStatusEnum.purchased && (
                  <a
                    className="dropdown-item"
                    onClick={() =>
                      confirmCancellation({
                        identifier: shipment.id as string,
                        label: `Mark shipment as ${formatRef(ManualShipmentStatusEnum.in_transit.toString())}`,
                        action: "Apply",
                        onConfirm: changeStatus(
                          shipment,
                          ManualShipmentStatusEnum.in_transit,
                        ),
                      })
                    }
                  >
                    Mark as{" "}
                    {formatRef(ManualShipmentStatusEnum.in_transit.toString())}
                  </a>
                )}

                {[
                  ShipmentStatusEnum.purchased,
                  ShipmentStatusEnum.in_transit,
                ].includes(shipment.status as any) && (
                    <a
                      className="dropdown-item"
                      onClick={() =>
                        confirmCancellation({
                          identifier: shipment.id as string,
                          label: `Mark shipment as ${formatRef(ManualShipmentStatusEnum.needs_attention.toString())}`,
                          action: "Save",
                          onConfirm: changeStatus(
                            shipment,
                            ManualShipmentStatusEnum.needs_attention,
                          ),
                        })
                      }
                    >
                      Mark as{" "}
                      {formatRef(
                        ManualShipmentStatusEnum.needs_attention.toString(),
                      )}
                    </a>
                  )}

                {[
                  ShipmentStatusEnum.purchased,
                  ShipmentStatusEnum.in_transit,
                  ShipmentStatusEnum.needs_attention,
                ].includes(shipment.status as any) && (
                    <a
                      className="dropdown-item"
                      onClick={() =>
                        confirmCancellation({
                          identifier: shipment.id as string,
                          label: `Mark shipment as ${formatRef(ManualShipmentStatusEnum.delivery_failed.toString())}`,
                          action: "Save",
                          onConfirm: changeStatus(
                            shipment,
                            ManualShipmentStatusEnum.delivery_failed,
                          ),
                        })
                      }
                    >
                      Mark as{" "}
                      {formatRef(
                        ManualShipmentStatusEnum.delivery_failed.toString(),
                      )}
                    </a>
                  )}

                {[
                  ShipmentStatusEnum.purchased,
                  ShipmentStatusEnum.in_transit,
                  ShipmentStatusEnum.needs_attention,
                ].includes(shipment.status as any) && (
                    <a
                      className="dropdown-item"
                      onClick={() =>
                        confirmCancellation({
                          identifier: shipment.id as string,
                          label: `Mark shipment as ${formatRef(ManualShipmentStatusEnum.delivered.toString())}`,
                          action: "Save",
                          onConfirm: changeStatus(
                            shipment,
                            ManualShipmentStatusEnum.delivered,
                          ),
                        })
                      }
                    >
                      Mark as{" "}
                      {formatRef(ManualShipmentStatusEnum.delivered.toString())}
                    </a>
                  )}
              </>
            )}

          {(document_templates?.edges || []).length > 0 && (
            <hr className="my-1" style={{ height: "1px" }} />
          )}

          {(document_templates?.edges || []).map(({ node: template }) => (
            <a
              className={`dropdown-item ${documentPrinter.isLoading ? 'is-loading' : ''}`}
              onClick={() => documentPrinter.openTemplate(
                template.id,
                { shipments: shipment.id }
              )}
              key={template.id}
            >
              Download {template.name}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};
