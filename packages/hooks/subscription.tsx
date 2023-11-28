import React from 'react';
import { SubscriptionType } from '@karrio/types';

export const Subscription = React.createContext<{ subscription?: SubscriptionType }>({});

export const SubscriptionProvider: React.FC<{ subscription?: SubscriptionType, children?: React.ReactNode }> = ({ children, subscription }) => {
  return (
    <Subscription.Provider value={{ subscription }}>
      {children}
    </Subscription.Provider>
  );
};

export function useSubscription() {
  return React.useContext(Subscription);
}
