import {
  ProductFilter,
  CreateProductInput,
  create_product,
  CREATE_PRODUCT,
  delete_product,
  DELETE_PRODUCT,
  get_products,
  GET_PRODUCTS,
  UpdateProductInput,
  update_product,
  UPDATE_PRODUCT,
} from "@karrio/types";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import { gqlstr, insertUrlParam, isNoneOrEmpty } from "@karrio/lib";
import { useQueryClient } from "@tanstack/react-query";
import React from "react";

const PAGE_SIZE = 25;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = ProductFilter & {
  setVariablesToURL?: boolean;
  isDisabled?: boolean;
  preloadNextPage?: boolean;
};

export function useProducts({
  setVariablesToURL = false,
  isDisabled = false,
  preloadNextPage = false,
  ...initialData
}: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<ProductFilter>({
    ...PAGINATION,
    ...initialData,
  });
  const fetch = (variables: { filter: ProductFilter }) =>
    karrio.graphql.request<get_products>(
      gqlstr(GET_PRODUCTS),
      { variables }
    );

  const query = useAuthenticatedQuery({
    queryKey: ["products", filter],
    queryFn: () => fetch({ filter }),
    enabled: !isDisabled,
    keepPreviousData: true,
    staleTime: 5000,
  });

  function setFilter(options: ProductFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof ProductFilter])
        ? acc
        : {
            ...acc,
            [key]:
              ["offset", "first"].includes(key)
                ? parseInt(options[key as keyof ProductFilter] as any)
                : options[key as keyof ProductFilter],
          };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (preloadNextPage === false) return;
    if (query.data?.products.page_info.has_next_page) {
      const _filter = { ...filter, offset: (filter.offset as number) + 20 };
      queryClient.prefetchQuery(["products", _filter], () =>
        fetch({ filter: _filter })
      );
    }
  }, [query.data, filter.offset, queryClient]);

  return {
    query,
    filter,
    setFilter,
  };
}

export function useProductMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ["products"] });
    queryClient.invalidateQueries({ queryKey: ["default_templates"] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ["products"] });
  };

  const createProduct = useAuthenticatedMutation({
    mutationFn: (data: CreateProductInput) =>
      karrio.graphql.request<create_product>(
        gqlstr(CREATE_PRODUCT),
        { data }
      ),
    onSuccess: invalidateCache,
  });

  const updateProduct = useAuthenticatedMutation({
    mutationFn: (data: UpdateProductInput) =>
      karrio.graphql.request<update_product>(
        gqlstr(UPDATE_PRODUCT),
        { data }
      ),
    onSuccess: invalidateCache,
  });

  const deleteProduct = useAuthenticatedMutation({
    mutationFn: (data: { id: string }) =>
      karrio.graphql.request<delete_product>(
        gqlstr(DELETE_PRODUCT),
        { data }
      ),
    onSuccess: invalidateCache,
  });

  return {
    createProduct,
    updateProduct,
    deleteProduct,
  };
}
