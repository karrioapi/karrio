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
import { deriveWeightRanges, type WeightRange, type ServiceRate } from "@karrio/ui/components/weight-rate-grid";
import { ServiceRateDetailView } from "@karrio/ui/components/service-rate-detail-view";
import { AddWeightRangeDialog } from "@karrio/ui/components/add-weight-range-dialog";
import { AddServicePopover } from "@karrio/ui/components/add-service-popover";
import { EditWeightRangeDialog } from "@karrio/ui/components/edit-weight-range-dialog";
import { SurchargesTab } from "@karrio/ui/components/surcharges-tab";
import { MarkupsTab } from "@karrio/ui/components/markups-tab";
import { ZoneEditorDialog } from "@karrio/ui/components/zone-editor-dialog";
import { SurchargeEditorDialog } from "@karrio/ui/components/surcharge-editor-dialog";
import { MarkupEditorDialog } from "@karrio/ui/components/markup-editor-dialog";
import { ServiceRateEditorDialog } from "@karrio/ui/components/service-rate-editor-dialog";
import { RateSheetCsvPreview, type MarkupPreviewItem } from "@karrio/ui/components/rate-sheet-csv-preview";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import type { MarkupType } from "@karrio/hooks/admin-markups";
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
  TableIcon,
} from "@radix-ui/react-icons";
import { Loader2, Save } from "lucide-react";

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
  return Object.fromEntries(features.map(feature => [feature, true]));
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
  markups?: MarkupType[];
  markupMutations?: {
    createMarkup: { mutateAsync: (input: any) => Promise<any> };
    updateMarkup: { mutateAsync: (input: any) => Promise<any> };
    deleteMarkup: { mutateAsync: (input: any) => Promise<any> };
  };
}

interface OriginalState {
  name: string;
  zones: Map<string, EmbeddedZone>;
  surcharges: Map<string, SharedSurcharge>;
  serviceRates: Map<string, { rate: number; cost?: number | null }>;
  serviceZoneIds: Map<string, string[]>;
  serviceSurchargeIds: Map<string, string[]>;
  serviceFields: Map<string, Record<string, any>>;
}

