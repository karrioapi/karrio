import React from 'react';
import { Link, LinkProps } from "@reach/router";

const NavLink = (props: React.PropsWithoutRef<LinkProps<any>> & React.RefAttributes<HTMLAnchorElement>) => (
    <Link
        {...props}
        getProps={({ isCurrent }) => {
            return {
                className: isCurrent ? `${props.className || 'menu-item'} is-active` : `${props.className || 'menu-item'}`
            };
        }}
    />
);

export default NavLink;