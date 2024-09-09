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
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@karrio/insiders/components/ui/dropdown-menu";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { MoreHorizontal, Plus, FileText } from "lucide-react";
import { Badge } from "@karrio/insiders/components/ui/badge";
import {
  Tabs,
  TabsList,
  TabsTrigger,
} from "@karrio/insiders/components/ui/tabs";

export const generateMetadata = dynamicMetadata("Orders");
export const description =
  "A page displaying a list of orders using a data table with sorting, filtering, and status tabs.";

// Sample order data
const orders = [
  {
    id: "100003",
    status: "unfulfilled",
    items: "2 items (purpleship sticker)",
    shipTo: "Convention center, Las Vegas NV, 89109, US",
    total: "70 CAD",
    date: "Mar 13, 11:31 AM",
    shippingService: "STANDARD SERVICE",
  },
  {
    id: "100002",
    status: "unfulfilled",
    items: "1 item (iPod Nano)",
    shipTo: "Jane Doe, Vancouver BC, V6M2V9, CA",
    total: "300 USD",
    date: "Mar 8, 12:01 PM",
    shippingService: "UNFULFILLED",
  },
  {
    id: "345098457777",
    status: "fulfilled",
    items: "3 items (Multiple)",
    shipTo: "Jane Doe, Vancouver BC, V6M2V9, CA",
    total: "219.89 USD",
    date: "Feb 10, 01:52 AM",
    shippingService: "UPS EXPRESS SAVER CA",
  },
  {
    id: "1003",
    status: "fulfilled",
    items: "3 items (purpleship sticker)",
    shipTo: "Daniel K, Montréal QC, H3E1W6, CA",
    total: "105 CAD",
    date: "Jan 23, 01:20 AM",
    shippingService: "STANDARD SERVICE",
  },
  // Add more order data as needed
];

export default function OrdersPage() {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "fulfilled":
        return "bg-green-500 hover:bg-green-600";
      case "unfulfilled":
        return "bg-yellow-500 hover:bg-yellow-600";
      case "cancelled":
        return "bg-red-500 hover:bg-red-600";
      default:
        return "bg-gray-500 hover:bg-gray-600";
    }
  };

  return (
    <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold md:text-2xl">Orders</h1>
        <div className="flex gap-2">
          <Button variant="outline">
            <FileText className="mr-2 h-4 w-4" />
            Manage manifests
          </Button>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Create order
          </Button>
        </div>
      </div>

      <Tabs defaultValue="all">
        <TabsList>
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="unfulfilled">Unfulfilled</TabsTrigger>
          <TabsTrigger value="fulfilled">Fulfilled</TabsTrigger>
          <TabsTrigger value="cancelled">Cancelled</TabsTrigger>
          <TabsTrigger value="drafts">Drafts</TabsTrigger>
        </TabsList>
      </Tabs>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">ORDER #</TableHead>
            <TableHead>ITEMS</TableHead>
            <TableHead></TableHead>
            <TableHead>SHIP TO</TableHead>
            <TableHead>TOTAL</TableHead>
            <TableHead>DATE</TableHead>
            <TableHead>SHIPPING SERVICE</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {orders.map((order) => (
            <TableRow key={order.id}>
              <TableCell className="font-medium">{order.id}</TableCell>
              <TableCell>{order.items}</TableCell>
              <TableCell>
                <Badge className={`ml-2 ${getStatusColor(order.status)}`}>
                  {order.status}
                </Badge>
              </TableCell>
              <TableCell>{order.shipTo}</TableCell>
              <TableCell>{order.total}</TableCell>
              <TableCell>{order.date}</TableCell>
              <TableCell>{order.shippingService}</TableCell>
              <TableCell className="text-right">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="h-8 w-8 p-0">
                      <span className="sr-only">Open menu</span>
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Actions</DropdownMenuLabel>
                    <DropdownMenuItem>Create label</DropdownMenuItem>
                    <DropdownMenuItem>View order</DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem>Cancel order</DropdownMenuItem>
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
