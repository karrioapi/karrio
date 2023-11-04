import { DocumentTemplateFilter, CreateDocumentTemplateMutationInput, CREATE_DOCUMENT_TEMPLATE, DELETE_DOCUMENT_TEMPLATE, get_document_templates, GET_DOCUMENT_TEMPLATES, UpdateDocumentTemplateMutationInput, UPDATE_DOCUMENT_TEMPLATE, GET_DOCUMENT_TEMPLATE, get_document_template, create_document_template, update_document_template, delete_document_template } from "@karrio/graphql";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, onError } from "@/lib/helper";
import { useAPIMetadata } from "@/context/api-metadata";
import { useKarrio } from "@/lib/client";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

export function useDocumentTemplates(initialData: DocumentTemplateFilter = {}) {
  const karrio = useKarrio();
  const { metadata: { DOCUMENTS_MANAGEMENT } } = useAPIMetadata();
  const [filter, setFilter] = React.useState<DocumentTemplateFilter>({ ...PAGINATION, ...initialData });

  // Queries
  const query = useQuery({
    queryKey: ['document_templates', filter],
    queryFn: () => karrio.graphql$.request<get_document_templates>(
      gqlstr(GET_DOCUMENT_TEMPLATES), { variables: { filter } }
    ),
    enabled: DOCUMENTS_MANAGEMENT === true,
    keepPreviousData: true,
    staleTime: 5000,
    onError
  });

  return {
    query,
    filter,
    setFilter,
  };
}

type Args = { id?: string, setVariablesToURL?: boolean };

export function useDocumentTemplate({ id, setVariablesToURL = false }: Args = {}) {
  const karrio = useKarrio();
  const [docId, _setDocId] = React.useState<string>(id || 'new');

  // Queries
  const query = useQuery(['document_templates', docId], {
    queryFn: () => karrio.graphql$.request<get_document_template>(
      gqlstr(GET_DOCUMENT_TEMPLATE), { variables: { id: docId } }
    ),
    enabled: (docId !== 'new'),
    onError,
  });

  function setDocId(docId: string) {
    if (setVariablesToURL) insertUrlParam({ id: docId });
    _setDocId(docId);
  }

  return {
    query,
    docId,
    setDocId,
  };
}


export function useDocumentTemplateMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => { queryClient.invalidateQueries(['document_templates']) };

  // Mutations
  const createDocumentTemplate = useMutation(
    (data: CreateDocumentTemplateMutationInput) => karrio.graphql$.request<create_document_template>(
      gqlstr(CREATE_DOCUMENT_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateDocumentTemplate = useMutation(
    (data: UpdateDocumentTemplateMutationInput) => karrio.graphql$.request<update_document_template>(
      gqlstr(UPDATE_DOCUMENT_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteDocumentTemplate = useMutation(
    (data: { id: string }) => karrio.graphql$.request<delete_document_template>(
      gqlstr(DELETE_DOCUMENT_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createDocumentTemplate,
    updateDocumentTemplate,
    deleteDocumentTemplate,
  };
}
