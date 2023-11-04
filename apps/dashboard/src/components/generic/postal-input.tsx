import InputField, { InputFieldComponent } from '@/components/generic/input-field';
import React, { ChangeEvent } from 'react';

interface PostalInputComponent extends InputFieldComponent {
  country?: string;
  onValueChange: (value: string | null) => void;
}

const PostalInput: React.FC<PostalInputComponent> = ({ country, onValueChange, ...props }) => {
  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    const [formatted, isValid] = formatPostalCode(e.target.value, country);
    if (formatted !== e.target.value) e.target.value = formatted;
    if (!isValid && formatted !== "") {
      e.target.setCustomValidity(`Invalid Postal code ${samplePostalCode(country)}`);
      e.target.classList.add('is-danger');
    }
    else {
      e.target.setCustomValidity("");
      e.target.classList.remove('is-danger');
    }
    onValueChange(formatted);
  };


  return (
    <InputField onChange={onChange} {...props} />
  )
};

function formatPostalCode(postal_code: string, country_code?: string): [string, boolean] {
  if (country_code === 'CA') return [
    postal_code.toLocaleUpperCase(),
    (/^([A-Za-z]\d[A-Za-z][-\s]?\d[A-Za-z]\d)/).test(postal_code)
  ];
  if (country_code === 'US') return [
    postal_code.trim(),
    (/^[0-9]{5}(?:-[0-9]{4})?$/).test(postal_code)
  ];
  return [postal_code, true];
}

function samplePostalCode(country_code?: string) {
  if (country_code === 'CA') return 'A1A1A1 or A1A 1A1';
  if (country_code === 'US') return 'Zip5 12345 or Zip4 12345-6789';
  return '';
}

export default PostalInput;
