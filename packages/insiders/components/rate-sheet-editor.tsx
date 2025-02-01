import { CarrierNameEnum } from "@karrio/types/graphql/admin/types";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Button } from "./ui/button";
import { useState } from "react";
import { cn } from "@karrio/insiders/lib/utils";
import { Loader2, Plus } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { ScrollArea } from "./ui/scroll-area";
import CodeMirror from "@uiw/react-codemirror";
import { json } from "@codemirror/lang-json";

interface RateSheetEditorProps {
  sheet?: any;
  onSubmit: (values: any) => Promise<any>;
  isLoading?: boolean;
}

const DEFAULT_SERVICE = {
  service_name: "STANDARD Courier",
  service_code: "standard_courier",
  carrier_service_code: null,
  description: null,
  active: true,
  currency: "AUD",
  transit_days: 1,
  transit_time: 4,
  max_width: 50,
  max_height: 50,
  max_length: 50,
  dimension_unit: "CM",
  weight_unit: "KG",
  zones: [
    {
      label: null,
      rate: 36.63,
      min_weight: null,
      max_weight: null,
      transit_days: null,
      cities: ["ALEXANDER HEIGHTS"],
      postal_codes: null,
      country_codes: null,
    },
  ],
};

const DEFAULT_STATE = {
  carrier_name: "generic",
  name: "",
  services: [DEFAULT_SERVICE],
};

