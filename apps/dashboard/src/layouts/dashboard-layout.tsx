import ExpandedSidebar from '@/components/sidebars/expanded-sidebar';
import Navbar from '@/components/navbar/navbar';
import Notifier from '@/components/notifier';
import Footer from '@/components/footer';
import React from 'react';


const DashboardLayout: React.FC<{ showModeIndicator?: boolean }> = ({ children, ...props }) => {
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

export default DashboardLayout;
