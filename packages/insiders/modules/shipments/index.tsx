"use client";

import { p } from "@karrio/lib";
import { Button } from "@karrio/insiders/components/ui/button";
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
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@karrio/insiders/components/ui/dropdown-menu";
import { Checkbox } from "@karrio/insiders/components/ui/checkbox";
import {
  Tabs,
  TabsList,
  TabsTrigger,
} from "@karrio/insiders/components/ui/tabs";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { Badge } from "@karrio/insiders/components/ui/badge";
import { MoreHorizontal } from "lucide-react";

export const generateMetadata = dynamicMetadata("Shipments");
export const description =
  "A page displaying a list of shipments with detailed information and actions.";

// Sample shipment data
const shipments = [
  {
    id: "0000000225",
    carrier: "TST Overland",
    service: "STANDARD SERVICE",
    status: "purchased",
    recipient: "Jane Doe, Vancouver BC, V6M2V9, CA",
    reference: "",
    date: "Sep 5, 05:28 PM",
  },
  {
    id: "794960527025",
    carrier: "fedex",
    service: "INTERNATIONAL PRIORITY",
    status: "purchased",
    recipient: "Convention center, Las Vegas NV, 89109, US",
    reference: "",
    date: "Sep 5, 05:27 PM",
  },
  {
    id: "794960527025",
    carrier: "fedex",
    service: "INTERNATIONAL PRIORITY",
    status: "purchased",
    recipient: "Convention center, Las Vegas NV, 89109, US",
    reference: "",
    date: "Sep 5, 05:26 PM",
  },
  {
    id: "0000000215",
    carrier: "TST Overland",
    service: "STANDARD SERVICE",
    status: "purchased",
    recipient: "Daniel K, Montréal QC, H3E1W6, CA",
    reference: "",
    date: "Sep 5, 05:25 PM",
  },
  {
    id: "123456789012",
    carrier: "canadapost",
    service: "CANADAPOST XPRESSPOST",
    status: "purchased",
    recipient: "Jane Doe, Vancouver BC, V6M2V9, CA",
    reference: "",
    date: "Mar 3, 10:41 PM",
  },
  {
    id: "123456789012",
    carrier: "canadapost",
    service: "CANADAPOST REGULAR PARCEL",
    status: "cancelled",
    recipient: "Daniel K, Montréal QC, H3E1W6, CA",
    reference: "",
    date: "Feb 29, 04:27 AM",
  },
  {
    id: "00340433330102000132199",
    carrier: "dhl",
    service: "DHL PAKET",
    status: "cancelled",
    recipient: "Maria Musterfrau, Bonn 53113, DE",
    reference: "",
    date: "Feb 25, 05:14 AM",
  },
  {
    id: "1ZXXXXXXXXXXXX",
    carrier: "ups",
    service: "UPS EXPRESS SAVER CA",
    status: "purchased",
    recipient: "Jane Doe, Vancouver BC, V6M2V9, CA",
    reference: "",
    date: "Feb 10, 02:46 PM",
  },
];

export default function ShipmentsPage() {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "purchased":
        return "bg-blue-500 hover:bg-blue-600";
      case "cancelled":
        return "bg-red-500 hover:bg-red-600";
      default:
        return "bg-gray-500 hover:bg-gray-600";
    }
  };

  return (
    <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold md:text-2xl">Shipments</h1>
        <div className="flex gap-2">
          <Button variant="outline">Manage manifests</Button>
          <Button>Create Label</Button>
          <Button variant="outline">
            Filter
            <svg
              className="ml-2 h-4 w-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </Button>
        </div>
      </div>

      <Tabs defaultValue="all">
        <TabsList>
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="purchased">Purchased</TabsTrigger>
          <TabsTrigger value="delivered">Delivered</TabsTrigger>
          <TabsTrigger value="exception">Exception</TabsTrigger>
          <TabsTrigger value="cancelled">Cancelled</TabsTrigger>
          <TabsTrigger value="draft">Draft</TabsTrigger>
        </TabsList>
      </Tabs>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[50px]">
              <Checkbox />
            </TableHead>
            <TableHead>SHIPPING SERVICE</TableHead>
            <TableHead></TableHead>
            <TableHead>RECIPIENT</TableHead>
            <TableHead>REFERENCE</TableHead>
            <TableHead>DATE</TableHead>
            <TableHead className="w-[50px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {shipments.map((shipment) => (
            <TableRow key={shipment.id}>
              <TableCell>
                <Checkbox />
              </TableCell>
              <TableCell>
                <div className="flex items-center space-x-2">
                  <img
                    src={p`/carriers/${shipment.carrier.toLowerCase()}_icon.svg`}
                    alt={shipment.carrier}
                    className="w-8 h-8"
                  />
                  <div>
                    <div className="text-xs font-medium">{shipment.id}</div>
                    <div className="text-xs font-medium text-gray-500">
                      {shipment.service}
                    </div>
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <Badge className={`mt-1 ${getStatusColor(shipment.status)}`}>
                  {shipment.status}
                </Badge>
              </TableCell>
              <TableCell>{shipment.recipient}</TableCell>
              <TableCell>{shipment.reference}</TableCell>
              <TableCell>{shipment.date}</TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="h-8 w-8 p-0">
                      <span className="sr-only">Open menu</span>
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>Print Label</DropdownMenuItem>
                    <DropdownMenuItem>View Shipment</DropdownMenuItem>
                    <DropdownMenuItem>Cancel Shipment</DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem>Mark as IN TRANSIT</DropdownMenuItem>
                    <DropdownMenuItem>Mark as NEEDS ATTENTION</DropdownMenuItem>
                    <DropdownMenuItem>Mark as DELIVERY FAILED</DropdownMenuItem>
                    <DropdownMenuItem>Mark as DELIVERED</DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem>
                      Download Customs Invoice
                    </DropdownMenuItem>
                    <DropdownMenuItem>Download Packing Slip</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </main>
  );
}