export function RateSheetEditor({ sheet, onSubmit, isLoading }: RateSheetEditorProps) {
  const [formData, setFormData] = useState(sheet || DEFAULT_STATE);
  const [selectedService, setSelectedService] = useState(0);
  const [jsonMode, setJsonMode] = useState(false);

  const handleBasicInfoChange = (field: string) => (e: any) => {
    setFormData((prev: any) => ({
      ...prev,
      [field]: e.target.value || e,
    }));
  };

  const handleServiceChange = (field: string) => (e: any) => {
    setFormData((prev: any) => ({
      ...prev,
      services: prev.services.map((service: any, idx: number) =>
        idx === selectedService
          ? { ...service, [field]: e.target.value || e }
          : service
      ),
    }));
  };

  const handleJsonChange = (value: string) => {
    try {
      const parsed = JSON.parse(value);
      setFormData(parsed);
    } catch (error) {
      // Handle JSON parse error
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit(formData);
  };

  const addService = () => {
    setFormData((prev: any) => ({
      ...prev,
      services: [...prev.services, { ...DEFAULT_SERVICE }],
    }));
    setSelectedService(formData.services.length);
  };

  const removeService = (index: number) => {
    setFormData((prev: any) => ({
      ...prev,
      services: prev.services.filter((_: any, idx: number) => idx !== index),
    }));
    setSelectedService(Math.max(0, selectedService - 1));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8 max-w-3xl">
      <div className="space-y-6">
        <div>
          <h3 className="text-base font-medium mb-1">Basic Information</h3>
          <p className="text-sm text-muted-foreground mb-4">
            Configure the basic settings for your rate sheet.
          </p>
          <div className="space-y-4 bg-white rounded-lg border p-4">
            <div className="grid gap-4">
              <div className="space-y-2">
                <Label className="text-sm font-medium">Carrier Name</Label>
                <Select
                  value={formData.carrier_name}
                  onValueChange={handleBasicInfoChange("carrier_name")}
                  disabled={!!formData.id}
                >
                  <SelectTrigger className="h-9">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(CarrierNameEnum).map(([key, value]) => (
                      <SelectItem key={value} value={value}>
                        {key.split("_").map(word => word.charAt(0) + word.slice(1).toLowerCase()).join(" ")}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-sm font-medium">Rate Sheet Name</Label>
                <Input
                  className="h-9"
                  value={formData.name}
                  onChange={(e) => handleBasicInfoChange("name")(e.target.value)}
                  placeholder="Enter rate sheet name"
                />
              </div>
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-base font-medium mb-1">Services</h3>
          <p className="text-sm text-muted-foreground mb-4">
            Configure shipping services and their rates.
          </p>
          <div className="space-y-4">
            <div className="grid grid-cols-[250px,1fr] gap-4">
              <div className="bg-white rounded-lg border p-4">
                <div className="space-y-2">
                  {formData.services.map((service: any, idx: number) => (
                    <div
                      key={idx}
                      className={cn(
                        "p-3 border rounded-md cursor-pointer hover:bg-accent/50 transition-colors",
                        selectedService === idx && "bg-accent"
                      )}
                      onClick={() => setSelectedService(idx)}
                    >
                      <div className="flex justify-between items-center">
                        <div>
                          <h4 className="font-medium text-sm">{service.service_name}</h4>
                          <p className="text-xs text-muted-foreground">{service.service_code}</p>
                        </div>
                        {formData.services.length > 1 && (
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-7 text-xs"
                            onClick={(e) => {
                              e.stopPropagation();
                              removeService(idx);
                            }}
                          >
                            Remove
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
                  <Button
                    variant="outline"
                    size="sm"
                    className="w-full text-xs"
                    onClick={addService}
                  >
                    <Plus className="h-3 w-3 mr-1" />
                    Add Service
                  </Button>
                </div>
              </div>

              <div className="bg-white rounded-lg border p-4">
                {formData.services[selectedService] && (
                  <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label className="text-sm font-medium">Service Name</Label>
                        <Input
                          className="h-9"
                          value={formData.services[selectedService].service_name}
                          onChange={(e) => handleServiceChange("service_name")(e.target.value)}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label className="text-sm font-medium">Service Code</Label>
                        <Input
                          className="h-9"
                          value={formData.services[selectedService].service_code}
                          onChange={(e) => handleServiceChange("service_code")(e.target.value)}
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label className="text-sm font-medium">Currency</Label>
                        <Select
                          value={formData.services[selectedService].currency}
                          onValueChange={handleServiceChange("currency")}
                        >
                          <SelectTrigger className="h-9">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="AUD">AUD</SelectItem>
                            <SelectItem value="USD">USD</SelectItem>
                            <SelectItem value="EUR">EUR</SelectItem>
                            <SelectItem value="GBP">GBP</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label className="text-sm font-medium">Transit Days</Label>
                        <Input
                          className="h-9"
                          type="number"
                          value={formData.services[selectedService].transit_days}
                          onChange={(e) => handleServiceChange("transit_days")(parseInt(e.target.value))}
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                      <div className="space-y-2">
                        <Label className="text-sm font-medium">Max Width (cm)</Label>
                        <Input
                          className="h-9"
                          type="number"
                          value={formData.services[selectedService].max_width}
                          onChange={(e) => handleServiceChange("max_width")(parseInt(e.target.value))}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label className="text-sm font-medium">Max Height (cm)</Label>
                        <Input
                          className="h-9"
                          type="number"
                          value={formData.services[selectedService].max_height}
                          onChange={(e) => handleServiceChange("max_height")(parseInt(e.target.value))}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label className="text-sm font-medium">Max Length (cm)</Label>
                        <Input
                          className="h-9"
                          type="number"
                          value={formData.services[selectedService].max_length}
                          onChange={(e) => handleServiceChange("max_length")(parseInt(e.target.value))}
                        />
                      </div>
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-4">
                        <Label className="text-sm font-medium">Zones</Label>
                        <Button variant="outline" size="sm" className="h-7 text-xs">
                          <Plus className="h-3 w-3 mr-1" />
                          Add Zone
                        </Button>
                      </div>
                      <div className="border rounded-lg overflow-hidden">
                        <Table>
                          <TableHeader>
                            <TableRow>
                              <TableHead className="text-xs">Rate</TableHead>
                              <TableHead className="text-xs">Min Weight</TableHead>
                              <TableHead className="text-xs">Max Weight</TableHead>
                              <TableHead className="text-xs">Cities</TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {formData.services[selectedService].zones.map((zone: any, idx: number) => (
                              <TableRow key={idx}>
                                <TableCell className="text-sm">{zone.rate}</TableCell>
                                <TableCell className="text-sm">{zone.min_weight || '-'}</TableCell>
                                <TableCell className="text-sm">{zone.max_weight || '-'}</TableCell>
                                <TableCell className="text-sm">{zone.cities?.join(", ") || '-'}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
  );
}
