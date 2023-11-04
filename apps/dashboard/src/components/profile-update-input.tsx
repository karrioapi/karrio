import React, { useContext, useState } from 'react';
import { UserType, useUser, useUserMutation } from '@/context/user';
import { NotificationType } from '@/lib/types';
import { Notify } from '@/components/notifier';

interface ProfileUpdateInputComponent {
  label: string;
  inputType: string;
  propertyKey: keyof UserType;
}

const ProfileUpdateInput: React.FC<ProfileUpdateInputComponent> = ({ label, inputType, propertyKey }) => {
  const mutation = useUserMutation();
  const { notify } = useContext(Notify);
  const { query: { data: { user } = {} } } = useUser();
  const [key, setKey] = useState<string>(`${propertyKey}-${Date.now()}`);
  const [originalValue, _] = useState<string>(((user || {}) as any)[propertyKey] || "");
  const [propertyValue, setPropertyValue] = useState<string>("");
  const [hasChanged, setHasChanged] = useState<boolean>(false);

  const cancel = (e: React.MouseEvent) => {
    e.preventDefault();
    setPropertyValue(originalValue);
    setHasChanged(false);
    setKey(`${propertyKey}-${Date.now()}`);
  };
  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    try {
      await mutation.updateUser.mutateAsync({ [propertyKey]: propertyValue });
      setHasChanged(false);
      notify({
        type: NotificationType.success, message: `${propertyValue} updated successfully!`
      });
    } catch (error: any) {
      notify({ type: NotificationType.error, message: error });
    }
  };
  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPropertyValue(e.target.value);
    setHasChanged(e.target.value !== (user as any)[propertyKey]);
  };

  return (
    <form className="field" onSubmit={handleSubmit} key={key}>
      <label className="label is-capitalized" style={{ fontSize: ".8em" }}>{label}</label>
      <div className="control">
        <input
          className="input is-small mr-1"
          onChange={handleOnChange}
          defaultValue={((user || {}) as any)[propertyKey] || ""}
          type={inputType}
          style={{ maxWidth: "60%" }} required />

        <input className="button is-success is-small mr-1" type="submit" value="Save"
          style={{ visibility: (hasChanged ? "visible" : "hidden") }} />
        <button className="button is-small"
          onClick={cancel}
          hidden={!hasChanged}
          style={{ visibility: (hasChanged ? "visible" : "hidden") }}>
          <span>Cancel</span>
        </button>
      </div>
    </form>
  )
};

export default ProfileUpdateInput;
