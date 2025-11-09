"use client";

import {
  ManualShipmentStatusEnum,
  ShipmentStatusEnum,
  DocumentTemplateType,
  ShipmentType,
} from "@karrio/types";
import { useDocumentTemplates } from "@karrio/hooks/document-template";
import { formatRef, isNone, isNoneOrEmpty, p, url$ } from "@karrio/lib";
import { useShipmentMutation } from "@karrio/hooks/shipment";
import { DeleteConfirmationDialog } from "./delete-confirmation-dialog";
import React, { useState } from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
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
import { MoreHorizontal, Loader2 } from "lucide-react";

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
  const { references } = useAPIMetadata();
  const mutation = useShipmentMutation();
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
      const errorMessage = error?.message || "Failed to cancel shipment";

      toast({
        variant: "destructive",
        title: "Failed to cancel shipment",
        description: errorMessage,
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
          const errorMessage = error?.message || "Failed to update status";

          toast({
            variant: "destructive",
            title: "Failed to update status",
            description: errorMessage,
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
