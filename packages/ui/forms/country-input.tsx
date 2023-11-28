import { DropdownInput, DropdownInputComponent } from '../components/dropdown-input';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import React, { useEffect, useState } from 'react';
import { isNone } from '@karrio/lib';

interface CountryInputComponent extends Omit<DropdownInputComponent, 'items'> { }

export const CountryInput: React.FC<CountryInputComponent> = ({ name, ...props }) => {
  const { references: { countries } } = useAPIMetadata();
  const [items, setItems] = useState<[string, string][]>();

  useEffect(() => {
    if (!isNone(countries)) {
      setItems(Object.entries(countries).map((value) => value));
    }
  }, [countries]);

  return (
    <DropdownInput name={name || 'country'} items={items} {...props} />
  )
};
