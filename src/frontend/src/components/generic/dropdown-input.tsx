import { Reference } from '@/library/context';
import { isNone } from '@/library/helper';
import { Collection } from '@/library/types';
import React, { useState, useRef, useContext, ChangeEvent, useEffect } from 'react';


interface DropdownInputComponent extends React.AllHTMLAttributes<HTMLInputElement> {
    label?: string;
    fieldClass?: string;
    controlClass?: string;
    dropdownClass?: string;
    onValueChange: (value: string | null) => void;
}


const DropdownInput: React.FC<DropdownInputComponent> = ({ label, defaultValue, fieldClass, controlClass, dropdownClass, required, onValueChange, ...props }) => {
    const btn = useRef<any>(null);
    const control = useRef<any>(null);
    const Ref = useContext(Reference);
    const [key, setKey] = useState<string>(`dropdown-${Date.now()}`);
    const [isActive, setIsActive] = useState<boolean>(false);
    const [search, setSearch] = useState<string>("");
    const [value, setValue] = useState<string>();
    const handleOnClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        e.preventDefault();
        if (!isActive) {
            setIsActive(true);
            document.addEventListener('click', onBodyClick);
        }
        setTimeout(() => {
            control.current.focus();
            control.current.select();
        });
    };
    const onBodyClick = (e: MouseEvent) => {
        if (e.target !== btn.current && e.target !== control.current) {
            setIsActive(false);
            setSearch("");
            setKey(`dropdown-${Date.now()}`);
            document.removeEventListener('click', onBodyClick);
        }
    };
    const onInput = (e: ChangeEvent<any>) => {
        setSearch(e.target.value as string);
    };
    const onChange = (e: ChangeEvent<any>) => {
        const code = Object.keys(Ref.countries).find(c => Ref.countries[c].toLowerCase() == e.target.value.toLowerCase());
        setValue(code || "");
        onValueChange(code as string);
    };
    const onSelect = (code: string) => (e: React.MouseEvent) => {
        setValue(code);
        onValueChange(code);
    };

    useEffect(() => {
        if (!isNone(Ref?.countries) && !isNone(defaultValue)) {
            setValue(Ref.countries[defaultValue as string]);
        }
    }, [Ref?.countries, defaultValue]);

    return (
        <div className={`field ${fieldClass}`}>
            {label !== undefined && <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
                {label}
                {required && <span className="icon is-small has-text-danger small-icon"><i className="fas fa-asterisk"></i></span>}
            </label>}
            <div className={`control ${controlClass}`}>
                <div className={`dropdown select is-fullwidth ${isActive ? 'is-active' : ''} ${dropdownClass}`} key={`dropdown-input-`}>
                    <input name="country" onChange={onChange} defaultValue={value} style={{ position: 'absolute', zIndex: -1 }}/>
                    <a onClick={handleOnClick} aria-haspopup="true" className="dropdown-trigger input is-fullwidth px-2" style={{ justifyContent: 'left' }} aria-controls={`dropdown-input-`} ref={btn}>
                        <span>{value}</span>
                    </a>

                    <div className="dropdown-menu py-0" id={`dropdown-input-`} role="menu" style={{ right: 0, left: 0 }}>
                        <div className="dropdown-content py-0">

                            <div className="panel-block px-1 py-1">
                                <p className="control">
                                    <input className="input" type="text" defaultValue={search} onInput={onInput} ref={control} />
                                </p>
                            </div>
                            <nav className="panel dropped-panel">
                                {Object
                                    .entries(Ref?.countries as Collection || {})
                                    .filter(([_, name]) => search === "" || name.toLowerCase().includes(search.toLowerCase()))
                                    .map(([code, name]) => <>
                                        <a className={`panel-block  ${code === value ? 'is-active' : ''}`} onClick={onSelect(code)} key={code} tabIndex={1}>
                                            <span>{name}</span>
                                        </a>
                                    </>)
                                }
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default DropdownInput;
