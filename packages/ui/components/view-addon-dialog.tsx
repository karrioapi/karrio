"use client";

import React from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "./ui/dialog";
import { Button } from "./ui/button";
import { Label } from "./ui/label";
import { StatusBadge } from "./status-badge";
import { DollarSign, Percent } from 'lucide-react';
import { AddonType } from "@karrio/hooks/admin-addons";

interface ViewAddonDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  addon: AddonType | null;
}

export function ViewAddonDialog({ open, onOpenChange, addon }: ViewAddonDialogProps) {
  if (!addon) return null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            {addon.surcharge_type === 'PERCENTAGE' ? (
              <Percent className="h-5 w-5 text-blue-600" />
            ) : (
              <DollarSign className="h-5 w-5 text-green-600" />
            )}
            {addon.name}
          </DialogTitle>
          <DialogDescription>
            View addon details and configuration
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label className="text-sm font-medium text-gray-600">Amount</Label>
              <p className="text-lg font-semibold">
                {addon.surcharge_type === 'PERCENTAGE' ? `${addon.amount}%` : `$${addon.amount}`}
              </p>
            </div>
            <div>
              <Label className="text-sm font-medium text-gray-600">Status</Label>
              <div className="mt-1">
                <StatusBadge status={addon.active ? "active" : "inactive"} />
              </div>
            </div>
          </div>

          <div>
            <Label className="text-sm font-medium text-gray-600">Addon ID</Label>
            <p className="text-sm font-mono text-gray-900 mt-1">{addon.id}</p>
          </div>

          {addon.carriers && addon.carriers.length > 0 && (
            <div>
              <Label className="text-sm font-medium text-gray-600">Carriers</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {addon.carriers.map((carrier) => (
                  <span
                    key={carrier}
                    className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded"
                  >
                    {carrier.toUpperCase()}
                  </span>
                ))}
              </div>
            </div>
          )}

          {addon.services && addon.services.length > 0 && (
            <div>
              <Label className="text-sm font-medium text-gray-600">Services</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {addon.services.map((service) => (
                  <span
                    key={service}
                    className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded"
                  >
                    {service.replace(/_/g, ' ')}
                  </span>
                ))}
              </div>
            </div>
          )}

          {addon.carrier_accounts && addon.carrier_accounts.length > 0 && (
            <div>
              <Label className="text-sm font-medium text-gray-600">Carrier Accounts</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {addon.carrier_accounts.map((account) => (
                  <span
                    key={account.id}
                    className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded"
                  >
                    {account.carrier_id}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="flex justify-end">
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              Close
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}