import React from 'react';
import { LazyQueryResult, useLazyQuery } from '@apollo/client';
import { GET_DEFAULT_TEMPLATES } from '@/graphql';
import { AddressType, CustomsType, ParcelType, TemplateType } from '@/library/types';
import { isNone } from '@/library/helper';


export class DefaultTemplates {
    constructor(private templates: TemplateType[]) { }

    get default_customs(): CustomsType | null {
        const template = this.templates.find(
            template => template.customs !== undefined && template.customs !== null
        );
        return (template || {}).customs || null
    }

    get default_address(): AddressType | null {
        const template = this.templates.find(
            template => template.address !== undefined && template.address !== null
        );
        return (template || {}).address || null
    }

    get default_parcel(): ParcelType | null {
        const template = this.templates.find(
            template => template.parcel !== undefined && template.parcel !== null
        );
        return (template || {}).parcel || null
    }
}


type DefaultTemplate = { default_templates: TemplateType[] };
export type DefaultTemplatesType = LazyQueryResult<DefaultTemplate, any> & { 
  default_address?: AddressType | null;
  default_customs?: CustomsType | null;
  default_parcel?: ParcelType | null;
  load: (options?: any) => void;
};

export const DefaultTemplatesData = React.createContext<DefaultTemplatesType>({} as DefaultTemplatesType);

const TemplatesQuery: React.FC = ({ children }) => {
  const [load, result] = useLazyQuery<DefaultTemplate>(GET_DEFAULT_TEMPLATES);

  const extract = (templates?: TemplateType[]) => {
    if (isNone(templates)) return {};
    const { default_address, default_customs, default_parcel } = new DefaultTemplates(templates || []);
    return { default_address, default_customs, default_parcel };
  };

  return (
    <DefaultTemplatesData.Provider value={{
      load,
      ...extract(result.data?.default_templates),
      ...result,
    }}>
      {children}
    </DefaultTemplatesData.Provider>
  );
};

export default TemplatesQuery;
