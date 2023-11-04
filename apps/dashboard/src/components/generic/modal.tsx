import React, { useState } from 'react';


interface ModalComponent {
  trigger: JSX.Element;
}
type ModalContextType = {
  open: (modal: JSX.Element) => void;
  close: (event?: React.MouseEvent) => void;
};
export type ModalFormProps<T> = T & {
  trigger: React.ReactElement;
};

const ModalContext = React.createContext<ModalContextType>({} as ModalContextType);

const ModalProvider: React.FC<ModalComponent> = ({ children }) => {
  const [isActive, setIsActive] = useState(false);
  const [key, setKey] = useState<string>(`modal-${Date.now()}`);
  const [modal, setModal] = useState<JSX.Element | undefined>();

  const open = (modal: JSX.Element) => {
    setModal(modal);
    setIsActive(true);
    setKey(`modal-${Date.now()}`);
  };
  const close = (_?: React.MouseEvent) => {
    setIsActive(false);
    setKey(`modal-${Date.now()}`);
  };

  return (
    <>
      <ModalContext.Provider value={{ open, close }}>
        {children}

        <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
          <div className="modal-background"></div>
          <div className="modal-card">

            {isActive && modal}

          </div>

          <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>
        </div>

      </ModalContext.Provider>
    </>
  );
};

export function useModal() {
  return React.useContext(ModalContext);
}


export default ModalProvider;
