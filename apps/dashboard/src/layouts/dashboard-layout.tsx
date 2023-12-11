import { ExpandedSidebar } from '@karrio/ui/components/expanded-sidebar';
import { ModeIndicator } from '@karrio/ui/components/mode-indicator';
import { Notifier } from '@karrio/ui/components/notifier';
import { Navbar } from '@karrio/ui/components/navbar';
import React from 'react';


export const DashboardLayout: React.FC<{ showModeIndicator?: boolean, children?: React.ReactNode }> = ({ children, ...props }) => {
  return (
    <>
      {props.showModeIndicator && <ModeIndicator />}
      <ExpandedSidebar />

      <div className="plex-wrapper is-flex is-flex-direction-column pb-0">
        <div className="wrapper-inner is-flex-grow-1 pb-0">
          <Notifier />
          <Navbar />

          <div className="dashboard-content is-relative pt-0 pb-4" style={{ minHeight: "93vh" }}>
            {children}
          </div>

        </div>
      </div>

    </>
  )
};
