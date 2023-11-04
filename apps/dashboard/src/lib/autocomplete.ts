import { Address } from "karrio/rest";
import { Subject } from "rxjs";
import { debounceTime } from "rxjs/operators";

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

type GooglePlace = {
  address_components: Array<any>
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

type AddressCallback = (address: Partial<Address>) => void;
type PredictionCallback = (predictions: QueryAutocompletePrediction[]) => void;
type PredictionInput = { input: string, country_code: string | undefined };

export interface AutocompleteService {
  getPlacePredictions: (params: PredictionInput, callback: PredictionCallback) => void;
  formatPrediction: (prediction: QueryAutocompletePrediction, callback: AddressCallback) => void;
}

export function initDebouncedPrediction(data: any) {
  if (!data?.is_enabled) return undefined;

  const request: Subject<{ params: PredictionInput, callback: PredictionCallback }> = new Subject();
  const serviceType = {
    google: initGoogleService,
    canadapost: initCanadaPostService
  }[data.provider as string];
  const service = serviceType !== undefined ? serviceType(data) : undefined;

  request.pipe(debounceTime(500)).subscribe((data) => {
    service?.getPlacePredictions(data.params, data.callback);
  });

  return {
    getPlacePredictions: (params: PredictionInput, callback: PredictionCallback) => {
      request.next({ params, callback });
    },
    formatPrediction: (prediction: QueryAutocompletePrediction, callback: AddressCallback) => {
      return service?.formatPrediction(prediction, callback);
    }
  };
}

function initGoogleService(): AutocompleteService {
  const autocomplete = new (window as any).google.maps.places.AutocompleteService();
  const placesService = new (window as any).google.maps.places.PlacesService(document.createElement('div'));

  return {
    getPlacePredictions(params, callback) {
      autocomplete.getPlacePredictions({
        input: params.input,
        componentRestrictions: {
          country: params.country_code
        },
        types: ['address'] // Maybe places also can be used
      }, (result: GooglePrediction[], status: string) => {
        if (status === "OK") {
          const predictions: QueryAutocompletePrediction[] = result.map(prediction => {
            return {
              id: prediction.place_id,
              description: prediction.description,
              details: prediction
            }
          });
          callback(predictions);
        } else {
          callback([])
        }
      });
    },
    formatPrediction(prediction: QueryAutocompletePrediction, callback) {
      placesService.getDetails({ placeId: prediction.id }, (place: GooglePlace, status: string) => {
        if (status === "OK") {
          let address: Partial<Address> = {};

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
                address.country_code = component.short_name
                break;
            }
          }
          callback(address);
        }
      });
    }
  };
}

function initCanadaPostService(data: AutocompleteConfig): AutocompleteService {

  const request = (url: string, formData: Object, callback: (response: any) => void) => {
    const xhr = new XMLHttpRequest();
    const payload = Object.entries(formData).reduce((formData: any, [key, value]) => {
      return key && value ?
        `${formData}&${encodeURIComponent(key)}=${encodeURIComponent(value || '')}` : formData;
    }, `Key=${data.key}`);

    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200) {
        const response = JSON.parse(xhr.responseText);
        callback(response);
      }
    };
    xhr.send(payload);
  }

  return {
    getPlacePredictions(params, callback) {
      try {
        const url = "http://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/v2.10/json3.ws";
        const formData = {
          SearchTerm: params.input,
          Country: params.country_code,
          SearchFor: 'Places',
          LanguagePreference: 'EN',
          MaxSuggestions: 7,
          MaxResults: 7
        };

        request(url, formData, response => {
          if (response.Items.length == 1 && typeof (response.Items[0].Error) != "undefined") {
            callback([]);
          } else {
            const predictions: QueryAutocompletePrediction[] = response.Items.map((prediction: CanadaPostPrediction) => {
              const country = (prediction.Id || '').split('|')[0].slice(0, 2);

              return {
                id: prediction.Id,
                description: `${prediction.Text}, ${prediction.Description}`,
                details: prediction
              }
            });
            callback(predictions)
          }
        });
      } catch (e) {
        callback([]);
      }
    },
    formatPrediction(prediction: QueryAutocompletePrediction, callback) {
      let url = "http://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Retrieve/v2.11/json3.ws";
      let formData = { Id: prediction.id };

      request(url, formData, response => {
        const place = response.Items[0];

        if (place && !place.Error) {
          const address: Partial<Address> = {
            address_line1: place.Line1,
            address_line2: place.Line2,
            city: place.City,
            country_code: place.CountryIso2,
            postal_code: place.PostalCode,
            state_code: place.ProvinceCode,
            residential: place.Type === "Residential"
          };

          callback(address);
        }
      });
    }
  };
}
