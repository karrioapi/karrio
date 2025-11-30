import React from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Textarea } from "./ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Separator } from "./ui/separator";
import {
  X,
  Save,
  Eye,
  Code,
  FileText,
  ExternalLink,
  RefreshCw
} from "lucide-react";
import {
  DocumentTemplateType,
  DOCUMENT_RELATED_OBJECTS,
  NotificationType,
  TemplateType,
} from "@karrio/types";
import {
  isEqual,
  isNoneOrEmpty,
  url$,
  validationMessage,
  validityCheck,
} from "@karrio/lib";
import {
  useDocumentTemplate,
  useDocumentTemplateMutation,
} from "@karrio/hooks/document-template";
import { useDocumentPrinter } from "@karrio/hooks/resource-token";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { DEFAULT_DOCUMENT_TEMPLATE } from "@karrio/lib/sample";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useSearchParams } from "next/navigation";
import CodeMirror from "@uiw/react-codemirror";
import { html } from "@codemirror/lang-html";
import { json } from "@codemirror/lang-json";
import { useKarrio } from "@karrio/hooks/karrio";
import { Badge } from "@karrio/ui/components/ui/badge";
import { EnhancedMetadataEditor } from "./enhanced-metadata-editor";

type stateValue = string | boolean | string[] | Partial<TemplateType>;
const DEFAULT_STATE = {
  related_object: "order",
  template: DEFAULT_DOCUMENT_TEMPLATE,
  metadata: {},
};

function reducer(
  state: any,
  { name, value }: { name: string; value: stateValue },
) {
  switch (name) {
    case "partial":
      return { ...(value as TemplateType) };
    default:
      return { ...state, [name]: value };
  }
}

interface TemplateEditorProps {
  templateId: string;
  onClose: () => void;
  onSave: () => void;
}

