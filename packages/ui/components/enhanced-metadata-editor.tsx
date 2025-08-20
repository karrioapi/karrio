import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Badge } from "./ui/badge";
import { PlusCircle, X, Eye, EyeOff, RotateCcw, Edit3 } from "lucide-react";

export type MetadataValue = string | number | boolean | null;
export type Metadata = Record<string, MetadataValue>;

interface EnhancedMetadataEditorProps {
  value?: Metadata;
  onChange?: (metadata: Metadata) => void;
  className?: string;
  placeholder?: string;
  emptyStateMessage?: string;
  allowEdit?: boolean;
  showTypeInference?: boolean;
  maxHeight?: string;
}

export function EnhancedMetadataEditor({
  value = {},
  onChange,
  className = "",
  placeholder = "No metadata configured",
  emptyStateMessage = "Add key-value pairs to configure metadata",
  allowEdit = true,
  showTypeInference = true,
  maxHeight = "300px",
}: EnhancedMetadataEditorProps) {
  const [metadata, setMetadata] = useState<Metadata>(value);
  const [newKey, setNewKey] = useState("");
  const [newValue, setNewValue] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [editingKey, setEditingKey] = useState<string | null>(null);

  // Sync internal state with external value changes
  useEffect(() => {
    setMetadata(value);
  }, [value]);

  const inferType = (value: string): MetadataValue => {
    if (value === "true") return true;
    if (value === "false") return false;
    if (value === "null") return null;
    if (value === "") return "";
    
    // Try to parse as number
    const num = Number(value);
    if (!isNaN(num) && isFinite(num) && value.trim() !== "") {
      return num;
    }
    
    return value;
  };

  const getTypeLabel = (value: MetadataValue): string => {
    if (value === null) return "null";
    if (typeof value === "boolean") return "boolean";
    if (typeof value === "number") return "number";
    return "string";
  };

  const getTypeColor = (value: MetadataValue): string => {
    if (value === null) return "bg-gray-100 text-gray-600";
    if (typeof value === "boolean") return "bg-blue-100 text-blue-700";
    if (typeof value === "number") return "bg-green-100 text-green-700";
    return "bg-purple-100 text-purple-700";
  };

  const handleAdd = () => {
    if (!newKey.trim()) return;

    const processedValue = inferType(newValue);
    const updatedMetadata = {
      ...metadata,
      [newKey]: processedValue,
    };
    setMetadata(updatedMetadata);
    onChange?.(updatedMetadata);
    setNewKey("");
    setNewValue("");
  };

  const handleRemove = (key: string) => {
    const { [key]: _, ...rest } = metadata;
    setMetadata(rest);
    onChange?.(rest);
  };

  const handleUpdate = (key: string, value: string) => {
    const processedValue = inferType(value);
    const updatedMetadata = {
      ...metadata,
      [key]: processedValue,
    };
    setMetadata(updatedMetadata);
    onChange?.(updatedMetadata);
  };

  const handleReset = () => {
    setMetadata({});
    onChange?.({});
    setNewKey("");
    setNewValue("");
  };

  const handleKeyPress = (e: React.KeyboardEvent, action: () => void) => {
    if (e.key === "Enter") {
      e.preventDefault();
      action();
    }
  };

  const toggleEditing = () => {
    if (!allowEdit) return;
    setIsEditing(!isEditing);
    setEditingKey(null);
  };

  const hasMetadata = Object.keys(metadata).length > 0;

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-slate-700">Metadata</span>
          {hasMetadata && (
            <Badge variant="outline" className="text-xs">
              {Object.keys(metadata).length} {Object.keys(metadata).length === 1 ? 'item' : 'items'}
            </Badge>
          )}
        </div>
        <div className="flex items-center gap-2">
          {hasMetadata && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={handleReset}
              className="h-7 px-2 text-xs text-slate-500"
            >
              <RotateCcw className="h-3 w-3 mr-1" />
              Reset
            </Button>
          )}
          {allowEdit && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={toggleEditing}
              className="h-7 px-2 text-xs"
            >
              {isEditing ? (
                <>
                  <EyeOff className="h-3 w-3 mr-1" />
                  View
                </>
              ) : (
                <>
                  <Edit3 className="h-3 w-3 mr-1" />
                  Edit
                </>
              )}
            </Button>
          )}
        </div>
      </div>

      {/* Content */}
      <div 
        className="space-y-2 overflow-auto border rounded-lg p-3 bg-slate-50"
        style={{ maxHeight }}
      >
        {/* Existing metadata */}
        {hasMetadata ? (
          <div className="space-y-2">
            {Object.entries(metadata).map(([key, value]) => (
              <div key={key} className="flex items-center gap-2 p-2 bg-white rounded border">
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-slate-700 truncate">{key}</div>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-sm text-slate-600 break-all">
                      {value?.toString() ?? "null"}
                    </span>
                    {showTypeInference && (
                      <Badge variant="secondary" className={`text-xs ${getTypeColor(value)}`}>
                        {getTypeLabel(value)}
                      </Badge>
                    )}
                  </div>
                </div>
                {isEditing && allowEdit && (
                  <div className="flex items-center gap-1">
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => setEditingKey(editingKey === key ? null : key)}
                      className="h-7 px-2"
                    >
                      <Edit3 className="h-3 w-3" />
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRemove(key)}
                      className="h-7 px-2 text-red-600 hover:text-red-700"
                    >
                      <X className="h-3 w-3" />
                    </Button>
                  </div>
                )}
                {/* Inline edit form */}
                {isEditing && editingKey === key && (
                  <div className="absolute inset-0 bg-white border rounded p-2 z-10">
                    <div className="flex items-center gap-2">
                      <Input
                        value={key}
                        disabled
                        className="flex-1 bg-gray-50 text-sm"
                      />
                      <Input
                        defaultValue={value?.toString() ?? ""}
                        onChange={(e) => handleUpdate(key, e.target.value)}
                        onKeyDown={(e) => handleKeyPress(e, () => setEditingKey(null))}
                        className="flex-1 text-sm"
                        placeholder="Enter value"
                        autoFocus
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => setEditingKey(null)}
                        className="h-7 px-2"
                      >
                        <X className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-slate-500">
            <div className="text-sm">{placeholder}</div>
            <div className="text-xs mt-1 text-slate-400">{emptyStateMessage}</div>
          </div>
        )}

        {/* Add new metadata form */}
        {isEditing && allowEdit && (
          <div className="border-t pt-3 mt-3">
            <div className="flex items-end gap-2">
              <div className="flex-1">
                <Input
                  value={newKey}
                  onChange={(e) => setNewKey(e.target.value)}
                  onKeyDown={(e) => handleKeyPress(e, handleAdd)}
                  placeholder="Enter key"
                  className="text-sm"
                />
              </div>
              <div className="flex-1">
                <Input
                  value={newValue}
                  onChange={(e) => setNewValue(e.target.value)}
                  onKeyDown={(e) => handleKeyPress(e, handleAdd)}
                  placeholder="Enter value (auto-typed)"
                  className="text-sm"
                />
              </div>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleAdd}
                disabled={!newKey.trim()}
                className="h-9 px-3"
              >
                <PlusCircle className="h-4 w-4" />
              </Button>
            </div>
            {showTypeInference && (
              <div className="text-xs text-slate-500 mt-2">
                Values are automatically typed: "true"/"false" → boolean, numbers → number, "null" → null
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}