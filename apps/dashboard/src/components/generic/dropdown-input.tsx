import { isNone, isNoneOrEmpty } from '@/lib/helper';
import React, { useState, useRef, ChangeEvent, useEffect, useCallback } from 'react';


export interface DropdownInputComponent extends React.AllHTMLAttributes<HTMLInputElement> {
  label?: string;
  fieldClass?: string;
  controlClass?: string;
  dropdownClass?: string;
  items?: [string, string][];
  onValueChange: (value?: string | null) => void;
}


const DropdownInput: React.FC<DropdownInputComponent> = ({ label, name, items, value, className, fieldClass, controlClass, dropdownClass, required, onValueChange, ...props }) => {
  const control = useRef<any>(null);
  const btn = useRef<HTMLInputElement>(null);
  const [key, setKey] = useState<string>(`dropdown-${Date.now()}`);
  const [isActive, setIsActive] = useState<boolean>(false);
  const [search, setSearch] = useState<string>("");
  const [selected, setSelected] = useState<string>();

  const find = useCallback((selection?: string) => {
    if (isNoneOrEmpty(selection)) { return ["", ""]; }
    return items?.find(([key, val]) => (
      key.toLowerCase().trim() == selection?.toLowerCase().trim() ||
      val.toLowerCase().trim() == selection?.toLowerCase().trim()
    ))
  }, [items]);
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
  const onSearch = (e: ChangeEvent<any>) => {
    setSearch(e.target.value as string);
  };
  const onRefChange = (e: ChangeEvent<any>) => {
    e.preventDefault();
    const [key, value] = find(e.target.value) || [];
    setSelected(value);
    onValueChange(key as string);
  };
  const onSelect = (key: string) => (e: React.MouseEvent) => {
    setSelected(key);
    onValueChange(key);
  };

  useEffect(() => {
    if (!isNone(items)) {
      const [_, selected] = find(value as string) || [];
      setSelected(selected);
    }
  }, [items, value, find]);

  return (
    <div className={`field ${fieldClass}`} key={key}>
      {label !== undefined && <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
        {label}
        {required && <span className="icon is-small has-text-danger small-icon">
          <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
        </span>}
      </label>}
      <div className={`control ${controlClass}`}>
        <div className={`dropdown select is-fullwidth ${isActive ? 'is-active' : ''} ${dropdownClass}`} key={`dropdown-input-${key}`}>
          <input
            onClick={handleOnClick}
            onChange={onRefChange}
            value={selected || ""}
            className={"dropdown-trigger input is-clickable is-fullwidth px-2" + ` ${className}` || ''}
            aria-haspopup="true"
            readOnly
            style={{ height: '100%' }}
            {...props}
          />
          <input
            style={{ zIndex: -1, position: "absolute", left: '20px', bottom: '0' }}
            name={name}
            value={selected || ""}
            onChange={onRefChange}
            tabIndex={-1}
            required={required}
          />

          <div className="dropdown-menu py-0" id={`dropdown-input-${key}`} role="menu" style={{ right: 0, left: 0 }}>
            <div className="dropdown-content py-0">

              <div className="panel-block px-1 py-1">
                <p className="control has-icons-left">
                  <input
                    type="text"
                    className={"input" + ` ${className}` || ''}
                    defaultValue={search || ''}
                    onInput={onSearch}
                    ref={control}
                  />
                  <span className="icon is-left is-small">
                    <i className="fas fa-search" aria-hidden="true"></i>
                  </span>
                </p>
              </div>

              {items?.length === 0 && <div className="panel-block px-1 py-1">
                No items found...
              </div>}

              <ul className="panel dropped-panel">
                {(items || [])
                  .filter(([_, val]) => search === "" || val.toLowerCase().includes(search.toLowerCase()))
                  .map(([key, val], index) => (
                    <li
                      key={`${key}-${Date.now()}`}
                      tabIndex={index + 1}
                      onClick={onSelect(key)}
                      className={`panel-block is-clickable ${key === selected ? 'is-active' : ''}`}>
                      <span className='is-size-7'>{val}</span>
                    </li>
                  ))
                }
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DropdownInput;
