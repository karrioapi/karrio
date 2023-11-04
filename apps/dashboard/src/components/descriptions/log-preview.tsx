import { LogComponent } from '@/modules/Developers/log';
import { useLocation } from '@/lib/helper';
import React, { useState } from 'react';

type LogPreviewContextType = {
  previewLog: (logId: string) => void,
};

interface LogPreviewComponent { }

export const LogPreviewContext = React.createContext<LogPreviewContextType>({} as LogPreviewContextType);

const LogPreview: React.FC<LogPreviewComponent> = ({ children }) => {
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`log-${Date.now()}`);
  const [logId, setLogId] = useState<string>();

  const previewLog = (logId: string) => {
    setLogId(logId);
    setIsActive(true);
    setKey(`log-${Date.now()}`);
    addUrlParam('modal', logId);
  };
  const dismiss = (_?: React.MouseEvent) => {
    setLogId(undefined);
    setIsActive(false);
    setKey(`log-${Date.now()}`);
    removeUrlParam('modal');
  };

  return (
    <>
      <LogPreviewContext.Provider value={{ previewLog }}>
        {children}
      </LogPreviewContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background" onClick={dismiss}></div>

        {isActive && <div className="modal-card is-medium-modal">
          <section className="modal-card-body px-5 pt-0 pb-6">
            <LogComponent logId={logId} />
          </section>
        </div>}

        <button className="modal-close is-large has-background-dark" aria-label="close" onClick={dismiss}></button>

      </div>
    </>
  )
};

export default LogPreview;
