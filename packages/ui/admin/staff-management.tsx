import { useUsers } from "@karrio/hooks/admin/users";
import { Dropdown } from "../components/dropdown";
import { formatDateTimeLong } from "@karrio/lib";
import { useUser } from "@karrio/hooks/user";


interface StaffManagementComponent { }

export const StaffManagement: React.FC<StaffManagementComponent> = () => {
  const { query: { data: { user } = {} } } = useUser();
  const { query: { data: { users } = {} } } = useUsers();

  return (
    <>
      <div className="card px-0">
        <header className="px-3 mt-3 is-flex is-justify-content-space-between">
          <span className="is-title is-size-6 has-text-weight-bold is-vcentered my-2">Staff</span>
          <div className="is-vcentered">
            <button className="button is-primary is-small is-pulled-right">
              <span>New member</span>
            </button>
          </div>
        </header>

        <hr className='my-1' style={{ height: '1px' }} />

        <div className="p-3">

          <div className="table-container">
            <table className="table is-fullwidth mb-0">

              <tbody className="members-table">
                <tr>
                  <td className="member is-size-7 pl-0">MEMBER</td>
                  <td className="role is-size-7">ROLE</td>
                  <td className="last-login is-size-7">LAST LOGIN</td>
                  <td className="action"></td>
                </tr>

                {(users?.edges || []).map(({ node: member }) => (

                  <tr key={`${member.email}-${Date.now()}`} style={{ height: '60px' }}>
                    <td className="member is-vcentered pl-0">
                      {member.full_name && <p className="is-size-7">
                        <span className="pr-2">{member.full_name}</span>
                        {member.email === user?.email && <span className="tag is-size-7 is-info is-light px-3">You</span>}
                      </p>}
                      <p className="is-size-7">{member.email}</p>
                    </td>
                    <td className="role is-vcentered">
                      <p>
                        {member.is_superuser && <span className="is-size-7">Super</span>}
                        {(member.is_superuser && member.is_staff) && ', '}
                        {member.is_staff && <span className="is-size-7">Staff</span>}
                        {(!member.is_superuser && !member.is_staff) && <span className="is-size-7">View Only</span>}
                      </p>
                    </td>
                    <td className="last-login is-vcentered">
                      {member.last_login && <span className="is-size-7">{formatDateTimeLong(member.last_login)}</span>}
                    </td>
                    <td className="action is-vcentered">
                      {(user?.is_superuser && member.email !== user?.email) && <div className="is-pulled-right">
                        <Dropdown >
                          {/* Trigger */}
                          <button className="button is-small is-white">
                            <span className="icon is-small">
                              <i className="fas fa-ellipsis-h"></i>
                            </span>
                          </button>

                          {/* Menu items */}
                          <div className="dropdown-content is-menu">
                            <a href="#" className="dropdown-item">Edit</a>
                            <a href="#" className="dropdown-item">Remove</a>
                          </div>
                        </Dropdown>
                      </div>}
                    </td>
                  </tr>

                ))}
              </tbody>

            </table>

            <hr style={{ height: '1px' }} className="m-0 mb-3" />

            <footer className="py-2 is-vcentered">
              <span className="is-size-7 has-text-weight-semibold">{(users?.edges || []).length} results</span>

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

        </div>
      </div>
    </>
  )
};
