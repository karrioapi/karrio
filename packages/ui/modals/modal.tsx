import React, { useState } from 'react';


interface ModalComponent {
  trigger: JSX.Element;
  children?: React.ReactNode;
}
type ModalContextType = {
  open: (modal: JSX.Element, props?: CustomProps) => void;
  close: (event?: React.MouseEvent) => void;
};
export type ModalFormProps<T> = T & {
  trigger: React.ReactElement;
};
export type CustomProps = {
  backgroundDismiss?: boolean;
  addCloseButton?: boolean;
  addBackground?: boolean;
  className?: string;
  modalClassName?: string;
};

export const ModalContext = React.createContext<ModalContextType>({} as ModalContextType);

export const ModalProvider: React.FC<ModalComponent> = ({ children }) => {
  const [isActive, setIsActive] = useState(false);
  const [key, setKey] = useState<string>(`modal-${Date.now()}`);
  const [modal, setModal] = useState<JSX.Element | undefined>();
  const [props, setProps] = useState<CustomProps>({ addCloseButton: true, addBackground: true });

  const open = (modal: JSX.Element, props: CustomProps = {}) => {
    setModal(modal);
    setProps({ addCloseButton: true, addBackground: true, ...props });
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

        <div className={`modal ${props.modalClassName || ''} ${isActive ? "is-active" : ""}`} key={key}>
          {props.addBackground && <div className="modal-background" {...(props.backgroundDismiss ? { onClick: close } : {})}></div>}

          <div className={`modal-card ${props.className || ''}`}>

            {isActive && modal}

          </div>

          {props.addCloseButton && <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>}
        </div>

      </ModalContext.Provider>
    </>
  );
};

export function useModal() {
  return React.useContext(ModalContext);
}

