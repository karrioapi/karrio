import { DocumentUploadData, DocumentsApiListRequest } from "@karrio/types/rest/api";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { handleFailure } from "@karrio/lib";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

export function useUploadRecords(params: DocumentsApiListRequest = {}) {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<DocumentsApiListRequest>({ ...PAGINATION, ...params });

  // Queries
  const query = useQuery(
    ['upload_records'],
    () => karrio.documents.list(filter).then(({ data }) => data),
    { keepPreviousData: true, staleTime: 5000 },
  );

  return {
    query,
    filter,
    setFilter,
  };
}

export function useUploadRecord(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery(
    ['upload_records', id],
    () => karrio.documents.retrieve({ id }),
  );

  return {
    query,
  };
}


export function useUploadRecordMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => { queryClient.invalidateQueries(['upload_records']) };

  // Mutations
  const uploadDocument = useMutation(
    (data: DocumentUploadData) => handleFailure(
      karrio.documents.upload({ documentUploadData: data })
    ),
    { onSuccess: invalidateCache }
  );

  return {
    uploadDocument,
  };
}
