import { useRateSheets } from "@karrio/hooks/admin/rate-sheets";
import { Spinner } from "../components";


interface RateSheetManagementComponent { }

export const RateSheetManagement: React.FC<RateSheetManagementComponent> = () => {
  const { query: { data: { rate_sheets } = {}, ...query } } = useRateSheets();

  return (
    <>
      <div className="card px-0" style={{ maxHeight: '500px', minHeight: '500px' }}>
        <header className="px-3 mt-3 is-flex is-justify-content-space-between">
          <span className="is-title is-size-6 has-text-weight-bold is-vcentered my-2">Rate sheets</span>
          <div className="is-vcentered">
            <button className="button is-primary is-small is-pulled-right" disabled>
              <span>New sheet</span>
            </button>
          </div>
        </header>

        <hr className='my-1' style={{ height: '1px' }} />

        <div className="p-3">

          {(query.isFetching && !query.isFetched) && <Spinner />}

          {(query.isFetched && (rate_sheets?.edges || []).length > 0) && <>

            <div className="table-container">
              <table className="table is-fullwidth mb-0">

                <tbody className="members-table">
                  <tr>
                    <td className="member is-size-7 pl-0">MEMBER</td>
                    <td className="role is-size-7">ROLE</td>
                    <td className="last-login is-size-7">LAST LOGIN</td>
                    <td className="action"></td>
                  </tr>

                  {(rate_sheets?.edges || []).map(({ node: sheet }) => (

                    <tr key={`${sheet.id}-${Date.now()}`} style={{ height: '60px' }}>
                      <td className="member is-vcentered pl-0">

                      </td>
                      <td className="action is-vcentered">
                      </td>
                    </tr>

                  ))}
                </tbody>

              </table>

              <hr style={{ height: '1px' }} className="m-0 mb-3" />

              <footer className="py-2 is-vcentered">
                <span className="is-size-7 has-text-weight-semibold">{(rate_sheets?.edges || []).length} results</span>

                <div className="buttons has-addons is-centered is-pulled-right pr-0">
                  <button className="button is-small" disabled>
                    <span>Previous</span>
                  </button>
                  <button className="button is-small" disabled>
                    <span>Next</span>
                  </button>
                </div>
              </footer>
            </div>
          </>}

          {(query.isFetched && (rate_sheets?.edges || []).length == 0) && <div className="message is-white my-6">

            <div className="has-text-centered">
              <p>No rate sheets found.</p>
              <p>Use the <strong>New sheet</strong> button above to add one</p>
            </div>

          </div>}

        </div>
      </div>
    </>
  )
};
