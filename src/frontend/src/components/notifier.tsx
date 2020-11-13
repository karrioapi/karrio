import { NotificationType, state } from '@/library/api';
import React from 'react';

interface NotifierComponent {}

const Notifier: React.FC<NotifierComponent> = () => {
    const notification = state.notification;
    const dismiss = (evt: React.MouseEvent) => {
        evt.preventDefault();
        state.setNotification();
    }

    if(notification === undefined) {
        return <></>;
    }

    return (
        <div className={`notification ${notification?.type || NotificationType.info} purplship-notifier`}>
            <button className="delete" onClick={dismiss}></button>
            {notification?.message}
        </div>
    )
};

export default Notifier;