import React from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Badge } from "./ui/badge";
import { Checkbox } from "./ui/checkbox";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogBody, DialogFooter } from "./ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "./ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from "./ui/dropdown-menu";
import {
  MapPin,
  Plus,
  MoreHorizontal,
  Edit,
  Trash2,
  CheckCircle
} from "lucide-react";
import { ConfirmationDialog } from "./confirmation-dialog";
import { AddressForm, AddressFormRef } from "./address-form";
import {
  formatAddressLocationShort,
  formatAddressShort,
  getURLSearchParams,
  isNoneOrEmpty,
} from "@karrio/lib";
import {
  useAddressTemplateMutation,
  useAddressTemplates,
} from "@karrio/hooks/address";
import { AddressType, NotificationType } from "@karrio/types";
import { useSearchParams } from "next/navigation";
import { useNotifier } from "@karrio/ui/core/components/notifier";

interface AddressEditDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  addressTemplate?: any;
  onSave: () => void;
}

function AddressEditDialog({
  open,
  onOpenChange,
  addressTemplate,
  onSave
}: AddressEditDialogProps) {
  const notifier = useNotifier();
  const { createAddressTemplate, updateAddressTemplate } = useAddressTemplateMutation();
  const [formData, setFormData] = React.useState({
    label: "",
    is_default: false,
    address: {},
  });
  const addressFormRef = React.useRef<AddressFormRef>(null);

  React.useEffect(() => {
    if (addressTemplate) {
      setFormData({
        label: addressTemplate.label || "",
        is_default: addressTemplate.is_default || false,
        address: addressTemplate.address || {},
      });
    } else {
      setFormData({
        label: "",
        is_default: false,
        address: {},
      });
    }
  }, [addressTemplate, open]);

  const handleAddressChange = (address: Partial<AddressType>) => {
    setFormData(prev => ({ ...prev, address }));
  };

  const handleSubmit = async (address: Partial<AddressType>) => {
    try {
      const payload = {
        ...formData,
        address,
      };

      if (addressTemplate) {
        await updateAddressTemplate.mutateAsync({ ...payload, id: addressTemplate.id });
        notifier.notify({
          type: NotificationType.success,
          message: "Address template updated successfully!",
        });
      } else {
        await createAddressTemplate.mutateAsync(payload);
        notifier.notify({
          type: NotificationType.success,
          message: "Address template created successfully!",
        });
      }

      onSave();
      onOpenChange(false);
    } catch (error: any) {
      notifier.notify({
        type: NotificationType.error,
        message: error.message || "Failed to save address template",
      });
    }
  };

  const handleSaveClick = () => {
    addressFormRef.current?.submit();
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>
            {addressTemplate ? "Edit Address Template" : "Create Address Template"}
          </DialogTitle>
          <DialogDescription>
            {addressTemplate
              ? "Update the address template details."
              : "Create a new address template for reuse."
            }
          </DialogDescription>
        </DialogHeader>

        <DialogBody className="p-4 pb-8">
          <div className="space-y-3">
            <div className="space-y-1">
              <Label htmlFor="label" className="text-xs text-slate-700">
                Template Label <span className="text-red-500">*</span>
              </Label>
              <Input
                id="label"
                placeholder="e.g., Home, Office, Warehouse"
                value={formData.label}
                onChange={(e) => setFormData(prev => ({ ...prev, label: e.target.value }))}
                required
                className="h-8"
              />
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="is_default"
                checked={formData.is_default}
                onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_default: !!checked }))}
              />
              <Label htmlFor="is_default" className="text-xs text-slate-700">Set as default address template</Label>
            </div>

            <div className="border-t pt-3">
              <AddressForm
                ref={addressFormRef}
                value={formData.address}
                onChange={handleAddressChange}
                onSubmit={handleSubmit}
                showSubmitButton={false}
              />
            </div>
          </div>
        </DialogBody>

        <DialogFooter>
          <Button variant="outline" size="sm" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button size="sm" onClick={handleSaveClick}>
            {addressTemplate ? "Update Template" : "Create Template"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export function AddressesManagement() {
  const searchParams = useSearchParams();
  const modal = searchParams.get("modal") as string;
  const { deleteAddressTemplate } = useAddressTemplateMutation();
  const [editDialogOpen, setEditDialogOpen] = React.useState(false);
  const [selectedAddress, setSelectedAddress] = React.useState<any>(null);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = React.useState(false);
  const [addressToDelete, setAddressToDelete] = React.useState<any>(null);

  const {
    query: { data: { address_templates } = {}, ...query },
    filter,
    setFilter,
  } = useAddressTemplates({
    setVariablesToURL: true,
  });

  const handleEdit = (template: any) => {
    setSelectedAddress(template);
    setEditDialogOpen(true);
  };

  const handleCreate = () => {
    setSelectedAddress(null);
    setEditDialogOpen(true);
  };

  const handleDelete = (template: any) => {
    setAddressToDelete(template);
    setDeleteConfirmOpen(true);
  };

  const confirmDelete = async () => {
    if (addressToDelete) {
      await deleteAddressTemplate.mutateAsync({ id: addressToDelete.id });
      setDeleteConfirmOpen(false);
      setAddressToDelete(null);
    }
  };

  const handleSave = () => {
    // Refresh the data
    query.refetch();
  };

  const addresses = address_templates?.edges || [];

  return (
    <div className="space-y-6">
      <div>
        {addresses.length === 0 ? (
          <div className="text-center py-12">
            <MapPin className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-muted-foreground mb-2">
              No addresses yet
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Create your first address template to get started.
            </p>
            <Button onClick={handleCreate}>
              <Plus className="h-4 w-4 mr-2" />
              Create Address
            </Button>
          </div>
        ) : (
          <div className="border-b">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Label</TableHead>
                  <TableHead>Address</TableHead>
                  <TableHead>Contact</TableHead>
                  <TableHead className="w-12"></TableHead>
                  <TableHead className="w-12"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {addresses.map(({ node: template }) => (
                  <TableRow key={template.id}>
                    <TableCell className="font-medium">
                      <div className="flex items-center gap-2">
                        {template.label}
                        {template.is_default && (
                          <Badge variant="secondary" className="text-xs">
                            <CheckCircle className="h-3 w-3 mr-1" />
                            Default
                          </Badge>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="space-y-1">
                        <div className="text-sm">
                          {formatAddressShort(template.address as AddressType)}
                        </div>
                        <div className="text-xs text-muted-foreground">
                          {formatAddressLocationShort(template.address as AddressType)}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="space-y-1">
                        {template.address.email && (
                          <div className="text-sm">{template.address.email}</div>
                        )}
                        {template.address.phone_number && (
                          <div className="text-xs text-muted-foreground">
                            {template.address.phone_number}
                          </div>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleEdit(template)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                    </TableCell>
                    <TableCell>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => handleEdit(template)}>
                            <Edit className="h-4 w-4 mr-2" />
                            Edit
                          </DropdownMenuItem>
                          <DropdownMenuItem
                            onClick={() => handleDelete(template)}
                            className="text-destructive"
                          >
                            <Trash2 className="h-4 w-4 mr-2" />
                            Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}

        {addresses.length > 0 && (
          <div className="flex items-center justify-between pt-4">
            <div className="text-sm text-muted-foreground">
              {addresses.length} address{addresses.length !== 1 ? 'es' : ''}
            </div>

            {/* Pagination would go here if needed */}
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                disabled={!address_templates?.page_info.has_previous_page}
                onClick={() => setFilter({
                  ...filter,
                  offset: Math.max(0, (filter.offset || 0) - 20)
                })}
              >
                Previous
              </Button>
              <Button
                variant="outline"
                size="sm"
                disabled={!address_templates?.page_info.has_next_page}
                onClick={() => setFilter({
                  ...filter,
                  offset: (filter.offset || 0) + 20
                })}
              >
                Next
              </Button>
            </div>
          </div>
        )}
      </div>

      <AddressEditDialog
        open={editDialogOpen}
        onOpenChange={setEditDialogOpen}
        addressTemplate={selectedAddress}
        onSave={handleSave}
      />

      <ConfirmationDialog
        open={deleteConfirmOpen}
        onOpenChange={setDeleteConfirmOpen}
        title="Delete Address Template"
        description={`Are you sure you want to delete "${addressToDelete?.label}"? This action cannot be undone.`}
        onConfirm={confirmDelete}
      />
    </div>
  );
}
