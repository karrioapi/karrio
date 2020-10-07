import React from 'react';
import { Link, LinkProps } from "@reach/router";

const NavLink = (props: React.PropsWithoutRef<LinkProps<any>> & React.RefAttributes<HTMLAnchorElement>) => (
    <Link
        {...props}
        getProps={({ isCurrent }) => {
            return {
                className: isCurrent ? "menu-item is-active" : "menu-item"
            };
        }}
    />
);

export default NavLink;