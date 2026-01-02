"use client";

import React, { useEffect, useState, useRef, useMemo, useCallback } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@karrio/ui/components/ui/sheet";
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogCancel,
  AlertDialogAction,
} from "@karrio/ui/components/ui/alert-dialog";
import { ServiceEditorModal } from "@karrio/ui/components/modals/service-editor-modal";
import { CURRENCY_OPTIONS, DIMENSION_UNITS, WEIGHT_UNITS } from "@karrio/types";
import { RateSheetTable } from "@karrio/ui/components/rate-sheet-table";
import { ZonesTab } from "@karrio/ui/components/zones-tab";
import { ServicesTab } from "@karrio/ui/components/services-tab";
import { SurchargesTab } from "@karrio/ui/components/surcharges-tab";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { MultiSelect } from "@karrio/ui/components/multi-select";
import { cn } from "@karrio/ui/lib/utils";
import {
  PlusIcon,
  Pencil1Icon,
  TrashIcon,
  Cross2Icon,
  HamburgerMenuIcon,
} from "@radix-ui/react-icons";
import { Loader2 } from "lucide-react";

// Generate a unique ID for new entities
const generateId = (prefix: string = "temp") =>
  `${prefix}-${crypto.randomUUID()}`;

// Convert features to object format for GraphQL mutation
// Handles both array format ['tracked', 'b2c'] and object format { tracked: true, b2c: true, first_mile: "drop_off" }
const featuresToObject = (features?: string[] | Record<string, any>): Record<string, any> | undefined => {
  if (!features) return undefined;

  // If already an object, return as-is (new structured format)
  if (!Array.isArray(features)) {
    // Filter out null/undefined/empty/whitespace string values but keep false values
    const result: Record<string, any> = {};
    for (const [key, value] of Object.entries(features)) {
      // Convert empty/whitespace strings to null
      if (typeof value === "string") {
        const trimmed = value.trim();
        if (trimmed === "") {
          result[key] = null;
        } else {
          result[key] = trimmed;
        }
      } else if (value !== null && value !== undefined) {
        result[key] = value;
      }
    }
    return Object.keys(result).length > 0 ? result : undefined;
  }

  // If array, convert to object (legacy format)
  if (features.length === 0) return undefined;
  return features.reduce((acc, feature) => {
    acc[feature] = true;
    return acc;
  }, {} as Record<string, boolean>);
};

// Convert features object to array for UI state
// { tracked: true, b2c: true, express: false } => ['tracked', 'b2c']
const featuresToArray = (features?: Record<string, any> | null): string[] => {
  if (!features || typeof features !== 'object') return [];
  return Object.entries(features)
    .filter(([_, value]) => value === true)
    .map(([key]) => key);
};

// Types for the rate sheet editor
export interface EmbeddedZone {
  id: string;
  label: string;
  rate: number;
  cost?: number | null;
  min_weight?: number | null;
  max_weight?: number | null;
  weight_unit?: string | null;
  transit_days?: number | null;
  transit_time?: number | null;
  country_codes?: string[];
  postal_codes?: string[];
  cities?: string[];
}

export interface SharedSurcharge {
  id: string;
  name: string;
  amount: number;
  surcharge_type?: string;
  cost?: number | null;
  active?: boolean;
}

export interface ServiceLevelWithZones {
  id: string;
  object_type?: string;
  service_name: string;
  service_code: string;
  carrier_service_code?: string | null;
  description?: string | null;
  active?: boolean;
  currency?: string;
  transit_days?: number | null;
  transit_time?: number | null;
  max_width?: number | null;
  max_height?: number | null;
  max_length?: number | null;
  dimension_unit?: string | null;
  max_weight?: number | null;
  weight_unit?: string | null;
  domicile?: boolean | null;
  international?: boolean | null;
  use_volumetric?: boolean;
  dim_factor?: number | null;
  zones?: EmbeddedZone[];
  zone_ids?: string[];
  surcharge_ids?: string[];
  features?: string[];
}

export interface RateSheetCarrier {
  id: string;
  active?: boolean;
  carrier_id: string;
  carrier_name: string;
  display_name?: string;
  capabilities?: string[];
  test_mode?: boolean;
}

interface RateSheetEditorProps {
  rateSheetId: string;
  onClose: () => void;
  preloadCarrier?: string;
  linkConnectionId?: string;
  isAdmin?: boolean;
  useRateSheet: (args: any) => any;
  useRateSheetMutation: () => any;
}

interface OriginalState {
  name: string;
  zones: Map<string, EmbeddedZone>;
  surcharges: Map<string, SharedSurcharge>;
  serviceRates: Map<string, { rate: number; cost?: number | null }>;
  serviceZoneIds: Map<string, string[]>;
  serviceSurchargeIds: Map<string, string[]>;
}

