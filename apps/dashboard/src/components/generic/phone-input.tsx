import InputField, { InputFieldComponent } from '@/components/generic/input-field';
import parsePhoneNumber, { AsYouType, PhoneNumber } from 'libphonenumber-js';
import React, { ChangeEvent } from 'react';

interface PhoneInputComponent extends InputFieldComponent {
  country?: string;
  onValueChange: (value: string | null) => void;
}

const PhoneInput: React.FC<PhoneInputComponent> = ({ country, onValueChange, ...props }) => {
  const onClick = (e: React.MouseEvent<HTMLInputElement>) => e.currentTarget.select();
  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    const [formatted, isValid] = formatPhoneNumber(e.target.value);
    if (formatted !== e.target.value) e.target.value = formatted;
    if (!isValid) {
      e.target.setCustomValidity(`Invalid Phone Number ${samplePhoneNumber(country)}`);
      e.target.classList.add('is-danger');
    }
    else {
      e.target.setCustomValidity("");
      e.target.classList.remove('is-danger');
    }
    onValueChange(formatted);
  };

  return (
    <InputField onChange={onChange} onClick={onClick} {...props} />
  )
};

function formatPhoneNumber(phoneNumber: string): [string, boolean] {
  const phone = parsePhoneNumber(phoneNumber) as PhoneNumber;
  return [new AsYouType().input(phoneNumber), phone?.isValid() || true];
}

function samplePhoneNumber(country_code?: string) {
  if (['CA', 'US'].includes(country_code as string)) return '1234567890, 123 456 7890, (123) 456 7890';
  return '';
}

export default PhoneInput;
