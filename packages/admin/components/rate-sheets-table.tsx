import {
  Table,
  TableBody,
  TableCell,
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
import { Badge } from "@karrio/insiders/components/ui/badge";
import { MoreVertical, Copy } from "lucide-react";
import { isNoneOrEmpty } from "@karrio/lib";
import { GetRateSheets_rate_sheets_edges_node as RateSheet } from "@karrio/types/graphql/admin/types";

interface RateSheetsTableProps {
  rateSheets?: { node: RateSheet }[];
  onEdit: (rateSheet: RateSheet) => void;
  onDelete: (rateSheet: RateSheet) => void;
  onCopy: (text: string, description: string) => void;
}

export function RateSheetsTable({
  rateSheets = [],
  onEdit,
  onDelete,
  onCopy,
}: RateSheetsTableProps) {
  if (rateSheets.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <p className="text-sm text-muted-foreground">No rate sheets found</p>
        <p className="text-sm text-muted-foreground">Add a rate sheet to get started</p>
      </div>
    );
  }

  return (
    <Table>
      <TableBody>
        {rateSheets?.map(({ node: sheet }) => (
          <TableRow key={sheet.id}>
            <TableCell>
              <div className="flex items-center space-x-4">
                <div className="space-y-1">
                  <div className="font-medium">{sheet.name}</div>
                  <div className="flex items-center space-x-1 text-xs text-gray-400">
                    <span>{sheet.id}</span>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-3 w-3 p-0 hover:bg-transparent"
                      onClick={() => onCopy(sheet.id, "Rate sheet ID has been copied to your clipboard")}
                    >
                      <Copy className="h-2.5 w-2.5" />
                    </Button>
                  </div>
                </div>
              </div>
            </TableCell>
            <TableCell>
              <div className="flex items-center space-x-2">
                <CarrierImage
                  carrier_name={sheet.carrier_name}
                  width={24}
                  height={24}
                />
                <span>{sheet.carrier_name}</span>
              </div>
            </TableCell>
            <TableCell>
              <div className="flex flex-wrap gap-1">
                {!isNoneOrEmpty(sheet.services) &&
                  sheet.services?.map((service) => (
                    <Badge
                      key={service.service_code}
                      variant="secondary"
                      className="whitespace-nowrap"
                    >
                      {service.service_code}
                    </Badge>
                  ))}
              </div>
            </TableCell>
            <TableCell>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" className="h-8 w-8">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem onClick={() => onEdit(sheet)}>
                    Edit
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    onClick={() => onDelete(sheet)}
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
  );
}
