import React, { type ReactNode } from 'react';

interface TailwindWrapperProps {
    children: ReactNode;
    className?: string;
}

export default function TailwindWrapper({
    children,
    className = ''
}: TailwindWrapperProps): JSX.Element {
    return (
        <div id="tailwind-selector" className={className}>
            {children}
        </div>
    );
}
