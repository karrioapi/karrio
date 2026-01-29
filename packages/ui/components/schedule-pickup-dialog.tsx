"use client";

import * as React from "react";
import { format } from "date-fns";
import { CalendarIcon, Package, Plus, X, Loader2, MapPin, Clock, Truck, Info, RefreshCw, Hand, AlertCircle } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { useSystemConnections } from "@karrio/hooks/system-connection";
import { usePickupMutation } from "@karrio/hooks/pickup";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useShipments } from "@karrio/hooks/shipment";
import { useAddresses } from "@karrio/hooks/address";
import { AddressType, CountryCodeEnum } from "@karrio/types";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import {
  Dialog,
  DialogBody,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "./ui/popover";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "./ui/command";
import { Calendar } from "./ui/calendar";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Badge } from "./ui/badge";
import { Checkbox } from "./ui/checkbox";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "./ui/collapsible";
import { useToast } from "@karrio/ui/hooks/use-toast";

interface SchedulePickupDialogProps {
  children?: React.ReactNode;
  onScheduled?: (pickup: any) => void;
}

type PickupSchedulingType = "one_time" | "recurring";

type RecurrenceConfig = {
  frequency: "weekly" | "biweekly" | "monthly";
  days_of_week: string[];
  end_date?: string;
};

type PackageDimensions = {
  length: number | undefined;
  width: number | undefined;
  height: number | undefined;
  weight: number | undefined;
};

type PickupFormData = {
  pickup_type: PickupSchedulingType;
  recurrence: RecurrenceConfig | null;
  address_id: string;
  address: Partial<AddressType>;
  parcels_count: number;
  packages_per_month: number | undefined;
  package_dimensions: PackageDimensions;
  carrier_name: string;
  pickup_date: Date | undefined;
  ready_time: string;
  closing_time: string;
  tracking_numbers: string[];
  instruction: string;
  package_location: string;
  custom_reference: string;
  agreed_to_terms: boolean;
};

const DEFAULT_FORM_DATA: PickupFormData = {
  pickup_type: "one_time",
  recurrence: null,
  address_id: "",
  address: {},
  parcels_count: 1,
  packages_per_month: undefined,
  package_dimensions: { length: undefined, width: undefined, height: undefined, weight: undefined },
  carrier_name: "",
  pickup_date: new Date(),
  ready_time: "09:00",
  closing_time: "18:00",
  tracking_numbers: [],
  instruction: "",
  package_location: "",
  custom_reference: "",
  agreed_to_terms: false,
};

const DAYS_OF_WEEK = [
  { value: "monday", label: "Monday" },
  { value: "tuesday", label: "Tuesday" },
  { value: "wednesday", label: "Wednesday" },
  { value: "thursday", label: "Thursday" },
  { value: "friday", label: "Friday" },
];

const MAX_INSTRUCTION_LENGTH = 500;

function formatErrorMessage(error: any): string {
  if (error?.data?.errors && Array.isArray(error.data.errors)) {
    return error.data.errors
      .map((e: any) => e.message || JSON.stringify(e))
      .join("; ");
  }
  if (error?.errors && Array.isArray(error.errors)) {
    return error.errors
      .map((e: any) => e.message || JSON.stringify(e))
      .join("; ");
  }
  if (error?.message) {
    return error.message;
  }
  if (typeof error === "string") {
    return error;
  }
  return "An unexpected error occurred";
}

function formatAddressDisplay(address: Partial<AddressType>): string {
  const parts = [
    address.address_line1,
    address.city,
    address.postal_code,
  ].filter(Boolean);
  return parts.join(", ");
}

