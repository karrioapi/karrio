import { Menu } from '@headlessui/react';
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
          <div className={`dropdown is-right ${open ? "is-active" : ""}`}>

            <Menu.Button as='div' className={`dropdown-trigger`}>
              {trigger}
            </Menu.Button>

            <div
              role="menu"
              className="dropdown-menu"
            >
              <Menu.Items className={'dropdown-content is-menu'}>
                {React.Children.map(children, (item: any, index) => {
                  return (
                    <Menu.Item key={index} as='a' className={'dropdown-item'}>
                      {item}
                    </Menu.Item>
                  );
                })}
              </Menu.Items>
            </div>

          </div>
        )}
      </Menu>
    </>
  );
};

const Item: React.FC<{ children?: React.ReactNode; }> = ({ children }) => (
  <Menu.Item>{children}</Menu.Item>
);

export const MenuComponent = {
  Menu: Wrapper,
  Item: Item,
};
