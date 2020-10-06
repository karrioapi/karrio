import { state } from '@/library/api';
import React from 'react';

interface DisconnectProviderButtonComponent {
    providerId: string;
    className?: string;
}

const DisconnectProviderButton: React.FC<DisconnectProviderButtonComponent> = ({ children, providerId, ...props }) => {
    const handleOnClick = async (evt: React.MouseEvent) => {
        evt.preventDefault();
        state.disconnectProvider(providerId);
    };

    return (
        <button {...props} onClick={handleOnClick}>
            {children}
        </button>
    )
};

export default DisconnectProviderButton;