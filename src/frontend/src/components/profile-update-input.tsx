import { state, UserInfo } from '@/library/api';
import React, { useState } from 'react';

interface ProfileUpdateInputComponent {
    user: UserInfo;
    label: string;
    inputType: string;
    propertyKey: keyof UserInfo;
}

const ProfileUpdateInput: React.FC<ProfileUpdateInputComponent> = ({ user, label, inputType, propertyKey }) => {
    const [key, setKey] = useState<string>(`${propertyKey}-${Date.now()}`);
    const [propertyValue, setPropertyValue] = useState<string>("");
    const [hasChanged, setHasChanged] = useState<boolean>(false);
    const cancel = (e: React.MouseEvent) => {
        e.preventDefault();
        const originalValue = (user as any)[propertyKey] || "";
        setPropertyValue(originalValue);
        setKey(`${propertyKey}-${Date.now()}`);
    };
    const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
        evt.preventDefault();
        try {
            await state.updateUserInfo({ [propertyKey]: propertyValue } as Partial<UserInfo>);
            setHasChanged(false);
        } catch(err) {
            console.error(err);
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
                    style={{ maxWidth: "60%" }}/>

                <input className="button is-success is-small mr-1" type="submit" value="Save" 
                    style={{ visibility: (hasChanged ? "visible" : "hidden")}}/>

                <button className="button is-small"
                    onClick={cancel}
                    hidden={!hasChanged}
                    style={{ visibility: (hasChanged ? "visible" : "hidden")}}>
                    Cancel
                </button>
            </div>
        </form>
    )
};

export default ProfileUpdateInput;