import { CreateUserMutationInput } from '@karrio/types/graphql/admin';
import { usePermissionGroups } from '@karrio/hooks/admin/permissions';
import { CheckBoxField } from '../components/checkbox-field';
import { StaffUserType } from '@karrio/hooks/admin/users';
import { InputField } from '../components/input-field';
import { useNotifier } from '../components/notifier';
import { ModalFormProps, useModal } from './modal';
import { NotificationType } from '@karrio/types';
import { useLoader } from '../components/loader';
import { isEqual } from '@karrio/lib';
import React from 'react';

type UserDataType = StaffUserType & CreateUserMutationInput;
type UserModalEditorProps = {
  header?: string;
  user?: UserDataType;
  onSubmit: (user: UserDataType) => Promise<any>;
};

function reducer(state: any, { name, value }: { name: string, value: string | boolean | object | string[] }) {
  switch (name) {
    case "full":
      return { ...(value as object) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}

export const UserModalEditor: React.FC<ModalFormProps<UserModalEditorProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const UserFormComponent: React.FC<UserModalEditorProps> = props => {
    const { user: defaultValue = { is_active: true }, header, onSubmit } = props;
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const [user, dispatch] = React.useReducer(reducer, defaultValue);
    const [key, setKey] = React.useState<string>(`user-${Date.now()}`);
    const { query: { data: { permission_groups } = {} } } = usePermissionGroups();

    const handleChange = (event: React.ChangeEvent<any>) => {
      const target = event.target;
      const name: string = target.name;
      let value = target.type === 'checkbox' ? target.checked : target.value;

      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value)
      }

      dispatch({ name, value });
    };
    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      const { date_joined, last_login, ...payload } = user;
      try {
        loader.setLoading(true);
        onSubmit && onSubmit(payload);
        setTimeout(() => close(), 1000);
      } catch (message: any) {
        notifier.notify({ type: NotificationType.error, message });
      }
      loader.setLoading(false);
    };

    return (
      <form className="modal-card-body modal-form" onSubmit={handleSubmit} key={key}>
        <div className="form-floating-header p-4">
          <span className="has-text-weight-bold is-size-6">{header || `Update user`}</span>
        </div>
        <div className="p-3 my-4"></div>

        {(user !== undefined) && <>

          <div className="columns mb-2">
            <InputField
              label="full_name"
              name="full_name"
              onChange={handleChange}
              defaultValue={user?.full_name || ""}
              className="is-small"
              wrapperClass="px-2 py-2"
              fieldClass="column mb-0 p-0"
              required
            />
          </div>

          <div className="columns mb-2">
            <InputField
              label="email"
              name="email"
              onChange={handleChange}
              defaultValue={user?.email || ""}
              className="is-small"
              wrapperClass="px-2 py-2"
              fieldClass="column mb-0 p-0"
              required
            />
          </div>

          <div className="columns mb-1 pl-1">
            <CheckBoxField
              name="is_active"
              onChange={handleChange}
              defaultChecked={user?.is_active as boolean}
              fieldClass="column mb-0 px-2 pt-3 pb-2 is-vcentered">
              <span>Activate user account</span>
            </CheckBoxField>
          </div>

          {(!user.id) && <>

            <div className="columns mb-2">
              <InputField
                name="password1"
                label="Password"
                type="password"
                onChange={handleChange}
                defaultValue={user?.password1 || ""}
                className="is-small"
                wrapperClass="px-2 py-2"
                fieldClass="column mb-0 p-0"
                required
              />
            </div>

            <div className="columns mb-2">
              <InputField
                name="password2"
                label="Password Confirmation"
                type="password"
                onChange={handleChange}
                defaultValue={user?.password2 || ""}
                className="is-small"
                wrapperClass="px-2 py-2"
                fieldClass="column mb-0 p-0"
                required
              />
            </div>

          </>}

          <hr style={{ height: '1px' }} className="m-0 my-4" />

          <p className="is-size-6 has-text-weight-semibold mb-4">Permissions</p>

          <div className="columns mb-1 pl-1">
            <CheckBoxField
              name="is_superuser"
              onChange={handleChange}
              defaultChecked={user?.is_superuser as boolean}
              fieldClass="column mb-0 px-2 pt-3 pb-2">
              <span>Make user super user</span>
            </CheckBoxField>
          </div>

          <div className="columns mb-1 pl-1">
            <CheckBoxField
              name="is_staff"
              onChange={handleChange}
              defaultChecked={user?.is_staff as boolean}
              fieldClass="column mb-0 px-2 pt-3 pb-2"
            >
              <span>Make user staff member</span>
            </CheckBoxField>
          </div>

          <div className="field mb-2">
            <div className="control">
              <div className="select is-multiple is-small is-fullwidth">
                <select name="permissions" value={(user as any).permissions} onChange={handleChange} size={6} multiple>
                  {(permission_groups?.edges || []).map(({ node: permission }) => (
                    <option key={`${permission.id}permission-${Date.now()}`} value={permission.name}>{permission.name}</option>)
                  )}
                </select>
              </div>
            </div>
          </div>


          <div className="p-3 my-5"></div>

          <div className="form-floating-footer has-text-centered p-1">
            <button className="button is-default m-1 is-small" type="button" onClick={close}>
              <span>Cancel</span>
            </button>
            <button className="button is-primary m-1 is-small"
              disabled={isEqual(defaultValue, user)}
              type="submit">
              <span>Save</span>
            </button>
          </div>

        </>}

      </form>
    )
  };

  return React.cloneElement(trigger, {
    onClick: () => modal.open(<UserFormComponent {...args} />)
  });
};
