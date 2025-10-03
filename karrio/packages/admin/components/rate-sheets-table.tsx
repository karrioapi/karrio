import {
  Table,
  TableBody,
  TableCell,
  TableRow,
} from "@karrio/ui/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { MoreVertical, Copy, Plus } from "lucide-react";
import { isNoneOrEmpty } from "@karrio/lib";
import { GetRateSheets_rate_sheets_edges_node as RateSheet } from "@karrio/types/graphql/admin/types";

interface RateSheetsTableProps {
  rateSheets?: { node: RateSheet }[];
  onEdit: (rateSheet: RateSheet) => void;
  onDelete: (rateSheet: RateSheet) => void;
  onCopy: (text: string, description: string) => void;
  onCreateNew: () => void;
}

export function RateSheetsTable({
  rateSheets = [],
  onEdit,
  onDelete,
  onCopy,
  onCreateNew,
}: RateSheetsTableProps) {
  if (rateSheets.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <p className="text-sm text-muted-foreground">No rate sheets found</p>
        <p className="text-sm text-muted-foreground mb-4">Add a rate sheet to get started</p>
        <Button onClick={onCreateNew}>
          <Plus className="h-4 w-4 mr-2" />
          Add Rate Sheet
        </Button>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-4 flex justify-end">
        <Button onClick={onCreateNew}>
          <Plus className="h-4 w-4 mr-2" />
          Add Rate Sheet
        </Button>
      </div>

      <Table>
        <TableBody>
          {rateSheets?.map(({ node: sheet }) => (
            <TableRow key={sheet.id}>
              <TableCell>
                <div className="flex items-center space-x-4">
                  <div className="space-y-1">
                    <div className="font-medium">{sheet.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {sheet.carrier_name}
                    </div>
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <div className="flex items-center space-x-2">
                  {sheet.services?.map((service) => (
                    <Badge key={service.service_code} variant="secondary">
                      {service.service_name}
                    </Badge>
                  ))}
                </div>
              </TableCell>
              <TableCell className="text-right">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => onEdit(sheet)}>
                      Edit
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => onDelete(sheet)}>
                      Delete
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      onClick={() =>
                        onCopy(sheet.id, "Rate sheet ID copied to clipboard")
                      }
                    >
                      <Copy className="h-4 w-4 mr-2" />
                      Copy ID
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
