import { Parcel, ParcelDimensionUnitEnum, ParcelWeightUnitEnum, Shipment } from '@/api';
import React, { FormEvent, useContext, useEffect, useReducer, useRef, useState } from 'react';
import InputField from '@/components/generic/input-field';
import SelectField from '@/components/generic/select-field';
import ButtonField from '@/components/generic/button-field';
import CheckBoxField from '@/components/generic/checkbox-field';
import { deepEqual, findPreset, formatDimension, formatRef, isNone } from '@/library/helper';
import { DIMENSION_UNITS, NotificationType, PresetCollection, WEIGHT_UNITS } from '@/library/types';
import { APIReference } from '@/components/data/references-query';
import { ParcelTemplates } from '@/components/data/parcel-templates-query';
import { DefaultTemplatesData } from '@/components/data/default-templates-query';
import ShipmentMutation from '@/components/data/shipment-mutation';
import { Notify } from '@/components/notifier';

type stateValue = string | boolean | Partial<Parcel>;
export const DEFAULT_PARCEL_CONTENT: Partial<Parcel> = {
    packaging_type: "envelope",
    is_document: false,
    weight_unit: ParcelWeightUnitEnum.Kg,
    dimension_unit: ParcelDimensionUnitEnum.Cm
};

interface ParcelFormComponent {
    value?: Parcel;
    shipment?: Shipment;
    update: (data: { changes?: Partial<Shipment>, refresh?: boolean }) => void;
}

function reducer(state: any, { name, value }: { name: string, value: stateValue }) {
    switch (name) {
        case 'parcel_type':
        case 'package_preset':
            const { width, height, length, dimension_unit, packaging_type, package_preset } = value as Parcel;
            return {
                ...state,
                width: width || null,
                height: height || null,
                length: length || null,
                dimension_unit: dimension_unit || null,
                packaging_type: packaging_type || null,
                package_preset: package_preset || null
            };
        case 'template':
            return { ...(value as Parcel) };
        default:
            return { ...state, [name]: value }
    }
}

