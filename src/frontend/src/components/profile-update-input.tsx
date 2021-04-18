import { NotificationType } from '@/library/types';
import React, { useContext, useEffect, useState } from 'react';
import { UserData, UserType } from '@/components/data/user-query';
import UserMutation from '@/components/data/user-mutation';
import { Notify } from './notifier';

interface ProfileUpdateInputComponent {
    label: string;
    inputType: string;
    propertyKey: keyof UserType;
}

const ProfileUpdateInput: React.FC<ProfileUpdateInputComponent> = UserMutation<ProfileUpdateInputComponent>(({ label, inputType, propertyKey, updateUser }) => {
    const { user, refetch } = useContext(UserData);
    const { notify } = useContext(Notify);
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
            await updateUser({ [propertyKey]: propertyValue });
            if (refetch !== undefined) refetch();
            setHasChanged(false);
            notify({ 
                type: NotificationType.success, message: `${propertyValue} updated successfully!` 
            });
        } catch(error) {
            // TODO:: add support for graphql error type
            notify({ type: NotificationType.error, message: error });
        }
    };
    const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPropertyValue(e.target.value);
        setHasChanged(e.target.value !== (user as any)[propertyKey]);
    };

    useEffect(() => { }, [user])

    return (
        <form className="field" onSubmit={handleSubmit} key={key}>
            <label className="label">{label}</label>
            <div className="control">
                <input
                    className="input is-small mr-1"
                    onChange={handleOnChange}
                    defaultValue={((user || {}) as any)[propertyKey] || ""}
                    type={inputType}
                    style={{ maxWidth: "60%" }} required/>

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
});

export default ProfileUpdateInput;