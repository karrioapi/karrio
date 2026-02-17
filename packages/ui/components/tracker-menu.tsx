"use client";

import { useTrackerMutation } from "@karrio/hooks/tracker";
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

interface TrackerMenuProps {
  tracker: {
    id: string;
    tracking_number: string;
    carrier_name: string;
  };
  onDelete?: () => void;
  className?: string;
}

export const TrackerMenu = ({
  tracker,
  onDelete,
  className,
}: TrackerMenuProps): JSX.Element => {
  const mutation = useTrackerMutation();
  const { toast } = useToast();

  const handleResendWebhooks = async () => {
    try {
      await mutation.resendWebhooks.mutateAsync({
        entityIds: [tracker.id],
      });
      toast({
        title: "Webhooks resent",
        description: `Webhook notifications triggered for tracker ${tracker.tracking_number}.`,
      });
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Failed to resend webhooks",
        description: error?.message || "An error occurred while resending webhooks.",
      });
    }
  };

  const handleRefreshTracking = async () => {
    try {
      await mutation.refreshTracker.mutateAsync({
        tracking_number: tracker.tracking_number,
        carrier_name: tracker.carrier_name,
      });
      toast({
        title: "Tracking refreshed",
        description: `Tracking data re-fetched from carrier for ${tracker.tracking_number}.`,
      });
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Failed to refresh tracking",
        description: error?.message || "An error occurred while refreshing tracking.",
      });
    }
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className={`h-8 w-8 p-0 hover:bg-muted ${className || ""}`}
        >
          <MoreHorizontal className="h-4 w-4" />
          <span className="sr-only">Open menu</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuItem
          onClick={handleRefreshTracking}
          disabled={mutation.refreshTracker.isLoading}
        >
          <span>Refresh Tracking</span>
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={handleResendWebhooks}
          disabled={mutation.resendWebhooks.isLoading}
        >
          <span>Resend Webhooks</span>
        </DropdownMenuItem>
        {onDelete && (
          <>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              onClick={onDelete}
              className="text-destructive focus:text-destructive"
            >
              <span>Delete Tracker</span>
            </DropdownMenuItem>
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
