import { OrganizationType, useOrganizationMutation, useOrganizations } from '@/context/organization';
import React, { useContext, useState } from 'react';
import { NotificationType } from '@/lib/types';
import { Notify } from '@/components/notifier';

interface OrganizationUpdateInputComponent {
  label?: string;
  inputType: string;
  propertyKey: keyof OrganizationType;
}

const OrganizationUpdateInput: React.FC<OrganizationUpdateInputComponent> = ({ label, inputType, propertyKey }) => {
  const { notify } = useContext(Notify);
  const mutation = useOrganizationMutation();
  const { organization } = useOrganizations();
  const [hasChanged, setHasChanged] = useState<boolean>(false);
  const [propertyValue, setPropertyValue] = useState<string>("");
  const [key, setKey] = useState<string>(`${propertyKey}-${Date.now()}`);
  const [originalValue, _] = useState<string>(((organization || {}) as any)[propertyKey] || "");

  const cancel = (e: React.MouseEvent) => {
    e.preventDefault();
    setPropertyValue(originalValue);
    setHasChanged(false);
    setKey(`${propertyKey}-${Date.now()}`);
  };
  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    try {
      await mutation.updateOrganization.mutateAsync({
        id: organization!.id,
        [propertyKey]: propertyValue
      });
      setHasChanged(false);
      notify({
        type: NotificationType.success, message: `${propertyValue} updated successfully!`
      });
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
  };
  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPropertyValue(e.target.value);
    setHasChanged(e.target.value !== (organization as any)[propertyKey]);
  };

  return (
    <form className="field" onSubmit={handleSubmit} key={key}>
      {label && <label className="label">{label}</label>}
      <div className="control">
        <input
          className="input is-small mr-1"
          onChange={handleOnChange}
          defaultValue={((organization || {}) as any)[propertyKey] || ""}
          type={inputType}
          style={{ maxWidth: "60%" }}
          disabled={!organization?.current_user?.is_admin}
          required
        />

        <input className="button is-success is-small mr-1" type="submit" value="Save"
          style={{ visibility: (hasChanged ? "visible" : "hidden") }} />
        <button className="button is-small"
          onClick={cancel}
          hidden={!hasChanged}
          disabled={!organization?.current_user?.is_admin}
          style={{ visibility: (hasChanged ? "visible" : "hidden") }}>
          <span>Cancel</span>
        </button>
      </div>
    </form>
  )
};

export default OrganizationUpdateInput;
