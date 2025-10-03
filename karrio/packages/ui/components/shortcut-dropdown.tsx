"use client";

import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@karrio/ui/components/ui/dropdown-menu";
import { Plus, Link, Package, FileText, MapPin } from "lucide-react";
import { AppLink } from '@karrio/ui/core/components/app-link';
import { Button } from "@karrio/ui/components/ui/button";

export function ShortcutDropdown() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="default" size="icon" className="rounded-full !rounded-full border-radius-50">
          <Plus className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel className="text-xs font-semibold text-gray-500 uppercase">
          Online Shipment
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild>
          <AppLink href="/connections?modal=new" className="flex items-center">
            <Link className="h-4 w-4 mr-2" />
            Carrier account
          </AppLink>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <AppLink href="/draft_orders/new" className="flex items-center">
            <Package className="h-4 w-4 mr-2" />
            Create order
          </AppLink>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <AppLink href="/create_label?shipment_id=new" className="flex items-center">
            <FileText className="h-4 w-4 mr-2" />
            Shipping label
          </AppLink>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <AppLink href="/trackers?modal=new" className="flex items-center">
            <MapPin className="h-4 w-4 mr-2" />
            Package tracker
          </AppLink>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
