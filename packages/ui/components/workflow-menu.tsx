import { useWorkflowMutation, WorkflowType } from '@karrio/hooks/workflows';
import { MenuComponent } from './menu';
import React from 'react';


interface WorkflowMenuComponent extends React.InputHTMLAttributes<HTMLDivElement> {
  workflow: WorkflowType;
  isViewing?: boolean;
}


export const WorkflowMenu: React.FC<WorkflowMenuComponent> = ({ workflow, isViewing }) => {

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
        <div className="icon-text is-size-7 has-text-grey">
          <span className="icon">
            <i className="fas fa-pen"></i>
          </span>
          <span>Edit</span>
        </div>
        <div className="icon-text is-size-7 has-text-grey">
          <span className="icon">
            <i className="fas fa-trash"></i>
          </span>
          <span>Delete</span>
        </div>
      </MenuComponent.Menu>
    </>
  );
};
