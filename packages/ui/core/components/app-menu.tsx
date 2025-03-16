import { ConfirmModalWrapper } from "../modals/form-modals";
import { MenuComponent } from "./menu";
import { AppLink } from "./app-link";
import React from "react";

interface AppMenuComponent extends React.InputHTMLAttributes<HTMLDivElement> {
  app: any;
  isViewing?: boolean;
}

export const AppMenu = ({ app, isViewing }: AppMenuComponent): JSX.Element => {
  const mutation = {} as any;

  return (
    <>
      <MenuComponent.Menu
        trigger={
          <button className="button is-default">
            <span className="icon is-small">
              <i className="fas fa-ellipsis-h"></i>
            </span>
          </button>
        }
      >
        <AppLink href={`/apps/${app.id}`} className="dropdown-item">
          <div className="icon-text is-size-7 has-text-grey">
            <span className="icon">
              <i className="fas fa-pen"></i>
            </span>
            <span>View app</span>
          </div>
        </AppLink>
        <ConfirmModalWrapper
          header="Uninstall app"
          onSubmit={() => mutation.deleteApp.mutateAsync({ id: app.id })}
          trigger={
            <MenuComponent.Item as="a" className={"dropdown-item"}>
              <div className="icon-text is-size-7 has-text-grey">
                <span className="icon">
                  <i className="fas fa-trash"></i>
                </span>
                <span>Uninstall app</span>
              </div>
            </MenuComponent.Item>
          }
        />
      </MenuComponent.Menu>
    </>
  );
};
