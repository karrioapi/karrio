import { ManifestFilter, GetManifests, GetManifest, GET_MANIFESTS, GET_MANIFEST } from "@karrio/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, handleFailure, insertUrlParam, onError } from "@karrio/lib";
import { ManifestData } from "@karrio/types/rest/api";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = ManifestFilter & { setVariablesToURL?: boolean, cacheKey?: string, isDisabled?: boolean; preloadNextPage?: boolean; };

export function useManifests({ setVariablesToURL = false, isDisabled = false, preloadNextPage = false, cacheKey, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<ManifestFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: ManifestFilter }) => karrio.graphql.request<GetManifests>(
    gqlstr(GET_MANIFESTS), { variables }
  );

  // Queries
  const query = useQuery({
    queryKey: [cacheKey || 'manifests', filter],
    queryFn: () => fetch({ filter }),
    enabled: !isDisabled,
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

  function setFilter(options: ManifestFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal", "tab"].includes(key)) return acc;
      if ((["carrier_name", "status", "service"].includes(key))) return ({
        ...acc,
        [key]: ([].concat(options[key as keyof ManifestFilter]).reduce(
          (acc, item: string) => (
            typeof item == 'string'
              ? [].concat(acc, item.split(',') as any)
              : [].concat(acc, item)
          ), []
        ))
      });
      if (["offset", "first"].includes(key)) return ({
        ...acc,
        [key]: parseInt(options[key as keyof ManifestFilter])
      });
      if (
        ["has_tracker", "has_manifest"].includes(key) ||
        ['true', 'false'].includes(options[key as keyof ManifestFilter])
      ) return ({
        ...acc,
        [key]: options[key as keyof ManifestFilter] === 'true'
      });

      return {
        ...acc,
        [key]: options[key as keyof ManifestFilter]
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (preloadNextPage === false) return;
    if (query.data?.manifests.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['manifests', _filter],
        () => fetch({ filter: _filter }),
      )
    }
  }, [query.data, filter.offset, queryClient])

  return {
    query,
    filter,
    setFilter,
  };
}

export function useManifest(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery({
    queryKey: ['manifests', id],
    queryFn: () => karrio.graphql.request<GetManifest>(gqlstr(GET_MANIFEST), { variables: { id } }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}

export function useManifestMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['shipments']);
  };

  // Mutations
  // REST requests
  const createManifest = useMutation(
    (data: ManifestData) => handleFailure(
      karrio.manifests.create({ manifestData: (data as any) }).then(({ data }) => data)
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createManifest,
  };
}
