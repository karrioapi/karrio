import { ExpandedSidebar } from '@karrio/ui/components/expanded-sidebar';
import { Notifier } from '@karrio/ui/components/notifier';
import { Navbar } from '@karrio/ui/components/navbar';
import { Footer } from '@karrio/ui/components/footer';
import React from 'react';


export const DashboardLayout: React.FC<{ showModeIndicator?: boolean, children?: React.ReactNode }> = ({ children, ...props }) => {
  return (
    <>
      <ExpandedSidebar />

      <div className="plex-wrapper is-flex is-flex-direction-column">
        <div className="wrapper-inner is-flex-grow-1 mb-3">
          <Notifier />
          <Navbar showModeIndicator={props.showModeIndicator} />

          <div className="dashboard-content is-relative" style={{ paddingTop: 0, height: '100%' }}>
            {children}
          </div>

        </div>

        <Footer />
      </div>

    </>
  )
};
