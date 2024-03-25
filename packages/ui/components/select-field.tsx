import React from 'react';

interface SelectFieldComponent extends React.SelectHTMLAttributes<any> {
  label?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  addonRight?: JSX.Element;
  addonLeft?: JSX.Element;
}

export const SelectField: React.FC<SelectFieldComponent> = ({ label, className, fieldClass, controlClass, wrapperClass, required, children, addonLeft, addonRight, ...props }) => {
  const Props = {
    required,
    ...props,
    ...(Object.keys(props).includes('value') ? { value: props.value || "" } : {}),
  };
  return (
    <div className={wrapperClass || ""}>

      {label !== undefined && <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
        {label}
        {required && <span className="icon is-small has-text-danger small-icon">
          <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
        </span>}
      </label>}

      <div className={`field ${fieldClass || ""}`}>
        {addonLeft ? <div className="control">{addonLeft}</div> : <></>}

        <div className={`control ${controlClass || ""}`}>
          <div className={`select ${className || ""}`}>
            <select {...Props}>
              {children}
            </select>
          </div>
        </div>

        {addonRight ? <div className="control">{addonRight}</div> : <></>}
      </div>

    </div>
  )
};
