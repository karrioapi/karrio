import { Subject } from "rxjs";
import { debounceTime } from "rxjs/operators";

export interface QueryAutocompletePrediction {
    description: string;
    place_id: string;
}

enum PlacesServiceStatus {
    OK = "OK"
};

type PredictionCallback = (predictions: QueryAutocompletePrediction[] | null, status: PlacesServiceStatus) => void;
type PredictionInput = { input: string };

export interface AutocompleteService {
    getPlacePredictions: (params: PredictionInput, callback: PredictionCallback) => void;
}

export function initDebouncedPrediction() {
    const request: Subject<{ params: PredictionInput, callback: PredictionCallback }> = new Subject();
    const service = new (window as any).google.maps.places.AutocompleteService();
    request.pipe(debounceTime(600)).subscribe((data) => {
        service.getPlacePredictions(data.params, data.callback);
    });

    return {
        getPlacePredictions: (params: PredictionInput, callback: PredictionCallback) => {
            request.next({ params, callback });
        }
    };
}
