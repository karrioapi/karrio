import { useAppMode } from '@/context/app-mode';
import React from 'react';

const ModeIndicator: React.FC = () => {
  const { testMode } = useAppMode();

  return (
    <>
      {testMode && <div className="mode-indicator">
        <span className="mode-indicator-label has-text-weight-semibold">TEST DATA</span>
      </div>}
    </>
  )
};

export default ModeIndicator;
