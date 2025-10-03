import { Download, MoreHorizontal, Printer, RefreshCw } from "lucide-react";
import { useRouter } from "next/navigation";
import { format } from "date-fns";
import * as React from "react";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/ui/components/ui/table";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import { Input } from "@karrio/ui/components/ui/input";
import { ShipmentStatus } from "../../hooks/use-shipments";

// Status badge colors
const STATUS_COLORS: Record<ShipmentStatus, string> = {
  draft: "bg-gray-100 text-gray-800",
  purchased: "bg-blue-100 text-blue-800",
  cancelled: "bg-red-100 text-red-800",
  shipped: "bg-green-100 text-green-800",
  in_transit: "bg-yellow-100 text-yellow-800",
  delivered: "bg-emerald-100 text-emerald-800",
  needs_attention: "bg-orange-100 text-orange-800",
  out_for_delivery: "bg-indigo-100 text-indigo-800",
  delivery_failed: "bg-rose-100 text-rose-800",
};

// Shipment type
export interface Shipment {
  id: string;
  carrier_name?: string;
  status: ShipmentStatus;
  created_at: string;
  recipient?: {
    person_name?: string;
    company_name?: string;
    city?: string;
    country_code?: string;
  };
  tracking_number?: string;
  service?: string;
  reference?: string;
  selected_rate?: {
    total_charge?: number;
    currency?: string;
  };
}

// Shipment table props
export interface ShipmentsTableProps {
  isLoading?: boolean;
  shipments: Shipment[];
  selectedIds?: string[];
  onSelectChange?: (ids: string[]) => void;
  onRefresh?: () => void;
  onViewShipment?: (id: string) => void;
  onStatusFilter?: (status: ShipmentStatus[]) => void;
  onSearchChange?: (search: string) => void;
}

export function ShipmentsTable({
  isLoading = false,
  shipments = [],
  selectedIds = [],
  onSelectChange,
  onRefresh,
  onViewShipment,
  onStatusFilter,
  onSearchChange,
}: ShipmentsTableProps) {
  const [searchQuery, setSearchQuery] = React.useState("");
  const router = useRouter();

  // Handle selection change
  const handleSelectAll = React.useCallback(
    (checked: boolean) => {
      if (checked) {
        onSelectChange?.(shipments.map((s) => s.id));
      } else {
        onSelectChange?.([]);
      }
    },
    [shipments, onSelectChange]
  );

  const handleSelectOne = React.useCallback(
    (id: string, checked: boolean) => {
      if (checked) {
        onSelectChange?.([...selectedIds, id]);
      } else {
        onSelectChange?.(selectedIds.filter((selectedId) => selectedId !== id));
      }
    },
    [selectedIds, onSelectChange]
  );

  // Handle search input
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchQuery(value);
    onSearchChange?.(value);
  };

  // Handle view shipment
  const handleViewShipment = (id: string) => {
    if (onViewShipment) {
      onViewShipment(id);
    } else {
      router.push(`/shipments/${id}`);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row justify-between gap-4">
        <div className="flex items-center gap-2">
          <Select
            onValueChange={(value) => {
              const statuses = value.split(",") as ShipmentStatus[];
              onStatusFilter?.(statuses);
            }}
            defaultValue="purchased,in_transit,out_for_delivery,delivery_failed"
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="draft">Draft</SelectItem>
              <SelectItem value="purchased">Purchased</SelectItem>
              <SelectItem value="cancelled">Cancelled</SelectItem>
              <SelectItem value="shipped,in_transit,out_for_delivery">In Transit</SelectItem>
              <SelectItem value="delivered">Delivered</SelectItem>
              <SelectItem value="needs_attention,delivery_failed">Issues</SelectItem>
              <SelectItem value="purchased,in_transit,out_for_delivery,delivery_failed">Active</SelectItem>
              <SelectItem value="draft,purchased,cancelled,shipped,in_transit,delivered,needs_attention,out_for_delivery,delivery_failed">All</SelectItem>
            </SelectContent>
          </Select>
          <Button
            variant="outline"
            size="icon"
            onClick={onRefresh}
            disabled={isLoading}
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <div className="relative">
          <Input
            placeholder="Search shipments..."
            value={searchQuery}
            onChange={handleSearchChange}
            className="max-w-sm"
          />
        </div>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[40px]">
                <Checkbox
                  checked={
                    shipments.length > 0 && selectedIds.length === shipments.length
                  }
                  onCheckedChange={handleSelectAll}
                  disabled={shipments.length === 0}
                  aria-label="Select all"
                />
              </TableHead>
              <TableHead className="w-[100px]">Status</TableHead>
              <TableHead className="w-[180px]">Created</TableHead>
              <TableHead className="w-[180px]">Recipient</TableHead>
              <TableHead>Tracking #</TableHead>
              <TableHead>Service</TableHead>
              <TableHead>Reference</TableHead>
              <TableHead className="text-right">Amount</TableHead>
              <TableHead className="w-[70px]"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={9} className="h-24 text-center">
                  Loading shipments...
                </TableCell>
              </TableRow>
            ) : shipments.length === 0 ? (
              <TableRow>
                <TableCell colSpan={9} className="h-24 text-center">
                  No shipments found.
                </TableCell>
              </TableRow>
            ) : (
              shipments.map((shipment) => (
                <TableRow
                  key={shipment.id}
                  className="cursor-pointer hover:bg-gray-50"
                  onClick={() => handleViewShipment(shipment.id)}
                >
                  <TableCell onClick={(e) => e.stopPropagation()}>
                    <Checkbox
                      checked={selectedIds.includes(shipment.id)}
                      onCheckedChange={(checked) =>
                        handleSelectOne(shipment.id, checked as boolean)
                      }
                      aria-label={`Select shipment ${shipment.id}`}
                    />
                  </TableCell>
                  <TableCell>
                    <Badge
                      variant="outline"
                      className={`${STATUS_COLORS[shipment.status] || "bg-gray-100 text-gray-800"}`}
                    >
                      {shipment.status.replace("_", " ")}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {shipment.created_at
                      ? format(new Date(shipment.created_at), "MMM d, yyyy")
                      : "N/A"}
                  </TableCell>
                  <TableCell>
                    <div className="font-medium">
                      {shipment.recipient?.person_name || "N/A"}
                    </div>
                    <div className="text-sm text-gray-500">
                      {[
                        shipment.recipient?.company_name,
                        shipment.recipient?.city,
                        shipment.recipient?.country_code,
                      ]
                        .filter(Boolean)
                        .join(", ") || "N/A"}
                    </div>
                  </TableCell>
                  <TableCell>{shipment.tracking_number || "N/A"}</TableCell>
                  <TableCell>{shipment.service || "N/A"}</TableCell>
                  <TableCell>{shipment.reference || "N/A"}</TableCell>
                  <TableCell className="text-right">
                    {shipment.selected_rate?.total_charge
                      ? `${shipment.selected_rate.total_charge} ${shipment.selected_rate.currency || ""
                      }`
                      : "N/A"}
                  </TableCell>
                  <TableCell onClick={(e) => e.stopPropagation()}>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          variant="ghost"
                          className="h-8 w-8 p-0"
                        >
                          <span className="sr-only">Open menu</span>
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem
                          onClick={() => handleViewShipment(shipment.id)}
                        >
                          View details
                        </DropdownMenuItem>
                        {shipment.status !== "draft" && (
                          <>
                            <DropdownMenuItem>
                              <Download className="mr-2 h-4 w-4" />
                              Download label
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Printer className="mr-2 h-4 w-4" />
                              Print label
                            </DropdownMenuItem>
                          </>
                        )}
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
