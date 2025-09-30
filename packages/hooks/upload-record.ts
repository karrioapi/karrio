import {
  DocumentUploadData,
  DocumentsApiUploadsRequest,
} from "@karrio/types/rest/api";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import { handleFailure } from "@karrio/lib";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

export function useUploadRecords(params: DocumentsApiUploadsRequest = {}) {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<DocumentsApiUploadsRequest>({
    ...PAGINATION,
    ...params,
  });

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["upload_records"],
    queryFn: () => karrio.documents.uploads(filter).then(({ data }) => data),
    keepPreviousData: true,
    staleTime: 5000,
  });

  return {
    query,
    filter,
    setFilter,
  };
}

export function useUploadRecord(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["upload_records", id],
    queryFn: () => karrio.documents.retrieveUpload({ id }),
  });

  return {
    query,
  };
}

export function useUploadRecordMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(["upload_records"]);
  };

  // Mutations
  const uploadDocument = useMutation(
    (data: DocumentUploadData) =>
      handleFailure(karrio.documents.upload({ documentUploadData: data })),
    { onSuccess: invalidateCache },
  );

  return {
    uploadDocument,
  };
}
