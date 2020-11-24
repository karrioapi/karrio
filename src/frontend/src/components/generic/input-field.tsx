import React from 'react';

interface InputFieldComponent extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    fieldClass?: string;
    controlClass?: string;
}

const InputField: React.FC<InputFieldComponent> = ({ label, required, className, fieldClass, controlClass, children, ...props }) => {
    const Props = {
        required,
        ...props
    };
    return (
        <div className={`field ${fieldClass}`}>
            {label !== undefined && <label className="label is-capitalized" style={{fontSize: ".8em"}}>
                {label} 
                {required && <span className="icon is-small has-text-danger small-icon"><i className="fas fa-asterisk"></i></span>}
            </label>}
            <div className={`control ${controlClass}`}>
                <input type="text" className={`input ${className}`} {...Props}/>
                {children}
            </div>
        </div>
    )
};

export default InputField;