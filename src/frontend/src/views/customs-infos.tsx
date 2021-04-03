import React, { Fragment, useContext, useEffect } from 'react';
import { CustomsType, View } from '@/library/types';
import CustomsInfoDescription from '@/components/descriptions/customs-info-description';
import DeleteItemModal from '@/components/delete-item-modal';
import CustomsInfoEditModal from '@/components/customs-info-edit-modal';
import TemplateMutation from '@/components/data/template-mutation';
import { CustomInfoTemplates } from '@/components/data/customs-templates-query';
import { isNone } from '@/library/helper';
import { Loading } from '@/components/loader';

interface CustomsInfosView extends View {}

const CustomsInfoPage: React.FC<CustomsInfosView> = TemplateMutation<CustomsInfosView>(({ deleteTemplate }) => {
  const { setLoading } = useContext(Loading);
  const { loading, templates, next, previous, load, loadMore, refetch} = useContext(CustomInfoTemplates);

  const refresh = () => refetch && refetch();
  const remove = (id: string) => async () => {
    await deleteTemplate(id);
    refresh();
  };

  useEffect(() => { !loading && load() }, []);
  useEffect(() => { setLoading(loading); });

  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Customs</span>
        <CustomsInfoEditModal className="button is-success is-pulled-right" onUpdate={refresh}>
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

          <tbody className="templates-table">
            {templates.map((template) => (

              <tr key={`${template.id}-${Date.now()}`}>
                <td className="template">
                  <p className="is-subtitle is-size-6 my-1 has-text-weight-semibold">{template.label}</p>
                  <CustomsInfoDescription customs={template.customs as CustomsType} />
                </td>
                <td className="action is-vcentered">
                  <div className="buttons is-centered">
                    <CustomsInfoEditModal className="button is-light" customsTemplate={template} onUpdate={refresh}>
                      <span className="icon is-small">
                        <i className="fas fa-pen"></i>
                      </span>
                    </CustomsInfoEditModal>
                    <DeleteItemModal label="Customs info Template" identifier={template.id as string} onConfirm={remove(template.id)}>
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

        {(templates.length == 0) && <div className="card my-6">

          <div className="card-content has-text-centered">
            <p>No customs info template has been added yet.</p>
            <p>Use the <strong>New Customs Info</strong> button above to add</p>
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

export default CustomsInfoPage;