export function TemplateEditor({ templateId, onClose, onSave }: TemplateEditorProps) {
  const [template, dispatch] = React.useReducer(reducer, DEFAULT_STATE);
  const [activeTab, setActiveTab] = React.useState("code");
  const [previewContent, setPreviewContent] = React.useState<string>("");
  const [previewLoading, setPreviewLoading] = React.useState(false);
  const [previewError, setPreviewError] = React.useState<string | null>(null);
  const [pdfUrl, setPdfUrl] = React.useState<string | null>(null);
  const [sampleData, setSampleData] = React.useState<string>("");
  const [metadata, setMetadata] = React.useState<string>("{}");
  const [options, setOptions] = React.useState<string>("{}");
  const [submitAttempted, setSubmitAttempted] = React.useState(false);

  const { references } = useAPIMetadata();
  const { documents } = useKarrio();
  const loader = useLoader();
  const notifier = useNotifier();
  const documentPrinter = useDocumentPrinter();

  const searchParams = useSearchParams();
  const id = templateId || searchParams.get("id") as string;
  const mutation = useDocumentTemplateMutation();
  const {
    query: { data: { document_template } = {} },
    docId: currentDocId,
    setDocId,
  } = useDocumentTemplate({
    setVariablesToURL: true,
    id: id as string,
  });

  const isNew = currentDocId === "new";

  const computeParams = (template: DocumentTemplateType) => {
    if (isNoneOrEmpty(template.related_object)) {
      return "";
    }
    return `?${template.related_object}s=sample`;
  };

  const handleChange = (event: React.ChangeEvent<any>) => {
    const target = event.target;
    let value = target.type === "checkbox" ? target.checked : target.value;
    let name: string = target.name;

    if (target.multiple === true) {
      value = Array.from(target.selectedOptions).map((o: any) => o.value);
    }

    dispatch({ name, value });
  };

  const handleCodeChange = (value: string) => {
    dispatch({ name: "template", value });
  };

  const handleSubmit = async (evt?: React.FormEvent<HTMLFormElement>) => {
    try {
      evt?.preventDefault();
      setSubmitAttempted(true);

      const nameValid = !!(template.name && String(template.name).trim());
      const slugValid = !!(template.slug && /^[a-z0-9_]+$/.test(String(template.slug)));
      if (!nameValid || !slugValid) {
        return;
      }

      loader.setLoading(true);

      const { preview_url, updated_at, ...templateData } = template as any;

      // Parse options from editor
      let parsedOptions = {};
      try {
        parsedOptions = options ? JSON.parse(options) : {};
      } catch (error) {
        console.warn('Invalid options JSON, using empty object:', error);
        parsedOptions = {};
      }

      const data = {
        ...templateData,
        active: template.active as boolean,
        options: parsedOptions,
      };

      if (isNew) {
        const { create_document_template } = await mutation.createDocumentTemplate.mutateAsync(data);
        notifier.notify({
          type: NotificationType.success,
          message: `Document template created successfully`,
        });
        loader.setLoading(false);

        setSubmitAttempted(false);
        const createdTemplate = create_document_template.template as any;
        const mergedTemplate = { ...createdTemplate, template: (template as any).template };
        dispatch({ name: "partial", value: mergedTemplate });
        if (createdTemplate?.id) setDocId(createdTemplate.id);
        onSave();
      } else {
        await mutation.updateDocumentTemplate.mutateAsync(data);
        notifier.notify({
          type: NotificationType.success,
          message: `Document template updated successfully`,
        });
        loader.setLoading(false);
        setSubmitAttempted(false);
        dispatch({ name: "partial", value: data as any });
        onSave();
      }
    } catch (error: any) {
      // Prefer GraphQL validation subtext if available
      const response = error?.response?.data || error?.data || {};
      const topLevelErrors = Array.isArray(response?.errors) ? response.errors : [];
      const mergedValidationRaw = topLevelErrors.reduce((acc: Record<string, string[] | string>, err: any) => ({
        ...acc,
        ...(err?.validation || {}),
      }), {} as Record<string, string[] | string>);
      // Prefer server-provided validation; otherwise use merged from errors
      const validationRaw: Record<string, string[] | string> | undefined = response?.validation || (Object.keys(mergedValidationRaw).length > 0 ? mergedValidationRaw : undefined);
      // Normalize to arrays so notifier shows "slug: message"
      const validation = validationRaw
        ? Object.fromEntries(
          Object.entries(validationRaw).map(([field, messages]) => [
            field,
            Array.isArray(messages) ? messages : [String(messages)],
          ])
        ) as Record<string, string[]>
        : undefined;

      if (validation) {
        notifier.notify({
          type: NotificationType.error,
          message: ({ message: "Failed to save template", validation } as any),
        });
      } else {
        const message = error.message || "Failed to save template";
        notifier.notify({ type: NotificationType.error, message });
      }
      loader.setLoading(false);
    }
  };

  const handlePreview = () => {
    if (!isNoneOrEmpty(template.id)) {
      // Use documentPrinter for saved templates with token-based access
      const params = computeParams(template).replace(/^\?/, '').split('&').reduce((acc, param) => {
        const [key, value] = param.split('=');
        if (key && value) acc[key] = decodeURIComponent(value);
        return acc;
      }, {} as Record<string, string>);

      documentPrinter.openTemplate(template.id as string, Object.keys(params).length > 0 ? params : undefined);
    } else {
      generatePreview();
    }
  };

  const generatePreview = async () => {
    if (!template.template || !template.related_object) {
      const errorMsg = "Template content and related object are required for preview";
      setPreviewError(errorMsg);
      notifier.notify({
        type: NotificationType.error,
        message: errorMsg
      });
      return;
    }

    setPreviewLoading(true);
    setPreviewError(null);
    setPreviewContent("");

    try {
      // Parse sample data, metadata, and options
      let currentSampleData, currentMetadata, currentOptions;
      let hasParseError = false;

      try {
        currentSampleData = sampleData ? JSON.parse(sampleData) : generateSampleData(template.related_object);
      } catch (parseError) {
        currentSampleData = generateSampleData(template.related_object);
        setPreviewError("Sample data has invalid JSON format. Using default data for preview.");
        hasParseError = true;
      }

      try {
        currentMetadata = template.metadata || (metadata ? JSON.parse(metadata) : {});
      } catch (parseError) {
        currentMetadata = template.metadata || {};
        if (!hasParseError) {
          setPreviewError("Metadata has invalid JSON format. Using empty metadata for preview.");
          hasParseError = true;
        }
      }

      try {
        currentOptions = options ? JSON.parse(options) : {};
      } catch (parseError) {
        currentOptions = {};
        if (!hasParseError) {
          setPreviewError("Options has invalid JSON format. Using empty options for preview.");
          hasParseError = true;
        }
      }

      const response = await documents.generateDocument({
        documentData: {
          template: template.template,
          doc_format: 'pdf',
          doc_name: template.name || 'preview',
          data: currentSampleData,
          options: currentOptions,
        }
      });

      // Handle the API response format: { doc_format, doc_name, doc_file }
      const apiResponse = response.data;

      if (apiResponse.doc_file) {
        // Handle different document formats
        if (apiResponse.doc_format === 'html') {
          // For HTML, decode base64 and use directly
          try {
            const decodedContent = atob(apiResponse.doc_file);
            setPreviewContent(decodedContent);
          } catch (decodeError) {
            // If base64 decoding fails, treat as plain content
            setPreviewContent(apiResponse.doc_file);
          }
        } else if (apiResponse.doc_format === 'pdf') {
          // Clean up previous PDF URL if exists (only for object URLs)
          if (pdfUrl && pdfUrl.startsWith('blob:')) {
            URL.revokeObjectURL(pdfUrl);
          }

          // For PDF, create a data URL directly from base64
          const pdfDataUrl = `data:application/pdf;base64,${apiResponse.doc_file}`;
          setPdfUrl(pdfDataUrl);

          setPreviewContent(`
            <div class="flex flex-col h-full">
              <div class="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p class="text-sm text-blue-800">
                  <strong>PDF Preview:</strong> ${apiResponse.doc_name || 'Document'}
                </p>
              </div>
              <iframe
                src="${pdfDataUrl}"
                class="flex-1 w-full border-0 rounded-lg shadow-sm"
                style="min-height: 600px;"
                title="Document Preview"
              ></iframe>
            </div>
          `);
        } else {
          // For other formats, decode and show as plain text
          try {
            const decodedContent = atob(apiResponse.doc_file);
            setPreviewContent(`
              <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                <h4 class="font-medium mb-2">Document Content (${apiResponse.doc_format?.toUpperCase() || 'Unknown'}):</h4>
                <pre class="text-sm text-gray-700 whitespace-pre-wrap">${decodedContent}</pre>
              </div>
            `);
          } catch (decodeError) {
            // If base64 decoding fails, show as base64
            setPreviewContent(`
              <div class="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                <h4 class="font-medium mb-2">Document Content (${apiResponse.doc_format?.toUpperCase() || 'Base64'}):</h4>
                <pre class="text-sm text-gray-700 whitespace-pre-wrap break-all">${apiResponse.doc_file}</pre>
              </div>
            `);
          }
        }
      } else {
        throw new Error('No document content received from API');
      }

      setActiveTab("preview");
    } catch (error: any) {
      console.error('Preview generation error:', error);

      // Extract error message from different possible error formats
      let errorMessage = "Failed to generate preview";

      if (error.response?.data?.errors?.[0]?.message) {
        errorMessage = error.response.data.errors[0].message;
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.message) {
        errorMessage = error.message;
      }

      setPreviewError(errorMessage);
      setPreviewContent("");

      notifier.notify({
        type: NotificationType.error,
        message: errorMessage
      });
    } finally {
      setPreviewLoading(false);
    }
  };

  const generateSampleData = (relatedObject: string) => {
    switch (relatedObject) {
      case 'shipment':
        return {
          shipment: {
            id: 'shp_f49473b250ae45bcb7e2a671f54f40ca',
            object_type: 'shipment',
            tracking_url: '/v1/trackers/tst_overland/0000000135',
            tracking_number: '0000000135',
            tracking_numbers: ['0000000135', '0000000134'],
            shipper: {
              id: 'adr_77cf815a63904280acb908b9357b727b',
              postal_code: 'E1C4Z8',
              city: 'Moncton',
              federal_tax_id: null,
              state_tax_id: null,
              person_name: 'John Doe',
              company_name: 'A corp.',
              country_code: 'CA',
              email: null,
              phone_number: '+1 514-000-0000',
              state_code: 'NB',
              street_number: null,
              residential: false,
              address_line1: '125 Church St',
              address_line2: null,
              validate_location: null,
              object_type: 'address',
              validation: null,
            },
            recipient: {
              id: 'adr_470c247fbd6441aaaaf3c282d8e80637',
              postal_code: 'V6M2V9',
              city: 'Vancouver',
              federal_tax_id: null,
              state_tax_id: null,
              person_name: 'Jane Doe',
              company_name: 'B corp.',
              country_code: 'CA',
              email: null,
              phone_number: '+1 514-000-0000',
              state_code: 'BC',
              street_number: null,
              residential: true,
              address_line1: '5840 Oak St',
              address_line2: null,
              validate_location: false,
              object_type: 'address',
              validation: null,
            },
            parcels: [
              {
                id: 'pcl_00baac55ac8347718342fdc32f6104f5',
                weight: 1,
                width: 33.7,
                height: 18.2,
                length: 10,
                packaging_type: 'medium_box',
                package_preset: null,
                description: null,
                content: null,
                is_document: false,
                weight_unit: 'KG',
                dimension_unit: 'CM',
                items: [
                  {
                    id: 'cdt_2e947981ee1c4cec995573bc16386f96',
                    weight: 0.75,
                    weight_unit: 'KG',
                    description: null,
                    title: 'Violet Suede Shoes',
                    quantity: 1,
                    sku: null,
                    value_amount: 85.95,
                    value_currency: 'USD',
                    origin_country: null,
                    parent_id: 'cdt_4b80710300ea4e22b67f6a488e588a34',
                    metadata: {},
                    object_type: 'commodity',
                  }
                ],
                freight_class: null,
                reference_number: '0000000135',
                object_type: 'parcel',
              }
            ],
            services: [],
            options: { shipment_date: new Date().toISOString().split('T')[0] },
            payment: { paid_by: 'sender', currency: null, account_number: null },
            customs: null,
            rates: [
              {
                id: 'rat_1640580c8c5a454b865f68e8f236d6d9',
                object_type: 'rate',
                carrier_name: 'tst_overland',
                carrier_id: 'tst-overland',
                currency: 'CAD',
                estimated_delivery: null,
                service: 'standard_service',
                discount: null,
                base_charge: 200,
                total_charge: 200,
                duties_and_taxes: null,
                transit_days: null,
                extra_charges: [],
                meta: {
                  service_name: 'STANDARD SERVICE',
                  rate_provider: 'tst_overland',
                  carrier_connection_id: 'car_9dac728533e841b09ec453178de5b3c3',
                },
                test_mode: true,
              }
            ],
            reference: 'Order #1073459962,394873849374',
            label_type: 'PDF',
            carrier_ids: [],
            tracker_id: null,
            created_at: new Date().toISOString(),
            metadata: { order_ids: '1073459962,394873849374' },
            messages: [],
            status: 'purchased',
            carrier_name: 'generic',
            carrier_id: 'tst-overland',
          }
        };
      case 'order':
        return {
          order: {
            id: 'ord_028e5cb83814487a9546d0690260f0ee',
            object_type: 'order',
            order_id: '1073459962',
            order_date: new Date().toISOString().split('T')[0],
            source: 'shopify',
            status: 'unfulfilled',
            shipping_to: {
              id: 'adr_4e038ec1bf4448d284069d0dfd761fb3',
              postal_code: 'E1C4Z8',
              city: 'Moncton',
              federal_tax_id: null,
              state_tax_id: null,
              person_name: 'John Doe',
              company_name: 'A corp.',
              country_code: 'CA',
              email: null,
              phone_number: '+1 514-000-0000',
              state_code: 'NB',
              street_number: null,
              residential: false,
              address_line1: '125 Church St',
              address_line2: null,
              validate_location: false,
              object_type: 'address',
              validation: null,
            },
            shipping_from: null,
            line_items: [
              {
                id: 'cdt_cd32372be5524a2fa492c4af598b7679',
                weight: 0.75,
                weight_unit: 'KG',
                description: null,
                title: 'Violet Suede Shoes',
                quantity: 1,
                unfulfilled_quantity: 1,
                sku: null,
                value_amount: 85.95,
                value_currency: 'USD',
                origin_country: null,
                parent_id: null,
                metadata: {},
                object_type: 'commodity',
              },
              {
                id: 'cdt_71ef30b72d4c4b94882337b44e0d3fb9',
                weight: 1.7,
                weight_unit: 'KG',
                description: null,
                title: 'Purple Leather Coat',
                quantity: 1,
                unfulfilled_quantity: 1,
                sku: null,
                value_amount: 129.99,
                value_currency: 'USD',
                origin_country: null,
                parent_id: null,
                metadata: {},
                object_type: 'commodity',
              },
            ],
            options: {},
            metadata: {},
            shipments: [],
            test_mode: true,
            created_at: new Date().toISOString(),
          }
        };
      default:
        return {};
    }
  };

  const refreshPreview = async () => {
    if (activeTab === "preview") {
      await generatePreview();
    }
  };

  React.useEffect(() => {
    if (currentDocId !== "new") {
      dispatch({ name: "partial", value: document_template as any });
    }
  }, [document_template]);

  // Initialize metadata and options from loaded template
  React.useEffect(() => {
    if (document_template && currentDocId !== "new") {
      // Initialize options from template
      if (document_template.options) {
        try {
          setOptions(JSON.stringify(document_template.options, null, 2));
        } catch (error) {
          console.warn('Failed to parse template options:', error);
          setOptions("{}");
        }
      } else {
        setOptions("{}");
      }
    }
  }, [document_template, currentDocId]);

  // Initialize sample data when template or related_object changes
  React.useEffect(() => {
    if (template.related_object) {
      const defaultSampleData = generateSampleData(template.related_object);
      setSampleData(JSON.stringify(defaultSampleData, null, 2));
    }
  }, [template.related_object]);

  // Cleanup PDF URL on unmount (only for object URLs, not data URLs)
  React.useEffect(() => {
    return () => {
      if (pdfUrl && pdfUrl.startsWith('blob:')) {
        URL.revokeObjectURL(pdfUrl);
      }
    };
  }, [pdfUrl]);

  const hasChanges = !isEqual(template, document_template || DEFAULT_STATE);

  const nameInvalid = submitAttempted && (!template.name || String(template.name).trim() === "");
  const _slug = String(template.slug || "");
  const slugEmpty = submitAttempted && _slug.trim() === "";
  const slugPatternInvalid = submitAttempted && _slug.trim() !== "" && !/^[a-z0-9_]+$/.test(_slug);
  const slugInvalid = slugEmpty || slugPatternInvalid;

  return (
    <div className="tailwind-only h-screen max-h-screen flex flex-col bg-slate-50 overflow-hidden">
      {/* Sticky Header */}
      <header className="bg-white border-b border-slate-200 px-3 lg:px-4 py-2 lg:py-3 flex items-center justify-between sticky top-0 z-10 shadow-sm flex-shrink-0">
        <div className="flex items-center gap-2 lg:gap-4 min-w-0 flex-1">
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            className="h-8 w-8 lg:h-10 lg:w-10 rounded-md p-0 hover:bg-slate-100 flex-shrink-0"
          >
            <X className="h-4 w-4 lg:h-5 lg:w-5" />
          </Button>
          <Separator orientation="vertical" className="h-4 lg:h-6 flex-shrink-0" />
          <div className="min-w-0 flex-1">
            <h1 className="text-sm lg:text-lg font-semibold text-slate-900 truncate">
              {isNew ? "Create template" : "Edit template"}
            </h1>
            {template.name && (
              <p className="text-xs lg:text-sm text-slate-500 truncate">{template.name}</p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-1 lg:gap-3 flex-shrink-0">
          <Button
            onClick={handlePreview}
            disabled={isNoneOrEmpty(template.id)}
            variant="outline"
            size="sm"
            className="flex items-center gap-1 lg:gap-2 h-8 lg:h-10 px-2 lg:px-4 text-xs lg:text-sm"
          >
            <Eye className="h-3 w-3 lg:h-4 lg:w-4" />
            <span className="hidden md:inline">Preview Template</span>
            <span className="md:hidden">Preview</span>
            <ExternalLink className="h-3 w-3" />
          </Button>
          <Button
            onClick={() => handleSubmit()}
            disabled={loader.loading || !hasChanges}
            className="flex items-center gap-1 lg:gap-2 h-8 lg:h-10 px-2 lg:px-4 text-xs lg:text-sm"
            size="sm"
          >
            <Save className="h-3 w-3 lg:h-4 lg:w-4" />
            <span className="hidden md:inline">Save Template</span>
            <span className="md:hidden">Save</span>
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden min-h-0">
        {/* Left Panel - Form */}
        <div className="w-full lg:w-1/3 lg:border-r border-b lg:border-b-0 border-slate-200 bg-white overflow-y-auto max-h-[50vh] lg:max-h-none flex-shrink-0">
          <div className="p-3 lg:p-6 space-y-4 lg:space-y-6">
            <div className="space-y-3 lg:space-y-4">
              <div className="space-y-1 lg:space-y-2">
                <Label htmlFor="name" className="text-xs lg:text-sm font-medium">
                  Template Name
                  {nameInvalid && (
                    <span className="text-red-600 ml-2 italic">* required field *</span>
                  )}
                </Label>
                <Input
                  id="name"
                  name="name"
                  value={template.name as string}
                  onChange={handleChange}
                  placeholder="e.g., Packing Slip"
                  className={`text-xs lg:text-sm h-8 lg:h-10 ${nameInvalid ? 'border-red-500 focus-visible:ring-red-500' : ''}`}
                  required
                />
              </div>

              <div className="space-y-1 lg:space-y-2">
                <Label htmlFor="slug" className="text-xs lg:text-sm font-medium">
                  Slug
                  {slugEmpty && (
                    <span className="text-red-600 ml-2 italic">* required field *</span>
                  )}
                  {!slugEmpty && slugPatternInvalid && (
                    <span className="text-red-600 ml-2 italic">* invalid input *</span>
                  )}
                </Label>
                <Input
                  id="slug"
                  name="slug"
                  value={template.slug as string}
                  onChange={validityCheck(handleChange)}
                  onInvalid={validityCheck(
                    validationMessage("Please enter a valid slug"),
                  )}
                  placeholder="e.g., packing_slip"
                  className={`text-xs lg:text-sm font-mono h-8 lg:h-10 ${slugInvalid ? 'border-red-500 focus-visible:ring-red-500' : ''}`}
                  pattern="^[a-z0-9_]+$"
                  required
                />
                <p className={`text-xs ${slugPatternInvalid ? 'text-red-600' : 'text-muted-foreground'}`}>
                  Only lowercase letters, numbers, and underscores
                </p>
              </div>

              <div className="space-y-1 lg:space-y-2">
                <Label htmlFor="related_object" className="text-xs lg:text-sm font-medium">
                  Related Object
                </Label>
                <Select
                  value={template.related_object as string}
                  onValueChange={(value) => {
                    dispatch({ name: "related_object", value });
                    if (activeTab === "preview") {
                      setPreviewContent("");
                    }
                  }}
                >
                  <SelectTrigger className="text-xs lg:text-sm h-8 lg:h-10">
                    <SelectValue placeholder="Select related object" />
                  </SelectTrigger>
                  <SelectContent>
                    {DOCUMENT_RELATED_OBJECTS.map((obj) => (
                      <SelectItem key={obj} value={obj}>
                        {obj.charAt(0).toUpperCase() + obj.slice(1)}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <p className="text-xs text-muted-foreground">
                  The type of object this template is for
                </p>
              </div>

              <div className="space-y-1 lg:space-y-2">
                <Label htmlFor="description" className="text-xs lg:text-sm font-medium">
                  Description (Optional)
                </Label>
                <Textarea
                  id="description"
                  name="description"
                  value={template.description as string || ""}
                  onChange={handleChange}
                  placeholder="Brief description of this template..."
                  className="text-xs lg:text-sm resize-none"
                  rows={2}
                />
              </div>

              <div className="space-y-1 lg:space-y-2">
                <EnhancedMetadataEditor
                  value={template.metadata || {}}
                  onChange={(metadata) => dispatch({ name: "metadata", value: metadata })}
                  className="border-0"
                  maxHeight="200px"
                />
              </div>

              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="active"
                  name="active"
                  checked={template.active as boolean}
                  onChange={handleChange}
                  className="rounded border-gray-300"
                />
                <Label htmlFor="active" className="text-xs lg:text-sm">
                  Active template
                </Label>
              </div>
            </div>

            {/* Template Variables Help */}
            <div className="space-y-2 lg:space-y-3">
              <h3 className="text-xs lg:text-sm font-medium">Available Variables</h3>
              <div className="space-y-2 text-xs">
                <div className="p-2 lg:p-3 bg-slate-50 rounded-lg">
                  <p className="font-medium mb-1 lg:mb-2 text-xs">Common Variables:</p>
                  <div className="grid grid-cols-1 gap-0.5 lg:gap-1 font-mono text-xs">
                    <code>{"{{ object.id }}"}</code>
                    <code>{"{{ object.created }}"}</code>
                    <code>{"{{ object.updated }}"}</code>
                  </div>
                </div>

                {template.related_object === "order" && (
                  <div className="p-2 lg:p-3 bg-blue-50 rounded-lg">
                    <p className="font-medium mb-1 lg:mb-2 text-xs">Order Variables:</p>
                    <div className="grid grid-cols-1 gap-0.5 lg:gap-1 font-mono text-xs">
                      <code>{"{{ order.order_id }}"}</code>
                      <code>{"{{ order.shipping_to }}"}</code>
                      <code>{"{{ order.shipping_from }}"}</code>
                      <code>{"{{ order.line_items }}"}</code>
                    </div>
                  </div>
                )}

                {template.related_object === "shipment" && (
                  <div className="p-2 lg:p-3 bg-green-50 rounded-lg">
                    <p className="font-medium mb-1 lg:mb-2 text-xs">Shipment Variables:</p>
                    <div className="grid grid-cols-1 gap-0.5 lg:gap-1 font-mono text-xs">
                      <code>{"{{ shipment.tracking_number }}"}</code>
                      <code>{"{{ shipment.recipient }}"}</code>
                      <code>{"{{ shipment.shipper }}"}</code>
                      <code>{"{{ shipment.service }}"}</code>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Right Panel - Code Editor and Preview */}
        <div className="flex-1 flex flex-col overflow-hidden min-h-0">
          {/* Tab Navigation */}
          <div className="flex border-b border-slate-200 bg-white px-3 lg:px-6 flex-shrink-0">
            <button
              onClick={() => setActiveTab("code")}
              className={`px-2 lg:px-4 py-2 lg:py-3 text-xs lg:text-sm font-medium border-b-2 transition-colors ${activeTab === "code"
                ? "border-blue-500 text-blue-600 bg-blue-50/50"
                : "border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300"
                }`}
            >
              <div className="flex items-center gap-1 lg:gap-2">
                <Code className="h-3 w-3 lg:h-4 lg:w-4" />
                <span className="hidden sm:inline">Template Code</span>
                <span className="sm:hidden">Code</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab("data")}
              className={`px-2 lg:px-4 py-2 lg:py-3 text-xs lg:text-sm font-medium border-b-2 transition-colors ${activeTab === "data"
                ? "border-blue-500 text-blue-600 bg-blue-50/50"
                : "border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300"
                }`}
            >
              <div className="flex items-center gap-1 lg:gap-2">
                <FileText className="h-3 w-3 lg:h-4 lg:w-4" />
                <span className="hidden sm:inline">Sample Data</span>
                <span className="sm:hidden">Data</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab("options")}
              className={`px-2 lg:px-4 py-2 lg:py-3 text-xs lg:text-sm font-medium border-b-2 transition-colors ${activeTab === "options"
                ? "border-blue-500 text-blue-600 bg-blue-50/50"
                : "border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300"
                }`}
            >
              <div className="flex items-center gap-1 lg:gap-2">
                <FileText className="h-3 w-3 lg:h-4 lg:w-4" />
                <span className="hidden sm:inline">Options</span>
                <span className="sm:hidden">Options</span>
              </div>
            </button>
            <button
              onClick={() => {
                setActiveTab("preview");
                if (!previewContent && !previewError && template.template) {
                  generatePreview();
                }
              }}
              className={`px-2 lg:px-4 py-2 lg:py-3 text-xs lg:text-sm font-medium border-b-2 transition-colors ${activeTab === "preview"
                ? "border-blue-500 text-blue-600 bg-blue-50/50"
                : "border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300"
                }`}
            >
              <div className="flex items-center gap-1 lg:gap-2">
                <Eye className="h-3 w-3 lg:h-4 lg:w-4" />
                <span className="hidden sm:inline">Live Preview</span>
                <span className="sm:hidden">Preview</span>
                {previewLoading && (
                  <div className="h-3 w-3 border border-blue-500 border-t-transparent rounded-full animate-spin" />
                )}
              </div>
            </button>
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-hidden min-h-0">
            {activeTab === "code" && (
              <div className="h-full w-full overflow-auto">
                <CodeMirror
                  value={template.template as string || DEFAULT_DOCUMENT_TEMPLATE}
                  onChange={handleCodeChange}
                  extensions={[html()]}
                  theme="light"
                  height="100%"
                  className="text-xs lg:text-sm"
                  basicSetup={{
                    lineNumbers: true,
                    foldGutter: true,
                    dropCursor: false,
                    allowMultipleSelections: false,
                    indentOnInput: true,
                    bracketMatching: true,
                    closeBrackets: true,
                    autocompletion: true,
                    highlightSelectionMatches: false,
                  }}
                />
              </div>
            )}

            {activeTab === "data" && (
              <div className="h-full flex flex-col bg-white min-h-0">
                <div className="flex items-center justify-between p-2 lg:p-3 border-b border-slate-200 flex-shrink-0">
                  <div className="flex items-center gap-2 min-w-0 flex-1">
                    <h3 className="text-xs lg:text-sm font-medium truncate">Sample Data</h3>
                    {template.related_object && (
                      <Badge variant="outline" className="text-xs flex-shrink-0">
                        {template.related_object} template
                      </Badge>
                    )}
                  </div>
                  <div className="flex items-center gap-1 lg:gap-2 flex-shrink-0">
                    <Button
                      onClick={() => {
                        const defaultSampleData = generateSampleData(template.related_object || 'shipment');
                        setSampleData(JSON.stringify(defaultSampleData, null, 2));
                      }}
                      variant="outline"
                      size="sm"
                      className="h-6 lg:h-7 px-1 lg:px-2 text-xs"
                    >
                      <RefreshCw className="h-3 w-3 lg:mr-1" />
                      <span className="hidden lg:inline">Reset</span>
                    </Button>
                  </div>
                </div>

                <div className="flex-1 overflow-auto">
                  <CodeMirror
                    value={sampleData}
                    onChange={(value) => setSampleData(value)}
                    extensions={[json()]}
                    theme="light"
                    height="100%"
                    className="text-xs lg:text-sm"
                    basicSetup={{
                      lineNumbers: true,
                      foldGutter: true,
                      dropCursor: false,
                      allowMultipleSelections: false,
                      indentOnInput: true,
                      bracketMatching: true,
                      closeBrackets: true,
                      autocompletion: true,
                      highlightSelectionMatches: false,
                    }}
                  />
                </div>

                <div className="border-t border-slate-200 p-2 lg:p-3 text-xs text-slate-500 flex-shrink-0">
                  <p>Edit the sample data above to customize the preview. Data must be valid JSON.</p>
                </div>
              </div>
            )}

            {activeTab === "options" && (
              <div className="h-full flex flex-col bg-white min-h-0">
                <div className="flex items-center justify-between p-2 lg:p-3 border-b border-slate-200 flex-shrink-0">
                  <div className="flex items-center gap-2 min-w-0 flex-1">
                    <h3 className="text-xs lg:text-sm font-medium truncate">Template Options</h3>
                  </div>
                  <div className="flex items-center gap-1 lg:gap-2 flex-shrink-0">
                    <Button
                      onClick={() => setOptions("{}")}
                      variant="outline"
                      size="sm"
                      className="h-6 lg:h-7 px-1 lg:px-2 text-xs"
                    >
                      <RefreshCw className="h-3 w-3 lg:mr-1" />
                      <span className="hidden lg:inline">Clear</span>
                    </Button>
                  </div>
                </div>
                <div className="flex-1 overflow-auto">
                  <CodeMirror
                    value={options}
                    onChange={(value) => setOptions(value)}
                    extensions={[json()]}
                    theme="light"
                    height="100%"
                    className="text-xs lg:text-sm"
                    basicSetup={{
                      lineNumbers: true,
                      foldGutter: true,
                      dropCursor: false,
                      allowMultipleSelections: false,
                      indentOnInput: true,
                      bracketMatching: true,
                      closeBrackets: true,
                      autocompletion: true,
                      highlightSelectionMatches: false,
                    }}
                  />
                </div>
                <div className="border-t border-slate-200 p-2 lg:p-3 text-xs text-slate-500 flex-shrink-0">
                  <p>Configure template options as JSON. These will be available in the template as variables.</p>
                </div>
              </div>
            )}

            {activeTab === "preview" && (
              <div className="h-full flex flex-col bg-white min-h-0">
                <div className="flex items-center justify-between p-2 lg:p-3 border-b border-slate-200 flex-shrink-0">
                  <div className="flex items-center gap-2 min-w-0 flex-1">
                    <h3 className="text-xs lg:text-sm font-medium truncate">Template Preview</h3>
                    {template.related_object && (
                      <Badge variant="outline" className="text-xs flex-shrink-0">
                        {template.related_object} data
                      </Badge>
                    )}
                  </div>
                  <div className="flex items-center gap-1 lg:gap-2 flex-shrink-0">
                    <Button
                      onClick={refreshPreview}
                      disabled={previewLoading || !template.template}
                      variant="outline"
                      size="sm"
                      className="h-6 lg:h-7 px-1 lg:px-2 text-xs"
                    >
                      <RefreshCw className={`h-3 w-3 ${previewLoading ? 'animate-spin' : ''} lg:mr-1`} />
                      <span className="hidden lg:inline">Refresh</span>
                    </Button>
                    {!isNew && template.id && (
                      <Button
                        onClick={handlePreview}
                        variant="outline"
                        size="sm"
                        className="h-6 lg:h-7 px-1 lg:px-2 text-xs"
                      >
                        <ExternalLink className="h-3 w-3 lg:mr-1" />
                        <span className="hidden lg:inline">Open</span>
                      </Button>
                    )}
                  </div>
                </div>

                <div className="flex-1 overflow-auto p-2 lg:p-4 min-h-0">
                  {previewLoading ? (
                    <div className="flex items-center justify-center h-full min-h-[200px]">
                      <div className="text-center space-y-2 lg:space-y-3">
                        <div className="h-6 w-6 lg:h-8 lg:w-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" />
                        <p className="text-xs lg:text-sm text-slate-600">Generating preview...</p>
                      </div>
                    </div>
                  ) : previewError ? (
                    <div className="flex items-center justify-center h-full min-h-[200px]">
                      <div className="text-center space-y-2 lg:space-y-3 max-w-xs lg:max-w-md mx-auto px-4">
                        <div className="h-10 w-10 lg:h-12 lg:w-12 bg-red-100 rounded-full flex items-center justify-center mx-auto">
                          <svg className="h-5 w-5 lg:h-6 lg:w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                          </svg>
                        </div>
                        <div>
                          <p className="text-xs lg:text-sm font-medium text-red-900">Preview Generation Failed</p>
                          <p className="text-xs text-red-700 mt-1 break-words">{previewError}</p>
                        </div>
                        <Button
                          onClick={() => {
                            setPreviewError(null);
                            generatePreview();
                          }}
                          size="sm"
                          variant="outline"
                          className="mt-2"
                        >
                          <RefreshCw className="h-3 w-3 mr-1" />
                          Try Again
                        </Button>
                      </div>
                    </div>
                  ) : previewContent ? (
                    <div
                      className="prose prose-xs lg:prose-sm max-w-none w-full"
                      dangerouslySetInnerHTML={{ __html: previewContent }}
                    />
                  ) : (
                    <div className="flex items-center justify-center h-full min-h-[200px]">
                      <div className="text-center space-y-2 lg:space-y-3 max-w-xs lg:max-w-md mx-auto px-4">
                        <FileText className="h-10 w-10 lg:h-12 lg:w-12 text-slate-400 mx-auto" />
                        <div>
                          <p className="text-xs lg:text-sm font-medium text-slate-900">No preview available</p>
                          <p className="text-xs text-slate-500 mt-1">
                            {!template.template
                              ? "Add template content to generate preview"
                              : !template.related_object
                                ? "Select a related object to generate preview"
                                : "Click refresh to generate preview"
                            }
                          </p>
                        </div>
                        {template.template && template.related_object && (
                          <Button
                            onClick={generatePreview}
                            size="sm"
                            className="mt-2"
                          >
                            Generate Preview
                          </Button>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
