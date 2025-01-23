import { GetSystemConnections_system_carrier_connections_edges_node } from "@karrio/types/graphql/admin/types";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/insiders/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@karrio/insiders/components/ui/dropdown-menu";
import { CarrierImage } from "@karrio/ui/components/carrier-image";
import { Button } from "@karrio/insiders/components/ui/button";
import { Switch } from "@karrio/insiders/components/ui/switch";
import { Badge } from "@karrio/insiders/components/ui/badge";
import { MoreVertical, Copy, ChevronLeft, ChevronRight } from "lucide-react";
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
  };
  onPageChange?: (page: number) => void;
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
}: CarrierConnectionsTableProps) {
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
          {connections?.map((connection) => (
            <TableRow key={connection.id}>
              <TableCell>
                <div className="flex items-center space-x-4">
                  <CarrierImage
                    carrier_name={connection.carrier_name}
                    width={40}
                    height={40}
                  />
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
                        className="whitespace-nowrap"
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
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => onEdit(connection)}>
                      Edit
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      onClick={() => onDelete(connection)}
                      className="text-red-600"
                    >
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {pagination && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Showing {connections.length} of {pagination.count} connections
          </p>
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
