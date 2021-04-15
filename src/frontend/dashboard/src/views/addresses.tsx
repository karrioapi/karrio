import React, { Fragment, useEffect, useState } from 'react';
import { PaginatedTemplates, Template, View } from '@/library/types';
import { state } from '@/library/api';
import AddressDescription from '@/components/descriptions/address-description';
import AddressEditModal from '@/components/address-edit-modal';
import DeleteItemModal from '@/components/delete-item-modal';
import { Address } from '@purplship/purplship';

interface AddressesView extends View {
  templates?: PaginatedTemplates;
}

const Addresses: React.FC<AddressesView> = ({ templates }) => {
  const [loading, setLoading] = useState<boolean>(false);

  const update = (url?: string | null) => async (_?: React.MouseEvent) => {
    await state.fetchAddresses(url as string);
  };
  const remove = (address: Template) => async () => {
    await state.removeTemplate(address.id as string);
    update(templates?.url)();
  };
  useEffect(() => {
    if (loading === false) {
      setLoading(true);
      state.fetchAddresses().catch(_ => _).then(() => setLoading(false));
    }
  }, []);

  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Addresses</span>
        <AddressEditModal className="button is-success is-pulled-right" onUpdate={update(templates?.url)}>
          <span>New Address</span>
        </AddressEditModal>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <thead className="templates-table">
            <tr>
              <th colSpan={2}>Address Templates</th>
              <th className="action"></th>
            </tr>
          </thead>

          <tbody className="templates-table">
            {templates?.results.map((template) => (

              <tr key={`${template.id}-${Date.now()}`}>
                <td className="template">
                  <p className="is-subtitle is-size-6 my-1 has-text-weight-semibold">{template.label}</p>
                  <AddressDescription address={template.address as Address} />
                </td>
                <td className="default is-vcentered">
                  {template.is_default && <span className="is-size-7 has-text-weight-semibold">
                    <span className="icon has-text-success"><i className="fas fa-check"></i></span> Default shipper address
                  </span>}
                </td>
                <td className="action is-vcentered">
                  <div className="buttons is-centered">
                    <AddressEditModal className="button is-light" addressTemplate={template} onUpdate={update(templates?.url)}>
                      <span className="icon is-small">
                        <i className="fas fa-pen"></i>
                      </span>
                    </AddressEditModal>
                    <DeleteItemModal label="Address Template" identifier={template.id as string} onConfirm={remove(template)}>
                      <span className="icon is-small">
                        <i className="fas fa-trash"></i>
                      </span>
                    </DeleteItemModal>
                  </div>
                </td>
              </tr>

            ))}
          </tbody>

        </table>

        {(templates?.count == 0) && <div className="card my-6">

          <div className="card-content has-text-centered">
            <p>No address has been added yet.</p>
            <p>Use the <strong>New Address</strong> button above to add</p>
          </div>

        </div>}

      </div>

      <footer className="px-2 py-2 is-vcentered">
        <div className="buttons has-addons is-centered">
          <button className="button is-small" onClick={update(templates?.previous)} disabled={templates?.previous === null}>
            <span>Previous</span>
          </button>
          <button className="button is-small" onClick={update(templates?.next)} disabled={templates?.next === null}>
            <span>Next</span>
          </button>
        </div>
      </footer>

    </Fragment>
  );
}

export default Addresses;