export const RateSheetEditor = ({
  rateSheetId,
  onClose,
  preloadCarrier,
  linkConnectionId,
  isAdmin = false,
  useRateSheet,
  useRateSheetMutation,
}: RateSheetEditorProps) => {
  const isNew = rateSheetId === "new";
  const isEditMode = !isNew;

  // Local state
  const [carrierName, setCarrierName] = useState<string>(preloadCarrier || "");
  const [name, setName] = useState<string>("");
  const [originCountries, setOriginCountries] = useState<string[]>([]);
  const [services, setServices] = useState<ServiceLevelWithZones[]>([]);
  const [surcharges, setSurcharges] = useState<SharedSurcharge[]>([]);
  const [sharedZones, setSharedZones] = useState<EmbeddedZone[]>([]);

  // Original state for change tracking
  const originalStateRef = useRef<OriginalState | null>(null);

  // Service dialog state
  const [serviceDialogOpen, setServiceDialogOpen] = useState(false);
  const [selectedService, setSelectedService] =
    useState<ServiceLevelWithZones | null>(null);

  // Delete confirmation state
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [serviceToDelete, setServiceToDelete] =
    useState<ServiceLevelWithZones | null>(null);
  const [zoneToDeleteLabel, setZoneToDeleteLabel] = useState<string | null>(
    null
  );
  const [deleteZoneConfirmOpen, setDeleteZoneConfirmOpen] = useState(false);

  // Loading states
  const [isLoadingDefaults, setIsLoadingDefaults] = useState(false);
  const [isDeletingService, setIsDeletingService] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Tab state
  const [activeTab, setActiveTab] = useState<
    "rate_sheet" | "zones" | "services" | "surcharges"
  >("rate_sheet");

  // Mobile sidebar state
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Text buffer state for smooth typing
  const [zoneTextBuffers, setZoneTextBuffers] = useState<
    Record<string, Partial<Record<"cities" | "postal_codes", string>>>
  >({});

  // Hooks
  const { references, metadata } = useAPIMetadata();
  const { toast } = useToast();
  const { query } = useRateSheet({ id: isEditMode ? rateSheetId : undefined });
  const mutations = useRateSheetMutation();

  const existingRateSheet = query?.data?.rate_sheet;
  const isRateSheetLoading = query?.isLoading;

  // Get list of carriers that support rate sheets
  // All enabled carriers are included (backend returns all carriers in ratesheets,
  // some with default zones/services, others with empty defaults for custom configuration)
  const carriers = useMemo(() => {
    const carriersList = references?.carriers || {};
    const ratesheets = references?.ratesheets || {};
    return Object.entries(carriersList)
      .filter(([id]) => ratesheets[id])
      .map(([id, name]) => ({
        id,
        name: String(name),
      }));
  }, [references?.carriers, references?.ratesheets]);

  // Get country options
  const countryOptions = useMemo(() => {
    const countries = references?.countries || {};
    return Object.entries(countries)
      .map(([code, name]) => ({
        value: code.toUpperCase(),
        label: String(name),
      }))
      .sort((a, b) => a.label.localeCompare(b.label));
  }, [references?.countries]);

  const currencyOptions = CURRENCY_OPTIONS;
  const weightUnitOptions = WEIGHT_UNITS;
  const dimensionUnitOptions = DIMENSION_UNITS;

  const selectedCurrency = services[0]?.currency ?? "USD";
  const selectedWeightUnit = services[0]?.weight_unit ?? "KG";
  const selectedDimensionUnit = services[0]?.dimension_unit ?? "CM";

  const connectedCarriers: RateSheetCarrier[] =
    (existingRateSheet?.carriers as RateSheetCarrier[]) ?? [];

  const isInitialLoading = isEditMode && isRateSheetLoading && !existingRateSheet;

  // Load existing rate sheet data when in edit mode
  useEffect(() => {
    if (existingRateSheet && isEditMode) {
      setCarrierName(existingRateSheet.carrier_name || "");
      setName(existingRateSheet.name || "");
      setOriginCountries(existingRateSheet.origin_countries || []);

      const existingSharedZones = existingRateSheet.zones || [];
      const serviceRates = existingRateSheet.service_rates || [];
      const rawServices = existingRateSheet.services || [];

      const zoneMap = new Map(existingSharedZones.map((z: any) => [z.id, z]));
      const rateMap = new Map(
        serviceRates.map((sr: any) => [`${sr.service_id}:${sr.zone_id}`, sr])
      );

      const linkedZoneIds = new Set<string>();

      const transformedServices = rawServices.map((service: any) => {
        const zoneIds = service.zone_ids || [];

        const embeddedZones = zoneIds.map((zoneId: string, index: number) => {
          const zone = zoneMap.get(zoneId) as any;
          const rateEntry = rateMap.get(`${service.id}:${zoneId}`) as any;
          linkedZoneIds.add(zoneId);

          return {
            id: zoneId,
            label: zone?.label || `Zone ${index + 1}`,
            rate: rateEntry?.rate ?? 0,
            cost: rateEntry?.cost ?? null,
            min_weight: rateEntry?.min_weight ?? zone?.min_weight ?? null,
            max_weight: rateEntry?.max_weight ?? zone?.max_weight ?? null,
            weight_unit: zone?.weight_unit ?? null,
            transit_days: rateEntry?.transit_days ?? zone?.transit_days ?? null,
            transit_time: rateEntry?.transit_time ?? zone?.transit_time ?? null,
            country_codes: zone?.country_codes || [],
            postal_codes: zone?.postal_codes || [],
            cities: zone?.cities || [],
          };
        });

        // Extract string enum fields from features object for the service editor
        const featuresObj = service.features as Record<string, any> | null;
        return {
          ...service,
          zones: embeddedZones,
          features: featuresToArray(service.features),
          // Extract logistics options from features for the service editor modal
          first_mile: featuresObj?.first_mile || "",
          last_mile: featuresObj?.last_mile || "",
          form_factor: featuresObj?.form_factor || "",
          age_check: featuresObj?.age_check || "",
        };
      });

      const unlinkedZones: EmbeddedZone[] = existingSharedZones
        .filter((z: any) => !linkedZoneIds.has(z.id))
        .map((zone: any) => ({
          id: zone.id,
          label: zone.label || "",
          rate: 0,
          cost: null,
          min_weight: zone.min_weight ?? null,
          max_weight: zone.max_weight ?? null,
          weight_unit: zone.weight_unit ?? null,
          transit_days: zone.transit_days ?? null,
          transit_time: zone.transit_time ?? null,
          country_codes: zone.country_codes || [],
          postal_codes: zone.postal_codes || [],
          cities: zone.cities || [],
        }));

      setServices(transformedServices as ServiceLevelWithZones[]);
      setSharedZones(unlinkedZones);
      setSurcharges(existingRateSheet.surcharges || []);

      // Store original state for change tracking
      const originalZones = new Map<string, EmbeddedZone>();
      existingSharedZones.forEach((z: any) => {
        originalZones.set(z.id, {
          id: z.id,
          label: z.label || "",
          rate: 0,
          country_codes: z.country_codes || [],
          postal_codes: z.postal_codes || [],
          cities: z.cities || [],
          transit_days: z.transit_days ?? null,
          transit_time: z.transit_time ?? null,
        });
      });

      const originalSurcharges = new Map<string, SharedSurcharge>();
      (existingRateSheet.surcharges || []).forEach((s: any) => {
        originalSurcharges.set(s.id, { ...s });
      });

      const originalServiceRates = new Map<
        string,
        { rate: number; cost?: number | null }
      >();
      serviceRates.forEach((sr: any) => {
        originalServiceRates.set(`${sr.service_id}:${sr.zone_id}`, {
          rate: sr.rate,
          cost: sr.cost,
        });
      });

      const originalServiceZoneIds = new Map<string, string[]>();
      const originalServiceSurchargeIds = new Map<string, string[]>();
      rawServices.forEach((s: any) => {
        originalServiceZoneIds.set(s.id, [...(s.zone_ids || [])]);
        originalServiceSurchargeIds.set(s.id, [...(s.surcharge_ids || [])]);
      });

      originalStateRef.current = {
        name: existingRateSheet.name || "",
        zones: originalZones,
        surcharges: originalSurcharges,
        serviceRates: originalServiceRates,
        serviceZoneIds: originalServiceZoneIds,
        serviceSurchargeIds: originalServiceSurchargeIds,
      };
    }
  }, [existingRateSheet, isEditMode]);

  // Reset form when creating new
  useEffect(() => {
    if (!isEditMode) {
      if (preloadCarrier) {
        setCarrierName(preloadCarrier);
        const carrier = carriers.find((c) => c.id === preloadCarrier);
        if (carrier) {
          setName(`${carrier.name} - sheet`);
        }
      } else {
        setCarrierName("");
        setName("");
      }
      setOriginCountries([]);
      setServices([]);
      setSharedZones([]);
      setSurcharges([]);
      originalStateRef.current = null;
    }
  }, [isEditMode, preloadCarrier, carriers]);

  // Track previous carrier to detect changes
  const prevCarrierRef = useRef<string>("");

  // Reset services and prefill name when carrier changes in create mode
  useEffect(() => {
    if (!isEditMode && carrierName) {
      const carrier = carriers.find((c) => c.id === carrierName);
      if (carrier) {
        setName(`${carrier.name} - sheet`);
      }
      if (prevCarrierRef.current && prevCarrierRef.current !== carrierName) {
        setServices([]);
      }
    }
    prevCarrierRef.current = carrierName;
  }, [carrierName, isEditMode, carriers]);

  // Handler functions
  const handleAddService = () => {
    setSelectedService(null);
    setServiceDialogOpen(true);
  };

  const handleEditService = (service: ServiceLevelWithZones) => {
    setSelectedService(service);
    setServiceDialogOpen(true);
  };

  const handleSaveService = (serviceData: Partial<ServiceLevelWithZones>) => {
    if (selectedService) {
      setServices((prev) =>
        prev.map((s) =>
          s.service_code === selectedService.service_code
            ? { ...s, ...serviceData }
            : s
        )
      );
    } else {
      const newService: ServiceLevelWithZones = {
        id: generateId("service"),
        object_type: "service_level",
        service_name: serviceData.service_name || "",
        service_code: serviceData.service_code || "",
        currency: serviceData.currency ?? "USD",
        carrier_service_code: serviceData.carrier_service_code ?? null,
        description: serviceData.description ?? null,
        transit_days: serviceData.transit_days ?? null,
        transit_time: null,
        zones: [
          {
            id: generateId("zone"),
            rate: 0,
            label: "Zone 1",
            min_weight: null,
            max_weight: null,
            weight_unit: null,
            transit_days: null,
            transit_time: null,
            cities: [],
            postal_codes: [],
            country_codes: [],
          },
        ],
        active: serviceData.active ?? true,
        domicile: serviceData.domicile ?? null,
        international: serviceData.international ?? null,
        max_weight: serviceData.max_weight ?? null,
        weight_unit: serviceData.weight_unit ?? null,
        max_width: serviceData.max_width ?? null,
        max_height: serviceData.max_height ?? null,
        max_length: serviceData.max_length ?? null,
        dimension_unit: serviceData.dimension_unit ?? null,
        features: serviceData.features ?? [],
      };
      setServices((prev) => [...prev, newService]);
    }
    setServiceDialogOpen(false);
    setSelectedService(null);
  };

  const handleUpdateService = (
    index: number,
    updatedService: ServiceLevelWithZones
  ) => {
    setServices((prev) => {
      const newServices = [...prev];
      newServices[index] = updatedService;
      return newServices;
    });
  };

  const handleDeleteClick = (service: ServiceLevelWithZones) => {
    setServiceToDelete(service);
    setDeleteConfirmOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (serviceToDelete) {
      const isExistingService =
        serviceToDelete.id && !serviceToDelete.id.startsWith("temp-");

      if (isExistingService && rateSheetId && mutations.deleteRateSheetService) {
        setIsDeletingService(true);
        try {
          await mutations.deleteRateSheetService.mutateAsync({
            rate_sheet_id: rateSheetId,
            service_id: serviceToDelete.id,
          });
          toast({
            title: "Service deleted",
            description: "Service has been removed from the rate sheet",
          });
        } catch (error) {
          toast({
            title: "Failed to delete service",
            description: "An error occurred while deleting the service",
            variant: "destructive",
          });
          setServiceToDelete(null);
          setDeleteConfirmOpen(false);
          setIsDeletingService(false);
          return;
        } finally {
          setIsDeletingService(false);
        }
      }

      setServices((prev) =>
        prev.filter((s) => s.service_code !== serviceToDelete.service_code)
      );
      setServiceToDelete(null);
      setDeleteConfirmOpen(false);
    }
  };

  // Collect all zone labels
  const collectAllZoneLabels = (): Set<string> => {
    const labels = new Set<string>();
    sharedZones.filter((z) => z.label).forEach((z) => labels.add(z.label));
    services
      .flatMap((s) => s.zones || [])
      .filter((z) => z.label)
      .forEach((z) => labels.add(z.label));
    return labels;
  };

  // Add a new shared zone
  const handleAddZoneAll = () => {
    const allZoneLabels = collectAllZoneLabels();
    let nextNum = 1;
    while (allZoneLabels.has(`Zone ${nextNum}`)) nextNum++;

    const newZone: EmbeddedZone = {
      id: generateId("zone"),
      rate: 0,
      label: `Zone ${nextNum}`,
      min_weight: null,
      max_weight: null,
      weight_unit: null,
      transit_days: null,
      transit_time: null,
      cities: [],
      postal_codes: [],
      country_codes: [],
    };

    setSharedZones((prev) => [...prev, newZone]);
  };

  // Update zone by label/key
  const handleUpdateZone = (zoneKey: string, updates: Partial<EmbeddedZone>) => {
    if (!zoneKey) return;

    setSharedZones((prev) =>
      prev.map((zone) => {
        if ((zone.label || zone.id) === zoneKey) {
          return { ...zone, ...updates };
        }
        return zone;
      })
    );

    setServices((prev) =>
      prev.map((service) => {
        const newZones = (service.zones || []).map((zone) => {
          if ((zone.label || zone.id) === zoneKey) {
            return { ...zone, ...updates };
          }
          return zone;
        });
        return {
          ...service,
          zones: newZones,
        };
      })
    );
  };

  // Remove zone from ALL services
  const handleRemoveZoneAll = (zoneLabel: string) => {
    setZoneToDeleteLabel(zoneLabel);
    setDeleteZoneConfirmOpen(true);
  };

  const handleConfirmRemoveZone = () => {
    if (zoneToDeleteLabel !== null) {
      setSharedZones((prev) =>
        prev.filter((zone) => (zone.label || zone.id) !== zoneToDeleteLabel)
      );

      setServices((prev) =>
        prev.map((service) => ({
          ...service,
          zones: (service.zones || []).filter(
            (zone) => (zone.label || zone.id) !== zoneToDeleteLabel
          ),
        }))
      );

      setZoneToDeleteLabel(null);
      setDeleteZoneConfirmOpen(false);
    }
  };

  // Text buffering helpers
  const getZoneTextValue = (
    zoneKey: string,
    field: "cities" | "postal_codes",
    currentArray: string[] | undefined | null
  ): string => {
    const buffered = zoneTextBuffers[zoneKey]?.[field];
    if (typeof buffered === "string") return buffered;
    return Array.isArray(currentArray) ? currentArray.join(", ") : "";
  };

  const setZoneTextValue = (
    zoneKey: string,
    field: "cities" | "postal_codes",
    text: string
  ) => {
    setZoneTextBuffers((prev) => ({
      ...prev,
      [zoneKey]: {
        ...(prev[zoneKey] || {}),
        [field]: text,
      },
    }));
  };

  const persistZoneTextValue = (
    zoneKey: string,
    field: "cities" | "postal_codes"
  ) => {
    const text = zoneTextBuffers[zoneKey]?.[field];
    if (text === undefined) return;
    const values = text
      .split(",")
      .map((v) => v.trim())
      .filter((v) => v.length > 0);
    handleUpdateZone(zoneKey, { [field]: values });
    setZoneTextBuffers((prev) => {
      const next = { ...prev };
      const zoneEntry = { ...(next[zoneKey] || {}) };
      delete zoneEntry[field];
      if (Object.keys(zoneEntry).length === 0) {
        delete next[zoneKey];
      } else {
        next[zoneKey] = zoneEntry;
      }
      return next;
    });
  };

  // Surcharge handlers
  const handleAddSurcharge = () => {
    const newSurcharge: SharedSurcharge = {
      id: generateId("surcharge"),
      name: "",
      amount: 0,
      surcharge_type: "fixed",
      active: true,
      cost: null,
    };
    setSurcharges((prev) => [...prev, newSurcharge]);
  };

  const handleUpdateSurcharge = (
    surchargeId: string,
    updates: Partial<SharedSurcharge>
  ) => {
    setSurcharges((prev) =>
      prev.map((s) => (s.id === surchargeId ? { ...s, ...updates } : s))
    );
  };

  const handleRemoveSurcharge = (surchargeId: string) => {
    setSurcharges((prev) => prev.filter((s) => s.id !== surchargeId));
  };

  // Toggle service-surcharge linking
  const handleToggleServiceSurcharge = (
    serviceId: string,
    surchargeId: string,
    linked: boolean
  ) => {
    setServices((prev) =>
      prev.map((service) => {
        if (service.id !== serviceId) return service;
        const currentIds = service.surcharge_ids || [];
        const newIds = linked
          ? [...currentIds, surchargeId]
          : currentIds.filter((id) => id !== surchargeId);
        return { ...service, surcharge_ids: newIds };
      })
    );
  };

  const handleLoadDefaults = async () => {
    if (!carrierName) return;

    setIsLoadingDefaults(true);
    try {
      const rateSheetDefaults = references?.ratesheets?.[carrierName];

      if (
        !rateSheetDefaults ||
        !rateSheetDefaults.services ||
        rateSheetDefaults.services.length === 0
      ) {
        toast({
          title: "No defaults available",
          description: `No default services found for ${carrierName}`,
          variant: "destructive",
        });
        return;
      }

      const {
        zones: defaultZones,
        services: defaultServicesList,
        service_rates: serviceRates,
      } = rateSheetDefaults;

      const zoneMap = new Map((defaultZones || []).map((z: any) => [z.id, z]));
      const rateMap = new Map(
        (serviceRates || []).map((sr: any) => [
          `${sr.service_id}:${sr.zone_id}`,
          sr,
        ])
      );

      const defaultServices: ServiceLevelWithZones[] = defaultServicesList.map(
        (service: any, index: number) => {
          const serviceId = service.id || String(index);
          const zoneIds = service.zone_ids || [];

          const zones = zoneIds.map((zoneId: string, zoneIndex: number) => {
            const zone = zoneMap.get(zoneId) || { label: `Zone ${zoneIndex + 1}` };
            const rateEntry = rateMap.get(`${serviceId}:${zoneId}`);

            return {
              id: generateId("zone"),
              label: zone.label || `Zone ${zoneIndex + 1}`,
              rate: rateEntry?.rate ?? 0,
              cost: rateEntry?.cost ?? null,
              min_weight: rateEntry?.min_weight ?? zone.min_weight ?? null,
              max_weight: rateEntry?.max_weight ?? zone.max_weight ?? null,
              weight_unit: zone.weight_unit ?? null,
              transit_days: rateEntry?.transit_days ?? zone.transit_days ?? null,
              transit_time: rateEntry?.transit_time ?? zone.transit_time ?? null,
              country_codes: zone.country_codes || [],
              postal_codes: zone.postal_codes || [],
              cities: zone.cities || [],
            } as EmbeddedZone;
          });

          const finalZones =
            zones.length > 0
              ? zones
              : [
                  {
                    id: generateId("zone"),
                    rate: 0,
                    label: "Zone 1",
                    min_weight: null,
                    max_weight: null,
                    weight_unit: null,
                    transit_days: null,
                    transit_time: null,
                    cities: [],
                    postal_codes: [],
                    country_codes: [],
                  } as EmbeddedZone,
                ];

          return {
            id: generateId("service"),
            object_type: "service_level",
            service_name: service.service_name || "",
            service_code: service.service_code || "",
            carrier_service_code: service.carrier_service_code ?? null,
            description: service.description ?? null,
            active: service.active ?? true,
            currency: service.currency ?? "USD",
            transit_days: service.transit_days ?? null,
            transit_time: service.transit_time ?? null,
            max_width: service.max_width ?? null,
            max_height: service.max_height ?? null,
            max_length: service.max_length ?? null,
            dimension_unit: service.dimension_unit ?? null,
            max_weight: service.max_weight ?? null,
            weight_unit: service.weight_unit ?? null,
            domicile: service.domicile ?? null,
            international: service.international ?? null,
            zones: finalZones,
            zone_ids: zoneIds,
            surcharge_ids: service.surcharge_ids || [],
          } as ServiceLevelWithZones;
        }
      );

      setServices(defaultServices);
      toast({
        title: "Defaults loaded",
        description: `Loaded ${defaultServices.length} services from ${carrierName}`,
      });
    } catch (error) {
      toast({
        title: "Failed to load defaults",
        description: "An error occurred while loading carrier defaults",
        variant: "destructive",
      });
    } finally {
      setIsLoadingDefaults(false);
    }
  };

  const validateForm = (): { isValid: boolean; errors: string[] } => {
    const errors: string[] = [];

    if (!name.trim()) {
      errors.push("Rate sheet name is required");
    }

    if (!carrierName) {
      errors.push("Carrier is required");
    }

    if (services.length === 0) {
      errors.push("At least one service is required");
    }

    return {
      isValid: errors.length === 0,
      errors,
    };
  };

  const handleSave = async () => {
    const validation = validateForm();

    if (!validation.isValid) {
      toast({
        title: "Validation Error",
        description: validation.errors.join(", "),
        variant: "destructive",
      });
      return;
    }

    setIsSaving(true);

    try {
      // Build unified zone map
      const buildZoneMap = () => {
        const zoneMap = new Map<
          string,
          {
            id: string;
            label: string;
            country_codes: string[];
            postal_codes: string[];
            cities: string[];
            transit_days: number | null;
            transit_time: number | null;
            min_weight: number | null;
            max_weight: number | null;
            weight_unit: string | null;
          }
        >();

        let zoneIndex = 0;

        sharedZones.forEach((zone) => {
          const zoneLabel = zone.label || `Zone ${zoneIndex + 1}`;
          if (!zoneMap.has(zoneLabel)) {
            const zoneId = zone.id?.startsWith("temp-")
              ? `zone_${zoneIndex}`
              : zone.id || `zone_${zoneIndex}`;
            zoneMap.set(zoneLabel, {
              id: zoneId,
              label: zoneLabel,
              country_codes: zone.country_codes || [],
              postal_codes: zone.postal_codes || [],
              cities: zone.cities || [],
              transit_days: zone.transit_days ?? null,
              transit_time: zone.transit_time ?? null,
              min_weight: zone.min_weight ?? null,
              max_weight: zone.max_weight ?? null,
              weight_unit: zone.weight_unit ?? null,
            });
            zoneIndex++;
          }
        });

        services.forEach((service) => {
          (service.zones || []).forEach((zone) => {
            const zoneLabel = zone.label || `Zone ${zoneIndex + 1}`;
            if (!zoneMap.has(zoneLabel)) {
              const zoneId = zone.id?.startsWith("temp-")
                ? `zone_${zoneIndex}`
                : zone.id || `zone_${zoneIndex}`;
              zoneMap.set(zoneLabel, {
                id: zoneId,
                label: zoneLabel,
                country_codes: zone.country_codes || [],
                postal_codes: zone.postal_codes || [],
                cities: zone.cities || [],
                transit_days: zone.transit_days ?? null,
                transit_time: zone.transit_time ?? null,
                min_weight: zone.min_weight ?? null,
                max_weight: zone.max_weight ?? null,
                weight_unit: zone.weight_unit ?? null,
              });
              zoneIndex++;
            }
          });
        });

        return zoneMap;
      };

      const zoneMap = buildZoneMap();
      const zoneLabelToId = new Map<string, string>();
      zoneMap.forEach((zone, label) => zoneLabelToId.set(label, zone.id));

      const zonesForMutation = Array.from(zoneMap.values()).map((zone) => ({
        id: zone.id,
        label: zone.label,
        country_codes:
          zone.country_codes.length > 0 ? zone.country_codes : undefined,
        postal_codes:
          zone.postal_codes.length > 0 ? zone.postal_codes : undefined,
        cities: zone.cities.length > 0 ? zone.cities : undefined,
        transit_days: zone.transit_days,
        transit_time: zone.transit_time,
        min_weight: zone.min_weight,
        max_weight: zone.max_weight,
        weight_unit: zone.weight_unit,
      }));

      const serviceRates: Array<{
        service_id: string;
        zone_id: string;
        rate: number;
        cost?: number | null;
        min_weight?: number | null;
        max_weight?: number | null;
        transit_days?: number | null;
        transit_time?: number | null;
      }> = [];

      const surchargeIdMap = new Map<string, string>();
      const surchargesForMutation = surcharges.map((surcharge, index) => {
        const newId = surcharge.id?.startsWith("temp-")
          ? `surcharge_${index}`
          : surcharge.id || `surcharge_${index}`;
        surchargeIdMap.set(surcharge.id, newId);
        return {
          id: newId,
          name: surcharge.name || "",
          amount: surcharge.amount || 0,
          surcharge_type: surcharge.surcharge_type || "fixed",
          cost: surcharge.cost ?? null,
          active: surcharge.active ?? true,
        };
      });

      if (isEditMode) {
        // Full update for edit mode
        const updateServices = services.map((service, serviceIndex) => {
          const serviceId = service.id?.startsWith("temp-")
            ? `temp-${serviceIndex}`
            : service.id;
          const zoneIds = (service.zones || [])
            .map((z) => zoneLabelToId.get(z.label || ""))
            .filter(Boolean) as string[];

          (service.zones || []).forEach((zone) => {
            const zoneId = zoneLabelToId.get(zone.label || "");
            if (zoneId) {
              serviceRates.push({
                service_id: serviceId,
                zone_id: zoneId,
                rate: zone.rate || 0,
                cost: zone.cost ?? null,
                min_weight: zone.min_weight ?? null,
                max_weight: zone.max_weight ?? null,
                transit_days: zone.transit_days ?? null,
                transit_time: zone.transit_time ?? null,
              });
            }
          });

          const mappedSurchargeIds = (service.surcharge_ids || [])
            .map((id) => surchargeIdMap.get(id) || id)
            .filter((id) => surchargesForMutation.some((s) => s.id === id));

          return {
            id: service.id?.startsWith("temp-") ? null : service.id,
            service_name: service.service_name || "",
            service_code: service.service_code || "",
            currency: service.currency || "USD",
            carrier_service_code: service.carrier_service_code,
            description: service.description,
            active: service.active,
            transit_days: service.transit_days,
            transit_time: service.transit_time,
            max_width: service.max_width,
            max_height: service.max_height,
            max_length: service.max_length,
            dimension_unit: service.dimension_unit,
            max_weight: service.max_weight,
            weight_unit: service.weight_unit,
            domicile: service.domicile,
            international: service.international,
            use_volumetric: service.use_volumetric,
            dim_factor: service.dim_factor,
            zone_ids: zoneIds,
            surcharge_ids: mappedSurchargeIds,
            features: featuresToObject(service.features),
          };
        });

        await mutations.updateRateSheet.mutateAsync({
          id: rateSheetId,
          name,
          origin_countries: originCountries,
          services: updateServices,
          zones: zonesForMutation,
          surcharges: surchargesForMutation,
          service_rates: serviceRates,
        } as any);

        toast({
          title: "Rate sheet updated",
          description: `"${name}" has been updated successfully`,
        });
      } else {
        // Create new rate sheet
        const createServices = services.map((service, serviceIndex) => {
          const tempServiceId = `temp-${serviceIndex}`;
          const zoneIds: string[] = [];

          (service.zones || []).forEach((zone) => {
            const zoneLabel = zone.label || "";
            const zoneId = zoneLabelToId.get(zoneLabel);
            if (zoneId) {
              zoneIds.push(zoneId);
              serviceRates.push({
                service_id: tempServiceId,
                zone_id: zoneId,
                rate: zone.rate || 0,
                cost: zone.cost ?? null,
                min_weight: zone.min_weight ?? null,
                max_weight: zone.max_weight ?? null,
                transit_days: zone.transit_days ?? null,
                transit_time: zone.transit_time ?? null,
              });
            }
          });

          const mappedSurchargeIds = (service.surcharge_ids || [])
            .map((id) => surchargeIdMap.get(id) || id)
            .filter((id) => surchargesForMutation.some((s) => s.id === id));

          return {
            service_name: service.service_name || "",
            service_code: service.service_code || "",
            currency: service.currency || "USD",
            carrier_service_code: service.carrier_service_code,
            description: service.description,
            active: service.active,
            transit_days: service.transit_days,
            transit_time: service.transit_time,
            max_width: service.max_width,
            max_height: service.max_height,
            max_length: service.max_length,
            dimension_unit: service.dimension_unit,
            max_weight: service.max_weight,
            weight_unit: service.weight_unit,
            domicile: service.domicile,
            international: service.international,
            use_volumetric: service.use_volumetric,
            dim_factor: service.dim_factor,
            zone_ids: zoneIds,
            surcharge_ids: mappedSurchargeIds,
            features: featuresToObject(service.features),
          };
        });

        await mutations.createRateSheet.mutateAsync({
          name,
          carrier_name: carrierName,
          origin_countries: originCountries,
          services: createServices,
          zones: zonesForMutation,
          surcharges: surchargesForMutation,
          service_rates: serviceRates,
        } as any);

        toast({
          title: "Rate sheet created",
          description: `"${name}" has been created successfully`,
        });
      }

      onClose();
    } catch (error: any) {
      toast({
        title: isEditMode
          ? "Failed to update rate sheet"
          : "Failed to create rate sheet",
        description: error?.message || "An unexpected error occurred",
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <>
      <Sheet open={true} onOpenChange={() => onClose()}>
        <SheetContent side="right" className="w-full sm:max-w-full p-0">
          {/* Header */}
          <SheetHeader className="px-4 sm:px-6 py-4 border-b border-border bg-background">
            <div className="flex items-center justify-between gap-3">
              {/* Mobile sidebar toggle */}
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 -ml-2 text-muted-foreground hover:text-foreground hover:bg-accent rounded-md"
                aria-label={sidebarOpen ? "Close settings" : "Open settings"}
                disabled={isInitialLoading}
              >
                {sidebarOpen ? (
                  <Cross2Icon className="h-5 w-5" />
                ) : (
                  <HamburgerMenuIcon className="h-5 w-5" />
                )}
              </button>
              <SheetTitle className="text-lg sm:text-xl font-semibold flex-1">
                {isInitialLoading
                  ? "Loading..."
                  : isEditMode
                    ? "Edit Rate Sheet"
                    : "Create Rate Sheet"}
              </SheetTitle>
              <Button
                onClick={handleSave}
                disabled={isSaving || isInitialLoading}
                className="mr-12"
              >
                {isSaving ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    <span className="hidden sm:inline">Saving...</span>
                  </>
                ) : (
                  "Save"
                )}
              </Button>
            </div>
          </SheetHeader>

          {isInitialLoading ? (
            <div className="flex h-[calc(100vh-73px)] flex-col items-center justify-center gap-3 text-muted-foreground">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
              <p className="text-sm">Loading rate sheet...</p>
            </div>
          ) : (
            <div className="flex h-[calc(100vh-73px)] overflow-hidden relative">
              {/* Mobile sidebar overlay */}
              {sidebarOpen && (
                <div
                  className="fixed inset-0 bg-black/50 z-40 lg:hidden"
                  onClick={() => setSidebarOpen(false)}
                />
              )}

              {/* Left Sidebar */}
              <div
                className={cn(
                  "fixed lg:relative inset-y-0 left-0 z-50 lg:z-auto",
                  "w-full lg:w-80 border-r border-border bg-background lg:bg-muted/30 overflow-y-auto",
                  "transform transition-transform duration-200 ease-in-out lg:transform-none",
                  "top-[73px] lg:top-0 h-[calc(100vh-73px)]",
                  sidebarOpen
                    ? "translate-x-0"
                    : "-translate-x-full lg:translate-x-0"
                )}
              >
                <div className="p-4 sm:p-6 space-y-6">
                  {/* Carrier Selector */}
                  <div>
                    <Label className="mb-2 block">
                      Carrier <span className="text-destructive">*</span>
                    </Label>
                    <Select
                      value={carrierName}
                      onValueChange={setCarrierName}
                      disabled={isEditMode}
                    >
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder="Select a carrier" />
                      </SelectTrigger>
                      <SelectContent className="z-[100]">
                        {carriers.length > 0 ? (
                          carriers.map((carrier) => (
                            <SelectItem key={carrier.id} value={carrier.id}>
                              {carrier.name}
                            </SelectItem>
                          ))
                        ) : (
                          <div className="p-2 text-sm text-muted-foreground">
                            No carriers available
                          </div>
                        )}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Rate Sheet Name */}
                  <div>
                    <Label className="mb-2 block">
                      Rate Sheet Name <span className="text-destructive">*</span>
                    </Label>
                    <Input
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="e.g., Standard Rates 2024"
                    />
                  </div>

                  {/* Services Section */}
                  <div className="pt-4 border-t border-border">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <h3 className="text-sm font-semibold text-foreground">
                          Services
                        </h3>
                        <span className="text-xs text-muted-foreground">
                          ({services.length})
                        </span>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={handleAddService}
                        className="h-7 px-2"
                      >
                        <PlusIcon className="h-3 w-3 mr-1" />
                        Add
                      </Button>
                    </div>

                    {services.length > 0 ? (
                      <div className="space-y-2 mt-2 max-h-45 overflow-y-auto pr-1">
                        {services.map((service) => (
                          <div
                            key={service.service_code}
                            className="p-3 bg-background border border-border rounded-md hover:border-primary/50 transition-colors"
                          >
                            <div className="flex items-start justify-between gap-2">
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-foreground truncate">
                                  {service.service_name}
                                </p>
                                <p className="text-xs text-muted-foreground truncate">
                                  {service.service_code}
                                </p>
                                <p className="text-xs text-muted-foreground mt-1">
                                  {service.zones?.length || 0} zones
                                </p>
                              </div>
                              <div className="flex items-center gap-1">
                                <Button
                                  variant="ghost"
                                  size="icon"
                                  className="h-7 w-7"
                                  onClick={() => handleEditService(service)}
                                >
                                  <Pencil1Icon className="h-3.5 w-3.5" />
                                </Button>
                                <Button
                                  variant="ghost"
                                  size="icon"
                                  className="h-7 w-7 text-muted-foreground hover:text-destructive"
                                  onClick={() => handleDeleteClick(service)}
                                >
                                  <TrashIcon className="h-3.5 w-3.5" />
                                </Button>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="space-y-3">
                        <p className="text-xs text-muted-foreground text-center py-4">
                          No services added yet
                        </p>
                        {carrierName && (
                          <Button
                            variant="outline"
                            className="w-full"
                            onClick={handleLoadDefaults}
                            disabled={isLoadingDefaults}
                          >
                            {isLoadingDefaults ? (
                              <>
                                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                                Loading...
                              </>
                            ) : (
                              <>
                                Load{" "}
                                {carriers.find((c) => c.id === carrierName)
                                  ?.name || carrierName}{" "}
                                Defaults
                              </>
                            )}
                          </Button>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Connected Carriers */}
                  {isEditMode && connectedCarriers.length > 0 && (
                    <div className="pt-4 border-t border-border">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <h3 className="text-sm font-semibold text-foreground">
                            Connected Carriers
                          </h3>
                          <span className="text-xs text-muted-foreground">
                            ({connectedCarriers.length})
                          </span>
                        </div>
                      </div>
                      <div className="space-y-2 max-h-40 overflow-y-auto pr-1 pb-1">
                        {connectedCarriers.map((carrier) => (
                          <div
                            key={carrier.id}
                            className="p-3 bg-background border border-border rounded-md"
                          >
                            <div className="flex items-center justify-between gap-3">
                              <div className="min-w-0">
                                <p className="text-sm font-medium text-foreground truncate">
                                  {carrier.display_name || carrier.carrier_id}
                                </p>
                                <p className="text-xs text-muted-foreground truncate">
                                  {carrier.carrier_id}
                                </p>
                              </div>
                              <div className="flex items-center gap-1 flex-shrink-0">
                                <span
                                  className={`px-2 py-0.5 rounded text-xs ${carrier.active ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}
                                >
                                  {carrier.active ? "Active" : "Inactive"}
                                </span>
                                <span
                                  className={`px-2 py-0.5 rounded text-xs ${carrier.test_mode ? "bg-yellow-100 text-yellow-700" : "bg-blue-100 text-blue-700"}`}
                                >
                                  {carrier.test_mode ? "Test" : "Live"}
                                </span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Default Settings */}
                  <div className="space-y-3 pt-4 border-t border-border">
                    <h3 className="text-sm font-semibold text-foreground">
                      Default Settings
                    </h3>

                    <div>
                      <Label className="text-xs mb-1 block">Currency</Label>
                      <Select
                        value={selectedCurrency}
                        onValueChange={(value) => {
                          setServices((prev) =>
                            prev.map((service) => ({
                              ...service,
                              currency: value,
                            }))
                          );
                        }}
                        disabled={services.length === 0}
                      >
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Select currency" />
                        </SelectTrigger>
                        <SelectContent className="z-[100] max-h-60">
                          {currencyOptions.map((code) => (
                            <SelectItem key={code} value={code}>
                              {code}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label className="text-xs mb-1 block">Origin Countries</Label>
                      <MultiSelect
                        options={countryOptions}
                        value={originCountries}
                        onValueChange={setOriginCountries}
                        placeholder="Select countries..."
                      />
                    </div>

                    <div>
                      <Label className="text-xs mb-1 block">Weight Unit</Label>
                      <Select
                        value={selectedWeightUnit}
                        onValueChange={(value) => {
                          setServices((prev) =>
                            prev.map((service) => ({
                              ...service,
                              weight_unit: value,
                            }))
                          );
                        }}
                        disabled={services.length === 0}
                      >
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Select weight unit" />
                        </SelectTrigger>
                        <SelectContent className="z-[100]">
                          {weightUnitOptions.map((unit) => (
                            <SelectItem key={unit} value={unit}>
                              {unit}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label className="text-xs mb-1 block">Dimension Unit</Label>
                      <Select
                        value={selectedDimensionUnit}
                        onValueChange={(value) => {
                          setServices((prev) =>
                            prev.map((service) => ({
                              ...service,
                              dimension_unit: value,
                            }))
                          );
                        }}
                        disabled={services.length === 0}
                      >
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Select dimension unit" />
                        </SelectTrigger>
                        <SelectContent className="z-[100]">
                          {dimensionUnitOptions.map((unit) => (
                            <SelectItem key={unit} value={unit}>
                              {unit}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </div>
              </div>

              {/* Main Content Area */}
              <div className="flex-1 flex flex-col overflow-hidden bg-background w-full lg:w-auto">
                {/* Tab Navigation */}
                <div className="border-b border-border px-4 sm:px-6 overflow-x-auto">
                  <div className="flex items-center min-w-min">
                    {(
                      [
                        { id: "rate_sheet", label: "Rate Sheet" },
                        { id: "zones", label: "Zones" },
                        { id: "services", label: "Services" },
                        { id: "surcharges", label: "Surcharges" },
                      ] as const
                    ).map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={cn(
                          "flex-1 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap px-2",
                          activeTab === tab.id
                            ? "border-primary text-primary"
                            : "border-transparent text-muted-foreground hover:text-foreground"
                        )}
                      >
                        {tab.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Tab Content */}
                <div className="flex-1 p-4 sm:p-6 overflow-hidden">
                  {activeTab === "rate_sheet" && (
                    <RateSheetTable
                      services={services}
                      sharedZonesFromParent={sharedZones}
                      onUpdateService={handleUpdateService}
                      onAddZone={handleAddZoneAll}
                      onRemoveZone={handleRemoveZoneAll}
                    />
                  )}
                  {activeTab === "zones" && (
                    <ZonesTab
                      services={services}
                      sharedZonesFromParent={sharedZones}
                      onUpdateZone={handleUpdateZone}
                      onAddZone={handleAddZoneAll}
                      onRemoveZone={handleRemoveZoneAll}
                      countryOptions={countryOptions}
                      getZoneTextValue={getZoneTextValue}
                      setZoneTextValue={setZoneTextValue}
                      persistZoneTextValue={persistZoneTextValue}
                    />
                  )}
                  {activeTab === "services" && (
                    <ServicesTab
                      services={services}
                      onEditService={handleEditService}
                      onDeleteService={handleDeleteClick}
                    />
                  )}
                  {activeTab === "surcharges" && (
                    <SurchargesTab
                      surcharges={surcharges}
                      services={services}
                      onUpdateSurcharge={handleUpdateSurcharge}
                      onAddSurcharge={handleAddSurcharge}
                      onRemoveSurcharge={handleRemoveSurcharge}
                      onToggleServiceSurcharge={handleToggleServiceSurcharge}
                    />
                  )}
                </div>
              </div>
            </div>
          )}
        </SheetContent>
      </Sheet>

      {/* Service Editor Modal */}
      <ServiceEditorModal
        isOpen={serviceDialogOpen}
        onClose={() => setServiceDialogOpen(false)}
        service={selectedService}
        onSubmit={handleSaveService}
        availableSurcharges={surcharges}
      />

      {/* Delete Service Confirmation Dialog */}
      <AlertDialog open={deleteConfirmOpen} onOpenChange={setDeleteConfirmOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Service</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete "{serviceToDelete?.service_name}"?
              This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isDeletingService}>
              Cancel
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={handleConfirmDelete}
              disabled={isDeletingService}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              {isDeletingService ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  Deleting...
                </>
              ) : (
                "Delete"
              )}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Delete Zone Confirmation Dialog */}
      <AlertDialog
        open={deleteZoneConfirmOpen}
        onOpenChange={setDeleteZoneConfirmOpen}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Zone</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete "{zoneToDeleteLabel}"? This will
              remove it from all services. This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleConfirmRemoveZone}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
};

export default RateSheetEditor;
