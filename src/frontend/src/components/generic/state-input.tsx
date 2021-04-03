import { isNone } from '@/library/helper';
import { Collection } from '@/library/types';
import React, { ChangeEvent, useContext, useEffect, useRef } from 'react';
import { APIReference } from '@/components/data/references-query';
import InputField, { InputFieldComponent } from '@/components/generic/input-field';

interface StateInputComponent extends InputFieldComponent {
    onValueChange: (value: string | null) => void;
    defaultValue?: string;
}

const StateInput: React.FC<StateInputComponent> = ({ name, onValueChange, defaultValue, ...props }) => {
    const onClick = (e: React.MouseEvent<HTMLInputElement>) => e.currentTarget.select();
    const input = useRef<HTMLInputElement>(null);
    const { states } = useContext(APIReference);
    const fname = (code_or_name?: string) => {
        const [_, name] = find(states, code_or_name);
        return name;
    };
    const onChange = (e: ChangeEvent<any>) => {
        e.preventDefault();
        let [code, name] = find(states, e.target.value);
        onValueChange(code || null);

        if (!isNone(code) && e.target.value === code) e.currentTarget.value = name;
    };

    useEffect(() => {}, [states]);

    return (
        <InputField onChange={onChange} onClick={onClick} defaultValue={fname(defaultValue)} list="state_or_provinces" {...props} ref={input}>
            <datalist id="state_or_provinces">
                {Object
                    .entries(states || {})
                    .map(([country, value]) => (
                        <optgroup label={country}>
                            {Object.entries(value as object).map(([state, name]) => (
                                <option key={state} value={name}>{state}</option>
                            ))}
                        </optgroup>
                    ))
                }
            </datalist>
        </InputField>
    )
};

function find(states?: object, code_or_name?: string): [string, string] | [] {
    const country: Collection<string> = (
        Object
            .values(states || {})
            .find(country => (
                Object.keys(country).includes(code_or_name as string) ||
                Object.values(country).includes(code_or_name as string)
            )) || {}
    );

    return (Object
        .entries(country)
        .find(([code, name]) => code === code_or_name || name === code_or_name) || []
    );
}

export default StateInput;
