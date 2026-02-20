"use client";

import {
  ManualShipmentStatusEnum,
  ShipmentStatusEnum,
  DocumentTemplateType,
  ShipmentType,
} from "@karrio/types";
import { useDocumentTemplates } from "@karrio/hooks/document-template";
import { useDocumentPrinter, FormatType } from "@karrio/hooks/resource-token";
import { errorToMessages, formatRef, isNone, isNoneOrEmpty, p } from "@karrio/lib";
import { useShipmentMutation } from "@karrio/hooks/shipment";
import { DeleteConfirmationDialog } from "./delete-confirmation-dialog";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAppMode } from "@karrio/hooks/app-mode";
import { useToast } from "@karrio/ui/hooks/use-toast";
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
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
}

export const ShipmentMenu = ({
  shipment,
  isViewing,
  variant = "ghost",
}: ShipmentMenuComponent): JSX.Element => {
  const router = useRouter();
  const { basePath } = useAppMode();
  const mutation = useShipmentMutation();
  const documentPrinter = useDocumentPrinter();
  const { toast } = useToast();
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [confirmAction, setConfirmAction] = useState<{
    title: string;
    description: string;
    confirmLabel: string;
    onConfirm: () => Promise<any>;
  } | null>(null);
  const {
    query: { data: { document_templates } = {} },
  } = useDocumentTemplates({
    related_object: "shipment",
    active: true,
  } as any);

  const createLabel = (_: React.MouseEvent) => {
    toast({
      title: "Opening create label page...",
      description: "Taking you to create a label for this shipment.",
    });

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
    try {
      await mutation.voidLabel.mutateAsync(shipment);

      toast({
        title: "Shipment cancelled successfully",
        description: `Shipment ${shipment.tracking_number || shipment.id} has been cancelled.`,
      });
    } catch (error: any) {
      const messages = errorToMessages(error);
      toast({
        variant: "destructive",
        title: "Failed to cancel shipment",
        description: messages
          .map((m: any) => (typeof m === "string" ? m : m.message || JSON.stringify(m)))
          .join("; "),
      });

      // Re-throw to prevent dialog from closing
      throw error;
    }
  };

  const changeStatus =
    ({ id }: ShipmentType, status: ManualShipmentStatusEnum) =>
      async () => {
        try {
          await mutation.changeStatus.mutateAsync({ id, status });

          toast({
            title: "Status updated successfully",
            description: `Shipment has been marked as ${formatRef(status.toString())}.`,
          });
        } catch (error: any) {
          const messages = errorToMessages(error);
          toast({
            variant: "destructive",
            title: "Failed to update status",
            description: messages
              .map((m: any) => (typeof m === "string" ? m : m.message || JSON.stringify(m)))
              .join("; "),
          });

          // Re-throw to prevent dialog from closing
          throw error;
        }
      };

  const duplicateShipment = async (_: React.MouseEvent) => {
    toast({
      title: "Creating duplicate shipment...",
      description: "Please wait while we duplicate your shipment.",
    });

    try {
      console.log("> duplicating shipment...");
      const duplicatedShipment =
        await mutation.duplicateShipment.mutateAsync(shipment);
      console.log("> shipment duplicate created successfully!");

      toast({
        title: "Shipment duplicated successfully!",
        description: "Opening create label page for the new shipment.",
      });

      router.push(
        p`${basePath}/create_label?shipment_id=${duplicatedShipment.id}`,
      );
    } catch (error) {
      console.error("Failed to duplicate shipment:", error);
      toast({
        variant: "destructive",
        title: "Failed to duplicate shipment",
        description: "Please try again or contact support if the issue persists.",
      });
    }
  };

  const handleConfirm = async () => {
    if (!confirmAction) return;

    try {
      await confirmAction.onConfirm();
      setConfirmDialogOpen(false);
      setConfirmAction(null);
    } catch (error) {
      console.error('Confirmation action failed:', error);
      // Dialog stays open for retry
    }
  };

  return (
    <div key={`menu-${shipment.id}`}>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant={variant}
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

          {!isViewing && (
            <DropdownMenuItem onClick={displayDetails}>
              <span>View Shipment</span>
            </DropdownMenuItem>
          )}

          {isNone(shipment.label_url) &&
            shipment.status === ShipmentStatusEnum.draft && (
              <DropdownMenuItem onClick={createLabel}>
                <span>Buy Label</span>
              </DropdownMenuItem>
            )}

          {!isNone(shipment.label_url) && (
            <DropdownMenuItem
              onClick={() => documentPrinter.openShipmentLabel(
                shipment.id,
                { format: (shipment.label_type || "pdf").toLowerCase() as FormatType, doc: "label" }
              )}
              disabled={documentPrinter.isLoading}
            >
              <span>Print Label</span>
            </DropdownMenuItem>
          )}

          {!isNone(shipment.invoice_url) && (
            <DropdownMenuItem
              onClick={() => documentPrinter.openShipmentLabel(
                shipment.id,
                { format: "pdf", doc: "invoice" }
              )}
              disabled={documentPrinter.isLoading}
            >
              <span>Print Invoice</span>
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
                onClick={() => {
                  setConfirmAction({
                    title: "Cancel Shipment",
                    description: `Are you sure you want to cancel shipment ${shipment.id}? This action cannot be undone.`,
                    confirmLabel: "Submit",
                    onConfirm: cancelShipment(shipment),
                  });
                  setConfirmDialogOpen(true);
                }}
                className="text-destructive focus:text-destructive"
              >
                <span>Cancel Shipment</span>
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
                    onClick={() => {
                      setConfirmAction({
                        title: "Update Shipment Status",
                        description: `Mark shipment ${shipment.id} as ${formatRef(ManualShipmentStatusEnum.in_transit.toString())}?`,
                        confirmLabel: "Apply",
                        onConfirm: changeStatus(
                          shipment,
                          ManualShipmentStatusEnum.in_transit,
                        ),
                      });
                      setConfirmDialogOpen(true);
                    }}
                  >
                    <span>Mark as {formatRef(ManualShipmentStatusEnum.in_transit.toString())}</span>
                  </DropdownMenuItem>
                )}

                {[
                  ShipmentStatusEnum.purchased,
                  ShipmentStatusEnum.in_transit,
                ].includes(shipment.status as any) && (
                    <DropdownMenuItem
                      onClick={() => {
                        setConfirmAction({
                          title: "Update Shipment Status",
                          description: `Mark shipment ${shipment.id} as ${formatRef(ManualShipmentStatusEnum.needs_attention.toString())}?`,
                          confirmLabel: "Save",
                          onConfirm: changeStatus(
                            shipment,
                            ManualShipmentStatusEnum.needs_attention,
                          ),
                        });
                        setConfirmDialogOpen(true);
                      }}
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
                      onClick={() => {
                        setConfirmAction({
                          title: "Update Shipment Status",
                          description: `Mark shipment ${shipment.id} as ${formatRef(ManualShipmentStatusEnum.delivery_failed.toString())}?`,
                          confirmLabel: "Save",
                          onConfirm: changeStatus(
                            shipment,
                            ManualShipmentStatusEnum.delivery_failed,
                          ),
                        });
                        setConfirmDialogOpen(true);
                      }}
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
                      onClick={() => {
                        setConfirmAction({
                          title: "Update Shipment Status",
                          description: `Mark shipment ${shipment.id} as ${formatRef(ManualShipmentStatusEnum.delivered.toString())}?`,
                          confirmLabel: "Save",
                          onConfirm: changeStatus(
                            shipment,
                            ManualShipmentStatusEnum.delivered,
                          ),
                        });
                        setConfirmDialogOpen(true);
                      }}
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
            <DropdownMenuItem
              key={template.id}
              onClick={() => documentPrinter.openTemplate(
                template.id,
                { shipments: shipment.id }
              )}
              disabled={documentPrinter.isLoading}
            >
              <span>Download {template.name}</span>
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      {confirmAction && (
        <DeleteConfirmationDialog
          open={confirmDialogOpen}
          onOpenChange={setConfirmDialogOpen}
          title={confirmAction.title}
          description={confirmAction.description}
          confirmLabel={confirmAction.title === "Cancel Shipment" ? "Cancel" : confirmAction.confirmLabel}
          cancelLabel={confirmAction.title === "Cancel Shipment" ? "Go Back" : "Cancel"}
          onConfirm={handleConfirm}
        />
      )}
    </div>
  );
};
