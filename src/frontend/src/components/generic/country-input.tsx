import React, { useContext, useEffect, useState } from 'react';
import DropdownInput, { DropdownInputComponent } from '@/components/generic/dropdown-input';
import { isNone } from '@/library/helper';
import { Collection } from '@/library/types';
import { APIReference } from '@/components/data/references-query';

interface CountryInputComponent extends Omit<DropdownInputComponent, 'items'> { }

const CountryInput: React.FC<CountryInputComponent> = ({ name, ...props }) => {
    const { countries } = useContext(APIReference);
    const [items, setItems] = useState<[string, string][]>();

    useEffect(() => {
        if (!isNone(countries)) {
            setItems(Object.entries(countries as Collection).map((value) => value));
        }
    }, [countries]);

    return (
        <DropdownInput name={name || 'country'} items={items} {...props} />
    )
};

export default CountryInput;