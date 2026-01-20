import React from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Badge } from "./ui/badge";
import { Checkbox } from "./ui/checkbox";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogBody, DialogFooter } from "./ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
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
  Package,
  Plus,
  MoreHorizontal,
  Edit,
  Trash2,
  CheckCircle
} from "lucide-react";
import { ConfirmationDialog } from "./confirmation-dialog";
import { ParcelForm, ParcelFormRef } from "./parcel-form";
import { getURLSearchParams, isNoneOrEmpty } from "@karrio/lib";
import {
  useParcelMutation,
  useParcels,
} from "@karrio/hooks/parcel";
import { ParcelType, NotificationType } from "@karrio/types";
import { useSearchParams } from "next/navigation";
import { useNotifier } from "@karrio/ui/core/components/notifier";

// Helper function to extract parcel fields from template (exclude template metadata)
const extractParcelFromTemplate = (template: any) => {
  if (!template) return {};
  const { id, label, is_default, object_type, meta, created_at, updated_at, created_by, ...parcelData } = template;
  return parcelData;
};

interface ParcelEditDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  parcelTemplate?: any;
  onSave: () => void;
}

function ParcelEditDialog({
  open,
  onOpenChange,
  parcelTemplate,
  onSave
}: ParcelEditDialogProps) {
  const notifier = useNotifier();
  const { createParcel, updateParcel } = useParcelMutation();
  const [formData, setFormData] = React.useState({
    label: "",
    is_default: false,
    parcel: {},
  });
  const parcelFormRef = React.useRef<ParcelFormRef>(null);

  React.useEffect(() => {
    if (parcelTemplate) {
      setFormData({
        label: parcelTemplate.meta?.label || "",
        is_default: parcelTemplate.meta?.is_default || false,
        parcel: extractParcelFromTemplate(parcelTemplate),
      });
    } else {
      setFormData({
        label: "",
        is_default: false,
        parcel: {},
      });
    }
  }, [parcelTemplate, open]);

  const handleParcelChange = (parcel: Partial<ParcelType>) => {
    setFormData(prev => ({ ...prev, parcel }));
  };

  const handleSubmit = async (parcel: Partial<ParcelType>) => {
    try {
      const payload = {
        ...formData,
        parcel,
      };

      if (parcelTemplate) {
        const { update_parcel } = await updateParcel.mutateAsync({ ...payload, id: parcelTemplate.id } as any);
        if (update_parcel.errors && update_parcel.errors.length > 0) {
          const errorMessage = update_parcel.errors.map(e => `${e.field}: ${e.messages.join(', ')}`).join('\n');
          notifier.notify({
            type: NotificationType.error,
            message: errorMessage,
          });
          return;
        }
        notifier.notify({
          type: NotificationType.success,
          message: "Parcel updated successfully!",
        });
      } else {
        const { create_parcel } = await createParcel.mutateAsync(payload as any);
        if (create_parcel.errors && create_parcel.errors.length > 0) {
          const errorMessage = create_parcel.errors.map(e => `${e.field}: ${e.messages.join(', ')}`).join('\n');
          notifier.notify({
            type: NotificationType.error,
            message: errorMessage,
          });
          return;
        }
        notifier.notify({
          type: NotificationType.success,
          message: "Parcel created successfully!",
        });
      }

      onSave();
      onOpenChange(false);
    } catch (error: any) {
      const detailed = error?.data || error?.response?.data || error;
      notifier.notify({
        type: NotificationType.error,
        message: detailed || { message: error?.message || "Failed to save parcel" },
      });
    }
  };

  const handleSaveClick = () => {
    parcelFormRef.current?.submit();
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>
            {parcelTemplate ? "Edit Parcel" : "Create Parcel"}
          </DialogTitle>
          <DialogDescription>
            {parcelTemplate
              ? "Update the parcel details."
              : "Create a new parcel for reuse."
            }
          </DialogDescription>
        </DialogHeader>

        <DialogBody className="p-4 pb-8">
          <div className="space-y-3">
            <div className="space-y-1">
              <Label htmlFor="label" className="text-xs text-slate-700">
                Label <span className="text-red-500">*</span>
              </Label>
              <Input
                id="label"
                placeholder="e.g., Small Box, Large Envelope"
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
              <Label htmlFor="is_default" className="text-xs text-slate-700">Set as default parcel</Label>
            </div>

            <div className="border-t pt-3">
              <ParcelForm
                ref={parcelFormRef}
                value={formData.parcel}
                onChange={handleParcelChange}
                onSubmit={handleSubmit}
                showSubmitButton={false}
                showTemplateSelector={true}
              />
            </div>
          </div>
        </DialogBody>

        <DialogFooter>
          <Button variant="outline" size="sm" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button size="sm" onClick={handleSaveClick} disabled={!formData.label.trim()}>
            {parcelTemplate ? "Update Parcel" : "Create Parcel"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function ParcelDescription({ parcel }: { parcel: any }) {
  if (!parcel) return <span className="text-muted-foreground">-</span>;

  const dimensions = [parcel.length, parcel.width, parcel.height]
    .filter(Boolean)
    .join(' × ');

  return (
    <div className="space-y-1">
      <div className="text-sm font-medium">
        {parcel.weight} {parcel.weight_unit}
        {dimensions && (
          <span className="text-muted-foreground">
            {' • '}{dimensions} {parcel.dimension_unit}
          </span>
        )}
      </div>
      {parcel.packaging_type && (
        <div className="text-xs text-muted-foreground capitalize">
          {parcel.packaging_type.replace('_', ' ')}
        </div>
      )}
    </div>
  );
}

export function ParcelsManagement() {
  const searchParams = useSearchParams();
  const modal = searchParams.get("modal") as string;
  const mutation = useParcelMutation();
  const [editDialogOpen, setEditDialogOpen] = React.useState(false);
  const [selectedParcel, setSelectedParcel] = React.useState<any>(null);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = React.useState(false);
  const [parcelToDelete, setParcelToDelete] = React.useState<any>(null);

  const {
    query: { data: { parcels } = {}, ...query },
    filter,
    setFilter,
  } = useParcels({
    setVariablesToURL: true,
  });

  const handleEdit = (template: any) => {
    setSelectedParcel(template);
    setEditDialogOpen(true);
  };

  const handleCreate = () => {
    setSelectedParcel(null);
    setEditDialogOpen(true);
  };

  const handleDelete = (template: any) => {
    setParcelToDelete(template);
    setDeleteConfirmOpen(true);
  };

  const confirmDelete = async () => {
    if (parcelToDelete) {
      await mutation.deleteParcel.mutateAsync({ id: parcelToDelete.id });
      setDeleteConfirmOpen(false);
      setParcelToDelete(null);
    }
  };

  const handleSave = () => {
    // Refresh the data
    query.refetch();
  };

  const parcelList = parcels?.edges || [];

  return (
    <div className="space-y-6">
      {parcelList.length > 0 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Manage your parcel templates for shipping packages.
          </p>
          <Button onClick={handleCreate} className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Create Parcel
          </Button>
        </div>
      )}
      
      <div>
        {parcelList.length === 0 ? (
          <div className="text-center py-12">
            <Package className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-muted-foreground mb-2">
              No parcels yet
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Create your first parcel template to get started.
            </p>
            <Button onClick={handleCreate}>
              <Plus className="h-4 w-4 mr-2" />
              Create Parcel
            </Button>
          </div>
        ) : (
          <div className="border-b">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Label</TableHead>
                  <TableHead>Parcel Details</TableHead>
                  <TableHead className="w-12"></TableHead>
                  <TableHead className="w-12"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {parcelList.map(({ node: template }) => (
                  <TableRow key={template.id}>
                    <TableCell className="font-medium">
                      <div className="flex items-center gap-2">
                        {template.meta?.label}
                        {template.meta?.is_default && (
                          <Badge variant="secondary" className="text-xs">
                            <CheckCircle className="h-3 w-3 mr-1" />
                            Default
                          </Badge>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <ParcelDescription parcel={template} />
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

        {parcelList.length > 0 && (
          <div className="flex items-center justify-between pt-4">
            <div className="text-sm text-muted-foreground">
              {parcelList.length} parcel{parcelList.length !== 1 ? 's' : ''}
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                disabled={!parcels?.page_info.has_previous_page}
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
                disabled={!parcels?.page_info.has_next_page}
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

      <ParcelEditDialog
        open={editDialogOpen}
        onOpenChange={setEditDialogOpen}
        parcelTemplate={selectedParcel}
        onSave={handleSave}
      />

      <ConfirmationDialog
        open={deleteConfirmOpen}
        onOpenChange={setDeleteConfirmOpen}
        title="Delete Parcel"
        description={`Are you sure you want to delete "${parcelToDelete?.meta?.label}"? This action cannot be undone.`}
        onConfirm={confirmDelete}
      />
    </div>
  );
}
