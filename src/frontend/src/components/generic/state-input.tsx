import { Reference } from '@/library/context';
import { Collection } from '@/library/types';
import React, { useContext, useEffect, useState } from 'react';
import DropdownInput, { DropdownInputComponent } from '@/components/generic/dropdown-input';
import { isNone } from '@/library/helper';

interface StateInputComponent extends Omit<DropdownInputComponent, 'items'> {
    country?: string;
}

const StateInput: React.FC<StateInputComponent> = ({ name, country, defaultValue, onValueChange, ...props }) => {
    const Ref = useContext(Reference);
    const [key, setKey] = useState<string>(`states-${Date.now()}`);
    const [items, setItems] = useState<[string, string][]>();
    const [value, setValue] = useState<string>();
    const onChange = (value?: string | null) => {
        const [state, _] = (value || '').split('|');
        onValueChange(state);
    };

    useEffect(() => {
        let current_value = value;
        if (!isNone(Ref?.states)) {
            const states = Object
                .entries(Ref.states as Collection<Collection>)
                .reduce((all, [cn, states]) => {
                    const country_states = Object.entries(states).map(([key, val]) => [`${key}|${cn}`, val]);
                    const country_selected = !isNone(country) && cn === country;
                    const match_state = Object.keys(states).includes(defaultValue as string);

                    if ((country_selected && match_state) || (isNone(country) && match_state))
                        current_value = `${defaultValue}|${country}`;

                    return all.concat(country_selected || isNone(country) ? country_states as [string, string][] : []);
                }, [] as [string, string][]);

            setItems(states);
        }
        if (!isNone(country) && !isNone(defaultValue)) {
            const [_, cn] = (current_value || '').split('|');
            const new_value = cn === country ? current_value : undefined;
            setValue(new_value);
            onChange(new_value);
            setKey(`states-${Date.now()}`);
        }
    }, [Ref?.states, defaultValue, country]);

    return (
        <DropdownInput key={key} name={name || 'state'} items={items} defaultValue={value} onValueChange={onChange} required={(items || []).length > 0} {...props} />
    )
};

export default StateInput;
