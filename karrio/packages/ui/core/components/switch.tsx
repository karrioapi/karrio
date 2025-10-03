import { Switch as ShadcnSwitch } from "@karrio/ui/components/ui/switch";
import React from "react";

interface SwitchProps {
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  className?: string;
  iconClassName?: string;
  disabled?: boolean;
}

export const Switch = ({
  className,
  iconClassName,
  checked,
  onChange,
  disabled,
  ...props
}: SwitchProps): JSX.Element => {
  return (
    <div className={`button ${className || "is-white is-large"}`}>
      <ShadcnSwitch
        checked={checked}
        onCheckedChange={onChange}
        disabled={disabled}
        {...props}
      />
      <span
        className={`icon ${checked ? "has-text-success" : "has-text-grey"} ${iconClassName || "is-medium"}`}
      >
        <i
          className={`fas fa-${checked ? "toggle-on" : "toggle-off"} fa-lg`}
        ></i>
      </span>
    </div>
  );
};
