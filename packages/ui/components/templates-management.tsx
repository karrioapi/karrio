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
import { DocumentTemplateType, NotificationType } from "@karrio/types";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { useRouter } from "next/navigation";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

function TemplateDescription({ template }: { template: DocumentTemplateType }) {
  const getTemplateTypeColor = (relatedObject: string) => {
    const colors: Record<string, string> = {
      order: "bg-blue-100 text-blue-800",
      shipment: "bg-green-100 text-green-800",
      pickup: "bg-purple-100 text-purple-800",
      invoice: "bg-orange-100 text-orange-800",
      default: "bg-gray-100 text-gray-800"
    };
    return colors[relatedObject] || colors.default;
  };

  return (
    <div className="space-y-2">
      <div className="text-sm text-muted-foreground">
        {template.description && (
          <div className="mt-1">{template.description}</div>
        )}
      </div>

      {template.updated_at && (
        <div className="text-xs text-muted-foreground">
          Updated: {new Date(template.updated_at).toLocaleDateString()}
        </div>
      )}
    </div>
  );
}

export function TemplatesManagement() {
  const router = useRouter();
  const { notify } = useNotifier();
  const mutation = useDocumentTemplateMutation();
  const [deleteConfirmOpen, setDeleteConfirmOpen] = React.useState(false);
  const [templateToDelete, setTemplateToDelete] = React.useState<DocumentTemplateType | null>(null);
  const { references } = useAPIMetadata();

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
    if (template.preview_url) {
      const previewUrl = template.preview_url.startsWith('http')
        ? template.preview_url
        : `${references.HOST?.replace(/\/$/, '')}${template.preview_url}`;
      window.open(previewUrl, '_blank');
      return;
    }

    const computeParams = (template: DocumentTemplateType) => {
      const params: Record<string, string> = {};
      if (template.related_object) {
        params.doc_type = template.related_object;
      }
      params.doc_template = template.slug;
      return params;
    };
    const params = new URLSearchParams(computeParams(template));
    window.open(`/document_template_preview?${params}`, '_blank');
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
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">
            Manage your document templates for shipments and labels.
          </p>
        </div>
        <Button onClick={handleCreate} className="flex items-center gap-2">
          <Plus className="h-4 w-4" />
          Create Template
        </Button>
      </div>

      {query.isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="space-y-3">
                  <div className="h-4 bg-muted rounded w-3/4"></div>
                  <div className="h-3 bg-muted rounded w-1/2"></div>
                  <div className="h-3 bg-muted rounded w-full"></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : templates.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <FileText className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No templates found</h3>
            <p className="text-muted-foreground mb-4">
              Get started by creating your first document template.
            </p>
            <Button onClick={handleCreate}>
              <Plus className="h-6 w-6 mr-2" />
              Create Template
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map(({ node: template }) => (
            <Card key={template.id} className="group hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="space-y-1 flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <CardTitle className="text-base font-medium truncate">
                        {template.name}
                      </CardTitle>
                      <Badge
                        variant={template.related_object === 'shipment' ? 'default' : 'secondary'}
                        className="text-xs"
                      >
                        {template.related_object}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <span className="font-mono text-xs bg-muted px-2 py-1 rounded">
                        {template.slug}
                      </span>
                    </div>
                  </div>
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
                </div>
              </CardHeader>
              <CardContent className="pt-0">
                <TemplateDescription template={template} />

                <div className="flex items-center justify-between mt-4 pt-4 border-t">
                  <div className="flex items-center gap-2">
                    <Switch
                      checked={template.active}
                      onCheckedChange={() => toggleTemplate(template)}
                    />
                    <span className="text-sm text-muted-foreground">
                      {template.active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    Updated {new Date(template.updated_at).toLocaleDateString()}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

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
