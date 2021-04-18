import React, { ChangeEvent, EventHandler, useRef } from 'react';

interface DataInputComponent<T> extends React.AllHTMLAttributes<HTMLDivElement> {
    state?: T | null;
    onChange: EventHandler<any>;
    name: string;
}

const DataInput: React.FC<DataInputComponent<object>> = ({ state, name, onChange, children, ...props }) => {
    const ref = useRef<any>(null);
    ref?.current?.addEventListener('change', (e: ChangeEvent<any>) => {
        e.stopPropagation();
        const property = e.target.name;
        const data = { ...state, [property]: e.target.type === 'checkbox' ? e.target.checked : e.target.value };
        onChange(new CustomEvent('change', { bubbles: true, detail: { value: data, name } } as any));
    });

    return (
        <div {...props} ref={ref}>{children}</div>
    )
};

export default DataInput;