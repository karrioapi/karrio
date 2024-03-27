import { AppFilter, GetApps, GET_APPS, GetApp, GET_APP, CreateApp, UpdateApp, UpdateAppMutationInput, CreateAppMutationInput, DELETE_APP, UPDATE_APP, CREATE_APP, DeleteMutationInput, GetApps_apps_edges_node, InstallAppMutationInput, InstallApp, INSTALL_APP, UninstallAppMutationInput, UninstallApp, UNINSTALL_APP, GET_PRIVATE_APPS, GET_PRIVATE_APP, GetPrivateApps, GetPrivateApp, AppInstallationFilter, GET_INSTALLATIONS, GetInstallations, GetInstallations_installations_edges_node_app } from "@karrio/types/graphql";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNotifier } from "@karrio/ui/components/notifier";
import { useLoader } from "@karrio/ui/components/loader";
import { NotificationType } from '@karrio/types';
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = AppFilter & { setVariablesToURL?: boolean };
type InstallationFilterType = AppInstallationFilter & { setVariablesToURL?: boolean };

export type AppType = GetApps_apps_edges_node | GetInstallations_installations_edges_node_app;

export function useApps({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<AppFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: AppFilter }) => karrio.graphql.request<GetApps>(
    gqlstr(GET_APPS), { variables }
  );

  // Queries
  const query = useQuery(
    ['apps', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, refetchInterval: 120000, onError },
  );

  function setFilter(options: AppFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof AppFilter]) ? acc : {
        ...acc,
        [key]: (["offset", "first"].includes(key)
          ? parseInt((options as any)[key])
          : options[key as keyof AppFilter]
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.apps.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['apps', _filter],
        () => fetch({ filter: _filter }),
      )
    }
  }, [query.data, filter.offset, queryClient])

  return {
    query,
    get filter() { return filter; },
    setFilter,
  };
}

export function useApp({ id, setVariablesToURL = false }: { id?: string, setVariablesToURL?: boolean } = {}) {
  const karrio = useKarrio();
  const [appId, _setAppId] = React.useState<string>(id || 'new');

  // Queries
  const query = useQuery(['apps', id], {
    queryFn: () => karrio.graphql.request<GetApp>(gqlstr(GET_APP), { variables: { id: appId } }),
    enabled: (appId !== 'new'),
    onError,
  });

  function setAppId(appId: string) {
    if (setVariablesToURL) insertUrlParam({ id: appId });
    _setAppId(appId);
  }

  return {
    query,
    appId,
    setAppId,
  };
}

export function usePrivateApps({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<AppFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: AppFilter }) => karrio.graphql.request<GetPrivateApps>(
    gqlstr(GET_PRIVATE_APPS), { variables }
  );

  // Queries
  const query = useQuery(
    ['private-apps', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, refetchInterval: 120000, onError },
  );

  function setFilter(options: AppFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof AppFilter]) ? acc : {
        ...acc,
        [key]: (["offset", "first"].includes(key)
          ? parseInt((options as any)[key])
          : options[key as keyof AppFilter]
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.private_apps.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['private-apps', _filter],
        () => fetch({ filter: _filter }),
      )
    }
  }, [query.data, filter.offset, queryClient])

  return {
    query,
    get filter() { return filter; },
    setFilter,
  };
}

export function usePrivateApp({ id, setVariablesToURL = false }: { id?: string, setVariablesToURL?: boolean } = {}) {
  const karrio = useKarrio();
  const [appId, _setAppId] = React.useState<string>(id || 'new');

  // Queries
  const query = useQuery(['private-apps', id], {
    queryFn: () => karrio.graphql.request<GetPrivateApp>(gqlstr(GET_PRIVATE_APP), { variables: { id: appId } }),
    enabled: (appId !== 'new'),
    onError,
  });

  function setAppId(appId: string) {
    if (setVariablesToURL) insertUrlParam({ id: appId });
    _setAppId(appId);
  }

  return {
    query,
    appId,
    setAppId,
  };
}

export function useInstallations({ setVariablesToURL = false, ...initialData }: InstallationFilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<AppInstallationFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: AppInstallationFilter }) => karrio.graphql.request<GetInstallations>(
    gqlstr(GET_INSTALLATIONS), { variables }
  );

  // Queries
  const query = useQuery(
    ['app-installations', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, refetchInterval: 120000, onError },
  );

  function setFilter(options: AppInstallationFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal", "tab"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof AppInstallationFilter]) ? acc : {
        ...acc,
        [key]: (["offset", "first"].includes(key)
          ? parseInt((options as any)[key])
          : options[key as keyof AppInstallationFilter]
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.installations.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['japp-installations', _filter],
        () => fetch({ filter: _filter }),
      )
    }
  }, [query.data, filter.offset, queryClient])

  return {
    query,
    get filter() { return filter; },
    setFilter,
  };
}

