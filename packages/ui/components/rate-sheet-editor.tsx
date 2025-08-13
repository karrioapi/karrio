"use client";

import { Sheet, SheetContent } from "@karrio/ui/components/ui/sheet";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@karrio/ui/components/ui/tabs";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { RateSheetTable } from "@karrio/ui/components/rate-sheet-table";
import { ServiceEditorModal } from "@karrio/ui/components/modals/service-editor-modal";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { useLoader } from "@karrio/ui/core/components/loader";
import { CURRENCY_OPTIONS, DIMENSION_UNITS, WEIGHT_UNITS } from "@karrio/types";
import { Cross2Icon, TrashIcon } from "@radix-ui/react-icons";
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogCancel,
  AlertDialogAction,
  AlertDialogTrigger,
} from "@karrio/ui/components/ui/alert-dialog";
import { isEqual, failsafe } from "@karrio/lib";
import CodeMirror from "@uiw/react-codemirror";
import { jsonLanguage } from "@codemirror/lang-json";
import React from "react";

interface RateSheetEditorProps {
  rateSheetId: string;
  onClose: () => void;
  preloadCarrier?: string; // For creating from carrier connections
  linkConnectionId?: string; // explicit carrier connection id to link after create
  isAdmin?: boolean; // Flag to use admin mutations/queries
  useRateSheet: (args: any) => any; // Pass in the appropriate hook
  useRateSheetMutation: () => any; // Pass in the appropriate mutation hook
}

