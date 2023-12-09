import { ModeIndicator } from '@karrio/ui/components/mode-indicator';
import { AdminSidebar } from '@karrio/ui/components/admin-sidebar';
import { AdminNavbar } from '@karrio/ui/components/admin-navbar';
import { Notifier } from '@karrio/ui/components/notifier';
import { AppLink } from '@karrio/ui/components/app-link';
import React from 'react';


export const AdminLayout: React.FC<{ showModeIndicator?: boolean, children?: React.ReactNode }> = ({ children, ...props }) => {
  return (
    <>

      <div className="is-flex is-flex-direction-column" style={{ minHeight: '100vh' }}>
        {props.showModeIndicator && <ModeIndicator />}

        <Notifier />
        <AdminNavbar />

        <div className="is-flex is-flex-grow-1" style={{ paddingTop: 0, height: '100%' }}>
          <div className="modal-background"></div>
          <div className="modal-card admin-modal" style={{ width: '100%' }}>

            <section className="modal-card-body modal-form p-0 pt-5">
              <header className="form-floating-header p-2 is-flex is-justify-content-space-between">
                <span className="icon-text has-text-weight-bold is-size-6">
                  <span className="icon">
                    <i className="fas fa-tools"></i>
                  </span>
                  <span>Administration</span>
                </span>
                <div>
                  <AppLink href="/" className="button is-small is-white" shallow={false} prefetch={false}>
                    <span className="icon is-size-6">
                      <i className="fa fa-times"></i>
                    </span>
                  </AppLink>
                </div>
              </header>

              <div className="admin-wrapper is-relative mt-6 p-0">

                <AdminSidebar />

                <div className="plex-wrapper" style={{ background: 'inherit', marginLeft: '260px', minHeight: '70vh' }}>
                  {children}
                </div>

              </div>

            </section>

          </div>
        </div>

      </div>
    </>
  )
};
