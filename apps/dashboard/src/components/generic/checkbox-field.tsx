import React from 'react';

interface CheckBoxFieldComponent extends React.InputHTMLAttributes<any> {
  fieldClass?: string;
  labelClass?: string;
  controlClass?: string;
}

const CheckBoxField: React.FC<CheckBoxFieldComponent> = ({ fieldClass, controlClass, labelClass, children, ...props } = { fieldClass: "", controlClass: "", labelClass: "" }) => {
  return (
    <div className={`field ${fieldClass || ''}`}>
      <div className={`control ${controlClass || ''}`}>
        <label className={`checkbox is-capitalized ${labelClass || ''}`} style={{ fontSize: ".8em" }}>
          <input style={{ marginRight: ".5em" }} type="checkbox" {...props} />
          {children}
        </label>
      </div>
    </div>
  );
};

export default CheckBoxField;
