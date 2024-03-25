import { isNone } from '@karrio/lib';
import React, { RefObject } from 'react';

export interface InputFieldComponent extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  addonRight?: JSX.Element;
  addonLeft?: JSX.Element;
  iconRight?: JSX.Element;
  iconLeft?: JSX.Element;
  ref?: RefObject<HTMLInputElement>;
}

export const InputField: React.FC<InputFieldComponent> = ({ label, required, className, fieldClass, controlClass, wrapperClass, children, ref, addonLeft, addonRight, iconLeft, iconRight, ...props }) => {
  const Ref = isNone(ref) ? { ref } : {};
  const Props = {
    required,
    ...props,
    ...(Object.keys(props).includes('value') ? { value: props.value || "" } : {}),
  };

  return (
    <div className={wrapperClass || "px-1 py-2"}>
      {label !== undefined && <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
        {label}
        {required && <span className="icon is-small has-text-danger small-icon">
          <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
        </span>}
      </label>}

      <div className={`field ${fieldClass || "p-0"}`}>
        {addonLeft ? <div className="control">{addonLeft}</div> : <></>}

        <div className={`control is-flex ${controlClass || ""}`}>
          <input type="text" className={`input ${className || ""}`} {...Props} {...Ref} />
          {iconLeft ? iconLeft : <></>}
          {iconRight ? iconRight : <></>}
        </div>

        {addonRight ? <div className="control">{addonRight}</div> : <></>}
      </div>

      {children}

    </div>
  )
};
