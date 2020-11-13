import { NotificationType, state, UserInfo } from '@/library/api';
import React, { useState } from 'react';

interface ProfileUpdateInputComponent {
    user: UserInfo;
    label: string;
    inputType: string;
    propertyKey: keyof UserInfo;
}

const ProfileUpdateInput: React.FC<ProfileUpdateInputComponent> = ({ user, label, inputType, propertyKey }) => {
    const [key, setKey] = useState<string>(`${propertyKey}-${Date.now()}`);
    const [originalValue, _] = useState<string>((user as any)[propertyKey] || "");
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
            await state.updateUserInfo({ [propertyKey]: propertyValue } as Partial<UserInfo>);
            setHasChanged(false);
            state.setNotification({ 
                type: NotificationType.success,
                message: `${propertyValue} updated successfully!` 
            });
        } catch (err) {
            state.setNotification({ type: NotificationType.error, message: err.message });
        }
    };
    const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPropertyValue(e.target.value);
        setHasChanged(e.target.value !== (user as any)[propertyKey]);
    };

    return (
        <form className="field" onSubmit={handleSubmit} key={key}>
            <label className="label">{label}</label>
            <div className="control">
                <input
                    className="input is-small mr-1"
                    onChange={handleOnChange}
                    defaultValue={(user as any)[propertyKey] || ""}
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
};

export default ProfileUpdateInput;