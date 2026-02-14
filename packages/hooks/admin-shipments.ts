"use client";

import { useAuthenticatedQuery } from "@karrio/hooks/karrio";
import { useKarrio } from "@karrio/hooks/karrio";
import { gqlstr } from "@karrio/lib";
import {
  GET_SYSTEM_SHIPMENTS,
  GET_SYSTEM_TRACKERS,
} from "@karrio/types/graphql/admin/queries";
import {
  GetSystemTrackers,
  GetSystemShipments,
} from "@karrio/types/graphql/admin";
import {
  GET_ACCOUNT_CARRIER_CONNECTIONS,
} from "@karrio/types/graphql/admin-ee/queries";
import {
  GetAccountCarrierConnections,
} from "@karrio/types/graphql/admin-ee";
import { TrackingEventType } from "@karrio/types/base";
import React from "react";

// Extended types for better type safety
export interface SystemTrackerNode {
  id: string;
  tracking_number: string;
  carrier_name: string;
  status: string;
  created_at: string;
  updated_at: string;
  events?: TrackingEventType[];
  meta?: {
    carrier?: string;
    [key: string]: any;
  };
  info?: {
    shipment_service?: string;
    [key: string]: any;
  };
  shipment?: {
    service?: string;
    meta?: {
      service_name?: string;
      [key: string]: any;
    };
    [key: string]: any;
  };
}

interface UseSystemShipmentsOptions {
  accountId: string;
  dateAfter?: string;
  dateBefore?: string;
  offset?: number;
  first?: number;
  enabled?: boolean;
}

export function useSystemShipments({
  accountId,
  dateAfter,
  dateBefore,
  offset = 0,
  first = 20,
  enabled = true,
}: UseSystemShipmentsOptions) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_system_shipments', accountId, dateAfter, dateBefore, offset, first],
    queryFn: () => karrio.admin.request<GetSystemShipments>(
      gqlstr(GET_SYSTEM_SHIPMENTS),
      {
        variables: {
          filter: {
            account_id: accountId,
            created_after: dateAfter,
            created_before: dateBefore,
            offset,
            first,
          }
        }
      }
    ),
    staleTime: 5000,
    enabled: !!accountId && enabled,
  });

  return {
    query,
    shipments: query.data?.shipments,
  };
}

interface UseSystemTrackersOptions {
  accountId: string;
  dateAfter?: string;
  dateBefore?: string;
  offset?: number;
  first?: number;
  enabled?: boolean;
}

export function useSystemTrackers({
  accountId,
  dateAfter,
  dateBefore,
  offset = 0,
  first = 20,
  enabled = true,
}: UseSystemTrackersOptions) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_system_trackers', accountId, dateAfter, dateBefore, offset, first],
    queryFn: () => karrio.admin.request<GetSystemTrackers>(
      gqlstr(GET_SYSTEM_TRACKERS),
      {
        variables: {
          filter: {
            account_id: accountId,
            created_after: dateAfter,
            created_before: dateBefore,
            offset,
            first,
          }
        }
      }
    ),
    staleTime: 5000,
    enabled: !!accountId && enabled,
  });

  return {
    query,
    trackers: query.data?.trackers,
  };
}

// Date range utilities
export interface UsageFilter {
  id: string;
  date_after: string;
  date_before: string;
}

export function useDateRangeFilter(accountId: string) {
  const getUsageFilter = React.useCallback((dateRange: string): UsageFilter => {
    const now = new Date();
    const startDate = new Date();

    switch (dateRange) {
      case "7d":
        startDate.setDate(now.getDate() - 7);
        break;
      case "30d":
        startDate.setDate(now.getDate() - 30);
        break;
      case "90d":
        startDate.setDate(now.getDate() - 90);
        break;
      case "1y":
        startDate.setFullYear(now.getFullYear() - 1);
        break;
      default:
        startDate.setDate(now.getDate() - 30);
    }

    return {
      id: accountId,
      date_after: startDate.toISOString(),
      date_before: now.toISOString()
    };
  }, [accountId]);

  return { getUsageFilter };
}

// Carrier connections hook
interface UseAccountCarrierConnectionsOptions {
  accountId: string;
  usageFilter: UsageFilter;
  enabled?: boolean;
}

export function useAccountCarrierConnections({
  accountId,
  usageFilter,
  enabled = true,
}: UseAccountCarrierConnectionsOptions) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_account_carrier_connections', accountId, usageFilter.date_after, usageFilter.date_before],
    queryFn: () => karrio.admin.request<GetAccountCarrierConnections>(
      gqlstr(GET_ACCOUNT_CARRIER_CONNECTIONS),
      {
        variables: {
          filter: { account_id: accountId },
          usageFilter: {
            date_after: usageFilter.date_after,
            date_before: usageFilter.date_before,
          }
        }
      }
    ),
    staleTime: 5000,
    enabled: !!accountId && enabled,
  });

  const carrierConnections = query.data?.carrier_connections?.edges || [];

  // Filter carriers based on search and filter
  const useFilteredCarriers = React.useCallback((search: string, filter: string) => {
    return carrierConnections.filter(({ node: carrier }) => {
      // Search filter
      const searchMatch = search === "" ||
        carrier.carrier_name.toLowerCase().includes(search.toLowerCase()) ||
        carrier.display_name?.toLowerCase().includes(search.toLowerCase()) ||
        carrier.carrier_id.toLowerCase().includes(search.toLowerCase());

      // Status filter
      const statusMatch = filter === "all" ||
        (filter === "active" && carrier.active) ||
        (filter === "inactive" && !carrier.active);

      return searchMatch && statusMatch;
    });
  }, [carrierConnections]);

  return {
    query,
    carrierConnections,
    useFilteredCarriers,
  };
}

// Pagination utilities
export interface PaginationState {
  page: number;
  pageSize: number;
  offset: number;
}

export function usePagination(initialPage = 1, pageSize = 20) {
  const [page, setPage] = React.useState(initialPage);

  const offset = (page - 1) * pageSize;

  const paginationState: PaginationState = {
    page,
    pageSize,
    offset,
  };

  const getPaginationRange = React.useCallback((totalItems: number) => {
    const start = offset + 1;
    const end = Math.min(offset + pageSize, totalItems);
    return { start, end };
  }, [offset, pageSize]);

  const canGoPrevious = page > 1;
  const canGoNext = (totalItems: number) => offset + pageSize < totalItems;

  const goToNextPage = React.useCallback(() => {
    setPage(prev => prev + 1);
  }, []);

  const goToPreviousPage = React.useCallback(() => {
    setPage(prev => Math.max(prev - 1, 1));
  }, []);

  const resetToFirstPage = React.useCallback(() => {
    setPage(1);
  }, []);

  return {
    paginationState,
    setPage,
    getPaginationRange,
    canGoPrevious,
    canGoNext,
    goToNextPage,
    goToPreviousPage,
    resetToFirstPage,
  };
}
