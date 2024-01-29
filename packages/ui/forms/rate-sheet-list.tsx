import { useRateSheetMutation, useRateSheets } from '@karrio/hooks/rate-sheet';
import { CarrierNameBadge } from '../components/carrier-name-badge';
import { RateSheetModalEditor } from '../modals/rate-sheet-editor';
import { ConfirmModalWrapper } from '../modals/form-modals';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import React from 'react';


export const RateSheetList: React.FC = () => {
  const { references } = useAPIMetadata();
  const mutation = useRateSheetMutation();
  const { query: { data: { rate_sheets } = {} } } = useRateSheets();

  const carrier = (name: string) => references?.carriers[name] || "Custom Carrier";

  return (
    <>

      {((rate_sheets?.edges || []).length > 0) && <>
        <div className="table-container">
          <table className="rate-sheets-table table is-fullwidth">

            <tbody>
              <tr>
                <td className="is-size-7" colSpan={3}>RATE SHEETS</td>
              </tr>

              {(rate_sheets?.edges || []).map(({ node: sheet }) => (

                <tr key={`sheet-${sheet.id}-${Date.now()}`}>
                  <td className="carrier is-vcentered pl-1">
                    <CarrierNameBadge
                      carrier_name={sheet.carrier_name}
                      display_name={carrier(sheet.carrier_name)}
                      className="box p-3 has-text-weight-bold"
                    />
                  </td>
                  <td className="details is-vcentered is-size-7 has-text-weight-bold text-ellipsis">
                    <span className="text-ellipsis" title={sheet.name}>{sheet.name}</span>
                  </td>
                  <td className="action has-text-right is-vcentered">
                    <div className="buttons is-justify-content-end">
                      <RateSheetModalEditor
                        sheet={sheet as any}
                        onSubmit={({ carrier_name, carriers, ..._ }) => mutation.updateRateSheet.mutateAsync(_)}
                        trigger={
                          <button className="button is-white">
                            <span className="icon is-small">
                              <i className="fas fa-pen"></i>
                            </span>
                          </button>
                        }
                      />
                      <ConfirmModalWrapper
                        header='Confirm rate sheet deletion'
                        onSubmit={() => mutation.deleteRateSheet.mutateAsync({ id: sheet.id })}
                        trigger={
                          <button className="button is-white">
                            <span className="icon is-small">
                              <i className="fas fa-trash"></i>
                            </span>
                          </button>
                        }
                      />
                    </div>
                  </td>
                </tr>

              ))}
            </tbody>

          </table>
        </div>
      </>}

      {((rate_sheets?.edges || []).length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No rate sheets added yet.</p>
          <p>Use the <strong>Add sheet</strong> button above to add one</p>
        </div>

      </div>}

    </>
  );
};
