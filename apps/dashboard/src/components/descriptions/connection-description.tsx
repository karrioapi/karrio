import { SystemConnectionType } from '@/context/system-connection';
import CopiableLink from '@/components/copiable-link';
import React from 'react';

interface ConnectionDescriptionComponent {
  connection: SystemConnectionType;
}

const CAPABILITY_DETAILS: any = {
  "pickup": "Use this account to schedule package pickups",
  "rating": "Use this account to get negotiated rates",
  "shipping": "Use this account to buy shipping labels",
  "tracking": "Use this account to track shipments",
};

const ConnectionDescription: React.FC<ConnectionDescriptionComponent> = ({ connection }) => {
  const [key] = React.useState<string>(`description-${connection.id}-${Date.now()}`);

  return (
    <div className="content is-small" key={key}>
      <ul>
        <li key={`carrier_id-${key}`}>
          <span className="is-size-7 my-1 has-text-weight-semibold">
            carrier id: <CopiableLink className="button is-white is-small" text={connection.carrier_id} />
          </span>
        </li>

        {(connection?.capabilities || []).map((capability: any, index: number) => {
          if (capability in CAPABILITY_DETAILS) {
            return (
              <li key={`${index}-${key}`}>
                <span className="is-size-7 my-1 has-text-weight-semibold">{CAPABILITY_DETAILS[capability]}</span>
              </li>
            );
          }
          return <React.Fragment key={`${index}-${key}`}></React.Fragment>;
        })}

      </ul>
    </div>
  );
};

export default ConnectionDescription;
