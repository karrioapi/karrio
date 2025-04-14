import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem
} from "@karrio/ui/components/ui/dropdown-menu";
import React from "react";

interface MenuProps {
  trigger: JSX.Element;
  children: React.ReactNode;
}

const Wrapper = ({ trigger, children }: MenuProps): JSX.Element => {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        {trigger}
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="dropdown-content is-menu">
        {children}
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

const Item = ({ children, ...props }: React.ComponentProps<typeof DropdownMenuItem>): JSX.Element => (
  <DropdownMenuItem {...props}>{children}</DropdownMenuItem>
);

export const MenuComponent = {
  Menu: Wrapper,
  Item: Item,
};
