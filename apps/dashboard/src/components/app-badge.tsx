import { useAPIMetadata } from '@/context/api-metadata';
import { formatCarrierSlug } from '@/lib/helper';
import React from 'react';

interface AppBadgeComponent extends React.AllHTMLAttributes<HTMLSpanElement> { }

const AppBadge: React.FC<AppBadgeComponent> = ({ className, ...props }) => {
  const { metadata: { APP_NAME } } = useAPIMetadata();

  return (
    <strong
      className={`is-lowercase has-text-weight-bold has-text-primary`}
      style={{ fontSize: '90%', borderRadius: '4px' }}
      {...props}
    >
      {formatCarrierSlug(APP_NAME)}
    </strong>
  );
};

export default AppBadge;
