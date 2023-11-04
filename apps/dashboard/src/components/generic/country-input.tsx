import DropdownInput, { DropdownInputComponent } from '@/components/generic/dropdown-input';
import { useAPIMetadata } from '@/context/api-metadata';
import React, { useEffect, useState } from 'react';
import { isNone } from '@/lib/helper';

interface CountryInputComponent extends Omit<DropdownInputComponent, 'items'> { }

const CountryInput: React.FC<CountryInputComponent> = ({ name, ...props }) => {
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

export default CountryInput;
