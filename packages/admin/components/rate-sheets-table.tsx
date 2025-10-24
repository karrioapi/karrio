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
      <div className="text-center py-12">
        <div className="mx-auto mb-4 text-gray-400">
          <svg className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-500 mb-2">
          No rate sheets found
        </h3>
        <p className="text-sm text-gray-400 mb-4">
          Get started by creating your first rate sheet to manage custom carrier pricing.
        </p>
        <Button onClick={onCreateNew}>
          <Plus className="h-4 w-4 mr-2" />
          Create Your First Rate Sheet
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
