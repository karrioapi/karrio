import InputField, { InputFieldComponent } from '@/components/generic/input-field';
import { useAPIMetadata } from '@/context/api-metadata';
import { isNoneOrEmpty } from '@/lib/helper';
import React, { ChangeEvent } from 'react';
import { Collection } from '@/lib/types';

interface StateInputComponent extends InputFieldComponent {
  onValueChange: (value: string | null) => void;
  value?: string;
  country_code?: string;
}

const StateInput: React.FC<StateInputComponent> = ({ name, country_code, value, onValueChange, ...props }) => {
  const onClick = (e: React.MouseEvent<HTMLInputElement>) => e.currentTarget.select();
  const { references: { states } } = useAPIMetadata();

  const onChange = (e: ChangeEvent<any>) => {
    e.preventDefault();
    let code = find(states, e.target.value, country_code);
    onValueChange(code || e.target.value);
  };

  return (
    <InputField onChange={onChange} onClick={onClick} defaultValue={value} list="state_or_provinces" {...props}>
      <datalist id="state_or_provinces">
        {Object
          .entries(states || {})
          .map(([country, data], index) => (
            <optgroup key={index} label={country}>
              {Object.entries(data as object).map(([state, name]) => (
                <option key={state} value={name}>{state}</option>
              ))}
            </optgroup>
          ))
        }
      </datalist>
    </InputField>
  );
};

function find(states?: Collection<Collection<string>>, code_or_name?: string, current_country?: string): string | null {
  const retrieve = (countryStates: Collection<string>) => {
    const state = code_or_name || '';

    return Object
      .keys(countryStates)
      .find(key => {
        const value = countryStates[key];
        return (
          key === state.toLocaleUpperCase() ||
          value.toLocaleLowerCase().includes(state.toLocaleLowerCase())
        );
      });
  };


  return Object
    .entries(states || {})
    .reduce<string | null>((acc, [country, data]) => {
      if (isNoneOrEmpty(code_or_name)) return acc;

      const state = retrieve(data as Collection<string>);

      if (state && !acc) { return state; }
      if (state && country === current_country) { return state; }

      return acc;
    }, null);
}

export default StateInput;
