import { Menu, MenuItemProps } from '@headlessui/react';
import React from 'react';

interface MenuProps {
  trigger: JSX.Element;
  children: React.ReactNode;
}

const Wrapper: React.FC<MenuProps> = ({ trigger, children }) => {
  return (
    <>
      <Menu>
        {({ open }) => (
          <div className={`dropdown is-right ${open ? "is-active" : ""}`} onClick={e => e.stopPropagation()}>

            <Menu.Button as='div' className={`dropdown-trigger`}>
              {trigger}
            </Menu.Button>

            <div
              role="menu"
              className="dropdown-menu"
            >
              <Menu.Items className={'dropdown-content is-menu'}>
                {children}
              </Menu.Items>
            </div>

          </div>
        )}
      </Menu>
    </>
  );
};

const Item: React.FC<MenuItemProps<any>> = ({ children, ...props }) => (
  <Menu.Item {...props}>{children}</Menu.Item>
);

export const MenuComponent = {
  Menu: Wrapper,
  Item: Item,
};
