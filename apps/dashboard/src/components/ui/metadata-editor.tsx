import * as React from 'react'
import { Plus, Trash2 } from 'lucide-react'
import { Button } from './button'
import { Input } from './input'

interface MetadataEditorProps {
  value: Record<string, any>
  onChange: (metadata: Record<string, any>) => void
}

export function EnhancedMetadataEditor({ value, onChange }: MetadataEditorProps) {
  const [entries, setEntries] = React.useState<Array<{ key: string; value: string }>>([])

  React.useEffect(() => {
    const metadataEntries = Object.entries(value || {}).map(([key, val]) => ({
      key,
      value: typeof val === 'string' ? val : JSON.stringify(val),
    }))
    setEntries(metadataEntries.length > 0 ? metadataEntries : [{ key: '', value: '' }])
  }, [value])

  const handleAddEntry = () => {
    const newEntries = [...entries, { key: '', value: '' }]
    setEntries(newEntries)
  }

  const handleRemoveEntry = (index: number) => {
    const newEntries = entries.filter((_, i) => i !== index)
    setEntries(newEntries)
    updateMetadata(newEntries)
  }

  const handleKeyChange = (index: number, newKey: string) => {
    const newEntries = [...entries]
    newEntries[index] = { ...newEntries[index], key: newKey }
    setEntries(newEntries)
    updateMetadata(newEntries)
  }

  const handleValueChange = (index: number, newValue: string) => {
    const newEntries = [...entries]
    newEntries[index] = { ...newEntries[index], value: newValue }
    setEntries(newEntries)
    updateMetadata(newEntries)
  }

  const updateMetadata = (entries: Array<{ key: string; value: string }>) => {
    const metadata = entries
      .filter((entry) => entry.key.trim() !== '')
      .reduce((acc, entry) => {
        try {
          // Try to parse as JSON first
          acc[entry.key] = JSON.parse(entry.value)
        } catch {
          // If parsing fails, use as string
          acc[entry.key] = entry.value
        }
        return acc
      }, {} as Record<string, any>)

    onChange(metadata)
  }

  return (
    <div className="space-y-4">
      <div className="text-sm text-muted-foreground">
        Add custom metadata key-value pairs for this connection.
      </div>

      <div className="space-y-2">
        {entries.map((entry, index) => (
          <div key={index} className="flex gap-2 items-start">
            <Input
              placeholder="Key"
              value={entry.key}
              onChange={(e) => handleKeyChange(index, e.target.value)}
              className="flex-1"
            />
            <Input
              placeholder="Value"
              value={entry.value}
              onChange={(e) => handleValueChange(index, e.target.value)}
              className="flex-1"
            />
            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={() => handleRemoveEntry(index)}
              className="flex-shrink-0"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        ))}
      </div>

      <Button
        type="button"
        variant="outline"
        size="sm"
        onClick={handleAddEntry}
        className="w-full"
      >
        <Plus className="h-4 w-4 mr-2" />
        Add Metadata Field
      </Button>
    </div>
  )
}
