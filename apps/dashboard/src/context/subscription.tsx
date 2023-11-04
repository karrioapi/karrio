import React from 'react';
import { SubscriptionType } from '@/lib/types';

export const Subscription = React.createContext<{ subscription?: SubscriptionType }>({});

const SubscriptionProvider: React.FC<{ subscription?: SubscriptionType }> = ({ children, subscription }) => {
  return (
    <Subscription.Provider value={{ subscription }}>
      {children}
    </Subscription.Provider>
  );
};

export function useSubscription() {
  return React.useContext(Subscription);
}

export default SubscriptionProvider;
