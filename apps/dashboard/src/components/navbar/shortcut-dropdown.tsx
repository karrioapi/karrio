import Dropdown, { closeDropdown } from '@/components/generic/dropdown';
import AppLink from '@/components/app-link';
import React from 'react';


interface ShortcutDropdownComponent { }


const ShortcutDropdown: React.FC<ShortcutDropdownComponent> = ({ ...props }) => {

  return (
    <Dropdown>

      {/* Dropdown trigger  */}
      <button className="button is-primary is-outlined is-small mx-1">
        <span className="is-size-7 has-text-weight-semibold">Create</span>
        <span className="icon">
          <i className="is-size-6 fas fa-angle-down"></i>
        </span>
      </button>

      {/* Dropdown content  */}
      <article className="menu-inner panel is-white p-0 has-background-white">
        <div className="menu-inner has-background-white" onClick={e => closeDropdown(e.target)}>
          <p className="is-size-7 mt-2 px-4 pt-2 has-text-weight-semibold">ONLINE SHIPMENT</p>

          <div className="options-items py-1">

            <AppLink href="/connections?modal=new" className="options-item py-2 has-text-info has-text-weight-bold is-size-7">
              <i className="fas fa-link pr-2"></i>
              <span>Carrier account</span>
            </AppLink>

            <AppLink href="/create_label?shipment_id=new" className="options-item py-2 has-text-info has-text-weight-bold is-size-7">
              <i className="fas fa-file-invoice pr-2"></i>
              <span>Shipping label</span>
            </AppLink>

            <AppLink href="/trackers?modal=new" className="options-item py-2 has-text-info has-text-weight-bold is-size-7">
              <i className="fas fa-location-arrow pr-2"></i>
              <span>Package tracker</span>
            </AppLink>

          </div>
        </div>
      </article>

    </Dropdown>
  );
}

export default ShortcutDropdown;
