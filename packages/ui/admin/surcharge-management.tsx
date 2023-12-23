import { useSurcharges } from "@karrio/hooks/admin/surcharges";


interface SurchargeManagementComponent { }

export const SurchargeManagement: React.FC<SurchargeManagementComponent> = () => {
  const { query: { data: { surcharges } = {}, ...query } } = useSurcharges();

  return (
    <>
      <div className="card px-0" style={{ maxHeight: '300px', minHeight: '300px' }}>
        <header className="px-3 mt-3 is-flex is-justify-content-space-between">
          <span className="is-title is-size-6 has-text-weight-bold is-vcentered my-2">Surcharges</span>
          <div className="is-vcentered">
            <button className="button is-primary is-small is-pulled-right">
              <span>Add surcharge</span>
            </button>
          </div>
        </header>

        <hr className='my-1' style={{ height: '1px' }} />

        <div className="p-3">

          {((surcharges || []).length > 0) && <div className="table-container">
            <table className="table is-fullwidth mb-0">

              <tbody className="surcharges-table">
                <tr>
                  <td className="surcharge is-size-7 pl-0">SURCHARGE</td>
                  <td className="name is-size-7">NAME</td>
                  <td className="action"></td>
                </tr>

                {(surcharges || []).map(surcharge => (

                  <tr key={`${surcharge.id}-${Date.now()}`}>
                    <td className="surcharge is-vcentered pl-0">
                      <p className="has-text-weight-bold is-size-6">
                        <span>{surcharge.amount}</span>
                        <span>{surcharge.surcharge_type == "AMOUNT" ? "$" : "%"}</span>
                      </p>
                    </td>
                    <td className="name is-vcentered">
                      <p className="is-size-6">{surcharge.name}</p>
                    </td>
                    <td className="active is-vcentered has-text-right px-0">
                      <button className="button is-white is-medium">
                        <span className={`icon is-medium ${true ? 'has-text-success' : 'has-text-grey'}`}>
                          <i className={`fas fa-${true ? 'toggle-on' : 'toggle-off'} fa-lg`}></i>
                        </span>
                      </button>
                      <button className="button is-white is-medium" title="edit surcharge">
                        <span className="icon is-small">
                          <i className="fas fa-pen"></i>
                        </span>
                      </button>
                      <button className="button is-white is-medium" title="edit surcharge">
                        <span className="icon is-small">
                          <i className="fas fa-trash"></i>
                        </span>
                      </button>
                    </td>
                  </tr>

                ))}
              </tbody>

            </table>
          </div>}

          {(query.isFetched && (surcharges || []).length == 0) && <div className="message is-white my-6">

            <div className="has-text-centered">
              <p>No surcharges found.</p>
            </div>

          </div>}

        </div>
      </div>
    </>
  )
};
