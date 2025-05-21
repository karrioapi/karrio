import React from "react";

interface CheckBoxFieldProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  fieldClass?: string;
  labelClass?: string;
  controlClass?: string;
  children?: React.ReactNode;
}

export const CheckBoxField = ({
  fieldClass = "",
  controlClass = "",
  labelClass = "",
  children,
  ...props
}: CheckBoxFieldProps): JSX.Element => {
  return (
    <div className={`field ${fieldClass || ""}`}>
      <div className={`control ${controlClass || ""}`}>
        <label
          className={`checkbox is-capitalized ${labelClass || ""}`}
          style={{ fontSize: ".8em" }}
        >
          <input style={{ marginRight: ".5em" }} type="checkbox" {...props} />
          {children}
        </label>
      </div>
    </div>
  );
};
