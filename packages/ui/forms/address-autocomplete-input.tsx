import { initDebouncedPrediction, QueryAutocompletePrediction } from '@karrio/lib/autocomplete';
import React, { ChangeEvent, useCallback, useEffect, useRef, useState } from 'react';
import { InputFieldComponent } from '../components/input-field';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { Address } from '@karrio/types/rest/api';
import { Subject } from 'rxjs/internal/Subject';
import { isNone } from '@karrio/lib';

interface AddressAutocompleteInputComponent extends InputFieldComponent {
  onValueChange: (value: Partial<Address>) => void;
  defaultValue?: string;
  disableSuggestion?: boolean;
  country_code?: string;
  dropdownClass?: string;
  wrapperClass?: string;
}

export const AddressAutocompleteInput: React.FC<AddressAutocompleteInputComponent> = ({ onValueChange, country_code, label, required, dropdownClass, className, fieldClass, controlClass, wrapperClass, name, children, ...props }) => {
  const Props = {
    required,
    ...props,
    ...(Object.keys(props).includes('value') ? { value: props.value || "" } : {}),
  };
  const { references: { ADDRESS_AUTO_COMPLETE } } = useAPIMetadata();
  const container = useRef<HTMLDivElement | null>(null);
  const [key] = useState<string>(`predictions_${Date.now()}`);
  const [isActive, setIsActive] = useState<boolean>(false);
  const [predictions, setPredictions] = useState<QueryAutocompletePrediction[]>([]);
  const [predictor, initPredictor] = useState<ReturnType<typeof initDebouncedPrediction> | undefined>();

  const updater: Subject<Partial<Address>> = new Subject();
  updater.subscribe(address => onValueChange(address));

  const onChange = (e: ChangeEvent<any>) => {
    e.preventDefault();
    const inputValue: string = e.target.value || "";
    if (inputValue.length > 3) {
      predictor?.getPlacePredictions({ input: inputValue, country_code }, predictions => setPredictions(predictions));
    }
    updater.next({ address_line1: inputValue });
  };
  const onSelect = (prediction: QueryAutocompletePrediction) => {
    predictor?.formatPrediction(prediction, address => {
      updater.next(address);
      setIsActive(false);
    });
  };
  const onBodyClick = useCallback((e: MouseEvent) => {
    if (container.current !== null && !container.current.contains(e.target as Element)) {
      setIsActive(false);
      document.removeEventListener('click', onBodyClick);
    }
  }, [container]);

  useEffect(() => {
    if (
      ADDRESS_AUTO_COMPLETE && (
        (ADDRESS_AUTO_COMPLETE.provider !== 'google') ||
        (ADDRESS_AUTO_COMPLETE.provider === 'google' && !isNone((window as any).google))
      )) {
      initPredictor(initDebouncedPrediction(ADDRESS_AUTO_COMPLETE));
    }
  }, [ADDRESS_AUTO_COMPLETE]);
  useEffect(() => {
    if (isActive) document.addEventListener('click', onBodyClick);
  }, [isActive, onBodyClick]);
  useEffect(() => { setIsActive(!!predictions.length); }, [predictions]);

  const content = (_: any) => (
    <div className={wrapperClass || ""}>
      {label !== undefined && <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
        {label}
        {required && <span className="icon is-small has-text-danger small-icon">
          <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
        </span>}
      </label>}

      <div className={`field ${fieldClass}`} key={key} ref={container}>

        <div className={`control ${controlClass}`}>
          <div className={`dropdown input is-fullwidth p-0 ${isActive ? 'is-active' : ''} ${dropdownClass}`}
            style={{ border: 'none' }}
            key={`dropdown-input-${key}`}>
            <input
              name={name}
              onChange={e => updater.next({ address_line1: e.target.value || "" })}
              style={{ position: 'absolute', right: 0, zIndex: -1 }}
              tabIndex={-1}
            />
            <input
              name={name}
              onChange={onChange}
              className={`input is-fullwidth ${className || ''}`}
              style={{ height: '100%' }}
              {...(ADDRESS_AUTO_COMPLETE?.is_enabled ? { autoComplete: key } : {})}
              {...Props}
            />
            <div className="dropdown-menu py-0" id={`dropdown-input-${key}`} role="menu" style={{ right: 0, left: 0 }}>
              <div className="dropdown-content is-menu py-0">
                <nav className="panel dropped-panel">
                  {(predictions || [])
                    .map((prediction) => (
                      <a key={`${prediction.id}-${Date.now()}`}
                        onClick={() => onSelect(prediction)}
                        className={`panel-block`}>
                        <span>{prediction.description}</span>
                      </a>
                    ))
                  }
                </nav>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );

  return <>{content(predictions)}</>;
};
