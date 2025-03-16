import { GetSystemConnections_system_carrier_connections_edges_node } from "@karrio/types/graphql/admin/types";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/ui/components/ui/table";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { Button } from "@karrio/ui/components/ui/button";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Copy, ChevronLeft, ChevronRight, Pencil, Trash2 } from "lucide-react";
import { isNoneOrEmpty } from "@karrio/lib";

export type Connection = GetSystemConnections_system_carrier_connections_edges_node & {
  credentials: Record<string, any>;
  config: Record<string, any>;
  metadata: Record<string, any>;
};

interface CarrierConnectionsTableProps {
  connections?: Connection[];
  onEdit: (connection: Connection) => void;
  onDelete: (connection: Connection) => void;
  onStatusChange: (connection: Connection, active: boolean) => void;
  onCopy: (text: string, description: string) => void;
  title?: string;
  onCreateNew?: () => void;
  pagination?: {
    count: number;
    hasNext: boolean;
    page: number;
    pageSize?: number;
  };
  onPageChange?: (page: number) => void;
  onPageSizeChange?: (pageSize: number) => void;
}

export function CarrierConnectionsTable({
  connections = [],
  onEdit,
  onDelete,
  onStatusChange,
  onCopy,
  title,
  onCreateNew,
  pagination,
  onPageChange,
  onPageSizeChange,
}: CarrierConnectionsTableProps) {
  // Calculate start and end indices for current page
  const pageSize = pagination?.pageSize || 10;
  const startIndex = pagination ? (pagination.page - 1) * pageSize : 0;
  const endIndex = pagination ? startIndex + pageSize : connections.length;
  const currentPageConnections = pagination ? connections.slice(startIndex, endIndex) : connections;

  if (connections.length === 0) {
    return (
      <div className="space-y-4">
        {title && (
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">{title}</h2>
            {onCreateNew && (
              <Button onClick={onCreateNew}>Add Connection</Button>
            )}
          </div>
        )}
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <p className="text-sm text-muted-foreground">No carrier connections found</p>
          <p className="text-sm text-muted-foreground">Add a connection to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {title && (
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">{title}</h2>
          {onCreateNew && (
            <Button onClick={onCreateNew}>Add Connection</Button>
          )}
        </div>
      )}
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Connection</TableHead>
            <TableHead>Capabilities</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="w-[50px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {currentPageConnections?.map((connection) => (
            <TableRow key={connection.id}>
              <TableCell>
                <div className="flex items-center space-x-4">
                  <div className="flex-none w-[48px] h-[48px]">
                    <CarrierImage
                      carrier_name={connection.carrier_name}
                      width={48}
                      height={48}
                    />
                  </div>
                  <div className="space-y-1">
                    <div className="font-medium space-x-1">
                      <span>{connection.carrier_id}</span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-3 w-3 p-0 hover:bg-transparent"
                        onClick={() => onCopy(connection.carrier_id, "Carrier ID has been copied to your clipboard")}
                      >
                        <Copy className="h-2.5 w-2.5" />
                      </Button>
                    </div>
                    <div className="flex items-center space-x-1 text-xs text-gray-400">
                      <span>{connection.id}</span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-3 w-3 p-0 hover:bg-transparent"
                        onClick={() => onCopy(connection.id, "Connection ID has been copied to your clipboard")}
                      >
                        <Copy className="h-2.5 w-2.5" />
                      </Button>
                    </div>
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <div className="flex flex-wrap gap-1">
                  {!isNoneOrEmpty(connection.capabilities) &&
                    connection.capabilities?.map((capability) => (
                      <Badge
                        key={capability}
                        variant="secondary"
                        className="whitespace-nowrap text-[10px] px-1.5 py-0"
                      >
                        {capability}
                      </Badge>
                    ))}
                </div>
              </TableCell>
              <TableCell>
                <Switch
                  checked={connection.active}
                  onCheckedChange={(checked) => onStatusChange(connection, checked)}
                />
              </TableCell>
              <TableCell>
                <div className="flex items-center gap-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={() => onEdit(connection)}
                  >
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 text-red-600 hover:text-red-600 hover:bg-red-100"
                    onClick={() => onDelete(connection)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {pagination && (
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <p className="text-sm text-muted-foreground">
              Showing {startIndex + 1} to {Math.min(endIndex, connections.length)} of {connections.length} connections
            </p>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-muted-foreground">Items per page:</span>
              <Select
                value={String(pageSize)}
                onValueChange={(value) => onPageSizeChange?.(Number(value))}
              >
                <SelectTrigger className="h-8 w-[70px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="5">5</SelectItem>
                  <SelectItem value="10">10</SelectItem>
                  <SelectItem value="20">20</SelectItem>
                  <SelectItem value="50">50</SelectItem>
                  <SelectItem value="100">100</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onPageChange?.(pagination.page - 1)}
              disabled={pagination.page <= 1}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onPageChange?.(pagination.page + 1)}
              disabled={!pagination.hasNext}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
