import SelectField from '@/components/generic/select-field';
import { NotificationType, WebhookType } from '@/lib/types';
import { useWebhookMutation } from '@/context/webhook';
import Notifier, { Notify } from '@/components/notifier';
import React, { useContext, useState } from 'react';
import json from 'highlight.js/lib/languages/json';
import { Loading } from '@/components/loader';
import hljs from 'highlight.js/lib/core';

hljs.registerLanguage('json', json);

const PLAIN_EVENT = JSON.stringify({
  event: "all",
  data: {
    "message": "this is a plain notification"
  }
}, null, 2);

type OperationType = {
  webhook?: WebhookType;
  onConfirm?: () => Promise<any>;
};
type WebhookTestContextType = {
  testWebhook: (operation?: OperationType) => void,
};
const WebhookTestModalContext = React.createContext<WebhookTestContextType>({} as WebhookTestContextType);

const WebhookTestModal: React.FC = ({ children }) => {
  const mutation = useWebhookMutation();
  const { notify } = useContext(Notify);
  const { setLoading, loading } = useContext(Loading);
  const [isActive, setIsActive] = useState<boolean>(false);
  const [payload, setPayload] = useState<string>(PLAIN_EVENT);
  const [key, setKey] = useState<string>(`webhook-test-${Date.now()}`);
  const [operation, setOperation] = useState<OperationType | undefined>();
  const NOTIFICATION_SAMPLE = testPayloadSample();

  const testWebhook = (operation?: OperationType) => {
    setIsActive(true);
    setOperation(operation);
    setPayload(PLAIN_EVENT);
    setKey(`webhook-test-${Date.now()}`);
  };
  const close = (_?: React.MouseEvent) => {
    setIsActive(false);
    setPayload(PLAIN_EVENT);
    setOperation(undefined);
    setKey(`webhook-test-${Date.now()}`);
  };
  const handleChange = (event: React.ChangeEvent<any>) => {
    event.preventDefault();
    setPayload(event.target.value);
  };
  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    setLoading(true);
    try {
      await mutation.testWebhook.mutateAsync({
        id: operation!.webhook!.id,
        payload: JSON.parse(payload),
      });
      notify({ type: NotificationType.success, message: `Webhook successfully Notified` });
    } catch (err: any) {
      notify({ type: NotificationType.error, message: err });
    }
    setLoading(false);
  };

  return (
    <>
      <WebhookTestModalContext.Provider value={{ testWebhook }}>
        {children}
      </WebhookTestModalContext.Provider>

      <Notifier>
        <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
          <div className="modal-background"></div>
          {operation !== undefined && <form className="modal-card" onSubmit={handleSubmit}>

            <section className="modal-card-body modal-form">

              <div className="form-floating-header p-4">
                <span className="has-text-weight-bold is-size-6">Test a webhook endpoint</span>
              </div>
              <div className="p-3 my-4"></div>

              <p className="is-subtitle is-size-6 has-text-weight-bold has-text-grey my-2">
                {operation.webhook?.url}
              </p>

              <SelectField label="Notification Payload" onChange={handleChange} className="is-fullwidth">
                <option key="plain" value={PLAIN_EVENT}>plain event</option>

                {Object.entries(NOTIFICATION_SAMPLE).map(([key, value]) => (
                  <option key={key} value={value}>{key}</option>
                ))}
              </SelectField>

              <div className="card-content py-3 px-0">
                <pre className="code p-1" style={{ height: '30vh', maxHeight: '30vh' }}>
                  <code
                    dangerouslySetInnerHTML={{
                      __html: hljs.highlight(payload, { language: 'json' }).value,
                    }}
                  />
                </pre>
              </div>

              <div className="p-3 my-5"></div>
              <div className="form-floating-footer has-text-centered p-1">
                <button className="button is-default m-1 is-small" type="button" onClick={close} disabled={loading}>
                  <span>Cancel</span>
                </button>
                <button className={`button is-primary ${loading ? 'is-loading' : ''} m-1 is-small`}
                  disabled={loading}
                  type="submit">
                  <span>Test Notification</span>
                </button>
              </div>

            </section>
          </form>}
          <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>
        </div>
      </Notifier>

    </>
  );
};

