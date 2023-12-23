import { isNone } from '@karrio/lib';
import React from 'react';

interface CheckBoxFieldComponent extends React.InputHTMLAttributes<any> {
  fieldClass?: string;
  labelClass?: string;
  controlClass?: string;
  children?: React.ReactNode;
}

export const CheckBoxField = React.forwardRef<HTMLInputElement, CheckBoxFieldComponent>((props, ref) => {
  const { fieldClass = "", controlClass = "", labelClass = "", children, ...Props } = props;

  return (
    <div className={`field ${fieldClass || ''}`}>
      <div className={`control ${controlClass || ''}`}>
        <label className={`checkbox is-capitalized ${labelClass || ''}`} style={{ fontSize: ".8em" }}>
          <input style={{ marginRight: ".5em" }} type="checkbox" {...Props} ref={ref} />
          {children}
        </label>
      </div>
    </div>
  );
});