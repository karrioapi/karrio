import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Badge } from "./ui/badge";
import { Checkbox } from "./ui/checkbox";
import { Textarea } from "./ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogBody,
  DialogFooter,
} from "./ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "./ui/form";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import {
  Package,
  Plus,
  MoreHorizontal,
  Edit,
  Trash2,
  CheckCircle,
} from "lucide-react";
import { ConfirmationDialog } from "./confirmation-dialog";
import { isNoneOrEmpty, isEqual } from "@karrio/lib";
import {
  useProductMutation,
  useProducts,
} from "@karrio/hooks/product";
import {
  ProductTemplateType,
  WEIGHT_UNITS,
  CURRENCY_OPTIONS,
  COUNTRY_OPTIONS,
} from "@karrio/types";
import { useSearchParams } from "next/navigation";
import { useToast } from "@karrio/ui/hooks/use-toast";

/**
 * ProductsManagement - React Hook Form Implementation
 *
 * This component manages product templates for customs declarations.
 * The ProductEditDialog uses react-hook-form for performance optimization.
 *
 * Key features:
 * - Zod schema validation
 * - Duplicate label detection (real-time validation)
 * - All product fields: label, title, SKU, HS code, weight, value, quantity, origin, description
 * - Textarea for description field
 * - is_default checkbox for setting default product
 *
 * The form uses uncontrolled inputs where possible to minimize re-renders.
 */

// Helper function to normalize product for comparison
const normalizeProductForComparison = (product: any) => {
  if (!product) return {};
  const { id, label, is_default, created_at, updated_at, object_type, meta, created_by, ...productData } = product;
  return productData;
};

// Helper function to check if two products are identical
const areProductsIdentical = (prod1: any, prod2: any) => {
  return isEqual(
    normalizeProductForComparison(prod1),
    normalizeProductForComparison(prod2)
  );
};

// Zod schema for product validation
const productSchema = z.object({
  label: z.string().min(1, "Label is required"),
  is_default: z.boolean().optional(),
  weight: z.number().min(0.01, "Weight must be greater than 0"),
  weight_unit: z.string().min(1, "Weight unit is required"),
  quantity: z.number().min(1, "Quantity must be at least 1").optional(),
  sku: z.string().optional(),
  title: z.string().optional(),
  hs_code: z.string().optional(),
  description: z.string().optional(),
  value_amount: z.number().optional(),
  value_currency: z.string().optional(),
  origin_country: z.string().optional(),
});

type ProductFormValues = z.infer<typeof productSchema>;

interface ProductEditDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  productTemplate?: ProductTemplateType;
  onSave: () => void;
  existingTemplates?: ProductTemplateType[];
}