const ParcelForm: React.FC<ParcelFormComponent> = ShipmentMutation<ParcelFormComponent>(
    ({ value, shipment, update, children, updateParcel }) => {
        const { notify } = useContext(Notify);
        const { packaging_types, package_presets } = useContext(APIReference);
        const { templates, called, loading, load } = useContext(ParcelTemplates);
        const { default_parcel } = useContext(DefaultTemplatesData);
        const form = useRef<HTMLFormElement>(null);
        const [key, setKey] = useState<string>(`parcel-${Date.now()}`);
        const [presets, setPresets] = useState<PresetCollection>(package_presets as PresetCollection);
        const [parcel, dispatch] = useReducer(reducer, value, () => value || DEFAULT_PARCEL_CONTENT);
        const [parcel_type, setParcelType] = useState<string>(isNone(value?.package_preset) ? 'custom' : 'preset');
        const [dimension, setDimension] = useState<string | undefined>(formatDimension(isNone(value?.package_preset) ? undefined : value));
        const nextTab = shipment?.shipper.country_code === shipment?.recipient.country_code ? 'options' : 'customs info';

        const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
            const target = event.target;
            let name: string = target.name;
            let value: stateValue = target.type === 'checkbox' ? target.checked : target.value;

            if (name === 'parcel_type') {
                const template = templates.find(p => p.id === value)?.parcel;
                const preset = { package_preset: undefined } as Partial<Parcel>;

                setParcelType(value as string);
                setDimension(formatDimension(value === 'customs' ? undefined : template || preset));
                value = template || preset as any;
                name = isNone(template) ? name : 'template';
            }
            else if (name === 'package_preset') {
                const preset = findPreset(presets, value as string) || parcel;
                setDimension(formatDimension(preset));
                value = preset;
            }

            dispatch({ name, value });
        };
        const handleSubmit = async (e: FormEvent) => {
            e.preventDefault();
            try {
                if (parcel.id !== undefined) {
                    await updateParcel(parcel as Parcel);
                    notify({ type: NotificationType.success, message: 'Parcel successfully updated!' });
                    update({ refresh: true });
                } else {
                    update({ changes: { parcels: [parcel] } });
                    form.current?.dispatchEvent(
                        new CustomEvent('label-select-tab', { bubbles: true, detail: { nextTab } })
                    );
                }
            } catch (err) {
                notify({ type: NotificationType.error, message: err });
            }
        };
        const isDimensionRequired = (parcel: Parcel) => {
            return !(
                isNone(parcel.width) &&
                isNone(parcel.height) &&
                isNone(parcel.length)
            );
        };

        useEffect(() => {
            if (!isNone(package_presets)) {
                setPresets(package_presets as PresetCollection);
                const preset = findPreset(package_presets as PresetCollection, parcel.package_preset) as Partial<Parcel>;
                if (!isNone(preset)) {
                    setDimension(formatDimension(preset));
                    dispatch({ name: "package_preset", value: preset });
                }
            }
        }, [package_presets]);

        useEffect(() => {
            if (!called && !loading) load();
            // Load parcel template if we are creating a new shipment and there is a default parcel preset
            if (!isNone(package_presets) && shipment !== undefined && isNone(shipment.id) && !isNone(default_parcel) && !deepEqual(default_parcel, parcel)) {
                const preset = findPreset(package_presets as PresetCollection, default_parcel?.package_preset as string) as Partial<Parcel>;
                if (!isNone(preset)) {
                    setDimension(formatDimension(preset));
                    setParcelType('preset');
                }
                dispatch({ name: 'template', value: { ...(preset || {}), ...default_parcel } as Parcel });
                setKey(`parcel-${Date.now()}`);
            }
        }, [templates]);

        return (
            <form className="px-1 py-2" onSubmit={handleSubmit} key={key} ref={form}>

                {React.Children.map(children, (child: any) => React.cloneElement(child, { ...child.props, parcel, onChange: handleChange }))}

                <div className="columns mb-0 px-2">

                    <CheckBoxField name="is_document" onChange={handleChange} defaultChecked={parcel.is_document} fieldClass="column mb-0 is-12 px-2 py-2">
                        <span>Document Only</span>
                    </CheckBoxField>

                </div>

                <SelectField name="parcel_type" onChange={handleChange} value={parcel_type} className="is-fullwidth" required>
                    <optgroup label="New">
                        <option value='custom'>Custom Measurements</option>
                        <option value='preset'>Carrier Parcel Presets</option>
                    </optgroup>
                    <optgroup label="Load your custom parcel template">
                        {templates.map(template => (
                            <option key={template.id} value={template.id}>{template.label}</option>
                        ))}
                    </optgroup>
                </SelectField>

                {parcel_type === 'preset' && <>

                    <SelectField name="package_preset" onChange={handleChange} value={parcel.package_preset} className="is-fullwidth is-capitalized" required>
                        <option value="">Select a Carrier Provided Parcel</option>

                        {Object
                            .entries(presets)
                            .map(([key, value]) => {
                                return (
                                    <optgroup key={key} label={formatRef(key)}>
                                        {Object.keys(value as object).map((preset) => (
                                            <option key={preset} value={preset}>{formatRef(preset)}</option>
                                        ))}
                                    </optgroup>
                                );
                            })
                        }
                    </SelectField>

                </>}

                {parcel_type !== 'custom' && <div className="is-size-7 mt-1 mb-2 has-text-grey">{dimension}</div>}

                {parcel_type === 'custom' && <>
                    <h6 className="is-size-7 my-2 has-text-weight-semibold">Dimensions</h6>

                    <div className="columns mb-0 px-2">

                        <SelectField name="packaging_type" onChange={handleChange} value={parcel.packaging_type} className="is-small is-fullwidth" fieldClass="column is-4 mb-0 px-1 py-2" required>
                            {packaging_types && Object
                                .entries(packaging_types)
                                .map(([key, value]) => {
                                    return (
                                        <optgroup key={key} label={formatRef(key)}>
                                            {Object.keys(value as object).map((type) => (
                                                <option key={type} value={type}>{formatRef(type)}</option>
                                            ))}
                                        </optgroup>
                                    );
                                })
                            }
                        </SelectField>

                        <span className="is-size-7 my-3">W:</span>
                        <InputField type="number" step="any" min="0" name="width" onChange={handleChange} defaultValue={parcel.width} className="is-small" fieldClass="column mb-0 px-1 py-2" required={isDimensionRequired(parcel)} />

                        <span className="is-size-7 my-3">H:</span>
                        <InputField type="number" step="any" min="0" name="height" onChange={handleChange} defaultValue={parcel.height} className="is-small" fieldClass="column mb-0 px-1 py-2" required={isDimensionRequired(parcel)} />

                        <span className="is-size-7 my-3">L:</span>
                        <InputField type="number" step="any" min="0" name="length" onChange={handleChange} defaultValue={parcel.length} className="is-small" fieldClass="column mb-0 px-1 py-2" required={isDimensionRequired(parcel)} />

                        <SelectField name="dimension_unit" onChange={handleChange} value={parcel.dimension_unit || ParcelDimensionUnitEnum.Cm} className="is-small is-fullwidth" fieldClass="column mb-0 px-1 py-2" required={isDimensionRequired(parcel)}>
                            {DIMENSION_UNITS.map(unit => (
                                <option key={unit} value={unit}>{unit}</option>
                            ))}
                        </SelectField>

                    </div>

                </>}

                <h6 className="is-size-7 my-2 has-text-weight-semibold">Weight</h6>

                <div className="columns mb-0 px-2">

                    <InputField type="number" step="any" min="0" name="weight" onChange={handleChange} defaultValue={parcel.weight} className="is-small" fieldClass="column is-2 mb-0 px-1 py-2" required />

                    <SelectField name="weight_unit" onChange={handleChange} value={parcel.weight_unit || ParcelWeightUnitEnum.Kg} className="is-small is-fullwidth" fieldClass="column is-2 mb-0 px-1 py-2" required>
                        {WEIGHT_UNITS.map(unit => (
                            <option key={unit} value={unit}>{unit}</option>
                        ))}
                    </SelectField>

                </div>

                <ButtonField type="submit" className="is-primary" fieldClass="has-text-centered mt-3" disabled={deepEqual(value, parcel)}>
                    <span>{parcel.id === undefined ? 'Continue' : 'Save'}</span>
                    {parcel.id === undefined && <span className="icon is-small">
                        <i className="fas fa-chevron-right"></i>
                    </span>}
                </ButtonField>

            </form>
        )
    });

export default ParcelForm;