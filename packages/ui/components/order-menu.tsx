"use client";

import {
  DocumentTemplateType,
  OrderType,
  OrderStatusEnum,
} from "@karrio/types";
import { useDocumentTemplates } from "@karrio/hooks/document-template";
import { DeleteConfirmationDialog } from "./delete-confirmation-dialog";
import React, { useState } from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useOrderMutation } from "@karrio/hooks/order";
import { useRouter } from "next/navigation";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { url$, p } from "@karrio/lib";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { Button } from "./ui/button";
import { MoreHorizontal } from "lucide-react";

interface OrderMenuComponent extends React.InputHTMLAttributes<HTMLDivElement> {
  order: OrderType;
  templates?: DocumentTemplateType[];
  isViewing?: boolean;
}

export const OrderMenu = ({
  order,
  isViewing,
}: OrderMenuComponent): JSX.Element => {
  const router = useRouter();
  const { references } = useAPIMetadata();
  const mutation = useOrderMutation();
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
    related_object: "order",
    active: true,
  } as any);

  const displayDetails = (_: React.MouseEvent) => {
    toast({
      title: "Opening order details...",
      description: "Taking you to view order details.",
    });
    
    router.push(p`/orders/${order.id}`);
  };

  const navigateToCreateLabel = (_: React.MouseEvent) => {
    toast({
      title: "Opening create label page...",
      description: "Taking you to create a label for this order.",
    });
    
    router.push(p`/orders/create_label?shipment_id=${computeShipmentId(order)}&order_id=${order?.id}`);
  };

  const navigateToEditOrder = (_: React.MouseEvent) => {
    toast({
      title: "Opening edit order page...",
      description: "Taking you to edit this draft order.",
    });
    
    router.push(p`/draft_orders/${order?.id}`);
  };

  const cancelOrder = (order: OrderType) => async () => {
    await mutation.cancelOrder.mutateAsync(order);
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

  const computeShipmentId = (order: OrderType) => {
    return order.shipments.find((s) => s.status === "draft")?.id || "new";
  };

  return (
    <div key={`menu-${order.id}`}>
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
          id={`order-menu-${order.id}`}
          role="menu"
        >
          {["unfulfilled", "partial"].includes(order?.status) && (
            <DropdownMenuItem onClick={navigateToCreateLabel} className="cursor-pointer">
              <span>Create label</span>
            </DropdownMenuItem>
          )}

          {order.shipments.filter(
            (s) => !["cancelled", "draft"].includes(s.status),
          ).length > 0 && (
            <DropdownMenuItem asChild>
              <a
                href={url$`${references.HOST}/documents/orders/label.${
                  order.shipments.filter((s) => !["cancelled", "draft"].includes(s.status))[0].label_type
                }?orders=${order.id}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center w-full"
              >
                <span>{`Print Label${
                  order.shipments.filter((s) => !["cancelled", "draft"].includes(s.status)).length > 1 ? "s" : ""
                }`}</span>
              </a>
            </DropdownMenuItem>
          )}

          {!isViewing && (
            <DropdownMenuItem onClick={displayDetails} className="cursor-pointer">
              <span>View order</span>
            </DropdownMenuItem>
          )}

          {order.source === "draft" && order.shipments.length === 0 && (
            <>
              <DropdownMenuItem onClick={navigateToEditOrder} className="cursor-pointer">
                <span>Edit order</span>
              </DropdownMenuItem>
              {order.status !== "cancelled" && (
                <DropdownMenuItem
                  onClick={() => {
                    setConfirmAction({
                      title: "Delete Order",
                      description: `Are you sure you want to delete order ${order.id}? This action cannot be undone.`,
                      confirmLabel: "Submit",
                      onConfirm: () => mutation.deleteOrder.mutateAsync({ id: order.id }),
                    });
                    setConfirmDialogOpen(true);
                  }}
                  className="text-destructive focus:text-destructive cursor-pointer"
                >
                  <span>Delete order</span>
                </DropdownMenuItem>
              )}
            </>
          )}

          {order.status === OrderStatusEnum.Unfulfilled && (
            <DropdownMenuItem
              onClick={() => {
                setConfirmAction({
                  title: "Cancel Order",
                  description: `Are you sure you want to cancel order ${order.id}? This action cannot be undone.`,
                  confirmLabel: "Submit",
                  onConfirm: cancelOrder(order),
                });
                setConfirmDialogOpen(true);
              }}
              className="text-destructive focus:text-destructive cursor-pointer"
            >
              <span>Cancel order</span>
            </DropdownMenuItem>
          )}

          {(document_templates?.edges || []).length > 0 &&
            !["fulfilled", "partial", "delivered", "cancelled"].includes(
              order?.status,
            ) && <DropdownMenuSeparator />}

          {(document_templates?.edges || []).map(({ node: template }) => (
            <DropdownMenuItem asChild key={template.id}>
              <a
                href={url$`${references.HOST}/documents/templates/${template.id}.${template.slug}?orders=${order.id}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center w-full"
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
          confirmLabel={confirmAction.title === "Cancel Order" ? "Cancel" : undefined}
          cancelLabel={confirmAction.title === "Cancel Order" ? "Go Back" : undefined}
          onConfirm={handleConfirm}
        />
      )}
    </div>
  );
};