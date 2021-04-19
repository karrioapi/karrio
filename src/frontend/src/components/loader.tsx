import React, { useState } from 'react';

interface LoadingNotifier {
    loading: boolean;
    setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

export const Loading = React.createContext<LoadingNotifier>({} as LoadingNotifier);

const Loader: React.FC = ({ children }) => {
    const [loading, setLoading] = useState<boolean>(false);

    return (
        <Loading.Provider value={{loading, setLoading}}>
            {loading && <progress className="progress is-primary purplship-loader" max="100">50%</progress>}
            {children}
        </Loading.Provider>
    )
};

export default Loader;