export function SchedulePickupDialog({
  children,
  onScheduled,
}: SchedulePickupDialogProps) {
  const [open, setOpen] = React.useState(false);
  const [formData, setFormData] = React.useState<PickupFormData>(DEFAULT_FORM_DATA);
  const [shipmentSearchOpen, setShipmentSearchOpen] = React.useState(false);
  const [showShipmentLinking, setShowShipmentLinking] = React.useState(false);
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  const { toast } = useToast();
  const { references } = useAPIMetadata();
  const mutation = usePickupMutation();
  const { user_connections } = useCarrierConnections();
  const { system_connections } = useSystemConnections();
  const { query: { data: { addresses } = {} } } = useAddresses();

  const { query: { data: { shipments } = {} } } = useShipments({
    status: ["purchased"] as any,
    first: 50,
  });

  const allConnections = React.useMemo(() => {
    return [
      ...(user_connections || []),
      ...(system_connections || []),
    ].filter((conn) => {
      const capabilities =
        references?.carrier_capabilities?.[conn.carrier_name] || [];
      return capabilities.includes("pickup");
    });
  }, [user_connections, system_connections, references]);

  const savedAddresses = React.useMemo(() => {
    return addresses?.edges?.map(({ node }) => node) || [];
  }, [addresses]);

  const availableShipments = React.useMemo(() => {
    if (!shipments?.edges) return [];
    return shipments.edges
      .map(({ node }) => node)
      .filter((s) => {
        if (!formData.carrier_name) return true;
        return s.carrier_name === formData.carrier_name;
      })
      .filter((s) => {
        return !formData.tracking_numbers.includes(s.tracking_number || "");
      });
  }, [shipments, formData.carrier_name, formData.tracking_numbers]);

  const handleAddressSelect = (addressId: string) => {
    const selected = savedAddresses.find((a) => a.id === addressId);
    if (selected) {
      setFormData((prev) => ({
        ...prev,
        address_id: addressId,
        address: selected as Partial<AddressType>,
      }));
    }
  };

  const handleAddShipment = (trackingNumber: string) => {
    if (!trackingNumber || formData.tracking_numbers.includes(trackingNumber)) return;

    const shipment = shipments?.edges?.find(
      ({ node }) => node.tracking_number === trackingNumber
    )?.node;

    setFormData((prev) => {
      const newData = {
        ...prev,
        tracking_numbers: [...prev.tracking_numbers, trackingNumber],
      };

      if (!prev.carrier_name && shipment?.carrier_name) {
        newData.carrier_name = shipment.carrier_name;
      }

      return newData;
    });

    setShipmentSearchOpen(false);
  };

  const handleRemoveShipment = (trackingNumber: string) => {
    setFormData((prev) => ({
      ...prev,
      tracking_numbers: prev.tracking_numbers.filter((t) => t !== trackingNumber),
    }));
  };

  const toggleDayOfWeek = (day: string) => {
    setFormData((prev) => {
      const currentDays = prev.recurrence?.days_of_week || [];
      const newDays = currentDays.includes(day)
        ? currentDays.filter((d) => d !== day)
        : [...currentDays, day];

      return {
        ...prev,
        recurrence: {
          frequency: prev.recurrence?.frequency || "weekly",
          days_of_week: newDays,
          end_date: prev.recurrence?.end_date,
        },
      };
    });
  };

  const handleSubmit = async () => {
    if (!formData.address?.address_line1 && !formData.address_id) {
      toast({
        variant: "destructive",
        title: "Validation Error",
        description: "Please select a pickup address",
      });
      return;
    }

    if (!formData.carrier_name) {
      toast({
        variant: "destructive",
        title: "Validation Error",
        description: "Please select a carrier",
      });
      return;
    }

    if (!formData.pickup_date) {
      toast({
        variant: "destructive",
        title: "Validation Error",
        description: "Please select a pickup date",
      });
      return;
    }

    if (formData.pickup_type === "one_time" && formData.parcels_count < 1) {
      toast({
        variant: "destructive",
        title: "Validation Error",
        description: "Please enter at least 1 parcel",
      });
      return;
    }

    if (formData.pickup_type === "recurring" && (!formData.recurrence?.days_of_week?.length)) {
      toast({
        variant: "destructive",
        title: "Validation Error",
        description: "Please select at least one pickup day",
      });
      return;
    }

    if (!formData.agreed_to_terms) {
      toast({
        variant: "destructive",
        title: "Validation Error",
        description: "Please agree to the carrier terms and conditions",
      });
      return;
    }

    setIsSubmitting(true);

    try {
      const payload: Record<string, any> = {
        pickup_date: format(formData.pickup_date, "yyyy-MM-dd"),
        ready_time: formData.ready_time,
        closing_time: formData.closing_time,
        instruction: formData.instruction || undefined,
        package_location: formData.package_location || undefined,
        pickup_type: formData.pickup_type,
        address: formData.address,
        parcels_count: formData.parcels_count,
      };

      if (formData.custom_reference) {
        payload.metadata = { reference: formData.custom_reference };
      }

      if (formData.tracking_numbers.length > 0) {
        payload.tracking_numbers = formData.tracking_numbers;
      }

      if (formData.pickup_type === "recurring" && formData.recurrence) {
        payload.recurrence = formData.recurrence;
        if (formData.packages_per_month) {
          payload.metadata = { ...payload.metadata, packages_per_month: formData.packages_per_month };
        }
        const dims = formData.package_dimensions;
        if (dims.length || dims.width || dims.height || dims.weight) {
          payload.metadata = {
            ...payload.metadata,
            avg_package: {
              length: dims.length,
              width: dims.width,
              height: dims.height,
              weight: dims.weight,
            },
          };
        }
      }

      const result = await mutation.schedulePickup.mutateAsync({
        carrierName: formData.carrier_name,
        data: payload,
      });

      toast({
        title: "Pickup Scheduled",
        description: `Pickup confirmation: ${result?.confirmation_number || "Success"}`,
      });

      onScheduled?.(result);
      setOpen(false);
      setFormData(DEFAULT_FORM_DATA);
      setShowShipmentLinking(false);
    } catch (error: any) {
      const errorMessage = formatErrorMessage(error);
      toast({
        variant: "destructive",
        title: "Failed to schedule pickup",
        description: errorMessage,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const isValid =
    (formData.address?.address_line1 || formData.address_id) &&
    formData.carrier_name &&
    formData.pickup_date &&
    formData.ready_time &&
    formData.closing_time &&
    formData.agreed_to_terms &&
    (formData.pickup_type === "one_time"
      ? formData.parcels_count >= 1
      : (formData.recurrence?.days_of_week?.length || 0) > 0);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children || (
          <Button size="sm">
            <Plus className="mr-2 h-4 w-4" />
            Schedule Pickup
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Request a Pickup</DialogTitle>
          <DialogDescription>
            Schedule a carrier pickup at your location.
          </DialogDescription>
        </DialogHeader>

        <DialogBody className="grid gap-6">
          {/* Section 1: Pickup Type Toggle */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Pickup type</Label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() =>
                  setFormData((prev) => ({
                    ...prev,
                    pickup_type: "one_time",
                    recurrence: null,
                  }))
                }
                className={cn(
                  "flex flex-col items-center justify-center p-4 rounded-md border transition-all",
                  formData.pickup_type === "one_time"
                    ? "border-primary bg-primary/5"
                    : "border-muted hover:border-muted-foreground/50"
                )}
              >
                <Hand className="h-6 w-6 mb-2" />
                <span className="font-medium">One time pickup</span>
              </button>
              <button
                type="button"
                onClick={() =>
                  setFormData((prev) => ({
                    ...prev,
                    pickup_type: "recurring",
                    recurrence: { frequency: "weekly", days_of_week: [] },
                  }))
                }
                className={cn(
                  "flex flex-col items-center justify-center p-4 rounded-md border transition-all",
                  formData.pickup_type === "recurring"
                    ? "border-primary bg-primary/5"
                    : "border-muted hover:border-muted-foreground/50"
                )}
              >
                <RefreshCw className="h-6 w-6 mb-2" />
                <span className="font-medium">Recurring pickup</span>
              </button>
            </div>
          </div>

          {/* Section 2: Form Content Card */}
          <div className="border rounded-md p-4 space-y-4 bg-muted/30">
            <h3 className="font-semibold">
              {formData.pickup_type === "one_time" ? "One time pickup" : "Recurring pickup"}
            </h3>

            {/* Pickup Address */}
            <div className="space-y-2">
              <Label htmlFor="address">Pickup address</Label>
              <Select
                value={formData.address_id}
                onValueChange={handleAddressSelect}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a pickup address">
                    {formData.address?.address_line1
                      ? formatAddressDisplay(formData.address)
                      : "Select a pickup address"}
                  </SelectValue>
                </SelectTrigger>
                <SelectContent>
                  {savedAddresses.map((addr) => (
                    <SelectItem key={addr.id} value={addr.id}>
                      <div className="flex flex-col">
                        <span className="font-medium">{addr.person_name || addr.company_name}</span>
                        <span className="text-xs text-muted-foreground">
                          {formatAddressDisplay(addr as Partial<AddressType>)}
                        </span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                To add a pickup address, head to{" "}
                <a href="/settings/addresses" className="text-primary hover:underline">
                  Settings &gt; Addresses
                </a>
              </p>
            </div>

            {/* Carrier */}
            <div className="space-y-2">
              <Label htmlFor="carrier">Carrier</Label>
              <Select
                value={formData.carrier_name}
                onValueChange={(value) =>
                  setFormData((prev) => ({ ...prev, carrier_name: value }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a carrier" />
                </SelectTrigger>
                <SelectContent>
                  {allConnections.map((connection) => (
                    <SelectItem
                      key={connection.id}
                      value={connection.carrier_name}
                    >
                      <div className="flex items-center gap-2">
                        <CarrierImage
                          carrier_name={connection.carrier_name}
                          height={20}
                          width={20}
                          text_color={connection.config?.text_color}
                          background={connection.config?.brand_color}
                        />
                        <span>{connection.carrier_id}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {allConnections.length === 0 && (
                <p className="text-xs text-amber-600">
                  No carriers with pickup capability found.
                </p>
              )}
              <p className="text-xs text-muted-foreground">
                Is your carrier not on the list? You can still request a recurring pickup by{" "}
                <a href="/support" className="text-primary hover:underline">
                  contacting support
                </a>
              </p>
            </div>

            {/* Recurring pickup specific fields */}
            {formData.pickup_type === "recurring" && (
              <>
                {/* Packages per month */}
                <div className="space-y-2">
                  <Label htmlFor="packages_per_month">Approximate number of packages per month</Label>
                  <Input
                    id="packages_per_month"
                    type="number"
                    min={1}
                    value={formData.packages_per_month || ""}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        packages_per_month: e.target.value ? parseInt(e.target.value, 10) : undefined,
                      }))
                    }
                    placeholder="e.g., 100"
                  />
                </div>

                {/* Package dimensions */}
                <div className="space-y-2">
                  <Label>Approximate volume of a single package</Label>
                  <p className="text-xs text-muted-foreground mb-2">
                    Please add the size of packages that will be picked up by the carrier.
                  </p>
                  <div className="flex items-center gap-2">
                    <div className="relative flex-1">
                      <Input
                        type="number"
                        min={0}
                        value={formData.package_dimensions.length || ""}
                        onChange={(e) =>
                          setFormData((prev) => ({
                            ...prev,
                            package_dimensions: {
                              ...prev.package_dimensions,
                              length: e.target.value ? parseFloat(e.target.value) : undefined,
                            },
                          }))
                        }
                        className="pr-10"
                      />
                      <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-muted-foreground">
                        cm
                      </span>
                    </div>
                    <span className="text-muted-foreground">×</span>
                    <div className="relative flex-1">
                      <Input
                        type="number"
                        min={0}
                        value={formData.package_dimensions.width || ""}
                        onChange={(e) =>
                          setFormData((prev) => ({
                            ...prev,
                            package_dimensions: {
                              ...prev.package_dimensions,
                              width: e.target.value ? parseFloat(e.target.value) : undefined,
                            },
                          }))
                        }
                        className="pr-10"
                      />
                      <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-muted-foreground">
                        cm
                      </span>
                    </div>
                    <span className="text-muted-foreground">×</span>
                    <div className="relative flex-1">
                      <Input
                        type="number"
                        min={0}
                        value={formData.package_dimensions.height || ""}
                        onChange={(e) =>
                          setFormData((prev) => ({
                            ...prev,
                            package_dimensions: {
                              ...prev.package_dimensions,
                              height: e.target.value ? parseFloat(e.target.value) : undefined,
                            },
                          }))
                        }
                        className="pr-10"
                      />
                      <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-muted-foreground">
                        cm
                      </span>
                    </div>
                  </div>
                </div>

                {/* Average weight */}
                <div className="space-y-2">
                  <Label htmlFor="avg_weight">Average weight of a single package (kg)</Label>
                  <p className="text-xs text-muted-foreground mb-2">
                    This number is an estimated average weight of a single package.
                  </p>
                  <Input
                    id="avg_weight"
                    type="number"
                    min={0}
                    step={0.1}
                    value={formData.package_dimensions.weight || ""}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        package_dimensions: {
                          ...prev.package_dimensions,
                          weight: e.target.value ? parseFloat(e.target.value) : undefined,
                        },
                      }))
                    }
                    placeholder="e.g., 2.5"
                  />
                </div>

                {/* Days for pickup */}
                <div className="space-y-2">
                  <Label>Days for the pickups</Label>
                  <p className="text-xs text-muted-foreground mb-2">
                    Select the working days which you want parcels to be picked up.
                  </p>
                  <div className="space-y-2">
                    {DAYS_OF_WEEK.map((day) => (
                      <div key={day.value} className="flex items-center space-x-2">
                        <Checkbox
                          id={day.value}
                          checked={formData.recurrence?.days_of_week?.includes(day.value)}
                          onCheckedChange={() => toggleDayOfWeek(day.value)}
                        />
                        <label
                          htmlFor={day.value}
                          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                        >
                          {day.label}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}

            {/* One-time pickup specific fields */}
            {formData.pickup_type === "one_time" && (
              <>
                {/* Pickup Date */}
                <div className="space-y-2">
                  <Label>Pickup date</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        className={cn(
                          "w-full justify-start text-left font-normal",
                          !formData.pickup_date && "text-muted-foreground"
                        )}
                      >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {formData.pickup_date ? (
                          format(formData.pickup_date, "dd/MM/yyyy")
                        ) : (
                          <span>Select a date</span>
                        )}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar
                        mode="single"
                        selected={formData.pickup_date}
                        onSelect={(date) =>
                          setFormData((prev) => ({ ...prev, pickup_date: date }))
                        }
                        disabled={(date) => date < new Date()}
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>
                  <p className="text-xs text-muted-foreground">
                    The day that the pickup should take place.
                    Pickups for the next working day need to be scheduled before 10:00PM.
                  </p>
                </div>

                {/* Time of earliest arrival */}
                <div className="space-y-2">
                  <Label htmlFor="ready_time">Time of earliest arrival</Label>
                  <p className="text-xs text-muted-foreground mb-1">
                    Time when your items will be ready for pickup.
                  </p>
                  <div className="relative">
                    <Input
                      id="ready_time"
                      type="time"
                      value={formData.ready_time}
                      onChange={(e) =>
                        setFormData((prev) => ({
                          ...prev,
                          ready_time: e.target.value,
                        }))
                      }
                    />
                  </div>
                </div>

                {/* Time of latest arrival */}
                <div className="space-y-2">
                  <Label htmlFor="closing_time">Time of latest arrival</Label>
                  <p className="text-xs text-muted-foreground mb-1">
                    Time until which someone is available.
                  </p>
                  <div className="relative">
                    <Input
                      id="closing_time"
                      type="time"
                      value={formData.closing_time}
                      onChange={(e) =>
                        setFormData((prev) => ({
                          ...prev,
                          closing_time: e.target.value,
                        }))
                      }
                    />
                  </div>
                </div>

                {/* Number of parcels */}
                <div className="space-y-2">
                  <Label htmlFor="parcels_count">Number of parcels</Label>
                  <Input
                    id="parcels_count"
                    type="number"
                    min={1}
                    value={formData.parcels_count}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        parcels_count: parseInt(e.target.value, 10) || 1,
                      }))
                    }
                  />
                  <p className="text-xs text-muted-foreground">
                    The number of parcels to be handed over to the driver.
                  </p>
                </div>
              </>
            )}

            {/* Start date for recurring */}
            {formData.pickup_type === "recurring" && (
              <div className="space-y-2">
                <Label>Start date for the pick-up</Label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      className={cn(
                        "w-full justify-start text-left font-normal",
                        !formData.pickup_date && "text-muted-foreground"
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {formData.pickup_date ? (
                        format(formData.pickup_date, "dd/MM/yyyy")
                      ) : (
                        <span>Select a date</span>
                      )}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      mode="single"
                      selected={formData.pickup_date}
                      onSelect={(date) =>
                        setFormData((prev) => ({ ...prev, pickup_date: date }))
                      }
                      disabled={(date) => {
                        const minDate = new Date();
                        minDate.setDate(minDate.getDate() + 2);
                        return date < minDate;
                      }}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
                <p className="text-xs text-muted-foreground">
                  There must be at least 2 workdays in low season (Feb-Oct) and 5 workdays during peak season (Nov-Jan) between today and the desired starting date.
                </p>
              </div>
            )}

            {/* Custom reference */}
            <div className="space-y-2">
              <Label htmlFor="custom_reference">
                Custom reference <span className="text-muted-foreground font-normal">(optional)</span>
              </Label>
              <Input
                id="custom_reference"
                value={formData.custom_reference}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    custom_reference: e.target.value,
                  }))
                }
                placeholder="Identifier for your pickup"
              />
              <p className="text-xs text-muted-foreground">
                Identifier for your pickup (optional).
              </p>
            </div>

            {/* Observations / Instructions */}
            <div className="space-y-2">
              <Label htmlFor="instruction">
                {formData.pickup_type === "recurring"
                  ? "Observations (any special notes for the carrier)"
                  : "Comment"}{" "}
                <span className="text-muted-foreground font-normal">(optional)</span>
              </Label>
              <p className="text-xs text-muted-foreground mb-1">
                {formData.pickup_type === "recurring"
                  ? "In this field you can indicate any special notes for the carrier"
                  : "Extra information for the carrier (optional)."}
              </p>
              <div className="relative">
                <Textarea
                  id="instruction"
                  value={formData.instruction}
                  onChange={(e) => {
                    if (e.target.value.length <= MAX_INSTRUCTION_LENGTH) {
                      setFormData((prev) => ({
                        ...prev,
                        instruction: e.target.value,
                      }));
                    }
                  }}
                  placeholder={
                    formData.pickup_type === "recurring"
                      ? "e.g., Please ring the bell at the back entrance"
                      : "e.g., Ring doorbell twice"
                  }
                  rows={3}
                />
                <span className="absolute bottom-2 right-2 text-xs text-muted-foreground">
                  {formData.instruction.length}/{MAX_INSTRUCTION_LENGTH} characters
                </span>
              </div>
            </div>

            {/* Link to Shipments (Optional) - One-time only */}
            {formData.pickup_type === "one_time" && (
              <Collapsible
                open={showShipmentLinking}
                onOpenChange={setShowShipmentLinking}
                className="border rounded-md"
              >
                <CollapsibleTrigger asChild>
                  <div className="flex items-center justify-between p-3 cursor-pointer hover:bg-muted/50">
                    <div>
                      <div className="flex items-center gap-2 text-sm font-medium">
                        <Package className="h-4 w-4 text-muted-foreground" />
                        <span>Link to existing shipments</span>
                        <Badge variant="outline" className="ml-2">Optional</Badge>
                      </div>
                      {formData.tracking_numbers.length > 0 && (
                        <p className="text-sm text-muted-foreground mt-1">
                          {formData.tracking_numbers.length} shipment(s) linked
                        </p>
                      )}
                    </div>
                    <span className="text-muted-foreground text-sm">
                      {showShipmentLinking ? "▲" : "▼"}
                    </span>
                  </div>
                </CollapsibleTrigger>
                <CollapsibleContent className="border-t">
                  <div className="p-3 space-y-2">
                    <div className="flex flex-wrap gap-2 min-h-[36px] p-2 border rounded-md bg-background">
                      {formData.tracking_numbers.map((trackingNumber) => (
                        <Badge key={trackingNumber} variant="secondary" className="gap-1">
                          <Package className="h-3 w-3" />
                          {trackingNumber}
                          <button
                            type="button"
                            onClick={() => handleRemoveShipment(trackingNumber)}
                            className="ml-1 hover:bg-muted rounded-full p-0.5"
                          >
                            <X className="h-3 w-3" />
                          </button>
                        </Badge>
                      ))}
                      <Popover open={shipmentSearchOpen} onOpenChange={setShipmentSearchOpen}>
                        <PopoverTrigger asChild>
                          <Button
                            variant="outline"
                            size="sm"
                            className="h-6 border-dashed text-xs"
                          >
                            <Plus className="mr-1 h-3 w-3" />
                            Add
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-[280px] p-0" align="start">
                          <Command>
                            <CommandInput placeholder="Search shipments..." />
                            <CommandList>
                              <CommandEmpty>No shipments found.</CommandEmpty>
                              <CommandGroup>
                                {availableShipments.map((shipment) => (
                                  <CommandItem
                                    key={shipment.id}
                                    value={shipment.tracking_number || shipment.id}
                                    onSelect={() =>
                                      handleAddShipment(shipment.tracking_number || "")
                                    }
                                  >
                                    <div className="flex flex-col">
                                      <span className="font-medium text-sm">
                                        {shipment.tracking_number || shipment.id}
                                      </span>
                                      <span className="text-xs text-muted-foreground">
                                        {shipment.carrier_name}
                                      </span>
                                    </div>
                                  </CommandItem>
                                ))}
                              </CommandGroup>
                            </CommandList>
                          </Command>
                        </PopoverContent>
                      </Popover>
                    </div>
                  </div>
                </CollapsibleContent>
              </Collapsible>
            )}
          </div>

          {/* Carrier Conditions */}
          <div className="flex gap-3 p-4 bg-blue-50 dark:bg-blue-950/30 rounded-md text-sm">
            <Info className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div className="space-y-2 text-blue-900 dark:text-blue-100">
              <p className="font-medium">Carrier conditions</p>
              <ul className="space-y-1 text-xs list-disc pl-4">
                <li>Pickups can only be requested Monday through Friday, there are no pickups on weekends or holidays.</li>
                <li>If you don't have parcels to be picked up, please contact the local office to notify them.</li>
                <li>Failed pickups due to parcels not being prepared on time or being absent may result in a surcharge.</li>
                <li>Available times can vary and are subject to the availability of the local office.</li>
              </ul>
            </div>
          </div>

          {/* Terms Agreement */}
          <div className="flex items-start space-x-2">
            <Checkbox
              id="terms"
              checked={formData.agreed_to_terms}
              onCheckedChange={(checked) =>
                setFormData((prev) => ({
                  ...prev,
                  agreed_to_terms: checked === true,
                }))
              }
            />
            <label
              htmlFor="terms"
              className="text-sm leading-tight cursor-pointer"
            >
              By clicking "Request pickup" I am agreeing to the{" "}
              <a href="/terms" className="text-primary hover:underline">
                terms and conditions
              </a>{" "}
              of the carrier.
            </label>
          </div>
        </DialogBody>

        <DialogFooter className="gap-2">
          <Button
            variant="outline"
            onClick={() => setOpen(false)}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={!isValid || isSubmitting}>
            {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Request pickup
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
