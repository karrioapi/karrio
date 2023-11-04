import React, { useState } from 'react';

interface LoadingNotifier {
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

export const Loading = React.createContext<LoadingNotifier>({} as LoadingNotifier);

const LoadingProvider: React.FC = ({ children }) => {
  const [loading, changeLoading] = useState<boolean>(false);

  const setLoading = (loading: boolean) => setTimeout(
    () => { changeLoading(loading); },
    loading ? 0 : 2000
  );

  return (
    <Loading.Provider value={{ loading, setLoading }}>
      {loading && <progress className="progress is-primary karrio-loader" max="100">50%</progress>}
      {children}
    </Loading.Provider>
  )
};

export function useLoader() {
  return React.useContext(Loading);
}

export default LoadingProvider;