export function useAppMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => { queryClient.invalidateQueries(['apps']) };

  // Mutations
  const createApp = useMutation(
    (data: CreateAppMutationInput) => karrio.graphql.request<CreateApp>(
      gqlstr(CREATE_APP), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateApp = useMutation(
    (data: UpdateAppMutationInput) => karrio.graphql.request<UpdateApp>(
      gqlstr(UPDATE_APP), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteApp = useMutation(
    (data: { id: string }) => karrio.graphql.request<DeleteMutationInput>(
      gqlstr(DELETE_APP), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const installApp = useMutation(
    (data: InstallAppMutationInput) => karrio.graphql.request<InstallApp>(
      gqlstr(INSTALL_APP), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const uninstallApp = useMutation(
    (data: UninstallAppMutationInput) => karrio.graphql.request<UninstallApp>(
      gqlstr(UNINSTALL_APP), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createApp,
    updateApp,
    deleteApp,
    installApp,
    uninstallApp,
  };
}

type AppDataType = UpdateAppMutationInput & {
  id?: string,
};

const DEFAULT_STATE = {} as AppDataType;
type ChangeType = {
  deleted?: boolean,
  created?: boolean,
  manuallyUpdated?: boolean,
  forcelocalUpdate?: boolean,
};

function reducer(state: Partial<AppDataType>, { name, value }: { name: string, value: Partial<AppDataType> }): AppDataType {
  switch (name) {
    case 'full':
      return { ...(value as AppDataType) };
    default:
      let newState = { ...state, ...(value as Partial<AppDataType>) } as AppDataType;
      Object.entries(value).forEach(([key, val]) => {
        if (val === undefined) delete newState[key as keyof AppDataType];
      });
      return { ...state, ...(newState as AppDataType) };
  }
}

export function useAppForm({ id }: { id?: string } = {}) {
  const loader = useLoader();
  const notifier = useNotifier();
  const mutation = useAppMutation();
  const [isNew, setIsNew] = React.useState<boolean>();
  const [app, dispatch] = React.useReducer(reducer, DEFAULT_STATE, () => DEFAULT_STATE);
  const { query: { data: { app: current } = {}, ...appQuery } } = useApp({ id });

  // state checks
  const isLocalDraft = (id?: string) => isNoneOrEmpty(id) || id === 'new';

  // Queries
  const query = useQuery({
    queryKey: ['app-data', id],
    queryFn: () => (id === 'new' ? { app } : current),
    enabled: (
      !!id && (id === 'new' || appQuery.isFetched)
    ),
  });

  // mutations
  const updateApp = async (changes: Partial<AppDataType>, change: ChangeType = { manuallyUpdated: false, forcelocalUpdate: false }) => {
    const updateLocalState = (
      change.forcelocalUpdate ||
      // always update local state if it is a new draft
      isLocalDraft(app.id) ||
      // only update local state first if it is not a draft and no new object is created or deleted.
      (!isLocalDraft(app.id) && !change.created && !change.deleted && !change.manuallyUpdated)
    );
    const uptateServerState = (
      !isLocalDraft(app.id) && !!change.deleted
    );

    if (updateLocalState) {
      dispatch({ name: "partial", value: { ...app, ...changes } });
    }

    // if it is not a draft and hasn't been manually updated already
    if (uptateServerState) {
      try {
        let { ...data } = changes;
        if (Object.keys(data).length === 0) return; // abort if no data changes
        await mutation.updateApp.mutateAsync({ id: app.id, ...data } as any)
          .then(({ update_app: { app } }) => {
            if (change.deleted && app) {
              dispatch({ name: "partial", value: changes });
            }
          });
      } catch (error: any) {
        notifier.notify({ type: NotificationType.error, message: error });
      }
    }
  };

  // requests
  const save = async () => {
    const { id, ...data } = app;

    try {
      loader.setLoading(true);
      if (isLocalDraft(id)) {
        const { create_app: { app } } = await mutation.createApp.mutateAsync(data as CreateAppMutationInput)
        notifier.notify({ type: NotificationType.success, message: 'App saved!' });
      } else {
        await mutation.updateApp.mutateAsync({ id, ...data } as UpdateAppMutationInput)
        notifier.notify({ type: NotificationType.success, message: 'App saved!' });
      }
    } catch (error: any) {
      notifier.notify({ type: NotificationType.error, message: error });
      loader.setLoading(false);
    }
  };

  React.useEffect(() => { setIsNew(id === 'new'); }, [id]);

  return {
    app,
    save,
    query,
    isNew,
    current,
    updateApp,
    DEFAULT_STATE,
  }
}
