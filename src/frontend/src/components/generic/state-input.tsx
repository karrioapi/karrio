import { Reference } from '@/library/context';
import { Collection } from '@/library/types';
import React, { ChangeEvent, useContext, useEffect, useState } from 'react';
import InputField, { InputFieldComponent } from '@/components/generic/input-field';

interface StateInputComponent extends InputFieldComponent {
    onValueChange: (value: string | null) => void;
    defaultValue?: string;
}

const StateInput: React.FC<StateInputComponent> = ({ defaultValue, onValueChange, ...props }) => {
    const onClick = (e: React.MouseEvent<HTMLInputElement>) => e.currentTarget.select();
    const Ref = useContext(Reference);
    const [states, setStates] = useState<Collection<Collection>>(Ref?.states || {});
    const onChange = (e: ChangeEvent<any>) => {
        e.preventDefault();
        let value = find(states, e.target.value);
        onValueChange(value || e.target.value);
    };
    useEffect(() => { 
        if(Ref !== undefined) {
            setStates(Ref.states);
        }
    }, [states]);

    return (<>
        <InputField onChange={onChange} onClick={onClick} defaultValue={find(Ref?.states, defaultValue)} list="state_or_provinces" {...props}>
            <datalist id="state_or_provinces">
                {Object
                    .entries(Ref?.states || {})
                    .map(([_, value]) => (
                        <>
                            {Object.entries(value as object).map(([state, name]) => (
                                <option key={state} value={state}>{name}</option>
                            ))}
                        </>
                    ))
                }
            </datalist>
        </InputField>
    </>)
};

function find(states: Collection<Collection<string>>, code_or_name?: string): string | undefined {
    const country = (
        Object
            .values(states || {})
            .find(country => (
                Object.keys(country).includes(code_or_name as string) ||
                Object.values(country).includes(code_or_name as string)
            )) || {}
    );

    const [code] = (Object
        .entries(country)
        .find(([code, name]) => code === code_or_name || name === code_or_name) || []
    );

    return code;
}

export default StateInput;