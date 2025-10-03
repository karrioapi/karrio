"use client";

import { BASE_PATH, TEST_BASE_PATH, setCookie } from "@karrio/lib";
import { usePathname } from "next/navigation";
import { useLocation } from "./location";
import React from "react";

type AppModeType = {
  basePath: string;
  testMode?: boolean;
  switchMode: () => void;
};

export function computeMode(pathname: string) {
  return pathname?.startsWith(TEST_BASE_PATH);
}

export function computeBasePath(testMode: boolean) {
  return testMode ? TEST_BASE_PATH : BASE_PATH;
}

// Init the APP client mode
export const AppMode = React.createContext<AppModeType>({} as AppModeType);

const AppModeProvider = ({
  children,
  pathname,
}: {
  pathname?: string;
  children?: React.ReactNode;
}): JSX.Element => {
  const currentPathName = usePathname();
  const { insertUrlParam } = useLocation();

  const switchMode = () => {
    insertUrlParam({});
    // const currentPathName = `${location.pathname}`;
    const isTestMode = computeMode(currentPathName);

    setCookie("testMode", !isTestMode);

    if (isTestMode)
      location.pathname = currentPathName.replace(TEST_BASE_PATH, "");
    else location.replace(TEST_BASE_PATH + currentPathName);
  };

  return (
    <AppMode.Provider
      value={{
        testMode: computeMode(pathname || currentPathName),
        basePath: computeBasePath(computeMode(pathname || currentPathName)),
        switchMode,
      }}
    >
      {children}
    </AppMode.Provider>
  );
};

export function useAppMode() {
  return React.useContext(AppMode);
}

export default AppModeProvider;
