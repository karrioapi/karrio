import { AddressDescription } from '../components/address-description';
import { useManifestMutation } from '@karrio/hooks/manifests';
import { InputField } from '../components/input-field';
import { ManifestData } from '@karrio/types/rest/api';
import { useNotifier } from '../components/notifier';
import { AddressForm } from '../forms/address-form';
import { ModalFormProps, useModal } from './modal';
import { NotificationType } from '@karrio/types';
import { useLoader } from '../components/loader';
import { Disclosure } from '@headlessui/react';
import { isEqual } from '@karrio/lib';
import React from 'react';

type CreateManifestModalProps = {
  header?: string;
  manifest: ManifestData;
};

function reducer(state: any, { name, value }: { name: string, value: string | boolean | object | string[] }): ManifestData {
  switch (name) {
    case "full":
      return { ...(value as ManifestData) };
    case "partial":
      return { ...state, ...(value as ManifestData) };
    default:
      return { ...state, [name]: value };
  }
}

export const CreateManifestModal: React.FC<ModalFormProps<CreateManifestModalProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const ManifestFormComponent: React.FC<CreateManifestModalProps> = props => {
    const { manifest: defaultValue, header } = props;
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const mutation = useManifestMutation();
    const [key, setKey] = React.useState<string>(`manifest-${Date.now()}`);
    const [manifest, dispatch] = React.useReducer(reducer, defaultValue, () => defaultValue);

    const handleChange = (event: React.ChangeEvent<any>) => {
      const target = event.target;
      const name: string = target.name;
      let value = target.type === 'checkbox' ? target.checked : target.value;

      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value)
      }

      dispatch({ name, value });
    };
    const handleSubmit = async (e: React.MouseEvent) => {
      e.preventDefault();
      const { ...payload } = manifest;
      try {
        loader.setLoading(true);
        await mutation.createManifest.mutateAsync(payload);
        setTimeout(() => close(), 1000);
      } catch (message: any) {
        notifier.notify({ type: NotificationType.error, message });
      }
      loader.setLoading(false);
    };

    return (
      <div className="modal-card-body modal-form" key={key}>
        <div className="form-floating-header p-4">
          <span className="has-text-weight-bold is-size-6">{header || `Create manifest`}</span>
        </div>
        <div className="p-3 my-4"></div>

        {(manifest !== undefined) && <>

          {/* Shipment IDs section */}
          <div className="field mb-2">
            <div className="control">
              <div className="select is-multiple is-small is-fullwidth">
                <select disabled name="permissions" value={manifest.shipment_ids} size={3} multiple>
                  {(manifest.shipment_ids || []).map((shipment_id) => (
                    <option key={`${shipment_id}permission-${Date.now()}`} value={shipment_id}>{shipment_id}</option>)
                  )}
                </select>
              </div>
            </div>
          </div>

          {/* Address section */}
          <Disclosure as='div' className="card px-0 my-3">
            <Disclosure.Button as='header' className="p-3 is-clickable">
              <header className="is-flex is-justify-content-space-between">
                <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">ADDRESS</span>
              </header>

              <AddressDescription address={manifest.address as any} />
            </Disclosure.Button>
            <Disclosure.Panel>
              <hr className='my-1' style={{ height: '1px' }} />

              <div className="p-3">

                <AddressForm name="template"
                  value={manifest.address as any}
                  shipment={manifest as any}
                  onSubmit={async data => { dispatch({ name: 'address', value: data }); }}
                />

              </div>

            </Disclosure.Panel>
          </Disclosure>

          {/* Reference section */}
          <InputField
            label="reference"
            name="reference"
            onChange={handleChange}
            defaultValue={manifest?.reference || ""}
            className="is-small"
            wrapperClass="column px-0 py-2"
            fieldClass="mb-0 p-0"
          />

          <div className="p-3 my-5"></div>

          <div className="form-floating-footer has-text-centered p-1">
            <button className="button is-default m-1 is-small" type="button" onClick={close}>
              <span>Cancel</span>
            </button>
            <button className={"button is-primary m-1 is-small" + (mutation.createManifest.isLoading ? " is-loading" : "")}
              disabled={mutation.createManifest.isLoading}
              onClick={handleSubmit} type="button">
              <span>Create manifest{manifest.shipment_ids.length > 0 ? 's' : ''}</span>
            </button>
          </div>

        </>}

      </div>
    )
  };

  return React.cloneElement(trigger, {
    onClick: () => modal.open(<ManifestFormComponent {...args} />)
  });
};