function ProductEditDialog({
  open,
  onOpenChange,
  productTemplate,
  onSave,
  existingTemplates = [],
}: ProductEditDialogProps) {
  const { toast } = useToast();
  const { createProduct, updateProduct } = useProductMutation();
  const [labelError, setLabelError] = React.useState<string>("");

  // Initialize form with react-hook-form
  const form = useForm<ProductFormValues>({
    resolver: zodResolver(productSchema),
    defaultValues: {
      label: "",
      is_default: false,
      weight: 0,
      weight_unit: "KG",
      quantity: 1,
      sku: "",
      title: "",
      hs_code: "",
      description: "",
      value_amount: undefined,
      value_currency: "",
      origin_country: "",
    },
    mode: "onBlur",
  });

  const labelValue = form.watch("label");

  // Reset form when dialog opens or productTemplate changes
  React.useEffect(() => {
    if (open) {
      if (productTemplate) {
        form.reset({
          label: productTemplate.meta?.label || "",
          is_default: productTemplate.meta?.is_default || false,
          weight: productTemplate.weight || 0,
          weight_unit: productTemplate.weight_unit || "KG",
          quantity: productTemplate.quantity || 1,
          sku: productTemplate.sku || "",
          title: productTemplate.title || "",
          hs_code: productTemplate.hs_code || "",
          description: productTemplate.description || "",
          value_amount: productTemplate.value_amount || undefined,
          value_currency: productTemplate.value_currency || "",
          origin_country: productTemplate.origin_country || "",
        });
      } else {
        form.reset({
          label: "",
          is_default: false,
          weight: 0,
          weight_unit: "KG",
          quantity: 1,
          sku: "",
          title: "",
          hs_code: "",
          description: "",
          value_amount: undefined,
          value_currency: "",
          origin_country: "",
        });
      }
      setLabelError("");
    }
  }, [productTemplate, open, form]);

  // Real-time label validation for duplicates
  React.useEffect(() => {
    const trimmedLabel = labelValue?.trim() || "";

    if (!trimmedLabel) {
      setLabelError("");
      return;
    }

    const templatesToCheck = existingTemplates.filter(
      (template) => !productTemplate || template.id !== productTemplate.id
    );

    const duplicateLabel = templatesToCheck.find(
      (template) =>
        template.meta?.label?.trim().toLowerCase() === trimmedLabel.toLowerCase()
    );

    if (duplicateLabel) {
      setLabelError("A product with this label already exists");
    } else {
      setLabelError("");
    }
  }, [labelValue, existingTemplates, productTemplate]);

  const handleSubmit = async (data: ProductFormValues) => {
    if (labelError) {
      return;
    }

    try {
      // Build payload with flat structure and meta field
      const payload = {
        weight: data.weight,
        weight_unit: data.weight_unit as any,
        quantity: data.quantity || 1,
        ...(data.sku && { sku: data.sku }),
        ...(data.title && { title: data.title }),
        ...(data.hs_code && { hs_code: data.hs_code }),
        ...(data.description && { description: data.description }),
        ...(data.value_amount && { value_amount: data.value_amount }),
        ...(data.value_currency && { value_currency: data.value_currency as any }),
        ...(data.origin_country && { origin_country: data.origin_country as any }),
        meta: {
          label: data.label,
          is_default: data.is_default || false,
        },
      };

      if (productTemplate) {
        await updateProduct.mutateAsync({
          ...payload,
          id: productTemplate.id,
        } as any);
        toast({
          title: "Success",
          description: "Product updated successfully!",
        });
      } else {
        await createProduct.mutateAsync(payload as any);
        toast({
          title: "Success",
          description: "Product created successfully!",
        });
      }

      onSave();
      onOpenChange(false);
    } catch (error: any) {
      const detailed = error?.data || error?.response?.data || error;
      toast({
        variant: "destructive",
        title: "Error",
        description:
          typeof detailed === "string"
            ? detailed
            : detailed?.message ||
              error?.message ||
              "Failed to save product",
      });
    }
  };

  const formValues = form.watch();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>
            {productTemplate ? "Edit Product" : "Create Product"}
          </DialogTitle>
          <DialogDescription>
            {productTemplate
              ? "Update the product details."
              : "Create a new product for reuse in shipments and customs."}
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)}>
            <DialogBody className="p-4 pb-8">
              <div className="space-y-4">
                {/* Label - full width */}
                <FormField
                  control={form.control}
                  name="label"
                  render={({ field }) => (
                    <FormItem className="space-y-1">
                      <FormLabel className="text-xs text-slate-700">
                        Label <span className="text-red-500">*</span>
                      </FormLabel>
                      <FormControl>
                        <Input
                          {...field}
                          placeholder="e.g., Widget Pro, T-Shirt M"
                          className={`h-8 ${
                            labelError
                              ? "border-red-500 focus:border-red-500 focus:ring-red-500"
                              : ""
                          }`}
                        />
                      </FormControl>
                      {labelError && (
                        <p className="text-xs text-red-500 mt-1">{labelError}</p>
                      )}
                      <FormMessage className="text-xs" />
                    </FormItem>
                  )}
                />

                {/* Product Title - full width */}
                <FormField
                  control={form.control}
                  name="title"
                  render={({ field }) => (
                    <FormItem className="space-y-1">
                      <FormLabel className="text-xs text-slate-700">
                        Product Title
                      </FormLabel>
                      <FormControl>
                        <Input
                          {...field}
                          placeholder="e.g., Widget Pro 2024"
                          className="h-8"
                        />
                      </FormControl>
                      <FormMessage className="text-xs" />
                    </FormItem>
                  )}
                />

                {/* SKU + HS Code - 2 columns */}
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="sku"
                    render={({ field }) => (
                      <FormItem className="space-y-1">
                        <FormLabel className="text-xs text-slate-700">
                          SKU
                        </FormLabel>
                        <FormControl>
                          <Input
                            {...field}
                            placeholder="e.g., WDG-PRO-001"
                            className="h-8"
                          />
                        </FormControl>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="hs_code"
                    render={({ field }) => (
                      <FormItem className="space-y-1">
                        <FormLabel className="text-xs text-slate-700">
                          HS Code
                        </FormLabel>
                        <FormControl>
                          <Input
                            {...field}
                            placeholder="e.g., 8471.30"
                            className="h-8"
                          />
                        </FormControl>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />
                </div>

                {/* Weight + Weight Unit - 2 columns */}
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="weight"
                    render={({ field }) => (
                      <FormItem className="space-y-1">
                        <FormLabel className="text-xs text-slate-700">
                          Weight <span className="text-red-500">*</span>
                        </FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            step="0.01"
                            min="0"
                            placeholder="0.00"
                            value={field.value?.toString() || ""}
                            onChange={(e) => field.onChange(parseFloat(e.target.value) || 0)}
                            className="h-8"
                          />
                        </FormControl>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="weight_unit"
                    render={({ field }) => (
                      <FormItem className="space-y-1">
                        <FormLabel className="text-xs text-slate-700">
                          Weight Unit <span className="text-red-500">*</span>
                        </FormLabel>
                        <Select
                          value={field.value}
                          onValueChange={field.onChange}
                        >
                          <FormControl>
                            <SelectTrigger className="h-8">
                              <SelectValue />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {WEIGHT_UNITS.map((unit) => (
                              <SelectItem key={`weight-${unit}`} value={unit}>
                                {unit}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />
                </div>

                {/* Value + Currency - 2 columns */}
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="value_amount"
                    render={({ field }) => (
                      <FormItem className="space-y-1">
                        <FormLabel className="text-xs text-slate-700">
                          Value
                        </FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            step="0.01"
                            min="0"
                            placeholder="0.00"
                            value={field.value?.toString() || ""}
                            onChange={(e) => field.onChange(parseFloat(e.target.value) || undefined)}
                            className="h-8"
                          />
                        </FormControl>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="value_currency"
                    render={({ field }) => (
                      <FormItem className="space-y-1">
                        <FormLabel className="text-xs text-slate-700">
                          Currency
                        </FormLabel>
                        <Select
                          value={field.value || ""}
                          onValueChange={field.onChange}
                        >
                          <FormControl>
                            <SelectTrigger className="h-8">
                              <SelectValue placeholder="Select currency" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {CURRENCY_OPTIONS.map((currency) => (
                              <SelectItem key={`currency-${currency}`} value={currency}>
                                {currency}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />
                </div>

                {/* Default Quantity + Origin Country - 2 columns */}
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="quantity"
                    render={({ field }) => (
                      <FormItem className="space-y-1">
                        <FormLabel className="text-xs text-slate-700">
                          Default Quantity
                        </FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min="1"
                            placeholder="1"
                            value={field.value?.toString() || ""}
                            onChange={(e) => field.onChange(parseInt(e.target.value) || 1)}
                            className="h-8"
                          />
                        </FormControl>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="origin_country"
                    render={({ field }) => (
                      <FormItem className="space-y-1">
                        <FormLabel className="text-xs text-slate-700">
                          Origin Country
                        </FormLabel>
                        <Select
                          value={field.value || ""}
                          onValueChange={field.onChange}
                        >
                          <FormControl>
                            <SelectTrigger className="h-8">
                              <SelectValue placeholder="Select country" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {COUNTRY_OPTIONS.map((country) => (
                              <SelectItem key={`country-${country}`} value={country}>
                                {country}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />
                </div>

                {/* Description - full width textarea */}
                <FormField
                  control={form.control}
                  name="description"
                  render={({ field }) => (
                    <FormItem className="space-y-1">
                      <FormLabel className="text-xs text-slate-700">
                        Description
                      </FormLabel>
                      <FormControl>
                        <Textarea
                          {...field}
                          placeholder="Product description for customs declarations"
                          className="min-h-[80px] resize-none"
                        />
                      </FormControl>
                      <FormMessage className="text-xs" />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="is_default"
                  render={({ field }) => (
                    <FormItem className="flex items-center space-x-2 pt-2">
                      <FormControl>
                        <Checkbox
                          id="is_default"
                          checked={field.value}
                          onCheckedChange={field.onChange}
                        />
                      </FormControl>
                      <Label htmlFor="is_default" className="text-xs text-slate-700">
                        Set as default product
                      </Label>
                    </FormItem>
                  )}
                />
              </div>
            </DialogBody>

            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => onOpenChange(false)}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                size="sm"
                disabled={!formValues.label?.trim() || !formValues.weight || !!labelError}
              >
                {productTemplate ? "Update Product" : "Create Product"}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}

export function ProductsManagement() {
  const searchParams = useSearchParams();
  const modal = searchParams.get("modal") as string;
  const { deleteProduct } = useProductMutation();
  const [editDialogOpen, setEditDialogOpen] = React.useState(false);
  const [selectedProduct, setSelectedProduct] =
    React.useState<ProductTemplateType | null>(null);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = React.useState(false);
  const [productToDelete, setProductToDelete] =
    React.useState<ProductTemplateType | null>(null);
  const { toast } = useToast();

  const {
    query: { data: { products } = {}, ...query },
    filter,
    setFilter,
  } = useProducts({
    setVariablesToURL: true,
  });

  const handleEdit = (template: ProductTemplateType) => {
    setSelectedProduct(template);
    setEditDialogOpen(true);
  };

  const handleCreate = () => {
    setSelectedProduct(null);
    setEditDialogOpen(true);
  };

  const handleDelete = (template: ProductTemplateType) => {
    setProductToDelete(template);
    setDeleteConfirmOpen(true);
  };

  const confirmDelete = async () => {
    if (productToDelete) {
      try {
        await deleteProduct.mutateAsync({ id: productToDelete.id });
        toast({
          title: "Success",
          description: "Product deleted successfully!",
        });
      } catch (error: any) {
        toast({
          variant: "destructive",
          title: "Error",
          description: error?.message || "Failed to delete product",
        });
      }
      setDeleteConfirmOpen(false);
      setProductToDelete(null);
    }
  };

  const handleSave = () => {
    query.refetch();
  };

  const productList = products?.edges || [];

  return (
    <div className="space-y-6">
      {productList.length > 0 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Manage your product templates for customs declarations and shipments.
          </p>
          <Button onClick={handleCreate} className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Create Product
          </Button>
        </div>
      )}

      <div>
        {productList.length === 0 ? (
          <div className="text-center py-12">
            <Package className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-muted-foreground mb-2">
              No products yet
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Create your first product template to get started.
            </p>
            <Button onClick={handleCreate}>
              <Plus className="h-4 w-4 mr-2" />
              Create Product
            </Button>
          </div>
        ) : (
          <div className="border-b">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Label</TableHead>
                  <TableHead>SKU</TableHead>
                  <TableHead>Weight</TableHead>
                  <TableHead>Value</TableHead>
                  <TableHead>Origin</TableHead>
                  <TableHead className="w-12"></TableHead>
                  <TableHead className="w-12"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {productList.map(({ node: template }) => (
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
                      {template.title && (
                        <div className="text-xs text-muted-foreground">
                          {template.title}
                        </div>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="text-sm">{template.sku || "-"}</div>
                      {template.hs_code && (
                        <div className="text-xs text-muted-foreground">
                          HS: {template.hs_code}
                        </div>
                      )}
                    </TableCell>
                    <TableCell>
                      {template.weight} {template.weight_unit}
                    </TableCell>
                    <TableCell>
                      {template.value_amount
                        ? `${template.value_amount} ${template.value_currency || ""}`
                        : "-"}
                    </TableCell>
                    <TableCell>{template.origin_country || "-"}</TableCell>
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

        {productList.length > 0 && (
          <div className="flex items-center justify-between pt-4">
            <div className="text-sm text-muted-foreground">
              {productList.length} product{productList.length !== 1 ? "s" : ""}
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                disabled={!products?.page_info.has_previous_page}
                onClick={() =>
                  setFilter({
                    ...filter,
                    offset: Math.max(0, (filter.offset || 0) - 20),
                  })
                }
              >
                Previous
              </Button>
              <Button
                variant="outline"
                size="sm"
                disabled={!products?.page_info.has_next_page}
                onClick={() =>
                  setFilter({
                    ...filter,
                    offset: (filter.offset || 0) + 20,
                  })
                }
              >
                Next
              </Button>
            </div>
          </div>
        )}
      </div>

      <ProductEditDialog
        open={editDialogOpen}
        onOpenChange={setEditDialogOpen}
        productTemplate={selectedProduct || undefined}
        onSave={handleSave}
        existingTemplates={productList.map(({ node }: any) => node)}
      />

      <ConfirmationDialog
        open={deleteConfirmOpen}
        onOpenChange={setDeleteConfirmOpen}
        title="Delete Product"
        description={`Are you sure you want to delete "${productToDelete?.meta?.label}"? This action cannot be undone.`}
        onConfirm={confirmDelete}
      />
    </div>
  );
}
