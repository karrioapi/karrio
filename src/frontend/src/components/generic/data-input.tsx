import React, { ChangeEvent, EventHandler, useRef } from 'react';

interface DataInputComponent<T> extends React.AllHTMLAttributes<HTMLDivElement> {
    state: T | undefined;
    onChange: EventHandler<any>;
}

const DataInput: React.FC<DataInputComponent<object>> = ({ state, onChange, children, ...props }) => {
    const ref = useRef<any>(null);
    ref?.current?.addEventListener('change', (e: ChangeEvent<any>) => {
        e.stopPropagation();
        const property = e.target.name;
        const data = { ...state, [property]: e.target.type === 'checkbox' ? e.target.checked : e.target.value };
        onChange(new CustomEvent('change', { bubbles: true, detail: { value: data, name: 'duty' } } as any));
    });

    return (
        <div {...props} ref={ref}>{children}</div>
    )
};

export default DataInput;