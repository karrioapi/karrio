import React from 'react';

interface SelectFieldComponent extends React.SelectHTMLAttributes<any> {
    label? : string;
    fieldClass?: string;
    controlClass?: string;
}

const SelectField: React.FC<SelectFieldComponent> = ({ label, className, fieldClass, controlClass, required, children, ...props }) => {
    const Props = {
        required,
        ...props
    };
    return (
        <div className={`field ${fieldClass}`}>

            {label !== undefined && <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
                {label}
                {required && <span className="icon is-small has-text-danger small-icon"><i className="fas fa-asterisk"></i></span>}
            </label>}

            <div className={`control ${controlClass}`}>
                <div className={`select ${className}`}>
                    <select {...Props}>
                        {children}
                    </select>
                </div>
            </div>
            
        </div>
    )
};

export default SelectField;