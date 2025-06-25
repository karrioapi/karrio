// This file is deprecated and replaced by useAddressAutocomplete hook
// Re-exporting types for backward compatibility

export interface QueryAutocompletePrediction {
  id: string;
  description: string;
  details: any;
}

export type AutocompleteConfig = {
  is_enabled: boolean;
  provider?: string;
  url?: string;
  key?: string;
};

// Legacy function for backward compatibility - will be removed
// Use useAddressAutocomplete hook instead
export function initDebouncedPrediction(data: any) {
  console.warn('initDebouncedPrediction is deprecated. Use useAddressAutocomplete hook instead.');
  return undefined;
}
