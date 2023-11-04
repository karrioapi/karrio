import { BASE_PATH, TEST_BASE_PATH } from "@/lib/client";
import { setCookie, useLocation } from "@/lib/helper";
import React from "react";


type AppModeType = {
  basePath: string;
  testMode?: boolean;
  switchMode: () => void;
};

export function computeMode(pathname: string) {
  return pathname?.startsWith(TEST_BASE_PATH);
};

export function computeBasePath(testMode: boolean) {
  return testMode ? TEST_BASE_PATH : BASE_PATH;
};

// Init the APP client mode
export const AppMode = React.createContext<AppModeType>({} as AppModeType);

const AppModeProvider: React.FC<{ pathname?: string }> = ({ children, pathname }) => {
  const { insertUrlParam } = useLocation();

  const switchMode = () => {
    insertUrlParam({});
    const currentPathName = `${window.location.pathname}`;
    const isTestMode = computeMode(currentPathName);

    setCookie("testMode", !isTestMode);

    if (isTestMode) window.location.pathname = currentPathName.replace(TEST_BASE_PATH, '');
    else window.location.replace(TEST_BASE_PATH + currentPathName);
  };

  return (
    <AppMode.Provider value={{
      testMode: computeMode(pathname || window.location.pathname),
      basePath: computeBasePath(computeMode(pathname || window.location.pathname)),
      switchMode
    }}>
      {children}
    </AppMode.Provider>
  );
};

export function useAppMode() {
  return React.useContext(AppMode);
}

export default AppModeProvider;
