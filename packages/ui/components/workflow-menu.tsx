import { useWorkflowMutation, WorkflowType } from '@karrio/hooks/workflows';
import { ConfirmModalWrapper } from '../modals/form-modals';
import { MenuComponent } from './menu';
import { AppLink } from './app-link';
import React from 'react';


interface WorkflowMenuComponent extends React.InputHTMLAttributes<HTMLDivElement> {
  workflow: WorkflowType;
  isViewing?: boolean;
}


export const WorkflowMenu: React.FC<WorkflowMenuComponent> = ({ workflow, isViewing }) => {
  const mutation = useWorkflowMutation();

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
        <AppLink href={`/workflows/${workflow.id}`} className="dropdown-item">
          <div className="icon-text is-size-7 has-text-grey">
            <span className="icon">
              <i className="fas fa-pen"></i>
            </span>
            <span>Edit</span>
          </div>
        </AppLink>
        <ConfirmModalWrapper
          header='Confirm workflow deletion'
          onSubmit={() => mutation.deleteWorkflow.mutateAsync({ id: workflow.id })}
          trigger={
            <MenuComponent.Item as='a' className={'dropdown-item'}>
              <div className="icon-text is-size-7 has-text-grey">
                <span className="icon">
                  <i className="fas fa-trash"></i>
                </span>
                <span>Delete</span>
              </div>
            </MenuComponent.Item>
          }
        />
      </MenuComponent.Menu>
    </>
  );
};
