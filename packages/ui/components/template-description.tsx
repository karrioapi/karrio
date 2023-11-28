import { DocumentTemplateType } from '@karrio/types';
import React from 'react';

interface TemplateDescriptionComponent {
  template: DocumentTemplateType;
}

export const TemplateDescription: React.FC<TemplateDescriptionComponent> = ({ template }) => (
  <>
    <p className="is-size-7 my-1 has-text-weight-semibold">{template.name}</p>
    <p className="is-size-7 my-1 has-text-grey">{template.description}</p>
  </>
);
