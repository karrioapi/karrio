import * as headlessui from '@headlessui/react';
import React from 'react';

interface SwitchProps extends headlessui.SwitchProps<any> {
  iconClassName?: string;
}

export const Switch: React.FC<SwitchProps> = ({ className, iconClassName, ...props }) => {

  return (
    <headlessui.Switch className={`button ${className || 'is-white is-large'}`} {...props} >
      <span className={`icon ${props.checked ? 'has-text-success' : 'has-text-grey'} ${iconClassName || 'is-medium'}`}>
        <i className={`fas fa-${props.checked ? 'toggle-on' : 'toggle-off'} fa-lg`}></i>
      </span>
    </headlessui.Switch>
  )
};
