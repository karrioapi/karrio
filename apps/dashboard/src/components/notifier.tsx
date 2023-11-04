import { FieldError, NotificationType, Notification, RequestError, ErrorType } from '@/lib/types';
import React, { useState } from 'react';

interface LoadingNotifier {
  notify: (notification: Notification) => void;
}

export const Notify = React.createContext<LoadingNotifier>({} as LoadingNotifier);

const Notifier: React.FC = ({ children }) => {
  const [notification, setNotification] = useState<Notification>();
  const [timer, setTimer] = useState<NodeJS.Timeout | number>();

  const dismiss = (evt?: React.MouseEvent) => {
    evt?.preventDefault();
    evt?.stopPropagation();
    setNotification(undefined);
    timer && clearTimeout(timer as NodeJS.Timeout);
  };
  const notify = (notification: Notification) => {
    dismiss();
    setNotification(notification);
    setTimer(setTimeout(() => { dismiss() }, 10000));
  };

  return (
    <Notify.Provider value={{ notify }}>
      {notification !== undefined &&
        <div className={`notification px-2 py-4 ${notification?.type || NotificationType.info} karrio-notifier is-size-6`}>
          <progress
            className={`progress karrio-notification-loader ${notification?.type || NotificationType.info}`}
            max="100">50%</progress>
          <button className="delete" onClick={dismiss}></button>
          {formatMessage(notification?.message || '')}
        </div>
      }
      {children}
    </Notify.Provider>
  )
};

export function formatMessage(msg: Notification['message']) {
  try {
    // Process plain text message
    if (typeof msg === 'string') {
      return msg;
    }

    // Process GraphQL errors
    if (Array.isArray(msg) && msg.length > 0 && msg[0] instanceof ErrorType) {
      return msg.map((error: any, index) => {
        return <p key={index}><strong>{error.field}:</strong> {error.messages.join(' | ')}</p>;
      });
    }

    // Process Rest Request errors
    if (Array.isArray(msg) && msg.length > 0) {
      return renderError(msg, 0);
    }

    // Process API errors
    if (msg instanceof RequestError) {
      return renderError(msg, 0);
    }

    return (msg as any).message;
  } catch (e) {
    console.log('Failed to parse error');
    console.error(e);
    return 'Uh Oh! An uncaught error occured...';
  }
};

function renderError(msg: any, _: number): any {
  const error = msg.data?.errors || msg.data?.messages || msg;
  if (error?.message !== undefined) {
    return error.message;
  }

  else if (error?.details?.messages !== undefined) {
    return (error.details.messages || []).map((msg: any, index: number) => {
      const carrier_name = msg.carrier_name !== undefined ? `${msg.carrier_id} :` : '';
      return <p key={index}>{carrier_name} {msg.message}</p>;
    });
  }

  else if (Array.isArray(error) && error.length > 0) {
    return (error || []).map((msg: any, index: number) => {
      if (msg.carrier_name) {
        return <p key={index}>{msg.carrier_name || msg.carrier_id || JSON.stringify(msg)} {msg.message}</p>;
      }
      if (msg.details) {
        return <>{renderError(msg, 0)}</>;
      }
      if (msg.validation) {
        return <>{renderError({ details: msg.validation }, 0)}</>;
      }
      if (msg.message) {
        return <p key={index}><strong>{JSON.stringify(msg.code)}:</strong> {msg.message}</p>;
      }
      return <p key={index}>{JSON.stringify(msg)}</p>;
    });
  }

  else if (typeof error?.details == 'object') {
    const render = ([field, msg]: [string, string | FieldError], index: number) => {
      let text = formatMessageObject(msg);
      return (<React.Fragment key={index}>
        <span className="is-size-7">
          {field} {formatMessageObject(msg).length > 0 && ` - ${text}`}
        </span>
        {!(msg as any).message && <ul className='pl-1'>
          <li className="is-size-7">
            {!Array.isArray(msg) && typeof msg === 'object' && !msg.message &&
              Object.entries(msg).map(render as any)}
          </li>
        </ul>}
        <br />
      </React.Fragment>);
    }
    return Object.entries(error?.details as FieldError).map(render as any);
  }

  return formatMessageObject(error);
}

function formatMessageObject(msg: any) {
  if (msg.message) return msg.message;
  if (typeof msg === 'string') return msg;
  if (Array.isArray(msg) && typeof msg[0] === 'string') return msg.join(' ');
  if (typeof msg === 'object') return "";
}

export function useNotifier() {
  return React.useContext(Notify);
}

export default Notifier;
