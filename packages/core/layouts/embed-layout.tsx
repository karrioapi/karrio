import { ExpandedSidebar } from '@karrio/ui/components/expanded-sidebar';
import { ModeIndicator } from '@karrio/ui/components/mode-indicator';
import React from 'react';


export const EmbedLayout: React.FC<{ showModeIndicator?: boolean, children?: React.ReactNode }> = ({ children, ...props }) => {
  return (
    <>
      {props.showModeIndicator && <ModeIndicator />}
      <ExpandedSidebar />

      <div className="plex-wrapper is-relative p-0">

        {children}

      </div>

    </>
  )
};
