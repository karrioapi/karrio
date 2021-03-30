import React, { Fragment, useEffect, useState } from 'react';
import { PaginatedTemplates, Template, View } from '@/library/types';
import ParcelDescription from '@/components/descriptions/parcel-description';
import ParcelEditModal from '@/components/parcel-edit-modal';
import DeleteItemModal from '@/components/delete-item-modal';
import { state } from '@/library/app';

interface ParcelsView extends View {
  templates?: PaginatedTemplates;
}

const Parcels: React.FC<ParcelsView> = ({ templates }) => {
  const [loading, setLoading] = useState<boolean>(false);

  const update = (url?: string | null) => async (_?: React.MouseEvent) => {
    await state.fetchParcels(url as string);
  };
  const remove = (parcel: Template) => async () => {
    await state.removeTemplate(parcel.id as string);
    update(templates?.url)();
  };
  useEffect(() => {
    if (loading === false) {
      setLoading(true);
      state.fetchParcels().catch(_ => _).then(() => setLoading(false));
    }
  }, []);

  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Parcels</span>
        <ParcelEditModal className="button is-success is-pulled-right" onUpdate={update(templates?.url)}>
          <span>New Parcel</span>
        </ParcelEditModal>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <thead className="templates-table">
            <tr>
              <th colSpan={2}>Parcel Templates</th>
              <th className="action"></th>
            </tr>
          </thead>

          <tbody className="templates-table">
            {templates?.results.map((template) => (

              <tr key={`${template.id}-${Date.now()}`}>
                <td className="template">
                  <p className="is-subtitle is-size-6 my-1 has-text-weight-semibold">{template.label}</p>
                  <ParcelDescription parcel={template.parcel} />
                </td>
                <td className="default is-vcentered">
                  {template.is_default && <span className="is-size-7 has-text-weight-semibold">
                    <span className="icon has-text-success"><i className="fas fa-check"></i></span> Default shipping parcel
                  </span>}
                </td>
                <td className="action is-vcentered">
                  <div className="buttons is-centered">
                    <ParcelEditModal className="button is-light" parcelTemplate={template} onUpdate={update(templates?.url)}>
                      <span className="icon is-small">
                        <i className="fas fa-pen"></i>
                      </span>
                    </ParcelEditModal>
                    <DeleteItemModal label="Parcel Template" identifier={template.id as string} onConfirm={remove(template)}>
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
            <p>No parcel has been added yet.</p>
            <p>Use the <strong>New Parcel</strong> button above to add</p>
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

export default Parcels;