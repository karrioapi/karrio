import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Switch } from "./ui/switch";
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
  DropdownMenuTrigger,
  DropdownMenuSeparator
} from "./ui/dropdown-menu";
import {
  FileText,
  Plus,
  MoreHorizontal,
  Edit,
  Trash2,
  Eye,
  ToggleLeft,
  ToggleRight
} from "lucide-react";
import { ConfirmationDialog } from "./confirmation-dialog";
import {
  useDocumentTemplateMutation,
  useDocumentTemplates,
} from "@karrio/hooks/document-template";
import { useDocumentPrinter } from "@karrio/hooks/resource-token";
import { DocumentTemplateType, NotificationType } from "@karrio/types";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { useRouter } from "next/navigation";


export function TemplatesManagement() {
  const router = useRouter();
  const { notify } = useNotifier();
  const mutation = useDocumentTemplateMutation();
  const documentPrinter = useDocumentPrinter();
  const [deleteConfirmOpen, setDeleteConfirmOpen] = React.useState(false);
  const [templateToDelete, setTemplateToDelete] = React.useState<DocumentTemplateType | null>(null);

  const {
    query: { data: { document_templates } = {}, ...query },
    filter,
    setFilter,
  } = useDocumentTemplates();

  const handleCreate = () => {
    router.push("/settings/template?id=new");
  };

  const handleEdit = (template: DocumentTemplateType) => {
    router.push(`/settings/template?id=${template.id}`);
  };

  const handlePreview = (template: DocumentTemplateType) => {
    // Build params for the template based on related object
    const params: Record<string, string> = {};
    if (template.related_object) {
      params[`${template.related_object}s`] = "sample";
    }

    // Use documentPrinter with token-based access
    documentPrinter.openTemplate(template.id, Object.keys(params).length > 0 ? params : undefined);
  };

  const handleDelete = (template: DocumentTemplateType) => {
    setTemplateToDelete(template);
    setDeleteConfirmOpen(true);
  };

  const confirmDelete = async () => {
    if (templateToDelete) {
      try {
        await mutation.deleteDocumentTemplate.mutateAsync({ id: templateToDelete.id });
        notify({
          type: NotificationType.success,
          message: "Template deleted successfully"
        });
      } catch (error: any) {
        notify({
          type: NotificationType.error,
          message: error.message || "Failed to delete template"
        });
      }
      setDeleteConfirmOpen(false);
      setTemplateToDelete(null);
    }
  };

  const toggleTemplate = async (template: DocumentTemplateType) => {
    try {
      await mutation.updateDocumentTemplate.mutateAsync({
        id: template.id,
        active: !template.active,
      });
      notify({
        type: NotificationType.success,
        message: `Template ${!template.active ? "enabled" : "disabled"}!`,
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || "Failed to update template"
      });
    }
  };

  const templates = document_templates?.edges || [];

  return (
    <div className="space-y-6">
      {templates.length > 0 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Manage your document templates for shipments and labels.
          </p>
          <Button onClick={handleCreate} className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Create Template
          </Button>
        </div>
      )}
      
      <div>
        {templates.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-muted-foreground mb-2">
              No templates yet
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Create your first document template to get started.
            </p>
            <Button onClick={handleCreate}>
              <Plus className="h-4 w-4 mr-2" />
              Create Template
            </Button>
          </div>
        ) : (
          <div className="border-b">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Description</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="w-12"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {templates.map(({ node: template }) => (
                  <TableRow key={template.id}>
                    <TableCell className="font-medium">
                      <div className="space-y-1">
                        <div>{template.name}</div>
                        <div className="font-mono text-xs text-muted-foreground">
                          {template.slug}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant={template.related_object === 'shipment' ? 'default' : 'secondary'}
                        className="text-xs"
                      >
                        {template.related_object}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="max-w-md">
                        <p className="text-sm text-muted-foreground truncate">
                          {template.description || "No description"}
                        </p>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Switch
                          checked={template.active}
                          onCheckedChange={() => toggleTemplate(template)}
                        />
                        <span className="text-sm text-muted-foreground">
                          {template.active ? 'Active' : 'Inactive'}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => handleEdit(template)}>
                            <Edit className="h-4 w-4 mr-2" />
                            Edit
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handlePreview(template)}>
                            <Eye className="h-4 w-4 mr-2" />
                            Preview
                          </DropdownMenuItem>
                          <DropdownMenuSeparator />
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
      </div>

      <ConfirmationDialog
        open={deleteConfirmOpen}
        onOpenChange={setDeleteConfirmOpen}
        title="Delete Template"
        description={`Are you sure you want to delete "${templateToDelete?.name}"? This action cannot be undone.`}
        onConfirm={confirmDelete}
        isLoading={mutation.deleteDocumentTemplate.isLoading}
      />
    </div>
  );
}
