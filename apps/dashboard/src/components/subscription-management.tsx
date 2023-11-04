import { NotificationType, PortalSessionType } from '@/lib/types';
import { useOrganizations } from '@/context/organization';
import { useSubscription } from '@/context/subscription';
import { useAPIMetadata } from '@/context/api-metadata';
import { useLoader } from '@/components/loader';
import { Notify } from '@/components/notifier';
import React, { useContext } from 'react';
import axios from 'axios';
import { url$ } from '@/lib/helper';

interface SubscriptionManagementComponent { }

const SubscriptionManagement: React.FC<SubscriptionManagementComponent> = () => {
  const { references } = useAPIMetadata();
  const { notify } = useContext(Notify);
  const { loading, setLoading } = useLoader();
  const { organization } = useOrganizations();
  const { subscription } = useSubscription();

  const openPortal = async () => {
    setLoading(true);
    try {
      const return_url = window.location.href;
      const response = await axios.post<PortalSessionType>(
        url$`${references.HOST}/v1/billing/portal`,
        { return_url },
        {
          headers: {
            'x-org-id': organization!.id,
            'authorization': `Token ${organization!.token}`,
          } as any
        }).then(({ data }) => data);

      window.location.href = response.url;
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
      setLoading(false);
    }
  }

  return (
    <div className="columns py-6">

      <div className="column is-4">
        <p className="subtitle is-6 py-1">Subscription</p>
      </div>

      <div className="column is-6">
        <div className="field">
          <label className="label">Level</label>
          <p className="is-size-6 has-text-weight-semibold" style={{ maxWidth: "60%" }}>{subscription?.subscription_type}</p>
        </div>

        <div className="field">
          <label className="label">Status</label>
          <p className="is-size-6 has-text-weight-semibold" style={{ maxWidth: "60%" }}>{subscription?.status}</p>
        </div>

        <div className="field">
          <label className="label">Period End</label>
          <p className="is-size-6 has-text-weight-semibold" style={{ maxWidth: "60%" }}>{subscription?.period_end}</p>
        </div>

        {subscription?.is_owner &&
          <button className="button is-primary mt-4" disabled={loading} onClick={openPortal}>
            <span>Open Customer Portal</span>
          </button>}
      </div>

    </div>
  )
};

export default SubscriptionManagement;
