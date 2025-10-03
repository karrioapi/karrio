import { useQuery } from "@tanstack/react-query";
import { useState, useCallback, useEffect } from "react";
import { Address } from "@karrio/types/rest/api";

export interface QueryAutocompletePrediction {
  id: string;
  description: string;
  details: any;
}

type GooglePrediction = {
  place_id: string;
  description: string;
  structured_formatting: {
    main_text: string;
    secondary_text: string;
  };
  terms: {
    offset: number;
    value: string;
  }[]
}

type CanadaPostPrediction = {
  Id: string,
  Text: string,
  Highlight: string,
  Cursor: string,
  Description: string,
  Next: string,
}

export type AutocompleteConfig = {
  is_enabled: boolean;
  provider?: string;
  url?: string;
  key?: string;
};

// Hook for address autocomplete predictions
export function useAddressAutocomplete(
  input: string,
  country_code?: string,
  config?: AutocompleteConfig,
  debounceMs: number = 500
) {
  const [debouncedInput, setDebouncedInput] = useState("");

  // Debounce the input
  const debounceInput = useCallback(
    (() => {
      let timeoutId: NodeJS.Timeout;
      return (value: string) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => setDebouncedInput(value), debounceMs);
      };
    })(),
    [debounceMs]
  );

  // Update debounced input when input changes
  useEffect(() => {
    debounceInput(input);
  }, [input, debounceInput]);

  const queryEnabled = Boolean(
    config?.is_enabled &&
    debouncedInput &&
    debouncedInput.length > 2
  );

  return useQuery(
    ['address-autocomplete', debouncedInput, country_code, config?.provider],
    async (): Promise<QueryAutocompletePrediction[]> => {
      if (!config?.is_enabled || !debouncedInput) return [];

      if (config.provider === 'google') {
        return await getGooglePredictions(debouncedInput, country_code);
      } else if (config.provider === 'canadapost') {
        return await getCanadaPostPredictions(debouncedInput, country_code, config.key);
      }

      return [];
    },
    {
      enabled: queryEnabled,
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes (gcTime in v5)
      refetchOnWindowFocus: false,
      retry: 1,
    }
  );
}

// Hook for formatting address prediction
export function useAddressPredictionFormat(config?: AutocompleteConfig) {
  const formatPrediction = useCallback(async (
    prediction: QueryAutocompletePrediction
  ): Promise<Partial<Address>> => {
    if (!config?.is_enabled) return {};

    if (config.provider === 'google') {
      return await formatGooglePrediction(prediction);
    } else if (config.provider === 'canadapost') {
      return await formatCanadaPostPrediction(prediction, config.key);
    }

    return {};
  }, [config]);

  return { formatPrediction };
}

// Google Places API implementation
async function getGooglePredictions(
  input: string,
  country_code?: string
): Promise<QueryAutocompletePrediction[]> {
  try {
    const url = `/api/places/autocomplete?input=${encodeURIComponent(input)}${country_code ? `&country=${country_code}` : ''
      }`;
    const res = await fetch(url);
    const data = await res.json();

    return (data.predictions || []).map((prediction: any) => ({
      id: prediction.place_id,
      description: prediction.description,
      details: prediction,
    }));
  } catch (e) {
    console.error('[Autocomplete] Error in getGooglePredictions:', e);
    return [];
  }
}

async function formatGooglePrediction(
  prediction: QueryAutocompletePrediction
): Promise<Partial<Address>> {
  try {
    const url = `/api/places/details?place_id=${encodeURIComponent(prediction.id)}`;
    const res = await fetch(url);
    const data = await res.json();
    const place = data.result;

    let address: Partial<Address> = {};
    if (place && place.address_components) {
      for (const component of place.address_components) {
        const componentType = component.types[0];
        switch (componentType) {
          case "street_number": {
            address.address_line1 = component.long_name;
            break;
          }
          case "route": {
            address.address_line1 = [component.short_name, address.address_line1]
              .filter(v => v).join(' ');
            break;
          }
          case "postal_code": {
            address.postal_code = component.long_name;
            break;
          }
          case "postal_code_suffix": {
            address.postal_code = `${address.postal_code}-${component.long_name}`;
            break;
          }
          case "locality":
            address.city = component.long_name;
            break;
          case "administrative_area_level_1": {
            address.state_code = component.short_name;
            break;
          }
          case "country":
            address.country_code = component.short_name;
            break;
        }
      }
    }
    return address;
  } catch (err) {
    console.error('[Autocomplete] Error in formatGooglePrediction:', err);
    return {};
  }
}

// Canada Post API implementation
async function getCanadaPostPredictions(
  input: string,
  country_code?: string,
  apiKey?: string
): Promise<QueryAutocompletePrediction[]> {
  if (!apiKey) return [];

  try {
    const url = "http://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/v2.10/json3.ws";
    const formData = new URLSearchParams({
      Key: apiKey,
      SearchTerm: input,
      Country: country_code || '',
      SearchFor: 'Places',
      LanguagePreference: 'EN',
      MaxSuggestions: '7',
      MaxResults: '7'
    });

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData
    });

    const data = await response.json();

    if (data.Items.length === 1 && typeof data.Items[0].Error !== "undefined") {
      return [];
    }

    return data.Items.map((prediction: CanadaPostPrediction) => ({
      id: prediction.Id,
      description: `${prediction.Text}, ${prediction.Description}`,
      details: prediction
    }));
  } catch (e) {
    console.error('[Autocomplete] Error in getCanadaPostPredictions:', e);
    return [];
  }
}

async function formatCanadaPostPrediction(
  prediction: QueryAutocompletePrediction,
  apiKey?: string
): Promise<Partial<Address>> {
  if (!apiKey) return {};

  try {
    const url = "http://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Retrieve/v2.11/json3.ws";
    const formData = new URLSearchParams({
      Key: apiKey,
      Id: prediction.id
    });

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData
    });

    const data = await response.json();
    const place = data.Items[0];

    if (place && !place.Error) {
      return {
        address_line1: place.Line1,
        address_line2: place.Line2,
        city: place.City,
        country_code: place.CountryIso2,
        postal_code: place.PostalCode,
        state_code: place.ProvinceCode,
        residential: place.Type === "Residential"
      };
    }

    return {};
  } catch (err) {
    console.error('[Autocomplete] Error in formatCanadaPostPrediction:', err);
    return {};
  }
}
