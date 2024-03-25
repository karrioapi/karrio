import { useAppMode } from '@karrio/hooks/app-mode';
import React from 'react';

export const ModeIndicator: React.FC = () => {
  const { testMode } = useAppMode();

  return (
    <>
      {testMode && <div className="mode-indicator">
        <span className="mode-indicator-label has-text-weight-bold">TEST DATA</span>
      </div>}
    </>
  )
};
