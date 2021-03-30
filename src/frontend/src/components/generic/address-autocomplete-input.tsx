import React, { ChangeEvent, useContext, useEffect, useState } from 'react';
import InputField, { InputFieldComponent } from '@/components/generic/input-field';
import { Address, AddressCountryCodeEnum } from '@/api';
import { isNone } from '@/library/helper';
import { initDebouncedPrediction, QueryAutocompletePrediction } from '@/library/autocomplete';
import { Reference } from '@/library/context';
import { Collection } from '@/library/types';

interface AddressAutocompleteInputComponent extends InputFieldComponent {
    onValueChange: (value: Partial<Address>) => void;
    defaultValue?: string;
    disableSuggestion?: boolean;
}

const AddressAutocompleteInput: React.FC<AddressAutocompleteInputComponent> = ({ defaultValue, onValueChange, ...props }) => {
    const Ref = useContext(Reference);
    const [predictions, setPredictions] = useState<QueryAutocompletePrediction[]>([]);
    const [predictor, initPredictor] = useState<ReturnType<typeof initDebouncedPrediction> | undefined>();
    const onClick = (e: React.MouseEvent<HTMLInputElement>) => e.currentTarget.select();
    const onInput = (e: ChangeEvent<any>) => {
        e.preventDefault();
        const value = e.target.value;

        if (predictor !== undefined) {
            let prediction = predictions.find(p => p.description.toLowerCase() === value.toLowerCase());
            let address: Partial<Address> = isNone(prediction) ? { address_line1: value } : addressValue(prediction as QueryAutocompletePrediction);
    
            onValueChange(address);

            if (isNone(prediction)) {
                predictor.getPlacePredictions(
                    { input: value },
                    (predictions, status) => {
                        const newPredictions = (status === "OK" ? predictions : []) as QueryAutocompletePrediction[];
                        setPredictions(newPredictions);
                    }
                );
                e.target.value = address.address_line1;
            }
        } else {
            onValueChange({ address_line1: value });
        }
    };

    const addressValue = (prediction: QueryAutocompletePrediction): Partial<Address> => {
        let extra: Partial<Address> = {};
        let content = prediction.description.split(', ');
        let address_line1 = prediction.description;

        if (content.length >= 3) {
            const [country, _] = Object.entries(Ref.countries as Collection).find(
                ([_, name]) => name.toLowerCase() === content[content.length - 1]
            ) || [];
            if (country !== undefined) extra.country_code = AddressCountryCodeEnum[country as (keyof typeof AddressCountryCodeEnum)];

            const state = content[content.length - 2];
            if (state !== undefined) extra.state_code = state;

            const city = content[content.length - 3];
            if (city !== undefined) extra.city = city;
        }

        if (content.length > 3) {
            address_line1 = (content.slice(0, content.length - 3)).join(' ');
        }
    
        return { address_line1, ...extra };
    };

    useEffect(() => {
        if ((window as any).google !== undefined) initPredictor(initDebouncedPrediction());
    }, [(window as any).google]);

    return (
        <InputField onInput={onInput} onClick={onClick} defaultValue={defaultValue} list="predictions" {...props}>
            <datalist id="predictions">
                {predictions
                    .map((prediction, index) => (
                        <option key={`${index}-auto-complete`} value={prediction.description}/>
                    ))
                }
            </datalist>
        </InputField>
    );
};

export default AddressAutocompleteInput;