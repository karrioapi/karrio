import { Operation, TrackingStatus } from '@/api';
import { handleFailure } from '@/library/helper';
import { RestClient } from '@/library/rest';
import React, { useContext } from 'react';


type TrackerMutator<T> = T & {
  createTracker: (tracking_number: string, carrier_name: string, test: boolean) => Promise<TrackingStatus>;
  removeTracker: (id: string) => Promise<Operation>;
}

const TrackerMutation = <T extends {}>(Component: React.FC<TrackerMutator<T>>) => (
  ({ children, ...props }: any) => {
    const purplship = useContext(RestClient);

    const createTracker = async (tracking_number: string, carrier_name: string, test: boolean) => handleFailure(
      purplship.trackers.retrieve({ carrierName: carrier_name, trackingNumber: tracking_number, test })
    );
    const removeTracker = async (id: string) => handleFailure(
      purplship.trackers.remove({ id })
    );

    return (
      <Component {...props}
        createTracker={createTracker}
        removeTracker={removeTracker}
      >
        {children}
      </Component>
    );
  }
);

export default TrackerMutation;
