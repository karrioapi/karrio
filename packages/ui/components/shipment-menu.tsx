"use client";

import {
  ManualShipmentStatusEnum,
  ShipmentStatusEnum,
  DocumentTemplateType,
  ShipmentType,
} from "@karrio/types";
import { useDocumentTemplates } from "@karrio/hooks/document-template";
import { formatRef, isNone, isNoneOrEmpty, p, url$ } from "@karrio/lib";
import { ConfirmModalContext } from "../core/modals/confirm-modal";
import { useShipmentMutation } from "@karrio/hooks/shipment";
import React, { useContext } from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useRouter } from "next/navigation";
import { useAppMode } from "@karrio/hooks/app-mode";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { Button } from "./ui/button";
import { MoreHorizontal } from "lucide-react";

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
  const { references } = useAPIMetadata();
  const mutation = useShipmentMutation();
  const { confirm: confirmCancellation } = useContext(ConfirmModalContext);
  const {
    query: { data: { document_templates } = {} },
  } = useDocumentTemplates({
    related_object: "shipment",
    active: true,
  } as any);

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
    <div key={`menu-${shipment.id}`}>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 p-0 hover:bg-muted"
          >
            <MoreHorizontal className="h-4 w-4" />
            <span className="sr-only">Open menu</span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          align="end"
          className="w-56"
          id={`shipment-menu-${shipment.id}`}
          role="menu"
        >
          {isNone(shipment.label_url) &&
            shipment.status === ShipmentStatusEnum.draft && (
              <DropdownMenuItem onClick={createLabel}>
                <span>Buy Label</span>
              </DropdownMenuItem>
            )}

          {!isNone(shipment.label_url) && (
            <DropdownMenuItem asChild>
              <a
                href={url$`${references.HOST}/${shipment?.label_url}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center"
              >
                <span>Print Label</span>
              </a>
            </DropdownMenuItem>
          )}

          {!isViewing && (
            <DropdownMenuItem onClick={displayDetails}>
              <span>View Shipment</span>
            </DropdownMenuItem>
          )}

          <DropdownMenuItem onClick={duplicateShipment}>
            <span>Duplicate Shipment</span>
          </DropdownMenuItem>

          {![
            ShipmentStatusEnum.cancelled,
            ShipmentStatusEnum.delivered,
          ].includes(shipment.status as any) && (
              <DropdownMenuItem
                onClick={() =>
                  confirmCancellation({
                    identifier: shipment.id as string,
                    label: `Cancel Shipment`,
                    action: "Submit",
                    onConfirm: cancelShipment(shipment),
                  })
                }
                className="text-destructive focus:text-destructive"
              >
                <span>Cancel Shipment</span>
              </DropdownMenuItem>
            )}

          {!isNone(shipment.invoice_url) && (
            <DropdownMenuItem asChild>
              <a
                href={url$`${references.HOST}/${shipment.invoice_url}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center"
              >
                <span>Print Invoice</span>
              </a>
            </DropdownMenuItem>
          )}

          {shipment.carrier_name &&
            isNoneOrEmpty(shipment.tracker_id) &&
            ![
              ShipmentStatusEnum.cancelled,
              ShipmentStatusEnum.delivered,
              ManualShipmentStatusEnum.delivery_failed,
            ].includes(shipment.status as any) && (
              <>
                <DropdownMenuSeparator />

                {shipment.status === ShipmentStatusEnum.purchased && (
                  <DropdownMenuItem
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
                    <span>Mark as {formatRef(ManualShipmentStatusEnum.in_transit.toString())}</span>
                  </DropdownMenuItem>
                )}

                {[
                  ShipmentStatusEnum.purchased,
                  ShipmentStatusEnum.in_transit,
                ].includes(shipment.status as any) && (
                    <DropdownMenuItem
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
                      <span>Mark as {formatRef(ManualShipmentStatusEnum.needs_attention.toString())}</span>
                    </DropdownMenuItem>
                  )}

                {[
                  ShipmentStatusEnum.purchased,
                  ShipmentStatusEnum.in_transit,
                  ShipmentStatusEnum.needs_attention,
                ].includes(shipment.status as any) && (
                    <DropdownMenuItem
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
                      <span>Mark as {formatRef(ManualShipmentStatusEnum.delivery_failed.toString())}</span>
                    </DropdownMenuItem>
                  )}

                {[
                  ShipmentStatusEnum.purchased,
                  ShipmentStatusEnum.in_transit,
                  ShipmentStatusEnum.needs_attention,
                ].includes(shipment.status as any) && (
                    <DropdownMenuItem
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
                      <span>Mark as {formatRef(ManualShipmentStatusEnum.delivered.toString())}</span>
                    </DropdownMenuItem>
                  )}
              </>
            )}

          {(document_templates?.edges || []).length > 0 && (
            <DropdownMenuSeparator />
          )}

          {(document_templates?.edges || []).map(({ node: template }) => (
            <DropdownMenuItem asChild key={template.id}>
              <a
                href={url$`${references.HOST}/documents/templates/${template.id}.${template.slug}?shipments=${shipment.id}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center"
              >
                <span>Download {template.name}</span>
              </a>
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};
