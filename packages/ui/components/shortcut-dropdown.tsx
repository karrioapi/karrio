import { Dropdown, closeDropdown } from './dropdown';
import { AppLink } from './app-link';
import React from 'react';


interface ShortcutDropdownComponent { }


export const ShortcutDropdown: React.FC<ShortcutDropdownComponent> = ({ ...props }) => {

  return (
    <Dropdown>

      {/* Dropdown trigger  */}
      <button className="button is-primary mx-1" style={{ borderRadius: '50%' }}>
        <span className="icon">
          <i className="is-size-6 fas fa-plus"></i>
        </span>
      </button>

      {/* Dropdown content  */}
      <article className="menu-inner panel is-white p-3 has-background-white">
        <div className="menu-inner has-background-white" onClick={e => closeDropdown(e.target)}>
          <p className="is-size-7 mt-2 px-2 pt-2 has-text-weight-semibold">ONLINE SHIPMENT</p>

          <div className="options-items py-1">

            <AppLink href="/connections?modal=new" className="options-item px-2 py-2 has-text-info has-text-weight-bold is-size-7">
              <i className="fas fa-link pr-2"></i>
              <span>Carrier account</span>
            </AppLink>

            <AppLink href="/draft_orders/new" className="options-item px-2 py-2 has-text-info has-text-weight-bold is-size-7">
              <i className="fas fa-inbox pr-2"></i>
              <span>Create order</span>
            </AppLink>

            <AppLink href="/create_label?shipment_id=new" className="options-item px-2 py-2 has-text-info has-text-weight-bold is-size-7">
              <i className="fas fa-file-invoice pr-2"></i>
              <span>Shipping label</span>
            </AppLink>

            <AppLink href="/trackers?modal=new" className="options-item px-2 py-2 has-text-info has-text-weight-bold is-size-7">
              <i className="fas fa-location-arrow pr-2"></i>
              <span>Package tracker</span>
            </AppLink>

          </div>
        </div>
      </article>

    </Dropdown>
  );
}
