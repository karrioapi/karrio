import { NotificationType, state } from '@/library/api';
import { RequestError } from '@/library/types';
import React from 'react';

interface NotifierComponent { }

const Notifier: React.FC<NotifierComponent> = () => {
    const notification = state.notification;
    const dismiss = (evt: React.MouseEvent) => {
        evt.preventDefault();
        state.setNotification();
    }

    if (notification === undefined) {
        return <></>;
    }

    return (
        <div className={`notification ${notification?.type || NotificationType.info} purplship-notifier`}>
            <button className="delete" onClick={dismiss}></button>
            {formatMessage(notification?.message)}
        </div>
    )
};

const formatMessage = (msg: string | Error | RequestError) => {
    if (typeof msg === 'string') {
        return msg;
    } else if (msg instanceof RequestError) {
        const error = msg.data.error.details;
        return (error.messages || []).map(msg => {
            const carrier_name = msg.carrier_name !== undefined ? `${msg.carrier_name} :` : '';
            return <p>{carrier_name} {msg.message}</p>;
        });
    }

    return msg.message;
};

export default Notifier;