export const RateSheetEditor = ({ 
  rateSheetId, 
  onClose, 
  preloadCarrier, 
  linkConnectionId,
  isAdmin = false,
  useRateSheet,
  useRateSheetMutation
}: RateSheetEditorProps) => {
  const loader = useLoader();
  const { references, metadata } = useAPIMetadata();
  const isNew = rateSheetId === 'new';

  // Fetch carrier metadata for optional fallback defaults
  React.useEffect(() => {
    if (metadata?.HOST) {
      fetch(`${metadata.HOST}/v1/carriers`)
        .then(res => res.json())
        .then((carriers) => {
          setCarrierMetadata(carriers);
        })
        .catch(console.error);
    }
  }, [metadata?.HOST]);

  // Fetch existing rate sheets when creating new ones
  React.useEffect(() => {
    if (isNew && metadata?.HOST) {
      // This would ideally be a GraphQL query, but for now we'll use existing data
      // The existing rate sheets would be fetched via the rate sheets list
    }
  }, [isNew, metadata?.HOST]);
  const { query, setRateSheetId } = useRateSheet({ id: rateSheetId });
  const { createRateSheet, updateRateSheet, deleteRateSheetService, batchUpdateRateSheetCells } = useRateSheetMutation();
  const [serviceModalOpen, setServiceModalOpen] = React.useState(false);
  const [editingService, setEditingService] = React.useState<any>(null);
  const [localData, setLocalData] = React.useState<any>(null);
  const [carrierMetadata, setCarrierMetadata] = React.useState<any[]>([]);
  const [existingRateSheets, setExistingRateSheets] = React.useState<any[]>([]);
  const [showExistingOptions, setShowExistingOptions] = React.useState(false);

  const rateSheet = query.data?.rate_sheet;
  const services = rateSheet?.services || [];
  const connectedCarriers = rateSheet?.carriers || [];

  // Define loadCarrierDefaults before useEffect to avoid initialization order issues
  const loadCarrierDefaults = React.useCallback((carrierName?: string) => {
    const targetCarrier = carrierName || localData?.carrier_name;
    if (!targetCarrier) return;

    // First check references for service_levels (primary source)
    const refs = references;
    if (refs?.service_levels?.[targetCarrier]) {
      const defaultServices = refs.service_levels[targetCarrier].map((service: any, index: number) => ({
        ...service,
        id: `temp_${Date.now()}_${index}`,
        // Ensure zones structure is correct - remove any IDs to let backend assign them
        zones: (service.zones || [{ label: 'Zone 1', rate: 0 }]).map((zone: any, zoneIndex: number) => ({
          label: zone.label || `Zone ${zoneIndex + 1}`,
          rate: zone.rate || 0
          // No ID field - let backend assign
        }))
      }));

      setLocalData((prev: any) => ({
        ...prev,
        services: defaultServices
      }));
      return;
    }

    // Fallback to carrier metadata if available
    const carrierMeta = carrierMetadata.find(c => c.carrier_name === targetCarrier);
    if (carrierMeta?.connection_fields?.services?.default) {
      const defaultServices = carrierMeta.connection_fields.services.default.map((service: any, index: number) => ({
        ...service,
        id: `temp_${Date.now()}_${index}`,
        zones: (service.zones || [{ rate: 0 }]).map((zone: any, zoneIndex: number) => ({
          label: zone.label || `Zone ${zoneIndex + 1}`,
          rate: zone.rate || 0
        }))
      }));

      setLocalData((prev: any) => ({
        ...prev,
        services: defaultServices
      }));
      return;
    }

    console.warn(`No default services found for ${targetCarrier}`);
  }, [carrierMetadata, references, localData?.carrier_name]);

  React.useEffect(() => {
    if (rateSheet && !localData) {
      setLocalData({
        name: rateSheet.name,
        carrier_name: rateSheet.carrier_name,
        services: [...(rateSheet.services || [])]
      });
    } else if (isNew && !localData) {
      // Initialize with preloaded carrier or defaults for new rate sheets
      const initialCarrier = preloadCarrier || 'generic';
      setLocalData({
        name: '',
        carrier_name: initialCarrier,
        services: []
      });

      // Auto-load defaults if carrier is preloaded
      if (preloadCarrier) {
        setTimeout(() => loadCarrierDefaults(preloadCarrier), 100);
      }
    }
  }, [rateSheet, localData, isNew, preloadCarrier, loadCarrierDefaults]);

  // Ensure defaults are loaded when launching from a carrier once references are available
  React.useEffect(() => {
    if (isNew && preloadCarrier && references?.service_levels?.[preloadCarrier]) {
      // Only load defaults if none are present yet
      if (!localData?.services || localData.services.length === 0) {
        loadCarrierDefaults(preloadCarrier);
      }
    }
  }, [isNew, preloadCarrier, references?.service_levels, loadCarrierDefaults, localData?.services]);

  // Capture a target carrier to link on create when coming from a connection
  const [linkCarrierId, setLinkCarrierId] = React.useState<string | null>(null);
  React.useEffect(() => {
    if (isNew && preloadCarrier && Array.isArray(carrierMetadata) && carrierMetadata.length > 0) {
      const carrier = carrierMetadata.find(c => c.carrier_name === preloadCarrier);
      if (carrier?.id) setLinkCarrierId(carrier.id);
    }
  }, [isNew, preloadCarrier, carrierMetadata]);

  const handleChange = (field: string, value: any) => {
    setLocalData((prev: any) => ({ ...prev, [field]: value }));

    // Auto-load defaults when carrier is selected for new rate sheets
    if (field === 'carrier_name' && isNew && value) {
      loadCarrierDefaults(value);
    }
  };

  const checkForExistingRateSheets = (carrierName: string) => {
    // This would check for existing rate sheets with same carrier_name
    // For now, we'll implement the basic structure
    setShowExistingOptions(false); // Reset for now
  };

  const handleSave = async () => {
    if (!localData) return;

    loader.setLoading(true);
    try {
      // Clean data for mutation - ensure we have at least basic validation
      if (!localData.name || !localData.name.trim()) {
        throw new Error('Rate sheet name is required');
      }

      if (!localData.carrier_name) {
        throw new Error('Carrier name is required');
      }

      if (!localData.services || localData.services.length === 0) {
        throw new Error('At least one service is required');
      }

      const cleanedData = {
        name: localData.name.trim(),
        // Note: carrier_name is stored locally but not sent in updates
        services: (localData.services || []).map((service: any, index: number) => {
          // Validate required service fields
          if (!service.service_name || !service.service_name.trim()) {
            throw new Error(`Service ${index + 1}: service_name is required`);
          }
          if (!service.service_code || !service.service_code.trim()) {
            throw new Error(`Service ${index + 1}: service_code is required`);
          }

          // Create a new clean service object with required fields for CreateServiceLevelInput
          const cleanService: any = {
            service_name: service.service_name.trim(),
            service_code: service.service_code.trim(),
            // currency is required for CreateServiceLevelInput
            currency: service.currency || 'USD'
          };

          // Only include id for existing services (for updates, not creates)
          if (service.id && !service.id.startsWith('temp_')) {
            cleanService.id = service.id;
          }

          // Include other service fields if they have values
          if (service.carrier_service_code) cleanService.carrier_service_code = service.carrier_service_code;
          if (service.description) cleanService.description = service.description;
          if (service.active !== undefined) cleanService.active = service.active;
          if (service.transit_days !== null && service.transit_days !== undefined) cleanService.transit_days = service.transit_days;
          if (service.transit_time) cleanService.transit_time = service.transit_time;
          if (service.max_width !== null && service.max_width !== undefined) cleanService.max_width = service.max_width;
          if (service.max_height !== null && service.max_height !== undefined) cleanService.max_height = service.max_height;
          if (service.max_length !== null && service.max_length !== undefined) cleanService.max_length = service.max_length;
          if (service.dimension_unit) cleanService.dimension_unit = service.dimension_unit;

          // Clean zones - zones are required for CreateServiceLevelInput
          cleanService.zones = (service.zones && Array.isArray(service.zones) && service.zones.length > 0) 
            ? service.zones.map((zone: any) => {
                const cleanZone: any = {
                  // rate is required for ServiceZoneInput
                  rate: Number(zone.rate) || 0
                };

                // Add optional fields if they have values
                if (zone.label) cleanZone.label = zone.label;
                if (zone.min_weight !== null && zone.min_weight !== undefined && zone.min_weight !== '') {
                  cleanZone.min_weight = Number(zone.min_weight);
                }
                if (zone.max_weight !== null && zone.max_weight !== undefined && zone.max_weight !== '') {
                  cleanZone.max_weight = Number(zone.max_weight);
                }
                if (zone.transit_days !== null && zone.transit_days !== undefined && zone.transit_days !== '') {
                  cleanZone.transit_days = Number(zone.transit_days);
                }
                if (zone.transit_time) cleanZone.transit_time = zone.transit_time;
                if (zone.cities && zone.cities.length > 0) cleanZone.cities = zone.cities;
                if (zone.postal_codes && zone.postal_codes.length > 0) cleanZone.postal_codes = zone.postal_codes;
                if (zone.country_codes && zone.country_codes.length > 0) cleanZone.country_codes = zone.country_codes;

                return cleanZone;
              })
            : [{ rate: 0 }]; // Default zone if none exist

          return cleanService;
        })
      };

      if (isNew) {
        // For new rate sheets, include carrier_name and carriers
        const createData: any = {
          ...cleanedData,
          carrier_name: localData.carrier_name,
        };

        // Add carriers array if we have connection IDs to link
        if (linkConnectionId) {
          createData.carriers = [linkConnectionId];
        } else if (linkCarrierId) {
          createData.carriers = [linkCarrierId];
        }

        console.log('Creating rate sheet with data:', JSON.stringify(createData, null, 2));
        let res;
        try {
          res = await createRateSheet.mutateAsync(createData);
          console.log('Create response:', res);
        } catch (err: any) {
          console.error('Create mutation failed:', err);
          console.error('Error details:', JSON.stringify(err, null, 2));
          
          // Extract more specific error message
          let errorMessage = 'Failed to create rate sheet';
          if (err?.response?.errors?.[0]?.message) {
            errorMessage = err.response.errors[0].message;
          } else if (err?.message) {
            errorMessage = err.message;
          }
          
          throw new Error(errorMessage);
        }
        const newId = (res as any)?.create_rate_sheet?.rate_sheet?.id;
        if (newId) {
          // Switch to edit mode without closing and refresh data from server
          setRateSheetId(newId);
          const refreshed = await query.refetch();
          const fresh = (refreshed.data as any)?.rate_sheet;
          if (fresh) {
            setLocalData({
              name: fresh.name,
              carrier_name: fresh.carrier_name,
              services: [...(fresh.services || [])]
            });
          }
        }
      } else {
        // For updates, don't send carrier_name
        await updateRateSheet.mutateAsync({
          id: rateSheetId,
          ...cleanedData
        });
        // Refresh data to reconcile IDs and removals
        const refreshed = await query.refetch();
        const fresh = (refreshed.data as any)?.rate_sheet;
        if (fresh) {
          setLocalData({
            name: fresh.name,
            carrier_name: fresh.carrier_name,
            services: [...(fresh.services || [])]
          });
        }
      }
      // Do not close the editor; leave it open
    } catch (error: any) {
      // Surface a friendly error, avoid throwing in console overlay
      const message = error?.response?.errors?.[0]?.message || error?.message || 'Unknown error';
      console.warn("Failed to save rate sheet:", message);
    } finally {
      loader.setLoading(false);
    }
  };

  const handleAddService = () => {
    setEditingService(null);
    setServiceModalOpen(true);
  };

  const handleEditService = (service: any) => {
    setEditingService(service);
    setServiceModalOpen(true);
  };

  const handleServiceSubmit = (serviceData: any) => {
    if (!localData) return;

    if (editingService?.id) {
      // Update existing service
      setLocalData((prev: any) => ({
        ...prev,
        services: prev.services.map((s: any) => {
          if (s.id !== editingService.id) return s;
          return {
            ...s,
            service_name: serviceData.service_name,
            service_code: serviceData.service_code,
            carrier_service_code: serviceData.carrier_service_code,
            description: serviceData.description,
            active: serviceData.active,
            currency: serviceData.currency,
            transit_days: serviceData.transit_days,
            transit_time: serviceData.transit_time,
            max_width: serviceData.max_width,
            max_height: serviceData.max_height,
            max_length: serviceData.max_length,
            dimension_unit: serviceData.dimension_unit,
            min_weight: serviceData.min_weight,
            max_weight: serviceData.max_weight,
            weight_unit: serviceData.weight_unit,
            domicile: serviceData.domicile,
            international: serviceData.international,
            // Preserve zones and id as-is unless changed elsewhere
            zones: s.zones,
          };
        })
      }));
    } else {
      // Add new service
      const newService = {
        ...serviceData,
        id: `temp_${Date.now()}`,
        zones: [{ rate: 0 }] // No client-generated IDs - let backend assign them
      };
      setLocalData((prev: any) => ({
        ...prev,
        services: [...prev.services, newService]
      }));
    }
    // Close modal after applying the update
    setServiceModalOpen(false);
    setEditingService(null);
  };

  const handleRemoveService = async (serviceId: string) => {
    if (!localData) return;

    // Check if this is an existing service (not temp)
    const service = localData.services.find((s: any) => s.id === serviceId);
    const isExistingService = service && !service.id.startsWith('temp_');

    if (isExistingService && !isNew) {
      // Use explicit delete API for existing services
      try {
        await deleteRateSheetService.mutateAsync({
          rate_sheet_id: rateSheetId,
          service_id: serviceId
        });
        // Refresh data from server
        const refreshed = await query.refetch();
        const fresh = (refreshed.data as any)?.rate_sheet;
        if (fresh) {
          setLocalData({
            name: fresh.name,
            carrier_name: fresh.carrier_name,
            services: [...(fresh.services || [])]
          });
        }
      } catch (error) {
        console.error("Failed to delete service:", error);
      }
    } else {
      // For temp services or new rate sheets, just remove from local state
      setLocalData((prev: any) => ({
        ...prev,
        services: prev.services.filter((s: any) => s.id !== serviceId)
      }));
    }
  };

  const handleAddZone = (serviceId: string) => {
    if (!localData) return;

    setLocalData((prev: any) => ({
      ...prev,
      services: prev.services.map((s: any) =>
        s.id === serviceId
          ? {
            ...s,
            zones: [...(s.zones || []), { rate: 0 }] // No client-generated IDs
          }
          : s
      )
    }));
  };

  const handleAddZoneAll = () => {
    if (!localData) return;
    setLocalData((prev: any) => ({
      ...prev,
      services: prev.services.map((s: any) => ({
        ...s,
        zones: [...(s.zones || []), { rate: 0 }]
      }))
    }));
  };

  const handleRemoveZoneAll = (zoneIndex: number) => {
    if (!localData) return;
    setLocalData((prev: any) => ({
      ...prev,
      services: prev.services.map((s: any) => ({
        ...s,
        zones: s.zones.filter((_: any, i: number) => i !== zoneIndex)
      }))
    }));
  };

  const handleUpdateZoneFieldAll = (zoneIndex: number, field: string, value: any) => {
    setLocalData((prev: any) => ({
      ...prev,
      services: prev.services.map((s: any) => ({
        ...s,
        zones: s.zones.map((z: any, i: number) => i === zoneIndex ? { ...z, [field]: value } : z)
      }))
    }));
  };

  const handleRemoveZone = (serviceId: string, zoneIndex: number) => {
    if (!localData) return;

    setLocalData((prev: any) => ({
      ...prev,
      services: prev.services.map((s: any) =>
        s.id === serviceId
          ? {
            ...s,
            zones: s.zones.filter((_: any, i: number) => i !== zoneIndex)
          }
          : s
      )
    }));
  };

  const handleCellChange = (serviceId: string, zoneId: string, field: string, value: any) => {
    if (!localData) return;

    setLocalData((prev: any) => ({
      ...prev,
      services: prev.services.map((s: any) =>
        s.id === serviceId
          ? {
            ...s,
            zones: s.zones.map((z: any, index: number) => {
              const currentZoneId = z.id || index.toString();
              return currentZoneId === zoneId
                ? { ...z, [field]: value }
                : z;
            })
          }
          : s
      )
    }));
  };

  const hasChanges = localData && rateSheet && !isEqual(localData, {
    name: rateSheet.name,
    carrier_name: rateSheet.carrier_name,
    services: rateSheet.services || []
  });

  const isValidNew = React.useMemo(() => {
    if (!localData) return false;
    const hasName = !!localData.name && localData.name.trim().length > 0;
    const hasCarrier = !!localData.carrier_name;
    const hasService = Array.isArray(localData.services) && localData.services.length > 0;
    const servicesValid = (localData.services || []).every((s: any) => !!s.service_name && !!s.service_code);
    return hasName && hasCarrier && hasService && servicesValid;
  }, [localData]);

  if (!localData && !isNew) {
    return null;
  }

  return (
    <>
      <Sheet open={true} onOpenChange={onClose}>
        <SheetContent
          side="right"
          full
          className="p-0 gap-0 overflow-hidden"
        >
          {/* Sticky Header */}
          <header
            className="flex items-center justify-between p-4 border-b bg-white"
            style={{
              position: "sticky",
              zIndex: 10,
              top: 0,
            }}
          >
            <div className="flex items-center">
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                className="rounded-full mr-2"
              >
                <Cross2Icon className="h-4 w-4" />
              </Button>
              <h1 className="text-lg font-semibold">
                {isNew ? "Create Rate Sheet" : "Edit Rate Sheet"}
              </h1>
            </div>
            <Button
              onClick={handleSave}
              disabled={loader.loading || (isNew ? !localData?.name : (!hasChanges || !localData?.name))}
              size="sm"
              className="bg-green-600 hover:bg-green-700"
            >
              {loader.loading ? "Saving..." : "Save"}
            </Button>
          </header>

          {/* Main Content Area */}
          <div
            className="flex h-full"
            style={{
              height: "calc(100vh - 80px)",
              overflow: "hidden"
            }}
          >
            {/* Left Sidebar */}
            <div
              className="w-80 border-r bg-gray-50 overflow-y-auto"
              style={{
                minWidth: "320px",
                maxWidth: "320px"
              }}
            >
              <div className="p-4 space-y-6">
                {/* Existing Rate Sheets Notice */}
                {showExistingOptions && (
                  <div className="p-3 bg-blue-50 border border-blue-200 rounded">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-sm font-semibold text-blue-800">Existing Rate Sheets Found</h4>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => setShowExistingOptions(false)}
                        className="h-6 w-6 p-0"
                      >
                        ×
                      </Button>
                    </div>
                    <p className="text-xs text-blue-700 mb-3">
                      Compatible rate sheets exist for this carrier. You can connect to an existing one or create a new one.
                    </p>
                    <div className="space-y-2">
                      {existingRateSheets.map((sheet: any) => (
                        <div key={sheet.id} className="flex items-center justify-between p-2 bg-white rounded border">
                          <div>
                            <div className="text-sm font-medium">{sheet.name}</div>
                            <div className="text-xs text-gray-500">{sheet.services?.length || 0} services</div>
                          </div>
                          <Button size="sm" variant="outline">
                            Connect
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                <div>
                  <Label htmlFor="carrier_name" className="text-sm font-semibold text-gray-700">Carrier</Label>
                  <Select
                    value={localData?.carrier_name || 'generic'}
                    onValueChange={(value) => handleChange('carrier_name', value)}
                    disabled={!isNew || !!preloadCarrier}
                  >
                    <SelectTrigger className="mt-1">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {Object.keys(references?.service_levels || {}).map(carrier => (
                        <SelectItem key={carrier} value={carrier}>
                          {references?.carriers?.[carrier] || carrier}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="name" className="text-sm font-semibold text-gray-700">Rate Sheet Name</Label>
                  <Input
                    id="name"
                    value={localData?.name || ''}
                    onChange={(e) => handleChange('name', e.target.value)}
                    placeholder="Courier negotiated rates"
                    className="mt-1"
                    required
                  />
                </div>

                <div>
                  <Label className="text-sm font-semibold text-gray-700">Services ({localData?.services?.length || 0})</Label>
                  <div className="space-y-2 mt-2 max-h-40 overflow-y-auto">
                    {localData?.services?.map((service: any) => (
                      <div key={service.id} className="flex items-center justify-between p-3 border rounded bg-white">
                        <div className="min-w-0 flex-1">
                          <div className="font-medium text-sm truncate">{service.service_name}</div>
                          <div className="text-xs text-gray-500 truncate">{service.service_code}</div>
                          <div className="text-xs text-gray-500">{service.zones?.length || 0} zones</div>
                        </div>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleEditService(service)}
                          className="ml-2 shrink-0"
                        >
                          Edit
                        </Button>
                        <AlertDialog>
                          <AlertDialogTrigger asChild>
                            <Button
                              size="sm"
                              variant="ghost"
                              className="ml-1 shrink-0 text-red-600 hover:text-red-700"
                              title="Delete service"
                            >
                              <TrashIcon className="h-3 w-3" />
                            </Button>
                          </AlertDialogTrigger>
                          <AlertDialogContent>
                            <AlertDialogHeader>
                              <AlertDialogTitle>Delete service</AlertDialogTitle>
                              <AlertDialogDescription>
                                Are you sure you want to delete "{service.service_name}"? This cannot be undone.
                              </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                              <AlertDialogCancel className="h-8 px-3 text-sm">Cancel</AlertDialogCancel>
                              <AlertDialogAction
                                className="h-8 px-3 text-sm bg-red-600 hover:bg-red-700"
                                onClick={() => handleRemoveService(service.id)}
                              >
                                Delete
                              </AlertDialogAction>
                            </AlertDialogFooter>
                          </AlertDialogContent>
                        </AlertDialog>
                      </div>
                    ))}
                    <div className="space-y-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleAddService}
                        className="w-full"
                      >
                        Add Service
                      </Button>
                      {localData?.carrier_name && (!localData?.services?.length || localData?.services?.length === 0) && (
                        <div className="space-y-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => loadCarrierDefaults()}
                            className="w-full"
                          >
                            Load {references?.carriers?.[localData.carrier_name] || localData.carrier_name} Defaults
                          </Button>
                          {isNew && (
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => checkForExistingRateSheets(localData.carrier_name)}
                              className="w-full text-xs"
                            >
                              Check for Existing Rate Sheets
                            </Button>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Connected Carriers */}
                {connectedCarriers.length > 0 && (
                  <div>
                    <Label className="text-sm font-semibold text-gray-700">Connected Carriers ({connectedCarriers.length})</Label>
                    <div className="space-y-2 mt-2 max-h-32 overflow-y-auto">
                      {connectedCarriers.map((carrier: any) => (
                        <div key={carrier.id} className="flex items-center justify-between p-2 border rounded bg-white text-sm">
                          <div className="min-w-0 flex-1">
                            <div className="font-medium truncate">{carrier.display_name}</div>
                            <div className="text-xs text-gray-500 truncate">{carrier.carrier_id}</div>
                          </div>
                          <div className="flex items-center space-x-2 text-xs">
                            <span className={`px-2 py-1 rounded ${carrier.active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                              {carrier.active ? 'Active' : 'Inactive'}
                            </span>
                            <span className={`px-2 py-1 rounded ${carrier.test_mode ? 'bg-yellow-100 text-yellow-700' : 'bg-blue-100 text-blue-700'}`}>
                              {carrier.test_mode ? 'Test' : 'Live'}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Default Settings */}
                <div className="space-y-3 pt-4 border-t">
                  <Label className="text-sm font-semibold text-gray-700">Default Settings</Label>

                  <div>
                    <Label htmlFor="currency" className="text-xs text-gray-600">Currency</Label>
                    <Select
                      value={localData?.services?.[0]?.currency || 'USD'}
                      onValueChange={(value) => {
                        setLocalData((prev: any) => ({
                          ...prev,
                          services: prev.services.map((s: any) => ({ ...s, currency: value }))
                        }));
                      }}
                    >
                      <SelectTrigger className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {CURRENCY_OPTIONS.map(currency => (
                          <SelectItem key={currency} value={currency}>
                            {currency}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="weight_unit" className="text-xs text-gray-600">Weight Unit</Label>
                    <Select
                      value={localData?.services?.[0]?.weight_unit || 'KG'}
                      onValueChange={(value) => {
                        setLocalData((prev: any) => ({
                          ...prev,
                          services: prev.services.map((s: any) => ({ ...s, weight_unit: value }))
                        }));
                      }}
                    >
                      <SelectTrigger className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {WEIGHT_UNITS.map(unit => (
                          <SelectItem key={unit} value={unit}>
                            {unit}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="dimension_unit" className="text-xs text-gray-600">Dimension Unit</Label>
                    <Select
                      value={localData?.services?.[0]?.dimension_unit || 'CM'}
                      onValueChange={(value) => {
                        setLocalData((prev: any) => ({
                          ...prev,
                          services: prev.services.map((s: any) => ({ ...s, dimension_unit: value }))
                        }));
                      }}
                    >
                      <SelectTrigger className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {DIMENSION_UNITS.map(unit => (
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

            {/* Main Content */}
            <div
              className="flex-1 bg-gray-100"
              style={{
                height: "100%",
                minHeight: "600px",
                overflow: "hidden"
              }}
            >
              <div
                className="h-full p-4"
                style={{
                  display: "flex",
                  flexDirection: "column"
                }}
              >
                <Tabs defaultValue="rates" className="flex flex-col h-full">
                  <TabsList className="grid w-full grid-cols-4 mb-4">
                    <TabsTrigger value="rates">Rate Sheet</TabsTrigger>
                    <TabsTrigger value="zones">Zones</TabsTrigger>
                    <TabsTrigger value="services">Services</TabsTrigger>
                    <TabsTrigger value="json">JSON Editor</TabsTrigger>
                  </TabsList>

                  <TabsContent
                    value="rates"
                    className="flex-1 mt-0"
                    style={{
                      height: "calc(100% - 60px)",
                      overflow: "auto"
                    }}
                  >
                    <div style={{ height: "100%", overflow: "auto" }}>
                      <RateSheetTable
                        rateSheetId={rateSheetId}
                        services={localData?.services || []}
                        onAddZone={handleAddZone}
                        onRemoveZone={handleRemoveZone}
                        onAddService={handleAddService}
                        onRemoveService={handleRemoveService}
            onCellChange={handleCellChange}
            onBatchUpdate={isAdmin ? async ({ id, updates }) => {
              try {
                if (batchUpdateRateSheetCells?.mutateAsync) {
                  await batchUpdateRateSheetCells.mutateAsync({ id, updates });
                }
              } catch (e) {
                console.error(e);
                throw e;
              }
            } : undefined}
                      />
                    </div>
                  </TabsContent>

                  <TabsContent
                    value="zones"
                    className="flex-1 mt-0"
                    style={{
                      height: "calc(100% - 60px)",
                      overflowY: "auto"
                    }}
                  >
                    <div className="space-y-3 pr-2">
                      <div className="flex justify-between items-center mb-2">
                        <h3 className="font-semibold">Zones</h3>
                        <div className="space-x-2">
                          <Button size="sm" variant="outline" onClick={handleAddZoneAll}>Add Zone</Button>
                          {(() => {
                            const maxZones = Math.max(0, ...(localData?.services || []).map((s: any) => (s.zones || []).length));
                            return maxZones > 0 ? (
                              <Button size="sm" variant="ghost" onClick={() => handleRemoveZoneAll(maxZones - 1)}>Remove Last Column</Button>
                            ) : null;
                          })()}
                        </div>
                      </div>
                      {(() => {
                        const maxZones = Math.max(0, ...(localData?.services || []).map((s: any) => (s.zones || []).length));
                        return Array.from({ length: maxZones }, (_, i) => {
                          const sample = localData?.services?.[0]?.zones?.[i] || {};
                          return (
                            <div key={i} className="border rounded p-4 bg-white">
                              <div className="flex items-center justify-between mb-3">
                                <h4 className="font-medium">Zone {i + 1}</h4>
                                <Button size="sm" variant="ghost" onClick={() => handleRemoveZoneAll(i)}>Remove Column</Button>
                              </div>
                              <div className="grid grid-cols-2 gap-4">
                                <div>
                                  <Label>Label</Label>
                                  <Input
                                    value={sample.label || ''}
                                    onChange={(e) => handleUpdateZoneFieldAll(i, 'label', e.target.value)}
                                    placeholder={`Zone ${i + 1}`}
                                  />
                                </div>
                                <div>
                                  <Label>Country Codes (comma separated)</Label>
                                  <Input
                                    value={(sample.country_codes || []).join(', ')}
                                    onChange={(e) => handleUpdateZoneFieldAll(i, 'country_codes', e.target.value.split(',').map(v => v.trim()).filter(Boolean))}
                                    placeholder="US, CA, MX"
                                  />
                                </div>
                                <div>
                                  <Label>Cities (comma separated)</Label>
                                  <Input
                                    value={(sample.cities || []).join(', ')}
                                    onChange={(e) => handleUpdateZoneFieldAll(i, 'cities', e.target.value.split(',').map(v => v.trim()).filter(Boolean))}
                                    placeholder="New York, Toronto"
                                  />
                                </div>
                                <div>
                                  <Label>Postal Codes (comma separated)</Label>
                                  <Input
                                    value={(sample.postal_codes || []).join(', ')}
                                    onChange={(e) => handleUpdateZoneFieldAll(i, 'postal_codes', e.target.value.split(',').map(v => v.trim()).filter(Boolean))}
                                    placeholder="10001, 94105"
                                  />
                                </div>
                              </div>
                            </div>
                          );
                        });
                      })()}
                      {((localData?.services || []).every((s: any) => (s.zones || []).length === 0)) && (
                        <div className="text-center py-8 text-gray-500 bg-white border rounded">
                          <p>No zones yet</p>
                          <Button className="mt-3" size="sm" variant="outline" onClick={handleAddZoneAll}>Add Zone</Button>
                        </div>
                      )}
                    </div>
                  </TabsContent>

                  <TabsContent
                    value="services"
                    className="flex-1 mt-0"
                    style={{
                      height: "calc(100% - 60px)",
                      overflowY: "auto"
                    }}
                  >
                    <div className="space-y-4 pr-2">
                      {localData?.services?.map((service: any) => (
                        <div key={service.id} className="border rounded p-4 bg-white">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="font-semibold">{service.service_name}</h3>
                            <div className="space-x-2">
                              <Button size="sm" onClick={() => handleEditService(service)}>Edit</Button>
                              <AlertDialog>
                                <AlertDialogTrigger asChild>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    className="text-red-600 border-red-200 hover:text-red-700"
                                  >
                                    Delete
                                  </Button>
                                </AlertDialogTrigger>
                                <AlertDialogContent>
                                  <AlertDialogHeader>
                                    <AlertDialogTitle>Delete service</AlertDialogTitle>
                                    <AlertDialogDescription>
                                      Are you sure you want to delete "{service.service_name}"? This cannot be undone.
                                    </AlertDialogDescription>
                                  </AlertDialogHeader>
                                  <AlertDialogFooter>
                                    <AlertDialogCancel className="h-8 px-3 text-sm">Cancel</AlertDialogCancel>
                                    <AlertDialogAction
                                      className="h-8 px-3 text-sm bg-red-600 hover:bg-red-700"
                                      onClick={() => handleRemoveService(service.id)}
                                    >
                                      Delete
                                    </AlertDialogAction>
                                  </AlertDialogFooter>
                                </AlertDialogContent>
                              </AlertDialog>
                            </div>
                          </div>
                          <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>Service Code: <code className="text-xs">{service.service_code}</code></div>
                            <div>Currency: <code className="text-xs">{service.currency}</code></div>
                            <div>Transit Days: <code className="text-xs">{service.transit_days || 'N/A'}</code></div>
                            <div>Max Weight: <code className="text-xs">{service.max_weight || 'N/A'} {service.weight_unit}</code></div>
                            <div>Zones: <code className="text-xs">{service.zones?.length || 0}</code></div>
                            <div>Active: <code className="text-xs">{service.active ? 'Yes' : 'No'}</code></div>
                          </div>
                        </div>
                      ))}
                      {localData?.services?.length === 0 && (
                        <div className="text-center py-8 text-gray-500">
                          <p>No services configured yet.</p>
                          <p className="text-sm">Click "Add Service" or "Load Defaults" to get started.</p>
                        </div>
                      )}
                    </div>
                  </TabsContent>

                  <TabsContent
                    value="json"
                    className="flex-1 mt-0"
                    style={{
                      height: "calc(100% - 60px)",
                      overflow: "hidden"
                    }}
                  >
                    <div className="h-full border rounded bg-white overflow-hidden">
                      <CodeMirror
                        height="100%"
                        extensions={[jsonLanguage]}
                        value={failsafe(() => JSON.stringify(localData?.services || [], null, 2), '')}
                        onChange={(value) => {
                          failsafe(() => {
                            const services = JSON.parse(value);
                            setLocalData((prev: any) => ({ ...prev, services }));
                          });
                        }}
                        basicSetup={{
                          lineNumbers: true,
                          foldGutter: true,
                          dropCursor: false,
                          allowMultipleSelections: false,
                          autocompletion: true,
                          bracketMatching: true,
                          highlightSelectionMatches: false,
                          searchKeymap: true,
                        }}
                        style={{
                          fontSize: '14px',
                          height: '100%',
                          overflow: 'auto'
                        }}
                      />
                    </div>
                  </TabsContent>
                </Tabs>
              </div>
            </div>
          </div>
        </SheetContent>
      </Sheet>

      {/* Service Editor Modal */}
      <ServiceEditorModal
        service={editingService}
        isOpen={serviceModalOpen}
        onClose={() => {
          setServiceModalOpen(false);
          setEditingService(null);
        }}
        onSubmit={handleServiceSubmit}
      />
    </>
  );
};
