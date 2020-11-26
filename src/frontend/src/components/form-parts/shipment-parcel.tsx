import { Parcel, Shipment } from '@purplship/purplship';
import React, { FormEvent, useEffect, useRef, useState } from 'react';
import InputField from '@/components/generic/input-field';
import { Reference } from '@/library/context';
import SelectField from '@/components/generic/select-field';
import ButtonField from '@/components/generic/button-field';
import { findPreset, formatDimension } from '@/library/helper';
import { DIMENSION_UNITS, PresetCollection, WEIGHT_UNITS } from '@/library/types';
import { NotificationType, state } from '@/library/api';

const DEFAULT_STATE: Partial<Parcel> = {
    weight_unit: Parcel.WeightUnitEnum.KG,
    dimension_unit: Parcel.DimensionUnitEnum.CM
};

interface ShipmentParcelComponent {
    shipment: Shipment;
    update: (payload: {}) => void;
}

const ShipmentParcel: React.FC<ShipmentParcelComponent> = ({ shipment, update }) => {
    const form = useRef<HTMLFormElement>(null);
    const [key, setKey] = useState<string>(`parcel-${Date.now()}`);
    const [parcel, setParcel] = useState<Partial<Parcel>>(shipment.parcels.length > 0 ? shipment.parcels[0] : DEFAULT_STATE);
    const [parcel_type, setParcelType] = useState<string>(parcel.package_preset === undefined ? 'custom' : 'preset');
    const [presets, setPresets] = useState<PresetCollection>({});
    const [preset, setPreset] = useState<Partial<Parcel> | undefined>(undefined);

    const nextTab = shipment.shipper.country_code === shipment.recipient.country_code ? 'options' : 'customs info';
    const _ = (property: string) => (e: React.ChangeEvent<any>) => {
        let new_state = DEFAULT_STATE;
        if (property === 'parcel_type') {
            setKey(`parcel-${Date.now()}`);
            setParcelType(e.target.value);
            setPreset(undefined);
        } else if (property === 'package_preset') {
            const preset = findPreset(presets, e.target.value);
            setPreset(preset);
            const { width, height, length, dimension_unit, packaging_type } = preset || {};
            new_state = {
                ...parcel,
                [property]: e.target.value || undefined,
                width, height, length, dimension_unit, packaging_type
            };
        } else {
            new_state = { ...parcel, [property]: e.target.value || undefined };
        }

        setParcel(new_state);
    };
    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        try {
            let data = { parcels: [parcel] };
            if (parcel.id !== undefined) {
                const updated_parcel = await state.updateParcel(parcel as Parcel);
                data = { parcels: [updated_parcel] };
                state.setNotification({ type: NotificationType.success, message: 'Parcel successfully updated!' });
            }
            update(data);
            form.current?.dispatchEvent(new CustomEvent(
                'label-select-tab', { bubbles: true, detail: { nextTab } }
            ));
        } catch(e) {
            state.setNotification({ type: NotificationType.error, message: e.message });
        }
    };

    return (
        <form className="px-1 py-2" onSubmit={handleSubmit} ref={form}>
            <Reference.Consumer>
                {(ref) => {
                    if (Object.values(ref || {}).length > 0) { 
                        setPresets(ref.package_presets);
                        setPreset(findPreset(ref.package_presets, parcel.package_preset))
                    }
                    return <></>;
                }}
            </Reference.Consumer>

            <SelectField onChange={_("parcel_type")} value={parcel_type} className="is-fullwidth" required>
                <option value='custom'>Custom Measurements</option>
                <option value='preset'>Carrier Parcel Presets</option>
            </SelectField>

            {parcel_type === 'preset' && <>

                <SelectField onChange={_("package_preset")}  value={parcel.package_preset} name="package_preset" className="is-fullwidth  is-capitalized" required>
                    <option value="">Select a Carrier Provided Parcel</option>

                    {Object
                        .entries(presets)
                        .map(([key, value]) => {
                            return (
                                <optgroup key={key} label={key.replaceAll('_', ' ').toLocaleUpperCase()}>
                                    {Object.keys(value as object).map((preset) => (
                                        <option key={preset} value={preset}>
                                            {preset.replaceAll('_', ' ').toLocaleUpperCase()}
                                        </option>
                                    ))}
                                </optgroup>
                            );
                        })
                    }
                </SelectField>

                <div className="is-size-7 mt-1 mb-2 has-text-grey">{formatDimension(preset)}</div>

            </>}

            {parcel_type === 'custom' && <>
                <h6 className="is-size-7 my-2 has-text-weight-semibold">Dimensions</h6>

                <div className="columns mb-0 px-2">

                    <SelectField onChange={_("packaging_type")} value={parcel.packaging_type} className="is-small is-fullwidth" fieldClass="column is-4 mb-0 px-1 py-2" required>
                        <option value="">Select a Packaging Type</option>

                        <Reference.Consumer>
                            {(ref) => (Object.values(ref || {}).length > 0) && Object
                                .entries(ref.packaging_types)
                                .map(([key, value]) => {
                                    return (
                                        <optgroup key={key} label={key.replaceAll('_', ' ').toLocaleUpperCase()}>
                                            {Object.keys(value as object).map((type) => (
                                                <option key={type} value={type}>{type.replaceAll('_', ' ').toLocaleUpperCase()}</option>
                                            ))}
                                        </optgroup>
                                    );
                                })
                            }
                        </Reference.Consumer>
                    </SelectField>

                    <span className="is-size-7 my-3">W:</span>
                    <InputField type="number" step=".01" min="0" onChange={_('width')} defaultValue={parcel.width} className="is-small" fieldClass="column mb-0 px-1 py-2" required />

                    <span className="is-size-7 my-3">H:</span>
                    <InputField type="number" step=".01" min="0" onChange={_('height')} defaultValue={parcel.height} className="is-small" fieldClass="column mb-0 px-1 py-2" required />

                    <span className="is-size-7 my-3">L:</span>
                    <InputField type="number" step=".01" min="0" onChange={_('length')} defaultValue={parcel.length} className="is-small" fieldClass="column mb-0 px-1 py-2" required />

                    <SelectField onChange={_("dimension_unit")} value={parcel.dimension_unit || Parcel.DimensionUnitEnum.CM} className="is-small is-fullwidth" fieldClass="column mb-0 px-1 py-2" required>
                        {DIMENSION_UNITS.map(unit => (
                            <option key={unit} value={unit}>{unit}</option>
                        ))}
                    </SelectField>

                </div>

            </>}

            <h6 className="is-size-7 my-2 has-text-weight-semibold">Weight</h6>

            <div className="columns mb-0 px-2">

                <InputField type="number" step=".01" min="0" onChange={_('weight')} defaultValue={parcel.weight} className="is-small" fieldClass="column is-2 mb-0 px-1 py-2" required />

                <SelectField onChange={_("weight_unit")} value={parcel.weight_unit || Parcel.WeightUnitEnum.KG} className="is-small is-fullwidth" fieldClass="column is-2 mb-0 px-1 py-2" required>
                    {WEIGHT_UNITS.map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                    ))}
                </SelectField>

            </div>

            <ButtonField type="submit" className="is-primary" fieldClass="has-text-centered mt-3" disabled={shipment.parcels.length > 0 && shipment.parcels[0] == parcel}>
                <span>Save</span>
                <span className="icon is-small">
                    <i className="fas fa-chevron-right"></i>
                </span>
            </ButtonField>

        </form>
    )
};

export default ShipmentParcel;