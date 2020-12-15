import { Parcel, Shipment } from '@purplship/purplship';
import React, { FormEvent, useContext, useEffect, useReducer, useRef, useState } from 'react';
import InputField from '@/components/generic/input-field';
import { Reference } from '@/library/context';
import SelectField from '@/components/generic/select-field';
import ButtonField from '@/components/generic/button-field';
import { deepEqual, findPreset, formatDimension, formatRef, isNone } from '@/library/helper';
import { DIMENSION_UNITS, PresetCollection, WEIGHT_UNITS } from '@/library/types';
import { NotificationType, state } from '@/library/api';

type stateValue = string | boolean | Partial<Parcel>;
const DEFAULT_STATE: Partial<Parcel> = {
    packaging_type: "envelope",
    weight_unit: Parcel.WeightUnitEnum.KG,
    dimension_unit: Parcel.DimensionUnitEnum.CM
};

interface ShipmentParcelComponent {
    shipment: Shipment;
    update: (payload: {}, refresh?: boolean) => void;
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
                packaging_type: packaging_type|| null,
                package_preset: package_preset || null 
            };
        default:
            return { ...state, [name]: value }
    }
}

const ShipmentParcel: React.FC<ShipmentParcelComponent> = ({ shipment, update }) => {
    const Ref = useContext(Reference);
    const form = useRef<HTMLFormElement>(null);
    const parcelValue = () => shipment.parcels.length > 0 ? shipment.parcels[0] : DEFAULT_STATE;
    const [key] = useState<string>(`parcel-${Date.now()}`);
    const [parcel, dispatch] = useReducer(reducer, parcelValue(), parcelValue);
    const [parcel_type, setParcelType] = useState<string>(parcel.package_preset === undefined ? 'custom' : 'preset');
    const [presets, setPresets] = useState<PresetCollection>({});
    const nextTab = shipment.shipper.country_code === shipment.recipient.country_code ? 'options' : 'customs info';

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const target = event.target;
        const name: string = target.name;
        let value: stateValue = target.type === 'checkbox' ? target.checked : target.value;

        if (name === 'parcel_type') {
            setParcelType(value as string);
            value = { ...parcel, package_preset: null };
        }
        if (name === 'package_preset') {
            value = findPreset(presets, value as string) || parcel;
        }

        dispatch({ name, value });
    };
    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        try {
            if (parcel.id !== undefined && shipment.id !== undefined) {
                await state.updateParcel(parcel as Parcel);
                const updated_shipment = await state.retrieveShipment(shipment.id);
                state.setNotification({ type: NotificationType.success, message: 'Parcel successfully updated!' });
                update({ ...updated_shipment }, true);
            } else {
                update({ parcels: [parcel] });
                form.current?.dispatchEvent(
                    new CustomEvent('label-select-tab', { bubbles: true, detail: { nextTab } })
                );
            }
        } catch (err) {
            state.setNotification({ type: NotificationType.error, message: err });
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
        if (Object.values(Ref || {}).length > 0) {
            setPresets(Ref.package_presets);
            const value = findPreset(Ref.package_presets, parcel.package_preset) as Partial<Parcel>;
            if (value !== undefined) dispatch({ name: "package_preset", value });
        }
    }, [Ref]);

    return (
        <form className="px-1 py-2" onSubmit={handleSubmit} key={key} ref={form}>

            <SelectField name="parcel_type" onChange={handleChange} value={parcel_type} className="is-fullwidth" required>
                <option value='custom'>Custom Measurements</option>
                <option value='preset'>Carrier Parcel Presets</option>
            </SelectField>

            {parcel_type === 'preset' && <>

                <SelectField name="package_preset" onChange={handleChange} value={parcel.package_preset} className="is-fullwidth  is-capitalized" required>
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

                <div className="is-size-7 mt-1 mb-2 has-text-grey">{formatDimension(findPreset(presets, parcel.package_preset))}</div>

            </>}

            {parcel_type === 'custom' && <>
                <h6 className="is-size-7 my-2 has-text-weight-semibold">Dimensions</h6>

                <div className="columns mb-0 px-2">

                    <SelectField name="packaging_type" onChange={handleChange} value={parcel.packaging_type} className="is-small is-fullwidth" fieldClass="column is-4 mb-0 px-1 py-2" required>
                        <Reference.Consumer>
                            {(ref) => (Object.values(ref || {}).length > 0) && Object
                                .entries(ref.packaging_types)
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
                        </Reference.Consumer>
                    </SelectField>

                    <span className="is-size-7 my-3">W:</span>
                    <InputField type="number" step=".01" min="0" name="width" onChange={handleChange} defaultValue={parcel.width} className="is-small" fieldClass="column mb-0 px-1 py-2" required={isDimensionRequired(parcel)} />

                    <span className="is-size-7 my-3">H:</span>
                    <InputField type="number" step=".01" min="0" name="height" onChange={handleChange} defaultValue={parcel.height} className="is-small" fieldClass="column mb-0 px-1 py-2" required={isDimensionRequired(parcel)} />

                    <span className="is-size-7 my-3">L:</span>
                    <InputField type="number" step=".01" min="0" name="length" onChange={handleChange} defaultValue={parcel.length} className="is-small" fieldClass="column mb-0 px-1 py-2" required={isDimensionRequired(parcel)} />

                    <SelectField name="dimension_unit" onChange={handleChange} value={parcel.dimension_unit || Parcel.DimensionUnitEnum.CM} className="is-small is-fullwidth" fieldClass="column mb-0 px-1 py-2" required={isDimensionRequired(parcel)}>
                        {DIMENSION_UNITS.map(unit => (
                            <option key={unit} value={unit}>{unit}</option>
                        ))}
                    </SelectField>

                </div>

            </>}

            <h6 className="is-size-7 my-2 has-text-weight-semibold">Weight</h6>

            <div className="columns mb-0 px-2">

                <InputField type="number" step=".01" min="0" name="weight" onChange={handleChange} defaultValue={parcel.weight} className="is-small" fieldClass="column is-2 mb-0 px-1 py-2" required />

                <SelectField name="weight_unit" onChange={handleChange} value={parcel.weight_unit || Parcel.WeightUnitEnum.KG} className="is-small is-fullwidth" fieldClass="column is-2 mb-0 px-1 py-2" required>
                    {WEIGHT_UNITS.map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                    ))}
                </SelectField>

            </div>

            <ButtonField type="submit" className="is-primary" fieldClass="has-text-centered mt-3" disabled={shipment.parcels.length > 0 && deepEqual(shipment.parcels[0], parcel)}>
                <span>{parcel.id === undefined ? 'Continue' : 'Save'}</span>
                {parcel.id === undefined && <span className="icon is-small">
                    <i className="fas fa-chevron-right"></i>
                </span>}
            </ButtonField>

        </form>
    )
};

export default ShipmentParcel;