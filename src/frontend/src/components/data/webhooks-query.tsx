import React, { useContext, useState } from 'react';
import { WebhookList } from '@/api';
import { RestClient } from '@/library/rest';
import { RequestError } from '@/library/types';
import { getCursorPagination } from '@/library/helper';

const DEFAULT_PAGINATED_RESULT = { results: [] };


type ResultType = WebhookList & {
  error?: RequestError;
  called: boolean;
  loading: boolean;
  load: (options?: any) => void;
  loadMore: (cursor: string) => void;
  refetch: (options?: any) => void;
};
export const Webhooks = React.createContext<ResultType>({} as ResultType);

const WebhooksQuery: React.FC = ({ children }) => {
  const purplship = useContext(RestClient);
  const [result, setValue] = useState<WebhookList>(DEFAULT_PAGINATED_RESULT);
  const [error, setError] = useState<RequestError>();
  const [called, setCalled] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [cursor, setCursor] = useState<string>('');

  const loadMore = async (cursor?: string) => {
    setCursor(cursor || '');
    setLoading(true);

    return purplship
      .webhooks
      .list(getCursorPagination(cursor))
      .then(setValue)
      .catch(setError)
      .then(() => setLoading(false));
  };
  const load = async () => {
    setCalled(true);

    return loadMore();
  };
  const refetch = async () => loadMore(cursor);

  return (
    <Webhooks.Provider value={{
      load,
      loadMore,
      called,
      loading,
      error,
      refetch,
      ...result
    }}>
      {children}
    </Webhooks.Provider>
  );
};

export default WebhooksQuery;
