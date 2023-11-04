import CustomsInfoDescription from '@/components/descriptions/customs-info-description';
import AddressDescription from '@/components/descriptions/address-description';
import OptionsDescription from '@/components/descriptions/options-description';
import ParcelDescription from '@/components/descriptions/parcel-description';
import RateDescription from '@/components/descriptions/rate-description';
import { CustomsType, PaymentType, ShipmentType } from '@/lib/types';
import React, { useContext, useEffect, useState } from 'react';
import ButtonField from '@/components/generic/button-field';
import { LabelTypeEnum, PaidByEnum } from 'karrio/graphql';
import InputField from '@/components/generic/input-field';
import { useRouter } from 'next/dist/client/router';
import { formatRef, isNone } from '@/lib/helper';
import { Loading } from '@/components/loader';
import { useLabelDataMutation } from '@/context/label-data';

interface LiveRatesComponent {
  shipment: ShipmentType;
}

const DEFAULT_PAYMENT: Partial<PaymentType> = { paid_by: PaidByEnum.sender };

const LiveRates: React.FC<LiveRatesComponent> = ({ shipment }) => {
  const { loading } = useContext(Loading);
  const mutation = useLabelDataMutation(shipment.id);
  const [payment, setPayment] = useState<Partial<PaymentType>>(DEFAULT_PAYMENT);
  const [key, setKey] = useState<string>(`details-${Date.now()}`);
  const [selected_rate, setSelectedRate] = useState<ShipmentType['rates'][0] | undefined>(
    shipment?.selected_rate_id ? { id: shipment?.selected_rate_id } as any : undefined
  );

  const computeDisabled = (shipment: ShipmentType) => {
    return (
      shipment.recipient.address_line1 === undefined ||
      shipment.shipper.address_line1 === undefined ||
      shipment.parcels.length === 0 ||
      loading === true
    );
  };

  useEffect(() => { setKey(`details-${Date.now()}`); }, [shipment]);

  return (
    <div key={key}>
      <div className="columns is-multiline">

        <div className="column is-12 pb-2">
          <span className="title is-5">Shipment Details</span>

          <button className={`button is-small is-outlined is-info is-pulled-right ${loading ? 'is-loading' : ''}`}
            onClick={mutation.fetchRates} disabled={computeDisabled(shipment)}>
            <span>Fetch Rates</span>
          </button>
        </div>

        <div className="column is-12 py-1" style={shipment.shipper.address_line1 === undefined ? { display: 'none' } : {}}>

          <p className="is-title is-size-6 my-2 has-text-weight-semibold">Shipper Address</p>
          <AddressDescription address={shipment.shipper} />

        </div>

        <div className="column is-12 py-1" style={{ display: `${shipment.recipient.address_line1 === undefined ? 'none' : 'block'}` }}>

          <p className="is-title is-size-6 my-2 has-text-weight-semibold">Recipient Address</p>
          <AddressDescription address={shipment.recipient} />

        </div>

        <div className="column is-12 py-1" style={{ display: `${shipment.parcels.length == 0 ? 'none' : 'block'}` }}>

          <p className="is-title is-size-6 my-2 has-text-weight-semibold">Parcels</p>
          <ParcelDescription parcel={shipment.parcels[0]} />

        </div>

        <div className="column is-12 py-1" style={{ display: `${Object.values(shipment.options as object).length === 0 ? 'none' : 'block'}` }}>

          <p className="is-title is-size-6 my-2 has-text-weight-semibold">Options</p>
          <OptionsDescription options={shipment.options} />

        </div>

        {!isNone(shipment.customs) && <div className="column is-12 py-1">

          <p className="is-title is-size-6 my-2 has-text-weight-semibold">Customs Declaration</p>
          <CustomsInfoDescription customs={shipment.customs as CustomsType} />

        </div>}

        <div className="column is-12 py-4 px-0" style={{ display: `${(shipment.rates || []).length === 0 ? 'none' : 'block'}` }} key={key}>

          <h6 className="is-title is-size-6 px-3 my-1 has-text-weight-semibold">Live Rates</h6>

          <div className="menu-list py-2 rates-list-box">
            {(shipment.rates || []).map(rate => (
              <a key={rate.id} {...(rate.test_mode ? { title: "Test Mode" } : {})}
                className={`columns m-0 p-1 ${rate.id === selected_rate?.id ? 'has-text-grey-dark has-background-grey-lighter' : 'has-text-grey'}`}
                onClick={() => setSelectedRate(rate)}>

                <span className={`icon is-medium ${rate.id === selected_rate?.id ? 'has-text-success' : ''}`}>
                  {(rate.id === selected_rate?.id) ? <i className="fas fa-check-square"></i> : <i className="fas fa-square"></i>}
                </span>

                <RateDescription rate={rate} />

                {rate.test_mode && <div className="has-text-warning p-1">
                  <i className="fas fa-exclamation-circle"></i>
                </div>}
              </a>
            ))}
          </div>

        </div>

        <div className="column is-12 py-2" style={{ display: `${(shipment.rates || []).length === 0 ? 'none' : 'block'}` }}>

          <h6 className="is-title is-size-6 mt-1 mb-2 has-text-weight-semibold">Select your label type</h6>
          <div className="control">
            <label className="radio">
              <input
                className="mr-1"
                type="radio"
                name="label_type"
                defaultChecked={shipment.label_type === LabelTypeEnum.PDF}
                onChange={() => mutation.updateShipment({ label_type: LabelTypeEnum.PDF })}
              />
              <span className="is-size-7 has-text-weight-bold">{LabelTypeEnum.PDF}</span>
            </label>
            <label className="radio">
              <input
                className="mr-1"
                type="radio"
                name="label_type"
                defaultChecked={shipment.label_type === LabelTypeEnum.ZPL}
                onChange={() => mutation.updateShipment({ label_type: LabelTypeEnum.ZPL })}
              />
              <span className="is-size-7 has-text-weight-bold">{LabelTypeEnum.ZPL}</span>
            </label>
          </div>

        </div>

        <div className="column is-12 py-2" style={{ display: `${(shipment.rates || []).length === 0 ? 'none' : 'block'}` }}>

          <h6 className="is-title is-size-6 mt-1 mb-2 has-text-weight-semibold">Shipment Paid By</h6>

          <div className="control">
            <label className="radio">
              <input
                className="mr-1"
                type="radio"
                name="paid_by"
                defaultChecked={payment.paid_by === PaidByEnum.sender}
                onChange={() => setPayment({ paid_by: PaidByEnum.sender })}
              />
              <span className="is-size-7 has-text-weight-bold">{formatRef(PaidByEnum.sender.toString())}</span>
            </label>
            <label className="radio">
              <input
                className="mr-1"
                type="radio"
                name="paid_by"
                defaultChecked={payment.paid_by === PaidByEnum.recipient}
                onChange={() => setPayment({ ...payment, paid_by: PaidByEnum.recipient })}
              />
              <span className="is-size-7 has-text-weight-bold">{formatRef(PaidByEnum.recipient.toString())}</span>
            </label>
            <label className="radio">
              <input
                className="mr-1"
                type="radio"
                name="paid_by"
                defaultChecked={payment.paid_by === PaidByEnum.third_party}
                onChange={() => setPayment({ ...payment, paid_by: PaidByEnum.third_party })}
              />
              <span className="is-size-7 has-text-weight-bold">{formatRef(PaidByEnum.third_party.toString())}</span>
            </label>
          </div>

          {(payment.paid_by !== PaidByEnum.sender) &&
            <div className="columns ml-3 my-1 px-2 py-0" style={{ borderLeft: "solid 2px #ddd" }}>
              <InputField
                label="account number"
                className="is-small"
                fieldClass="column"
                defaultValue={payment?.account_number as string}
                onChange={e => setPayment({ ...payment, account_number: e.target.value })} />
            </div>}

        </div>

      </div>

      <hr className='my-1' style={{ height: '1px' }} />

      <ButtonField
        className={`is-success`}
        fieldClass="has-text-centered mt-3 p-3"
        onClick={() => mutation.buyLabel(selected_rate as any)}
        disabled={((shipment.rates || []).filter(r => r.id === selected_rate?.id).length === 0) || loading}
      >
        <span className="px-6">Buy shipping label</span>
      </ButtonField>

    </div>
  )
};

export default LiveRates;
