import React, { useContext, useEffect, useState } from 'react';
import DropdownInput, { DropdownInputComponent } from '@/components/generic/dropdown-input';
import { Reference } from '@/library/context';
import { isNone } from '@/library/helper';
import { Collection } from '@/library/types';

interface CountryInputComponent extends Omit<DropdownInputComponent, 'items'> {}

const CountryInput: React.FC<CountryInputComponent> = ({ name, ...props }) => {
    const Ref = useContext(Reference);
    const [items, setItems] = useState<[string, string][]>();

    useEffect(() => {
        if (!isNone(Ref?.countries)) {
            setItems(Object.entries(Ref.countries as Collection).map((value) => value));
        }
    }, [Ref?.countries]);

    return (
        <DropdownInput name={name || 'country'} items={items} {...props}/>
    )
};

export default CountryInput;