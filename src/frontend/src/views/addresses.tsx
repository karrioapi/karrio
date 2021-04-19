import React, { Fragment, useContext, useEffect } from 'react';
import { View } from '@/library/types';
import AddressDescription from '@/components/descriptions/address-description';
import AddressEditModal from '@/components/address-edit-modal';
import DeleteItemModal from '@/components/delete-item-modal';
import { AddressTemplates } from '@/components/data/address-templates-query';
import TemplateMutation from '@/components/data/template-mutation';
import { isNone } from '@/library/helper';
import { Loading } from '@/components/loader';

interface AddressesView extends View {}

const AddressesPage: React.FC<AddressesView> = TemplateMutation<AddressesView>(({ deleteTemplate }) => {
  const { setLoading } = useContext(Loading);
  const { loading, templates, next, previous, load, loadMore, refetch } = useContext(AddressTemplates);

  const update = async (_?: React.MouseEvent) => refetch && await refetch();
  const remove = (id: string) => async () => {
    await deleteTemplate(id);
    update();
  };

  useEffect(() => { !loading && load() }, []);
  useEffect(() => { setLoading(loading); });

  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Addresses</span>
        <AddressEditModal className="button is-success is-pulled-right" onUpdate={update}>
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
            {templates.map((template) => (

              <tr key={`${template.id}-${Date.now()}`}>
                <td className="template">
                  <p className="is-subtitle is-size-6 my-1 has-text-weight-semibold">{template.label}</p>
                  <AddressDescription address={template.address} />
                </td>
                <td className="default is-vcentered">
                  {template.is_default && <span className="is-size-7 has-text-weight-semibold">
                    <span className="icon has-text-success"><i className="fas fa-check"></i></span> Default shipper address
                  </span>}
                </td>
                <td className="action is-vcentered">
                  <div className="buttons is-centered">
                    <AddressEditModal className="button is-light" addressTemplate={template} onUpdate={update}>
                      <span className="icon is-small">
                        <i className="fas fa-pen"></i>
                      </span>
                    </AddressEditModal>
                    <DeleteItemModal label="Address Template" identifier={template.id} onConfirm={remove(template.id)}>
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

        {(templates?.length == 0) && <div className="card my-6">

          <div className="card-content has-text-centered">
            <p>No address has been added yet.</p>
            <p>Use the <strong>New Address</strong> button above to add</p>
          </div>

        </div>}

      </div>

      <footer className="px-2 py-2 is-vcentered">
        <div className="buttons has-addons is-centered">
          <button className="button is-small" onClick={() => loadMore(previous)} disabled={isNone(previous)}>
            <span>Previous</span>
          </button>
          <button className="button is-small" onClick={() => loadMore(next)} disabled={isNone(next)}>
            <span>Next</span>
          </button>
        </div>
      </footer>

    </Fragment>
  );
});

export default AddressesPage;