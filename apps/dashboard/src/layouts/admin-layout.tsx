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
        <div className="modal-card m-4" style={{ width: '100%' }}>

          <section className="modal-card-body modal-form">
            <div className="form-floating-header p-2">
              <span className="icon-text has-text-weight-bold is-size-6">
                <span className="icon">
                  <i className="fas fa-toolbox"></i>
                </span>
                <span>Administration</span>
              </span>
            </div>
            <div className="p-3 my-4"></div>

            <div className="columns px-6 pb-6 m-0">

              <div className="column is-5 px-0 pb-6 is-relative"></div>

              <div className="p-2"></div>

              <div className="column px-0">
                {children}
              </div>

            </div>

          </section>

        </div>
      </div>

    </div>
  )
};