export function useTestWebhookModal() {
  return useContext(WebhookTestModalContext);
}

export default WebhookTestModal;


function testPayloadSample() {
  return {
    "shipment purchased": JSON.stringify({
      event: "shipment.purchased",
      data: {
        "id": "shp_4998174814864a0690a1d0d626c101e1",
        "status": "purchased",
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "label": "JVBERiqrnC --- truncated base64 label ---",
        "tracking_number": "123456789012",
        "shipment_identifier": "123456789012",
        "selected_rate": {
          "id": "rat_fe4608bfc02445b387ada33e0da8d1f1",
          "carrier_name": "canadapost",
          "carrier_id": "canadapost",
          "currency": "CAD",
          "service": "canadapost_regular_parcel",
          "total_charge": 46.45,
          "transit_days": 10,
          "extra_charges": [
            {
              "name": "Fuel surcharge",
              "amount": 4.17,
              "currency": "CAD"
            },
            {
              "name": "SMB Savings",
              "amount": -2.95,
              "currency": "CAD"
            }
          ],
          "meta": null,
          "carrier_ref": "car_773f4a5577e4471e8918a9a1d47b208b",
          "test_mode": true
        },
        "selected_rate_id": "rat_fe4608bfc02445b387ada33e0da8d1f1",
        "rates": [
          {
            "id": "rat_fe4608bfc02445b387ada33e0da8d1f1",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "service": "canadapost_regular_parcel",
            "total_charge": 46.45,
            "transit_days": 10,
            "extra_charges": [
              {
                "name": "Fuel surcharge",
                "amount": 4.17,
                "currency": "CAD"
              },
              {
                "name": "SMB Savings",
                "amount": -2.95,
                "currency": "CAD"
              }
            ],
            "meta": null,
            "carrier_ref": "car_773f4a5577e4471e8918a9a1d47b208b",
            "test_mode": true
          }
        ],
        "tracking_url": "/v1/trackers/canadapost/123456789012?test",
        "service": "canadapost_priority",
        "shipper": {
          "id": "adr_ab7bf955708c4d82bfe314e56a00c12a",
          "postal_code": "V6M2V9",
          "city": "Vancouver",
          "person_name": "Jane Doe",
          "company_name": "B corp.",
          "country_code": "CA",
          "email": null,
          "phone_number": "+1 514-000-0000",
          "state_code": "BC",
          "residential": false,
          "address_line1": "5840 Oak St",
          "address_line2": null,
          "validate_location": false,
        },
        "recipient": {
          "id": "adr_b0abf7fc21534e6280ddbd4df33b2326",
          "postal_code": "E1C4Z8",
          "city": "Moncton",
          "person_name": "John Doe",
          "company_name": "A corp.",
          "country_code": "CA",
          "email": null,
          "phone_number": "+1 514-000-0000",
          "state_code": "NB",
          "residential": false,
          "address_line1": "125 Church St",
          "address_line2": null,
          "validate_location": false,
        },
        "parcels": [
          {
            "id": "pcl_eecb90bb2c9c4f18acdb1b5eab8ea22a",
            "weight": 1,
            "width": 46,
            "height": 46,
            "length": 40.6,
            "packaging_type": null,
            "package_preset": "canadapost_corrugated_large_box",
            "description": null,
            "content": null,
            "is_document": false,
            "weight_unit": "KG",
            "dimension_unit": "CM"
          }
        ],
        "services": [],
        "options": {},
        "payment": {
          "paid_by": "sender",
          "currency": "CAD",
          "account_number": null
        },
        "customs": null,
        "reference": null,
        "label_type": "PDF",
        "carrier_ids": [],
        "meta": {},
        "created_at": "2021-05-15 02:25:18.785392+00:00",
        "test_mode": true,
        "messages": []
      }
    }, null, 2)
  };
}
