import React from 'react';

type StatusType = 'beta' | 'production-ready' | 'in-development' | string;

interface IntegrationStatusBadgeProps {
  status: StatusType;
  showPrefix?: boolean;
}

export const IntegrationStatusBadge: React.FC<IntegrationStatusBadgeProps> = ({
  status = 'in-development',
  showPrefix = true,
}) => {
  // Define color schemes based on status
  const getStatusColor = (status: StatusType): string => {
    switch (status.toLowerCase()) {
      case 'production-ready':
        return 'is-success';
      case 'beta':
        return 'is-info';
      case 'in-development':
      default:
        return 'is-warning';
    }
  };

  return (
    <span className={`tag is-light is-small ${getStatusColor(status)}`}>
      {showPrefix ? 'Status: ' : ''}{status}
    </span>
  );
};