export const RateSheetEditor = ({
  rateSheetId,
  onClose,
  preloadCarrier,
  linkConnectionId,
  isAdmin = false,
  useRateSheet,
  useRateSheetMutation,
  markups: adminMarkups = [],
  markupMutations,
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
  const [localServiceRates, setLocalServiceRates] = useState<ServiceRate[]>([]);
  // Optimistic overlay for edit mode: when set, overrides existingRateSheet.service_rates
  const [editModeRatesOverride, setEditModeRatesOverride] = useState<ServiceRate[] | null>(null);

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
  const [isDeletingService, setIsDeletingService] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Tab state
  const [activeTab, setActiveTab] = useState<
    "rate_sheet" | "surcharges" | "markups"
  >("rate_sheet");

  // Weight range state
  const [weightRangeDialogOpen, setWeightRangeDialogOpen] = useState(false);
  const [detailServiceId, setDetailServiceId] = useState<string | null>(null);
  const [removeWeightRangeConfirmOpen, setRemoveWeightRangeConfirmOpen] = useState(false);
  const [weightRangeToRemove, setWeightRangeToRemove] = useState<{ min_weight: number; max_weight: number } | null>(null);

  // Mobile sidebar state
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Zone editor dialog state
  const [zoneEditorOpen, setZoneEditorOpen] = useState(false);
  const [selectedZone, setSelectedZone] = useState<EmbeddedZone | null>(null);

  // Surcharge editor dialog state
  const [surchargeEditorOpen, setSurchargeEditorOpen] = useState(false);
  const [selectedSurcharge, setSelectedSurcharge] = useState<SharedSurcharge | null>(null);

  // Markup editor dialog state
  const [markupEditorOpen, setMarkupEditorOpen] = useState(false);
  const [selectedMarkup, setSelectedMarkup] = useState<MarkupType | null>(null);
  const [isNewMarkup, setIsNewMarkup] = useState(false);

  // Service rate editor dialog state
  const [rateEditorOpen, setRateEditorOpen] = useState(false);
  const [selectedRate, setSelectedRate] = useState<ServiceRate | null>(null);

  // CSV preview state
  const [csvPreviewOpen, setCsvPreviewOpen] = useState(false);

  // Service add popover state
  const [serviceAddPopoverOpen, setServiceAddPopoverOpen] = useState(false);

  // Edit weight range dialog state
  const [editWeightRangeDialogOpen, setEditWeightRangeDialogOpen] = useState(false);
  const [weightRangeToEdit, setWeightRangeToEdit] = useState<WeightRange | null>(null);

  // Staged/committed pattern refs
  const zoneSaveRef = useRef(false);
  const surchargeSaveRef = useRef(false);
  const [pendingZoneServiceId, setPendingZoneServiceId] = useState<string | null>(null);

  // Pending service rates for staged clone/preset services (cleared on save or cancel)
  const [pendingServiceRates, setPendingServiceRates] = useState<ServiceRate[]>([]);

  // Per-service pending weight ranges (edit mode)
  const [editModePendingRanges, setEditModePendingRanges] = useState<Record<string, WeightRange[]>>({});

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

  const servicePresets = useMemo(() => {
    if (!carrierName || !references?.ratesheets?.[carrierName]?.services) return [];
    const existingCodes = new Set(services.map(s => s.service_code));
    return references.ratesheets[carrierName].services
      .filter((s: any) => !existingCodes.has(s.service_code))
      .map((s: any) => ({ code: s.service_code, name: s.service_name }))
      .sort((a: any, b: any) => a.name.localeCompare(b.name));
  }, [carrierName, references?.ratesheets, services]);

  const zonePresets = useMemo(() => {
    if (!carrierName || !references?.ratesheets?.[carrierName]?.zones) return [];
    const existingLabels = new Set(sharedZones.map(z => z.label));
    return references.ratesheets[carrierName].zones
      .filter((z: any) => z.label && !existingLabels.has(z.label))
      .map((z: any) => ({ id: z.id, label: z.label, countries: (z.country_codes || []).length }))
      .sort((a: any, b: any) => a.label.localeCompare(b.label));
  }, [carrierName, references?.ratesheets, sharedZones]);

  const surchargePresets = useMemo(() => {
    if (!carrierName || !references?.ratesheets?.[carrierName]?.surcharges) return [];
    const existingNames = new Set(surcharges.map(s => s.name));
    return references.ratesheets[carrierName].surcharges
      .filter((s: any) => s.name && !existingNames.has(s.name))
      .map((s: any) => ({ id: s.id, name: s.name, amount: s.amount, surcharge_type: s.surcharge_type }))
      .sort((a: any, b: any) => a.name.localeCompare(b.name));
  }, [carrierName, references?.ratesheets, surcharges]);

  const isInitialLoading = isEditMode && isRateSheetLoading && !existingRateSheet;

  // Auto-select first service tab when services change
  useEffect(() => {
    if (services.length > 0) {
      const exists = detailServiceId && services.some(s => s.id === detailServiceId);
      if (!exists) setDetailServiceId(services[0].id);
    } else {
      setDetailServiceId(null);
    }
  }, [services]);

  // Clear optimistic overlay when server data refreshes (after mutation + refetch)
  useEffect(() => {
    if (editModeRatesOverride !== null) {
      setEditModeRatesOverride(null);
    }
  }, [(existingRateSheet as any)?.service_rates]);

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

      // Store ALL zones in sharedZones so ServiceRateDetailView can find them via zone_ids
      const allZones: EmbeddedZone[] = existingSharedZones.map((zone: any) => ({
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
      setSharedZones(allZones);
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
      const originalServiceFields = new Map<string, Record<string, any>>();
      rawServices.forEach((s: any) => {
        originalServiceZoneIds.set(s.id, [...(s.zone_ids || [])]);
        originalServiceSurchargeIds.set(s.id, [...(s.surcharge_ids || [])]);
        originalServiceFields.set(s.id, {
          service_name: s.service_name,
          service_code: s.service_code,
          currency: s.currency,
          active: s.active,
          transit_days: s.transit_days,
          description: s.description,
          features: s.features,
        });
      });

      originalStateRef.current = {
        name: existingRateSheet.name || "",
        zones: originalZones,
        surcharges: originalSurcharges,
        serviceRates: originalServiceRates,
        serviceZoneIds: originalServiceZoneIds,
        serviceSurchargeIds: originalServiceSurchargeIds,
        serviceFields: originalServiceFields,
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
      setLocalServiceRates([]);
      originalStateRef.current = null;
    }
  }, [isEditMode, preloadCarrier, carriers]);

  // Track previous carrier to detect changes
  const prevCarrierRef = useRef<string>("");

  // Auto-load carrier defaults when carrier changes in create mode
  useEffect(() => {
    if (!isEditMode && carrierName) {
      const carrier = carriers.find((c) => c.id === carrierName);
      if (carrier) {
        setName(`${carrier.name} - sheet`);
      }

      if (prevCarrierRef.current !== carrierName) {
        const rateSheetDefaults = references?.ratesheets?.[carrierName];

        if (rateSheetDefaults?.services?.length > 0) {
          const {
            zones: defaultZones,
            services: defaultServicesList,
            surcharges: defaultSurcharges,
            service_rates: defaultServiceRates,
          } = rateSheetDefaults;

          const zoneMap = new Map(
            (defaultZones || []).map((z: any) => [z.id, z])
          );

          // Build a lookup from reference service_rates: "refServiceId:zoneId" → rate data
          const defaultRateLookup = new Map<string, { rate: number; cost: number | null }>();
          for (const sr of (defaultServiceRates || []) as any[]) {
            const key = `${sr.service_id}:${sr.zone_id}:${sr.min_weight ?? 0}:${sr.max_weight ?? 0}`;
            defaultRateLookup.set(key, { rate: sr.rate ?? 0, cost: sr.cost ?? null });
          }

          const loadedSharedZones: EmbeddedZone[] = (defaultZones || []).map(
            (zone: any) => ({
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
            })
          );

          const loadedSurcharges: SharedSurcharge[] = (
            defaultSurcharges || []
          ).map((s: any) => ({
            id: s.id || generateId("surcharge"),
            name: s.name || "",
            amount: s.amount ?? 0,
            surcharge_type: s.surcharge_type || "fixed",
            cost: s.cost ?? null,
            active: s.active ?? true,
          }));

          // Map reference service IDs → generated IDs, and collect service rates
          const mappedServiceRates: ServiceRate[] = [];

          const defaultServices: ServiceLevelWithZones[] =
            defaultServicesList.map((service: any) => {
              const generatedId = generateId("service");
              const refServiceId = service.id; // reference ID (e.g. "0", "1")
              const zoneIds = service.zone_ids || [];
              const zones = zoneIds.map(
                (zoneId: string, zoneIndex: number) => {
                  const zone = zoneMap.get(zoneId) || {
                    label: `Zone ${zoneIndex + 1}`,
                  };
                  // Look up default rate for this service+zone
                  const rateData = defaultRateLookup.get(
                    `${refServiceId}:${zoneId}:0:0`
                  );
                  return {
                    id: zoneId,
                    label: zone.label || `Zone ${zoneIndex + 1}`,
                    rate: rateData?.rate ?? 0,
                    cost: rateData?.cost ?? null,
                    min_weight: zone.min_weight ?? null,
                    max_weight: zone.max_weight ?? null,
                    weight_unit: zone.weight_unit ?? null,
                    transit_days: zone.transit_days ?? null,
                    transit_time: zone.transit_time ?? null,
                    country_codes: zone.country_codes || [],
                    postal_codes: zone.postal_codes || [],
                    cities: zone.cities || [],
                  } as EmbeddedZone;
                }
              );

              // Build mapped service rates for the grid (re-keyed to generated service ID)
              for (const sr of (defaultServiceRates || []) as any[]) {
                if (String(sr.service_id) === String(refServiceId)) {
                  mappedServiceRates.push({
                    service_id: generatedId,
                    zone_id: sr.zone_id,
                    rate: sr.rate ?? 0,
                    cost: sr.cost ?? null,
                    min_weight: sr.min_weight ?? null,
                    max_weight: sr.max_weight ?? null,
                  });
                }
              }

              return {
                id: generatedId,
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
                zones,
                zone_ids: zoneIds,
                surcharge_ids: service.surcharge_ids || [],
                features: featuresToArray(service.features),
                ...(service.features
                  ? {
                      first_mile: service.features.first_mile || "",
                      last_mile: service.features.last_mile || "",
                      form_factor: service.features.form_factor || "",
                      age_check: service.features.age_check || "",
                    }
                  : {}),
              } as ServiceLevelWithZones;
            });

          setServices(defaultServices);
          setSharedZones(loadedSharedZones);
          setSurcharges(loadedSurcharges);
          setLocalServiceRates(mappedServiceRates);
        } else {
          setServices([]);
          setSharedZones([]);
          setSurcharges([]);
          setLocalServiceRates([]);
        }
      }
    }
    prevCarrierRef.current = carrierName;
  }, [carrierName, isEditMode, carriers]);

  // Handler functions
  const handleAddService = () => {
    setSelectedService(null);
    setServiceDialogOpen(true);
  };

  const handleAddServiceFromPreset = (serviceCode: string) => {
    if (!carrierName || !references?.ratesheets?.[carrierName]) return;

    const rateSheetDefaults = references.ratesheets[carrierName];
    const preset = (rateSheetDefaults.services || []).find(
      (s: any) => s.service_code === serviceCode
    );
    if (!preset) return;

    const generatedId = generateId("service");
    const refServiceId = preset.id;
    const zoneIds = preset.zone_ids || [];

    // Look up default rates for this service's zones
    const defaultServiceRates = (rateSheetDefaults.service_rates || []) as any[];
    const zones = zoneIds
      .map((zid: string) => {
        const zone = sharedZones.find((z) => z.id === zid);
        if (!zone) return null;
        const rateEntry = defaultServiceRates.find(
          (sr: any) =>
            String(sr.service_id) === String(refServiceId) &&
            sr.zone_id === zid
        );
        return {
          ...zone,
          rate: rateEntry?.rate ?? 0,
          cost: rateEntry?.cost ?? null,
        };
      })
      .filter(Boolean) as EmbeddedZone[];

    // Build service rates for the grid
    const newRates: ServiceRate[] = defaultServiceRates
      .filter((sr: any) => String(sr.service_id) === String(refServiceId))
      .map((sr: any) => ({
        service_id: generatedId,
        zone_id: sr.zone_id,
        rate: sr.rate ?? 0,
        cost: sr.cost ?? null,
        min_weight: sr.min_weight ?? null,
        max_weight: sr.max_weight ?? null,
      }));

    const newService: ServiceLevelWithZones = {
      id: generatedId,
      object_type: "service_level",
      service_name: preset.service_name || "",
      service_code: preset.service_code || "",
      carrier_service_code: preset.carrier_service_code ?? null,
      description: preset.description ?? null,
      active: preset.active ?? true,
      currency: preset.currency ?? "USD",
      transit_days: preset.transit_days ?? null,
      transit_time: preset.transit_time ?? null,
      max_width: preset.max_width ?? null,
      max_height: preset.max_height ?? null,
      max_length: preset.max_length ?? null,
      dimension_unit: preset.dimension_unit ?? null,
      max_weight: preset.max_weight ?? null,
      weight_unit: preset.weight_unit ?? null,
      domicile: preset.domicile ?? null,
      international: preset.international ?? null,
      zones,
      zone_ids: zoneIds,
      surcharge_ids: preset.surcharge_ids || [],
      features: featuresToArray(preset.features),
      ...(preset.features
        ? {
            first_mile: preset.features.first_mile || "",
            last_mile: preset.features.last_mile || "",
            form_factor: preset.features.form_factor || "",
            age_check: preset.features.age_check || "",
          }
        : {}),
    };
    // Stage — don't add to services yet, add on dialog save
    setPendingServiceRates(newRates);
    setSelectedService(newService);
    setServiceDialogOpen(true);
    setServiceAddPopoverOpen(false);
  };

  const handleAddZoneFromPreset = (presetZoneId: string) => {
    if (!carrierName || !references?.ratesheets?.[carrierName]) return;
    const rateSheetDefaults = references.ratesheets[carrierName];
    const preset = (rateSheetDefaults.zones || []).find((z: any) => z.id === presetZoneId);
    if (!preset) return;

    const newZone: EmbeddedZone = {
      id: generateId("zone"),
      rate: 0,
      label: preset.label || "",
      min_weight: null,
      max_weight: null,
      weight_unit: null,
      transit_days: preset.transit_days ?? null,
      transit_time: null,
      cities: preset.cities || [],
      postal_codes: preset.postal_codes || [],
      country_codes: preset.country_codes || [],
    };

    // Staged: don't add to state yet, just open dialog. handleSaveZone adds on save.
    setSelectedZone(newZone);
    setZoneEditorOpen(true);
  };

  const handleAddSurchargeFromPreset = (presetSurchargeId: string) => {
    if (!carrierName || !references?.ratesheets?.[carrierName]) return;
    const rateSheetDefaults = references.ratesheets[carrierName];
    const preset = (rateSheetDefaults.surcharges || []).find((s: any) => s.id === presetSurchargeId);
    if (!preset) return;

    const newSurcharge: SharedSurcharge = {
      id: generateId("surcharge"),
      name: preset.name || "",
      amount: preset.amount ?? 0,
      surcharge_type: preset.surcharge_type || "fixed",
      active: true,
      cost: preset.cost ?? null,
    };

    // Staged: don't add to state yet, just open dialog. handleSaveSurcharge adds on save.
    setSelectedSurcharge(newSurcharge);
    setSurchargeEditorOpen(true);
  };

  const handleCloneZone = (zone: EmbeddedZone) => {
    const newZone: EmbeddedZone = {
      ...zone,
      id: generateId("zone"),
      label: `${zone.label} (copy)`,
    };
    // Staged: don't add to state yet, just open dialog. handleSaveZone adds on save.
    setSelectedZone(newZone);
    setZoneEditorOpen(true);
  };

  const handleCloneSurcharge = (surcharge: SharedSurcharge) => {
    const newSurcharge: SharedSurcharge = {
      ...surcharge,
      id: generateId("surcharge"),
      name: `${surcharge.name} (copy)`,
    };
    // Staged: don't add to state yet, just open dialog. handleSaveSurcharge adds on save.
    setSelectedSurcharge(newSurcharge);
    setSurchargeEditorOpen(true);
  };

  const handleCloneService = (service: ServiceLevelWithZones) => {
    const newId = generateId("service");
    const newService: ServiceLevelWithZones = {
      ...service,
      id: newId,
      service_name: `${service.service_name} (copy)`,
    };
    // Clone rates from serviceRatesData (includes overlay in edit mode)
    const clonedRates = serviceRatesData
      .filter(sr => sr.service_id === service.id)
      .map(sr => ({ ...sr, service_id: newId }));
    // Stage — don't add to services yet, add on dialog save
    setPendingServiceRates(clonedRates);
    setSelectedService(newService);
    setServiceDialogOpen(true);
  };

  const handleEditService = (service: ServiceLevelWithZones) => {
    setSelectedService(service);
    setServiceDialogOpen(true);
  };

  const handleSaveService = (serviceData: Partial<ServiceLevelWithZones>) => {
    const isExistingInList = selectedService && services.some(s => s.id === selectedService.id);

    if (selectedService && isExistingInList) {
      // Path 1: Edit existing service in list — match by id
      setServices((prev) =>
        prev.map((s) =>
          s.id === selectedService.id
            ? { ...s, ...serviceData }
            : s
        )
      );
    } else if (selectedService) {
      // Path 2: New from clone/preset — add to list now
      const merged = { ...selectedService, ...serviceData };
      setServices((prev) => [...prev, merged]);
      setDetailServiceId(merged.id); // Select new tab

      // Apply pending rates (from clone or preset)
      if (pendingServiceRates.length > 0) {
        if (isEditMode) {
          setEditModeRatesOverride((prev) => {
            const base = prev ?? (((existingRateSheet as any)?.service_rates ?? []) as ServiceRate[]);
            return [...base, ...pendingServiceRates];
          });
        } else {
          setLocalServiceRates((prev) => [...prev, ...pendingServiceRates]);
        }
        setPendingServiceRates([]);
      }
    } else {
      // Path 3: Brand new service
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
      setDetailServiceId(newService.id); // Select new tab
    }
    setServiceDialogOpen(false);
    setSelectedService(null);
    setPendingServiceRates([]);
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
      const isBackendService = isEditMode &&
        originalStateRef.current?.serviceFields?.has(serviceToDelete.id);

      if (isBackendService && rateSheetId && mutations.deleteRateSheetService) {
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
        prev.filter((s) => s.id !== serviceToDelete.id)
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

    // Staged: don't add to state yet, just open dialog. handleSaveZone adds on save.
    setSelectedZone(newZone);
    setZoneEditorOpen(true);
  };

  // Assign an existing shared zone to a service
  const handleAssignZoneToService = (serviceId: string, zoneId: string) => {
    const zone = sharedZones.find((z) => z.id === zoneId);
    if (!zone) return;

    setServices((prev) =>
      prev.map((service) => {
        if (service.id !== serviceId) return service;
        const currentZoneIds: string[] = service.zone_ids || [];
        if (currentZoneIds.includes(zoneId)) return service;
        return {
          ...service,
          zones: [...(service.zones || []), zone],
          zone_ids: [...currentZoneIds, zoneId],
        };
      })
    );
  };

  // Create a new zone for a service and open the editor (staged pattern)
  const handleCreateZoneForService = (serviceId: string) => {
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

    // Staged: track which service to link on save, don't add to state yet
    setPendingZoneServiceId(serviceId);
    setSelectedZone(newZone);
    setZoneEditorOpen(true);
  };

  // Remove a zone from a specific service (unlink)
  const handleRemoveZoneFromService = (serviceId: string, zoneId: string) => {
    setServices((prev) =>
      prev.map((service) => {
        if (service.id !== serviceId) return service;
        return {
          ...service,
          zones: (service.zones || []).filter((z) => z.id !== zoneId),
          zone_ids: (service.zone_ids || []).filter((id) => id !== zoneId),
        };
      })
    );
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

  // Zone/Surcharge editor helpers
  const handleEditZone = (zone: EmbeddedZone) => {
    setSelectedZone(zone);
    setZoneEditorOpen(true);
  };

  const handleEditSurcharge = (surcharge: SharedSurcharge) => {
    setSelectedSurcharge(surcharge);
    setSurchargeEditorOpen(true);
  };

  // Save zone from dialog — sets save ref so onOpenChange knows it's a save, not cancel
  const handleSaveZone = (zoneKey: string, updates: Partial<EmbeddedZone>) => {
    zoneSaveRef.current = true;
    const isExistingInList = selectedZone && sharedZones.some((z) => z.id === selectedZone.id);

    if (selectedZone && isExistingInList) {
      // Edit existing zone
      handleUpdateZone(zoneKey, updates);
    } else if (selectedZone) {
      // New staged zone — add to sharedZones now
      const newZone = { ...selectedZone, ...updates };
      setSharedZones((prev) => {
        if (prev.some((z) => z.id === newZone.id)) return prev;
        return [...prev, newZone];
      });

      // If created for a specific service, link it
      if (pendingZoneServiceId) {
        setServices((prev) =>
          prev.map((service) => {
            if (service.id !== pendingZoneServiceId) return service;
            const currentZoneIds: string[] = service.zone_ids || [];
            if (currentZoneIds.includes(newZone.id)) return service;
            return {
              ...service,
              zones: [...(service.zones || []), newZone],
              zone_ids: [...currentZoneIds, newZone.id],
            };
          })
        );
      }
    }
  };

  // Save surcharge from dialog — sets save ref so onOpenChange knows it's a save, not cancel
  const handleSaveSurcharge = (surchargeId: string, updates: Partial<SharedSurcharge>) => {
    surchargeSaveRef.current = true;
    const isExistingInList = selectedSurcharge && surcharges.some((s) => s.id === selectedSurcharge.id);

    if (selectedSurcharge && isExistingInList) {
      // Edit existing surcharge
      handleUpdateSurcharge(surchargeId, updates);
    } else if (selectedSurcharge) {
      // New staged surcharge — add to surcharges now
      const newSurcharge = { ...selectedSurcharge, ...updates };
      setSurcharges((prev) => {
        if (prev.some((s) => s.id === newSurcharge.id)) return prev;
        return [...prev, newSurcharge];
      });
    }
  };

  // Service rate editor
  const handleEditRate = (serviceRate: ServiceRate) => {
    setSelectedRate(serviceRate);
    setRateEditorOpen(true);
  };

  const handleSaveRate = async (updated: ServiceRate) => {
    if (!isEditMode) return;
    try {
      await mutations.updateServiceRate.mutateAsync({
        rate_sheet_id: rateSheetId,
        service_id: updated.service_id,
        zone_id: updated.zone_id,
        rate: updated.rate,
        cost: updated.cost,
        min_weight: updated.min_weight ?? 0,
        max_weight: updated.max_weight ?? 0,
        transit_days: updated.transit_days,
        transit_time: updated.transit_time,
      });
    } catch (err: any) {
      toast({
        title: "Failed to update rate",
        description: err?.message,
        variant: "destructive",
      });
    }
  };

  // Toggle service-zone linking
  const handleToggleServiceZone = (
    serviceId: string,
    zoneId: string,
    linked: boolean
  ) => {
    setServices((prev) =>
      prev.map((service) => {
        if (service.id !== serviceId) return service;
        const currentZones = service.zones || [];
        const currentZoneIds = service.zone_ids || [];
        if (linked) {
          const zone = sharedZones.find((z) => z.id === zoneId) ||
            services.flatMap((s) => s.zones || []).find((z) => z.id === zoneId) ||
            (selectedZone?.id === zoneId ? selectedZone : undefined);
          if (!zone) return service;
          if (currentZoneIds.includes(zoneId)) return service;
          return {
            ...service,
            zones: [...currentZones, zone],
            zone_ids: [...currentZoneIds, zoneId],
          };
        } else {
          return {
            ...service,
            zones: currentZones.filter((z) => z.id !== zoneId),
            zone_ids: currentZoneIds.filter((id) => id !== zoneId),
          };
        }
      })
    );
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
    // Staged: don't add to state yet, just open dialog. handleSaveSurcharge adds on save.
    setSelectedSurcharge(newSurcharge);
    setSurchargeEditorOpen(true);
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

  // ─────────────────────────────────────────────────────────────────
  // Markup Handlers (admin mode only)
  // ─────────────────────────────────────────────────────────────────

  const handleAddMarkup = () => {
    setSelectedMarkup(null);
    setIsNewMarkup(true);
    setMarkupEditorOpen(true);
  };

  const handleEditMarkup = (markup: MarkupType) => {
    setSelectedMarkup(markup);
    setIsNewMarkup(false);
    setMarkupEditorOpen(true);
  };

  const handleRemoveMarkup = async (markupId: string) => {
    if (!markupMutations) return;
    try {
      await markupMutations.deleteMarkup.mutateAsync({ id: markupId });
      toast({ title: "Markup deleted" });
    } catch (err: any) {
      toast({ title: "Failed to delete markup", description: err?.message, variant: "destructive" });
    }
  };

  const markupsForPreview: MarkupPreviewItem[] = useMemo(() => {
    return adminMarkups.map((m: any) => ({
      id: m.id,
      name: m.name,
      amount: m.amount,
      markup_type: m.markup_type,
      active: m.active,
      meta: m.meta,
    }));
  }, [adminMarkups]);

  // ─────────────────────────────────────────────────────────────────
  // Weight Range Handlers
  // ─────────────────────────────────────────────────────────────────

  const serviceRatesData: ServiceRate[] = useMemo(
    () =>
      isEditMode
        ? ((editModeRatesOverride ?? ((existingRateSheet as any)?.service_rates ?? [])) as ServiceRate[])
        : localServiceRates,
    [isEditMode, editModeRatesOverride, (existingRateSheet as any)?.service_rates, localServiceRates]
  );
  const weightRanges: WeightRange[] = useMemo(
    () => deriveWeightRanges(serviceRatesData),
    [serviceRatesData]
  );

  const weightRangePresets = useMemo(() => {
    if (!carrierName || !references?.ratesheets?.[carrierName]?.service_rates) return [];
    const rates = references.ratesheets[carrierName].service_rates as any[];
    const existingSet = new Set(weightRanges.map(r => `${r.min_weight}:${r.max_weight}`));
    // Also exclude locally-pending ranges for the current service
    const pendingForService = detailServiceId ? (editModePendingRanges[detailServiceId] || []) : [];
    for (const pr of pendingForService) {
      existingSet.add(`${pr.min_weight}:${pr.max_weight}`);
    }
    const seen = new Set<string>();
    const presets: { min_weight: number; max_weight: number }[] = [];
    for (const sr of rates) {
      if (sr.min_weight == null || sr.max_weight == null) continue;
      const key = `${sr.min_weight}:${sr.max_weight}`;
      if (seen.has(key) || existingSet.has(key)) continue;
      seen.add(key);
      presets.push({ min_weight: sr.min_weight, max_weight: sr.max_weight });
    }
    return presets.sort((a, b) => a.min_weight - b.min_weight || a.max_weight - b.max_weight);
  }, [carrierName, references?.ratesheets, weightRanges, detailServiceId, editModePendingRanges]);

  // Per-service weight range functions
  const getServiceWeightRanges = useCallback((serviceId: string): WeightRange[] => {
    // Get weight ranges that have rates for this specific service
    const serviceSpecificRates = serviceRatesData.filter(
      (sr) => sr.service_id === serviceId
    );
    const seen = new Set<string>();
    const ranges: WeightRange[] = [];
    for (const sr of serviceSpecificRates) {
      const min = sr.min_weight ?? 0;
      const max = sr.max_weight ?? 0;
      if (min === 0 && max === 0) continue;
      const key = `${min}:${max}`;
      if (!seen.has(key)) {
        seen.add(key);
        ranges.push({ min_weight: min, max_weight: max });
      }
    }
    // Include edit-mode pending ranges
    const pending = editModePendingRanges[serviceId] || [];
    for (const wr of pending) {
      const key = `${wr.min_weight}:${wr.max_weight}`;
      if (!seen.has(key)) {
        seen.add(key);
        ranges.push(wr);
      }
    }
    return ranges.sort((a, b) => a.min_weight - b.min_weight);
  }, [serviceRatesData, editModePendingRanges]);

  const getMissingWeightRanges = useCallback((serviceId: string): WeightRange[] => {
    const serviceRanges = getServiceWeightRanges(serviceId);
    const serviceRangeKeys = new Set(
      serviceRanges.map((r) => `${r.min_weight}:${r.max_weight}`)
    );
    return weightRanges.filter(
      (r) => !serviceRangeKeys.has(`${r.min_weight}:${r.max_weight}`)
    );
  }, [weightRanges, getServiceWeightRanges]);

  // Edit weight range handler
  const handleEditWeightRange = (range: WeightRange) => {
    setWeightRangeToEdit(range);
    setEditWeightRangeDialogOpen(true);
  };

  const handleSaveWeightRangeEdit = (oldMin: number, oldMax: number, newMax: number) => {
    if (isEditMode && rateSheetId && detailServiceId) {
      // Check if this is a locally-pending range (no backend rates)
      const hasBackendRates = serviceRatesData.some(
        (r) => r.min_weight === oldMin && r.max_weight === oldMax
      );

      if (hasBackendRates) {
        // Per-service: find rates for current service + old weight range
        const oldRates = serviceRatesData.filter(
          (r) =>
            r.service_id === detailServiceId &&
            r.min_weight === oldMin &&
            r.max_weight === oldMax
        );
        // Optimistic update: re-key only this service's rates
        setEditModeRatesOverride((prev) => {
          const rates = prev ?? (((existingRateSheet as any)?.service_rates ?? []) as ServiceRate[]);
          return rates.map((r) =>
            r.service_id === detailServiceId &&
            r.min_weight === oldMin &&
            r.max_weight === oldMax
              ? { ...r, max_weight: newMax } as ServiceRate
              : r
          );
        });
        // Fire per-service mutations in background: delete old entries, create new ones
        Promise.all(
          oldRates.map((r) =>
            mutations.deleteServiceRate.mutateAsync({
              rate_sheet_id: rateSheetId,
              service_id: r.service_id,
              zone_id: r.zone_id,
              min_weight: r.min_weight,
              max_weight: r.max_weight,
            })
          )
        ).then(() =>
          Promise.all(
            oldRates.map((r) =>
              mutations.updateServiceRate.mutateAsync({
                rate_sheet_id: rateSheetId,
                service_id: r.service_id,
                zone_id: r.zone_id,
                rate: r.rate ?? 0,
                min_weight: oldMin,
                max_weight: newMax,
              })
            )
          )
        ).then(() => {
          toast({ title: "Weight range updated", variant: "default" });
        }).catch((err: any) => {
          toast({ title: "Failed to update weight range", description: err?.message, variant: "destructive" });
          setEditModeRatesOverride(null); // rollback to server data
        });
      } else {
        // Locally-pending range: update in local state
        setEditModePendingRanges((prev) => {
          const updated = { ...prev };
          for (const [svcId, ranges] of Object.entries(updated)) {
            updated[svcId] = ranges.map((r) =>
              r.min_weight === oldMin && r.max_weight === oldMax
                ? { ...r, max_weight: newMax }
                : r
            );
          }
          return updated;
        });
        toast({ title: "Weight range updated", variant: "default" });
      }
    } else {
      // Create mode: update local state
      setLocalServiceRates((prev) =>
        prev.map((r) =>
          r.min_weight === oldMin && r.max_weight === oldMax
            ? { ...r, max_weight: newMax }
            : r
        )
      );
      toast({ title: "Weight range updated", variant: "default" });
    }
  };

  const handleAddWeightRange = async (minWeight: number, maxWeight: number) => {
    if (isEditMode && rateSheetId) {
      // Edit mode: add locally for the current service only (no global backend mutation)
      // The weight range will be committed to the backend when the user enters a rate value
      if (!detailServiceId) return;
      setEditModePendingRanges((prev) => {
        const existing = prev[detailServiceId] || [];
        const alreadyPending = existing.some(
          (r) => r.min_weight === minWeight && r.max_weight === maxWeight
        );
        if (alreadyPending) return prev;
        return {
          ...prev,
          [detailServiceId]: [...existing, { min_weight: minWeight, max_weight: maxWeight }],
        };
      });
      toast({ title: "Weight range added", variant: "default" });
    } else {
      // Create mode: add rate=0 entries for the current service's zones
      const currentService = services.find((s) => s.id === detailServiceId);
      if (currentService) {
        const zoneIds: string[] = currentService.zone_ids || [];
        const newRates: ServiceRate[] = zoneIds.map((zoneId) => ({
          service_id: currentService.id,
          zone_id: zoneId,
          rate: 0,
          min_weight: minWeight,
          max_weight: maxWeight,
        } as ServiceRate));
        if (newRates.length > 0) {
          setLocalServiceRates((prev) => [...prev, ...newRates]);
        }
      }
      toast({ title: "Weight range added", variant: "default" });
    }
  };

  const handleRemoveWeightRange = (minWeight: number, maxWeight: number) => {
    setWeightRangeToRemove({ min_weight: minWeight, max_weight: maxWeight });
    setRemoveWeightRangeConfirmOpen(true);
  };

  const handleConfirmRemoveWeightRange = () => {
    if (!weightRangeToRemove) return;

    if (isEditMode && rateSheetId) {
      const { min_weight, max_weight } = weightRangeToRemove;

      // Check if this range is locally-pending (no backend rates for this service)
      const hasBackendRates = serviceRatesData.some(
        (r) =>
          r.service_id === detailServiceId &&
          r.min_weight === min_weight &&
          r.max_weight === max_weight
      );

      if (hasBackendRates) {
        // Optimistic update: remove matching rates for this service from overlay
        const ratesToDelete = serviceRatesData.filter(
          (r) =>
            r.service_id === detailServiceId &&
            r.min_weight === min_weight &&
            r.max_weight === max_weight
        );
        setEditModeRatesOverride((prev) => {
          const rates = prev ?? (((existingRateSheet as any)?.service_rates ?? []) as ServiceRate[]);
          return rates.filter(
            (r) =>
              !(
                r.service_id === detailServiceId &&
                r.min_weight === min_weight &&
                r.max_weight === max_weight
              )
          );
        });
        setRemoveWeightRangeConfirmOpen(false);
        setWeightRangeToRemove(null);
        // Fire deletions in background (per-service, not global removeWeightRange)
        Promise.all(
          ratesToDelete.map((r) =>
            mutations.deleteServiceRate.mutateAsync({
              rate_sheet_id: rateSheetId,
              service_id: r.service_id,
              zone_id: r.zone_id,
              min_weight: r.min_weight,
              max_weight: r.max_weight,
            })
          )
        ).then(() => {
          toast({ title: "Weight range removed", variant: "default" });
        }).catch((err: any) => {
          toast({ title: "Failed to remove weight range", description: err?.message, variant: "destructive" });
          setEditModeRatesOverride(null); // rollback to server data
        });
      } else {
        // Locally-pending only — just remove from local state
        setEditModePendingRanges((prev) => {
          if (!detailServiceId) return prev;
          const existing = prev[detailServiceId] || [];
          return {
            ...prev,
            [detailServiceId]: existing.filter(
              (r) => !(r.min_weight === min_weight && r.max_weight === max_weight)
            ),
          };
        });
        setRemoveWeightRangeConfirmOpen(false);
        setWeightRangeToRemove(null);
        toast({ title: "Weight range removed", variant: "default" });
      }
    } else {
      // Create mode: remove rates only for the current service
      const { min_weight, max_weight } = weightRangeToRemove;
      setLocalServiceRates((prev) =>
        prev.filter(
          (r) =>
            !(
              r.service_id === detailServiceId &&
              r.min_weight === min_weight &&
              r.max_weight === max_weight
            )
        )
      );
      setRemoveWeightRangeConfirmOpen(false);
      setWeightRangeToRemove(null);
      toast({ title: "Weight range removed", variant: "default" });
    }
  };

  const handleDeleteServiceRate = (
    serviceId: string,
    zoneId: string,
    minWeight: number,
    maxWeight: number
  ) => {
    if (isEditMode && rateSheetId) {
      // Optimistic update: remove rate from overlay
      setEditModeRatesOverride((prev) => {
        const rates = prev ?? (((existingRateSheet as any)?.service_rates ?? []) as ServiceRate[]);
        return rates.filter(
          (r) =>
            !(
              r.service_id === serviceId &&
              r.zone_id === zoneId &&
              r.min_weight === minWeight &&
              r.max_weight === maxWeight
            )
        );
      });
      // Fire mutation in background
      mutations.deleteServiceRate.mutate(
        {
          rate_sheet_id: rateSheetId,
          service_id: serviceId,
          zone_id: zoneId,
          min_weight: minWeight,
          max_weight: maxWeight,
        },
        {
          onError: (err: any) => {
            toast({ title: "Failed to delete rate", description: err?.message, variant: "destructive" });
            setEditModeRatesOverride(null); // rollback
          },
        }
      );
    } else {
      // Create mode: remove from local state
      setLocalServiceRates((prev) =>
        prev.filter(
          (r) =>
            !(
              r.service_id === serviceId &&
              r.zone_id === zoneId &&
              r.min_weight === minWeight &&
              r.max_weight === maxWeight
            )
        )
      );
    }
  };

  const handleWeightRateCellEdit = (
    serviceId: string,
    zoneId: string,
    minWeight: number,
    maxWeight: number,
    newRate: number
  ) => {
    if (isEditMode && rateSheetId) {
      // Optimistic update: apply change to overlay immediately
      setEditModeRatesOverride((prev) => {
        const rates = prev ?? (((existingRateSheet as any)?.service_rates ?? []) as ServiceRate[]);
        const idx = rates.findIndex(
          (r) =>
            r.service_id === serviceId &&
            r.zone_id === zoneId &&
            r.min_weight === minWeight &&
            r.max_weight === maxWeight
        );
        if (idx >= 0) {
          const updated = [...rates];
          updated[idx] = { ...updated[idx], rate: newRate };
          return updated;
        }
        return [...rates, { service_id: serviceId, zone_id: zoneId, rate: newRate, min_weight: minWeight, max_weight: maxWeight } as ServiceRate];
      });
      // Fire mutation in background
      mutations.updateServiceRate.mutate(
        {
          rate_sheet_id: rateSheetId,
          service_id: serviceId,
          zone_id: zoneId,
          rate: newRate,
          min_weight: minWeight,
          max_weight: maxWeight,
        },
        {
          onError: (err: any) => {
            toast({ title: "Failed to update rate", description: err?.message, variant: "destructive" });
          },
        }
      );
    } else {
      // Create mode: update local service rates
      setLocalServiceRates((prev) => {
        const idx = prev.findIndex(
          (r) =>
            r.service_id === serviceId &&
            r.zone_id === zoneId &&
            r.min_weight === minWeight &&
            r.max_weight === maxWeight
        );
        if (idx >= 0) {
          const updated = [...prev];
          updated[idx] = { ...updated[idx], rate: newRate };
          return updated;
        }
        return [
          ...prev,
          {
            service_id: serviceId,
            zone_id: zoneId,
            rate: newRate,
            min_weight: minWeight,
            max_weight: maxWeight,
          } as ServiceRate,
        ];
      });
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
        // Build ID remap maps for create mode
        const serviceIdRemap = new Map<string, string>();
        services.forEach((service, i) => serviceIdRemap.set(service.id, `temp-${i}`));

        const zoneIdRemap = new Map<string, string>();
        sharedZones.forEach((zone) => {
          const mutationId = zoneLabelToId.get(zone.label || "");
          if (mutationId) {
            zoneIdRemap.set(zone.id, mutationId);
          }
        });

        // Build service_rates from localServiceRates with remapped IDs
        for (const sr of localServiceRates) {
          const mappedServiceId = serviceIdRemap.get(sr.service_id);
          const mappedZoneId = zoneIdRemap.get(sr.zone_id);
          if (mappedServiceId && mappedZoneId) {
            serviceRates.push({
              service_id: mappedServiceId,
              zone_id: mappedZoneId,
              rate: sr.rate,
              cost: sr.cost ?? null,
              min_weight: sr.min_weight ?? null,
              max_weight: sr.max_weight ?? null,
            });
          }
        }

        // Create new rate sheet
        const createServices = services.map((service) => {
          // Remap zone_ids to mutation IDs
          const zoneIds = (service.zone_ids || [])
            .map((id) => zoneIdRemap.get(id) || id)
            .filter((id) => zonesForMutation.some((z) => z.id === id));

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
        <SheetContent side="right" className="w-full sm:max-w-full p-0" hideCloseButton>
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
              <div className="flex items-center gap-2">
                <button
                  onClick={handleSave}
                  disabled={isSaving || isInitialLoading}
                  className="p-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-accent transition-colors disabled:opacity-50 disabled:pointer-events-none"
                  aria-label="Save"
                  title="Save"
                >
                  {isSaving ? (
                    <Loader2 className="h-5 w-5 animate-spin" />
                  ) : (
                    <Save className="h-5 w-5" />
                  )}
                </button>
                <button
                  onClick={() => setCsvPreviewOpen(true)}
                  className="p-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                  aria-label="Preview as spreadsheet"
                  title="Preview as spreadsheet"
                  disabled={isInitialLoading}
                >
                  <TableIcon className="h-5 w-5" />
                </button>
                <button
                  onClick={() => onClose()}
                  className="p-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                  aria-label="Close"
                >
                  <Cross2Icon className="h-5 w-5" />
                </button>
              </div>
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
                        { id: "surcharges", label: "Surcharges" },
                        ...(isAdmin ? [{ id: "markups" as const, label: "Brokerage" }] : []),
                      ] as const
                    ).map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={cn(
                          "py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap px-4",
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
                <div className="flex-1 pt-4 px-4 sm:pt-4 sm:px-6 pb-4 sm:pb-6 overflow-hidden relative">
                  {activeTab === "rate_sheet" && (
                    <div className="h-full flex flex-col">
                      {/* Service tabs */}
                      {services.length > 0 && (
                        <div
                          className="flex items-center gap-1 mb-3 pb-1 border-b border-border overflow-x-auto [&::-webkit-scrollbar]:hidden"
                          style={{ scrollbarWidth: 'none' }}
                        >
                          {services.map((svc) => {
                            const isActive = detailServiceId === svc.id;
                            return (
                              <div key={svc.id} className="relative flex items-center flex-shrink-0">
                                <button
                                  onClick={() => setDetailServiceId(svc.id)}
                                  className={cn(
                                    "px-4 py-2 text-sm font-medium rounded-md whitespace-nowrap transition-colors",
                                    isActive
                                      ? "bg-primary text-primary-foreground"
                                      : "text-muted-foreground hover:text-foreground hover:bg-accent"
                                  )}
                                >
                                  {svc.service_name || svc.service_code || "Unnamed"}
                                </button>
                                {isActive && (
                                  <div className="flex items-center gap-0.5 ml-0.5">
                                    <button
                                      onClick={(e) => { e.stopPropagation(); handleEditService(svc); }}
                                      className="p-0.5 rounded-sm text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                                      title="Edit service"
                                    >
                                      <Pencil1Icon className="h-3 w-3" />
                                    </button>
                                    <button
                                      onClick={(e) => { e.stopPropagation(); handleDeleteClick(svc); }}
                                      className="p-0.5 rounded-sm text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
                                      title="Delete service"
                                    >
                                      <TrashIcon className="h-3 w-3" />
                                    </button>
                                  </div>
                                )}
                              </div>
                            );
                          })}

                          {/* Add service popover - sticky at end */}
                          <div className="flex-shrink-0 sticky right-0 bg-background pl-1">
                            <AddServicePopover
                              services={services}
                              onAddService={handleAddService}
                              servicePresets={servicePresets}
                              onAddServiceFromPreset={handleAddServiceFromPreset}
                              onCloneService={handleCloneService}
                              iconOnly
                              align="end"
                            />
                          </div>
                        </div>
                      )}

                      {/* Content: per-service detail grid */}
                      <div className="flex-1 overflow-hidden relative">
                        {/* Carrier gate: disabled overlay in create mode when no carrier */}
                        {!isEditMode && !carrierName && (
                          <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/60">
                            <p className="text-sm text-muted-foreground">Select a carrier to get started</p>
                          </div>
                        )}
                        {services.length === 0 ? (
                          <div className="flex-1 flex items-center justify-center text-muted-foreground bg-muted/50 rounded border-2 border-dashed h-full">
                            <div className="text-center p-8">
                              <p className="text-sm">No services configured</p>
                              <div className="mt-2">
                                <AddServicePopover
                                  services={services}
                                  onAddService={handleAddService}
                                  servicePresets={servicePresets}
                                  onAddServiceFromPreset={handleAddServiceFromPreset}
                                  onCloneService={handleCloneService}
                                />
                              </div>
                            </div>
                          </div>
                        ) : (
                          (() => {
                            const svc = services.find((s) => s.id === detailServiceId);
                            if (!svc) return null;
                            return (
                              <ServiceRateDetailView
                                service={svc}
                                sharedZones={sharedZones}
                                serviceRates={serviceRatesData}
                                weightRanges={weightRanges}
                                weightUnit={selectedWeightUnit}
                                onCellEdit={handleWeightRateCellEdit}
                                onDeleteRate={handleDeleteServiceRate}
                                onAddWeightRange={() => setWeightRangeDialogOpen(true)}
                                onRemoveWeightRange={handleRemoveWeightRange}
                                onAssignZoneToService={handleAssignZoneToService}
                                onCreateNewZone={handleCreateZoneForService}
                                onRemoveZoneFromService={handleRemoveZoneFromService}
                                serviceFilteredWeightRanges={getServiceWeightRanges(svc.id)}
                                onEditWeightRange={handleEditWeightRange}
                                onEditZone={handleEditZone}
                                onDeleteZone={handleRemoveZoneAll}
                                missingRanges={getMissingWeightRanges(svc.id)}
                                onAddMissingRange={handleAddWeightRange}
                                weightRangePresets={weightRangePresets}
                                onAddFromPreset={handleAddWeightRange}
                              />
                            );
                          })()
                        )}
                      </div>
                    </div>
                  )}
                  {activeTab === "surcharges" && (
                    <SurchargesTab
                      surcharges={surcharges}
                      services={services}
                      onEditSurcharge={handleEditSurcharge}
                      onAddSurcharge={handleAddSurcharge}
                      onRemoveSurcharge={handleRemoveSurcharge}
                      surchargePresets={surchargePresets}
                      onAddSurchargeFromPreset={handleAddSurchargeFromPreset}
                      onCloneSurcharge={handleCloneSurcharge}
                    />
                  )}
                  {activeTab === "markups" && isAdmin && (
                    <MarkupsTab
                      markups={adminMarkups}
                      onEditMarkup={handleEditMarkup}
                      onAddMarkup={handleAddMarkup}
                      onRemoveMarkup={handleRemoveMarkup}
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
        onClose={() => {
          setServiceDialogOpen(false);
          setSelectedService(null);
          setPendingServiceRates([]);
        }}
        service={selectedService}
        onSubmit={handleSaveService}
        availableSurcharges={surcharges}
        servicePresets={servicePresets}
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

      {/* Add Weight Range Dialog */}
      <AddWeightRangeDialog
        open={weightRangeDialogOpen}
        onOpenChange={setWeightRangeDialogOpen}
        existingRanges={weightRanges}
        weightUnit={selectedWeightUnit}
        onAdd={handleAddWeightRange}
      />

      {/* Edit Weight Range Dialog */}
      <EditWeightRangeDialog
        open={editWeightRangeDialogOpen}
        onOpenChange={setEditWeightRangeDialogOpen}
        weightRange={weightRangeToEdit}
        existingRanges={weightRanges}
        weightUnit={selectedWeightUnit}
        onSave={handleSaveWeightRangeEdit}
      />

      {/* Remove Weight Range Confirmation */}
      <AlertDialog open={removeWeightRangeConfirmOpen} onOpenChange={setRemoveWeightRangeConfirmOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Remove Weight Range</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to remove the weight range{" "}
              {weightRangeToRemove?.min_weight ?? 0} –{" "}
              {weightRangeToRemove?.max_weight ?? 0}? All rates in this range
              will be deleted.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleConfirmRemoveWeightRange}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Remove
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Zone Editor Dialog */}
      <ZoneEditorDialog
        open={zoneEditorOpen}
        onOpenChange={(open) => {
          setZoneEditorOpen(open);
          if (!open) {
            // On cancel (not save) for a staged zone, undo any service linkings
            if (!zoneSaveRef.current && selectedZone && !sharedZones.some(z => z.id === selectedZone.id)) {
              setServices((prev) =>
                prev.map((service) => ({
                  ...service,
                  zones: (service.zones || []).filter((z) => z.id !== selectedZone.id),
                  zone_ids: (service.zone_ids || []).filter((id) => id !== selectedZone.id),
                }))
              );
            }
            zoneSaveRef.current = false;
            setSelectedZone(null);
            setPendingZoneServiceId(null);
          }
        }}
        zone={selectedZone}
        onSave={handleSaveZone}
        countryOptions={countryOptions}
        services={services}
        onToggleServiceZone={handleToggleServiceZone}
      />

      {/* Surcharge Editor Dialog */}
      <SurchargeEditorDialog
        open={surchargeEditorOpen}
        onOpenChange={(open) => {
          setSurchargeEditorOpen(open);
          if (!open) {
            // On cancel (not save) for a staged surcharge, undo any service linkings
            if (!surchargeSaveRef.current && selectedSurcharge && !surcharges.some(s => s.id === selectedSurcharge.id)) {
              setServices((prev) =>
                prev.map((service) => ({
                  ...service,
                  surcharge_ids: (service.surcharge_ids || []).filter((id) => id !== selectedSurcharge.id),
                }))
              );
            }
            surchargeSaveRef.current = false;
            setSelectedSurcharge(null);
          }
        }}
        surcharge={selectedSurcharge}
        onSave={handleSaveSurcharge}
        services={services}
        onToggleServiceSurcharge={handleToggleServiceSurcharge}
      />

      {/* Service Rate Editor Dialog */}
      <ServiceRateEditorDialog
        open={rateEditorOpen}
        onOpenChange={setRateEditorOpen}
        serviceRate={selectedRate}
        onSave={handleSaveRate}
        services={services}
        sharedZones={sharedZones}
        weightUnit={selectedWeightUnit}
      />

      {/* Markup Editor Dialog (admin only) */}
      {isAdmin && (
        <MarkupEditorDialog
          open={markupEditorOpen}
          onOpenChange={(open) => {
            setMarkupEditorOpen(open);
            if (!open) {
              setSelectedMarkup(null);
              setIsNewMarkup(false);
            }
          }}
          markup={selectedMarkup}
          isNew={isNewMarkup}
          onSave={async (data) => {
            if (!markupMutations) return;
            try {
              if (isNewMarkup) {
                await markupMutations.createMarkup.mutateAsync({
                  name: data.name,
                  amount: data.amount,
                  markup_type: data.markup_type as any,
                  active: data.active,
                  is_visible: data.is_visible,
                  meta: Object.keys(data.meta).length > 0 ? data.meta : undefined,
                } as any);
                toast({ title: "Markup created" });
              } else if (selectedMarkup) {
                await markupMutations.updateMarkup.mutateAsync({
                  id: selectedMarkup.id,
                  name: data.name,
                  amount: data.amount,
                  markup_type: data.markup_type as any,
                  active: data.active,
                  is_visible: data.is_visible,
                  meta: Object.keys(data.meta).length > 0 ? data.meta : undefined,
                } as any);
                toast({ title: "Markup updated" });
              }
            } catch (err: any) {
              toast({ title: "Failed to save markup", description: err?.message, variant: "destructive" });
            }
          }}
        />
      )}

      {/* CSV Preview */}
      <RateSheetCsvPreview
        open={csvPreviewOpen}
        onOpenChange={setCsvPreviewOpen}
        name={name}
        carrierName={carrierName}
        originCountries={originCountries}
        services={services}
        sharedZones={sharedZones}
        serviceRates={serviceRatesData}
        weightRanges={weightRanges}
        surcharges={surcharges}
        weightUnit={selectedWeightUnit}
        markups={isAdmin ? markupsForPreview : undefined}
        isAdmin={isAdmin}
      />
    </>
  );
};

export default RateSheetEditor;
