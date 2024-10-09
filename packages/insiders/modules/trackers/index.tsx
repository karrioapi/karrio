"use client";

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
  DropdownMenuTrigger,
} from "@karrio/insiders/components/ui/dropdown-menu";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { MoreHorizontal, Trash2 } from "lucide-react";
import { Badge } from "@karrio/insiders/components/ui/badge";
import {
  Tabs,
  TabsList,
  TabsTrigger,
} from "@karrio/insiders/components/ui/tabs";
import { p } from "@karrio/lib";

export const generateMetadata = dynamicMetadata("Trackers");
export const description =
  "A page displaying a list of shipment trackers with status and last event information.";

// Sample tracker data
const trackers = [
  {
    id: "275260192970",
    carrier: "fedex",
    service: "FEDEX INTERNATIONAL PRIORITY",
    status: "on hold",
    lastEvent: "Return tracking number",
    date: "2024-01-10 14:53",
  },
  {
    id: "794960527025",
    carrier: "fedex",
    service: "FEDEX PRIORITY OVERNIGHT",
    status: "pending",
    lastEvent: "Label created and ready for shipment",
    date: "2024-03-22 16:47",
  },
  {
    id: "123456789012",
    carrier: "canadapost",
    service: "CANADAPOST XPRESSPOST",
    status: "pending",
    lastEvent: "Label created and ready for shipment",
    date: "2024-03-04 06:41",
  },
  {
    id: "1ZXXXXXXXXXXXXXXXXX",
    carrier: "ups",
    service: "UPS EXPRESS SAVER CA",
    status: "pending",
    lastEvent: "Label created and ready for shipment",
    date: "2024-02-10 22:46",
  },
  {
    id: "329033206411",
    carrier: "purolator",
    service: "PUROLATOR GROUND",
    status: "delivered",
    lastEvent: "Shipment delivered to",
    date: "2015-10-01 16:43",
  },
  // Add more tracker data as needed
];

export default function TrackersPage() {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "delivered":
        return "bg-green-500 hover:bg-green-600";
      case "pending":
        return "bg-blue-500 hover:bg-blue-600";
      case "on hold":
        return "bg-yellow-500 hover:bg-yellow-600";
      case "exception":
        return "bg-red-500 hover:bg-red-600";
      default:
        return "bg-gray-500 hover:bg-gray-600";
    }
  };

  return (
    <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold md:text-2xl">Trackers</h1>
        <Button>Track a Shipment</Button>
      </div>

      <Tabs defaultValue="all">
        <TabsList>
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="in-transit">In-Transit</TabsTrigger>
          <TabsTrigger value="pending">Pending</TabsTrigger>
          <TabsTrigger value="exception">Exception</TabsTrigger>
          <TabsTrigger value="delivered">Delivered</TabsTrigger>
          <TabsTrigger value="failed">Failed</TabsTrigger>
        </TabsList>
      </Tabs>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>SHIPPING SERVICE</TableHead>
            <TableHead>LAST EVENT</TableHead>
            <TableHead className="text-right">DATE</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {trackers.map((tracker) => (
            <TableRow key={tracker.id}>
              <TableCell>
                <div className="flex items-center">
                  <img
                    src={p`/carriers/${tracker.carrier.toLowerCase()}_icon.svg`}
                    alt={tracker.carrier}
                    className="w-8 h-8 mr-2"
                  />
                  <div>
                    <div className="font-medium">{tracker.id}</div>
                    <div className="text-sm text-gray-500">
                      {tracker.service}
                    </div>
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <Badge className={`${getStatusColor(tracker.status)}`}>
                  {tracker.status}
                </Badge>
                <span className="ml-2">{tracker.lastEvent}</span>
              </TableCell>
              <TableCell className="text-right">{tracker.date}</TableCell>
              <TableCell className="text-right">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="h-8 w-8 p-0">
                      <span className="sr-only">Open menu</span>
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>View details</DropdownMenuItem>
                    <DropdownMenuItem>
                      <Trash2 className="mr-2 h-4 w-4" />
                      <span>Delete</span>
                    </DropdownMenuItem>
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
