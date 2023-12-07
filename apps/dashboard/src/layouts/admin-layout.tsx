import { AdminSidebar } from '@karrio/ui/components/admin-sidebar';
import { AdminNavbar } from '@karrio/ui/components/admin-navbar';
import { Notifier } from '@karrio/ui/components/notifier';
import React from 'react';


export const AdminLayout: React.FC<{ showModeIndicator?: boolean, children?: React.ReactNode }> = ({ children, ...props }) => {
  return (
    <div className="is-flex is-flex-direction-column" style={{ minHeight: '100vh' }}>

      <Notifier />
      <AdminNavbar showModeIndicator={props.showModeIndicator} />

      <div className="is-flex is-flex-grow-1" style={{ paddingTop: 0, height: '100%' }}>
        <div className="modal-background"></div>
        <div className="modal-card admin-modal" style={{ width: '100%' }}>

          <section className="modal-card-body modal-form p-0">
            <div className="form-floating-header p-2">
              <span className="icon-text has-text-weight-bold is-size-6">
                <span className="icon">
                  <i className="fas fa-tools"></i>
                </span>
                <span>Administration</span>
              </span>
            </div>

            <div className="admin-wrapper is-relative">

              <AdminSidebar />

              <div className="plex-wrapper" style={{ background: 'inherit', minHeight: '70vh' }}>
                {children}
              </div>

            </div>

          </section>

        </div>
      </div>

    </div>
  )
};
