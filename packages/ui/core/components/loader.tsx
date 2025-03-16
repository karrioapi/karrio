import React, { useState } from "react";

interface LoadingNotifier {
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

interface LoadingProviderComponent {
  children: React.ReactNode;
}

export const Loading = React.createContext<LoadingNotifier>(
  {} as LoadingNotifier,
);

export const LoadingProvider = ({
  children,
}: LoadingProviderComponent): JSX.Element => {
  const [loading, changeLoading] = useState<boolean>(false);

  const setLoading = (loading: boolean) =>
    setTimeout(
      () => {
        changeLoading(loading);
      },
      loading ? 0 : 2000,
    );

  return (
    <Loading.Provider value={{ loading, setLoading }}>
      {loading && (
        <progress className="progress is-primary karrio-loader" max="100">
          50%
        </progress>
      )}
      {children}
    </Loading.Provider>
  );
};

export function useLoader() {
  return React.useContext(Loading);
}
