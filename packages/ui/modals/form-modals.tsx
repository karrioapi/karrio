import { AddressType, CustomsType, DEFAULT_PARCEL_CONTENT, NotificationType, ParcelType, ShipmentType } from '@karrio/types';
import { CustomsInfoForm } from '../forms/customs-info-form';
import { useNotifier } from '../components/notifier';
import { AddressForm } from '../forms/address-form';
import React, { FormEvent, useEffect } from 'react';
import { ModalFormProps, useModal } from './modal';
import { ParcelForm } from '../forms/parcel-form';
import { useLoader } from '../components/loader';
import { isEqual } from '@karrio/lib';


type AddressModalEditorProps = {
  header?: string;
  shipment?: ShipmentType;
  address: AddressType | ShipmentType['recipient'] | ShipmentType['shipper'];
  onSubmit: (address: AddressType) => Promise<any>;
};

export const AddressModalEditor: React.FC<ModalFormProps<AddressModalEditorProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const FormComponent: React.FC<AddressModalEditorProps> = props => {
    const { address, shipment, header, onSubmit } = props;
    const { close } = useModal();

    return (
      <section className="modal-card-body modal-form">
        <div className="form-floating-header p-4">
          <span className="has-text-weight-bold is-size-6">{header || `Edit address`}</span>
        </div>
        <div className="p-3 my-4"></div>

        <AddressForm
          name="template"
          value={address}
          shipment={shipment}
          onSubmit={async (data) => { await onSubmit(data); close(); }}
        />
      </section>
    )
  };

  return React.cloneElement(trigger, {
    onClick: () => modal.open(<FormComponent {...args} />)
  });
};

type ParcelModalEditorProps = {
  header?: string;
  parcel?: ParcelType;
  shipment?: ShipmentType;
  onSubmit: (parcel: ParcelType) => Promise<any>;
};

export const ParcelModalEditor: React.FC<ModalFormProps<ParcelModalEditorProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const FormComponent: React.FC<ParcelModalEditorProps> = props => {
    const { parcel: value, header, shipment, onSubmit } = props;
    const { close } = useModal();
    const notifier = useNotifier();
    const loader = useLoader();
    const [parcel, setParcel] = React.useState(value || DEFAULT_PARCEL_CONTENT);

    const handleSubmit = async (e: FormEvent) => {
      e.preventDefault();
      try {
        parcel.id && loader.setLoading(true);

        await onSubmit(parcel as ParcelType);

        parcel.id && notifier.notify({
          type: NotificationType.success,
          message: 'Parcel successfully updated!'
        });
        close();
      } catch (err: any) {
        notifier.notify({ type: NotificationType.error, message: err });
      }
      loader.setLoading(false);
    };

    useEffect(() => { setParcel(value || DEFAULT_PARCEL_CONTENT); }, [value]);

    return (
      <section className="modal-card-body modal-form">
        <div className="form-floating-header p-4">
          <span className="has-text-weight-bold is-size-6">{header || `Edit parcel`}</span>
        </div>
        <div className="p-3 my-4"></div>

        <form onSubmit={handleSubmit}>
          <ParcelForm
            shipment={shipment}
            value={parcel as ParcelType}
            onChange={(parcel) => setParcel(parcel)}
          >
            <div className="p-3 my-5"></div>
            <div className="form-floating-footer has-text-centered p-1">
              <button className="button is-default m-1 is-small" type="button" onClick={close}>
                <span>Cancel</span>
              </button>
              <button className="button is-primary m-1 is-small"
                disabled={isEqual(value, parcel)}
                type="submit">
                <span>Save</span>
              </button>
            </div>
          </ParcelForm>
        </form>
      </section>
    )
  };

  return React.cloneElement(trigger, {
    onClick: () => modal.open(<FormComponent {...args} />)
  });
};

type CustomsModalEditorProps = {
  header?: string;
  customs?: CustomsType | null;
  shipment?: ShipmentType;
  onSubmit: (customs: CustomsType | null) => Promise<any>;
};

export const CustomsModalEditor: React.FC<ModalFormProps<CustomsModalEditorProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const FormComponent: React.FC<CustomsModalEditorProps> = props => {
    const { customs, header, onSubmit } = props;
    const { close } = useModal();

    return (
      <section className="modal-card-body modal-form">
        <div className="form-floating-header p-4">
          <span className="has-text-weight-bold is-size-6">{header || `Edit customs info`}</span>
        </div>
        <div className="p-3 my-4"></div>

        <CustomsInfoForm
          value={customs}
          onSubmit={async (data) => { await onSubmit(data); close(); }}
        />
      </section>
    )
  };

  return React.cloneElement(trigger, {
    onClick: () => modal.open(<FormComponent {...args} />)
  });
};


type ConfirmModalWrapperProps = {
  header?: string;
  action?: string;
  onSubmit: () => Promise<any>;
};

export const ConfirmModalWrapper: React.FC<ModalFormProps<ConfirmModalWrapperProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const FormComponent: React.FC<ConfirmModalWrapperProps> = props => {
    const { header, action, onSubmit } = props;
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const [key, setKey] = React.useState<string>(`confirm-${Date.now()}`);

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      try {
        loader.setLoading(true);
        onSubmit && onSubmit();
        setTimeout(() => close(), 1000);
      } catch (message: any) {
        notifier.notify({ type: NotificationType.error, message });
      }
      loader.setLoading(false);
    };

    return (
      <section className="modal-card-body modal-form">
        <div className="form-floating-header p-4">
          <span className="has-text-weight-bold is-size-6">{header || `Confirm action`}</span>
        </div>
        <div className="p-3 my-4"></div>

        <form className="px-1 py-2" onSubmit={handleSubmit} key={key}>

          <div className="buttons my=2">
            <button
              className="button is-info is-light is-small"
              onClick={close}
              disabled={loader.loading}
            >
              <span>Cancel</span>
            </button>
            <input
              type="submit"
              className={"button is-danger is-small" + `${loader.loading ? " is-loading" : ""}`}
              value={action || "Delete"}
              disabled={loader.loading}
            />
          </div>

        </form>
      </section>
    )
  };

  return React.cloneElement(trigger, {
    onClick: (e: React.MouseEvent) => {
      e.stopPropagation();
      modal.open(<FormComponent {...args} />)
    }
  });
};
