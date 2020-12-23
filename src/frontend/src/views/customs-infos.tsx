import React, { Fragment, useEffect, useState } from 'react';
import { Customs } from '@purplship/purplship';
import { View } from '@/library/types';
import { PaginatedTemplates, state, Template } from '@/library/api';
import CustomsInfoDescription from '@/components/descriptions/customs-info-description';
import DeleteItemModal from '@/components/delete-item-modal';
import CustomsInfoEditModal from '@/components/customs-info-edit-modal';

interface CustomsInfosView extends View {
  templates?: PaginatedTemplates;
}

const CustomsInfos: React.FC<CustomsInfosView> = ({ templates }) => {
  const [loading, setLoading] = useState<boolean>(false);

  const update = (url?: string | null) => async (_?: React.MouseEvent) => {
    await state.fetchCustomsInfos(url as string);
  };
  const remove = (customs: Template) => async () => {
    await state.removeTemplate(customs.id as string);
    update(templates?.url)();
  };
  useEffect(() => {
    if ((templates === undefined || templates?.fetched === false) && loading === false) {
      setLoading(true);
      state.fetchCustomsInfos().catch(_ => _).then(() => setLoading(false));
    }
  }, templates?.results);

  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Customs</span>
        <CustomsInfoEditModal className="button is-success is-pulled-right" onUpdate={update(templates?.url)}>
          <span>New Customs Info</span>
        </CustomsInfoEditModal>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <thead className="templates-table">
            <tr>
              <th>Customs Info Templates</th>
              <th className="action"></th>
            </tr>
          </thead>

          <tbody className="CustomsInfos-table">
            {templates?.results.map((template) => (

              <tr key={`${template.id}-${Date.now()}`}>
                <td className="template">
                  <p className="is-subtitle is-size-6 my-1 has-text-weight-semibold">{template.label}</p>
                  <CustomsInfoDescription customs={template.customs as Customs} />
                </td>
                <td className="action is-vcentered">
                  <div className="buttons is-centered">
                    <CustomsInfoEditModal className="button is-light" customsTemplate={template} onUpdate={update(templates?.url)}>
                      <span className="icon is-small">
                        <i className="fas fa-pen"></i>
                      </span>
                    </CustomsInfoEditModal>
                    <DeleteItemModal label="Customs info Template" identifier={template.id as string} onConfirm={remove(template)}>
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
            <p>No customs info template has been added yet.</p>
            <p>Use the <strong>New Customs Info</strong> button above to add</p>
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

export default CustomsInfos;