import React from 'react';

interface ButtonFieldComponent extends React.ButtonHTMLAttributes<any> {
    fieldClass?: string;
    controlClass?: string;
}

const ButtonField: React.FC<ButtonFieldComponent> = ({ className, fieldClass, controlClass, children, ...props } = { className: "", fieldClass: "", controlClass: ""}) => {
    return (
        <div className={`field ${fieldClass}`}>
            <div className={`control ${controlClass}`}>
                <button className={`button ${className}`} {...props}>{children}</button>
            </div>
        </div>
    )
};

export default ButtonField;