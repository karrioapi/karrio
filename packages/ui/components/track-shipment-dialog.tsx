"use client";

import React, { useState, useContext, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import {
  SystemConnectionType,
  useSystemConnections,
} from "@karrio/hooks/system-connection";
import {
  CarrierConnectionType,
  useCarrierConnections,
} from "@karrio/hooks/user-connection";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useTrackerMutation } from "@karrio/hooks/tracker";
import { Notifier, Notify } from "@karrio/ui/core/components/notifier";
import { Loading } from "@karrio/ui/core/components/loader";
import { errorToMessages, removeUrlParam } from "@karrio/lib";
import { NotificationType } from "@karrio/types";

type Connection = CarrierConnectionType | SystemConnectionType;
type OperationType = {
  onChange?: () => void;
};

interface TrackerModalInterface {
  addTracker: (operation?: OperationType) => void;
}

export const TrackerModalContext = React.createContext<TrackerModalInterface>(
  {} as TrackerModalInterface,
);

export const TrackerModalProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const mutation = useTrackerMutation();
  const { notify } = useContext(Notify);
  const { references } = useAPIMetadata();
  const { loading, setLoading } = useContext(Loading);
  const {
    query: { data: userQuery },
  } = useCarrierConnections();
  const {
    query: { data: systemQuery },
  } = useSystemConnections();
  
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [operation, setOperation] = useState<OperationType>({});
  const [trackingNumber, setTrackingNumber] = useState<string>("");
  const [selectedCarrierId, setSelectedCarrierId] = useState<string>("");
  const [carrierList, setCarrierList] = useState<Connection[]>([]);

  const addTracker = (operation?: OperationType) => {
    operation && setOperation(operation);
    setIsOpen(true);
  };

  const handleClose = () => {
    setTrackingNumber("");
    setSelectedCarrierId("");
    setIsOpen(false);
    setOperation({});
    removeUrlParam("modal");
  };

  const handleSubmit = async () => {
    if (!trackingNumber || !selectedCarrierId) return;
    
    const selectedCarrier = carrierList.find(
      (carrier) => carrier.carrier_id === selectedCarrierId,
    );
    
    if (!selectedCarrier) return;

    setLoading(true);
    try {
      await mutation.createTracker.mutateAsync({
        tracking_number: trackingNumber,
        carrier_name: selectedCarrier.carrier_name,
      });
      notify({
        type: NotificationType.success,
        message: "Tracker successfully added!",
      });
      operation?.onChange && operation.onChange();
      handleClose();
    } catch (error: any) {
      notify({ type: NotificationType.error, message: errorToMessages(error) });
    }
    setLoading(false);
  };

  useEffect(() => {
    if (!references?.carriers) return;

    const userConns: any[] = Array.isArray((userQuery as any)?.user_connections)
      ? (userQuery as any).user_connections
      : (userQuery as any)?.user_connections?.edges?.map((e: any) => e.node) || [];

    const systemConns: any[] = Array.isArray((systemQuery as any)?.system_connections)
      ? (systemQuery as any).system_connections
      : (systemQuery as any)?.system_connections?.edges?.map((e: any) => e.node) || [];

    const connections = [...userConns, ...systemConns]
      .filter(Boolean)
      .filter(
        (c: any) =>
          (c.active === true || c.enabled === true) &&
          c.carrier_name in references?.carriers &&
          c.carrier_name !== "generic" &&
          c.capabilities?.includes?.("tracking"),
      );

    setCarrierList(connections);
  }, [userQuery, systemQuery, references?.carriers]);

  const isFormValid = trackingNumber.trim() !== "" && selectedCarrierId !== "";

  return (
    <>
      <TrackerModalContext.Provider value={{ addTracker }}>
        {children}
      </TrackerModalContext.Provider>

      <Notifier>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogContent className="max-w-lg">
            <DialogHeader className="px-4 py-3 border-b">
              <DialogTitle>Track Package</DialogTitle>
            </DialogHeader>
            
            <div className="px-4 py-3">
              <div className="space-y-6">
                {/* Tracking Number Field */}
                <div className="space-y-2">
                  <Label htmlFor="tracking_number" className="text-sm font-medium">
                    Tracking Number <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="tracking_number"
                    className="h-8"
                    placeholder="Enter tracking number"
                    value={trackingNumber}
                    onChange={(e) => setTrackingNumber(e.target.value)}
                    required
                  />
                </div>
                
                {/* Carrier Selection Field */}
                {carrierList.length > 0 && (
                  <div className="space-y-2">
                    <Label htmlFor="carrier" className="text-sm font-medium">
                      Carrier <span className="text-red-500">*</span>
                    </Label>
                    <Select value={selectedCarrierId} onValueChange={setSelectedCarrierId}>
                      <SelectTrigger className="h-8">
                        <SelectValue placeholder="Select a carrier" />
                      </SelectTrigger>
                      <SelectContent>
                        {carrierList.map((carrier, index) => (
                          <SelectItem key={index} value={carrier.carrier_id}>
                            {`${(references.carriers as any)[carrier.carrier_name]}`}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}

                {/* No Carriers Warning */}
                {carrierList.length === 0 && (
                  <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                    <p className="text-sm text-yellow-800">
                      No carrier connections available to process tracking requests.
                    </p>
                  </div>
                )}
              </div>
            </div>
            
            <DialogFooter className="px-4 py-3 border-t">
              <Button 
                type="button" 
                variant="outline" 
                onClick={handleClose}
                disabled={loading}
              >
                Cancel
              </Button>
              <Button
                type="button"
                onClick={handleSubmit}
                disabled={loading || !isFormValid}
              >
                {loading ? "Loading..." : "Submit"}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </Notifier>
    </>
  );
};

export const useTrackerModal = () => {
  return useContext(TrackerModalContext);
};