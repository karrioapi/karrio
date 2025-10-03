import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import { useKarrioAPI } from './use-karrio-api';

// GraphQL query for fetching shipments
const GET_SHIPMENTS = `
  query get_shipments($filter: ShipmentFilter) {
    shipments(filter: $filter) {
      page_info {
        count
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
      edges {
        node {
          id
          carrier_id
          carrier_name
          created_at
          updated_at
          status
          recipient {
            postal_code
            city
            person_name
            company_name
            country_code
          }
          shipper {
            postal_code
            city
            person_name
            company_name
            country_code
          }
          tracking_number
          shipment_identifier
          label_url
          tracking_url
          service
          reference
          selected_rate {
            id
            carrier_name
            carrier_id
            currency
            service
            transit_days
            total_charge
          }
          test_mode
        }
      }
    }
  }
`;

const GET_SHIPMENT = `
  query get_shipment($id: String!) {
    shipment(id: $id) {
      id
      carrier_id
      carrier_name
      created_at
      updated_at
      status
      recipient {
        id
        postal_code
        city
        person_name
        company_name
        country_code
        email
        phone_number
        state_code
        address_line1
        address_line2
      }
      shipper {
        id
        postal_code
        city
        person_name
        company_name
        country_code
        email
        phone_number
        state_code
        address_line1
        address_line2
      }
      parcels {
        id
        width
        height
        length
        dimension_unit
        weight
        weight_unit
        packaging_type
        items {
          id
          weight
          title
          description
          quantity
          value_amount
        }
      }
      tracking_number
      shipment_identifier
      label_url
      tracking_url
      service
      reference
      selected_rate {
        id
        carrier_name
        carrier_id
        currency
        service
        transit_days
        total_charge
      }
      rates {
        id
        carrier_name
        carrier_id
        currency
        service
        transit_days
        total_charge
      }
      test_mode
    }
  }
`;

// Default pagination settings
const DEFAULT_PAGINATION = {
  first: 20,
  offset: 0,
};

// Types for the filter parameters
export type ShipmentStatus =
  | 'draft'
  | 'purchased'
  | 'cancelled'
  | 'shipped'
  | 'in_transit'
  | 'delivered'
  | 'needs_attention'
  | 'out_for_delivery'
  | 'delivery_failed';

export interface ShipmentFilter {
  first?: number;
  offset?: number;
  carrier_name?: string | string[];
  status?: ShipmentStatus | ShipmentStatus[];
  service?: string | string[];
  tracking_number?: string;
  reference?: string;
  recipient_name?: string;
  created_after?: string;
  created_before?: string;
  search?: string;
}

// Hook for fetching shipments list with filters and pagination
export function useShipments({
  enabled = true,
  preloadNextPage = false,
  ...initialFilter
}: {
  enabled?: boolean;
  preloadNextPage?: boolean;
} & ShipmentFilter = {}) {
  const api = useKarrioAPI();
  const queryClient = useQueryClient();
  const [filter, setFilterState] = useState<ShipmentFilter>({
    ...DEFAULT_PAGINATION,
    ...initialFilter
  });

  // Normalize filter values for arrays (e.g., status, carrier_name)
  const normalizeFilterValue = (value: any): any => {
    if (Array.isArray(value)) {
      return value;
    } else if (typeof value === 'string' && value.includes(',')) {
      return value.split(',');
    }
    return value;
  };

  // Update filter state with normalized values
  const setFilter = (newFilter: Partial<ShipmentFilter>) => {
    const normalizedFilter = Object.entries(newFilter).reduce(
      (acc, [key, value]) => ({
        ...acc,
        [key]: normalizeFilterValue(value),
      }),
      {} as ShipmentFilter
    );

    setFilterState(prev => ({
      ...prev,
      ...normalizedFilter,
    }));

    return normalizedFilter;
  };

  // Query for fetching shipments
  const query = useQuery({
    queryKey: ['shipments', filter],
    queryFn: async () => {
      try {
        const response = await api.graphql({
          query: GET_SHIPMENTS,
          variables: { filter },
        });
        return response.data;
      } catch (error) {
        console.error('Error fetching shipments:', error);
        throw error;
      }
    },
    enabled: enabled && !!api,
    keepPreviousData: true,
  });

  // Preload next page if requested
  useEffect(() => {
    if (!preloadNextPage || !query.data?.shipments.page_info.has_next_page) return;

    const nextPageFilter = {
      ...filter,
      offset: (filter.offset || 0) + (filter.first || DEFAULT_PAGINATION.first)
    };

    queryClient.prefetchQuery({
      queryKey: ['shipments', nextPageFilter],
      queryFn: async () => {
        const response = await api.graphql({
          query: GET_SHIPMENTS,
          variables: { filter: nextPageFilter },
        });
        return response.data;
      },
    });
  }, [query.data, filter, queryClient, preloadNextPage, api]);

  return {
    query,
    filter,
    setFilter,
  };
}

// Hook for fetching a single shipment
export function useShipment(id?: string) {
  const api = useKarrioAPI();

  const query = useQuery({
    queryKey: ['shipment', id],
    queryFn: async () => {
      const response = await api.graphql({
        query: GET_SHIPMENT,
        variables: { id },
      });
      return response.data;
    },
    enabled: !!id && !!api && id !== 'new',
  });

  return { query };
}

// Hook for shipment mutations (update, delete)
export function useShipmentMutation() {
  const api = useKarrioAPI();
  const queryClient = useQueryClient();

  // Update shipment mutation
  const updateShipment = useMutation({
    mutationFn: async ({
      id,
      data,
    }: {
      id: string;
      data: Record<string, any>;
    }) => {
      const response = await api.graphql({
        query: `
          mutation update_shipment($id: ID!, $data: ShipmentUpdateInput!) {
            update_shipment(id: $id, input: $data) {
              shipment {
                id
              }
              errors {
                field
                messages
              }
            }
          }
        `,
        variables: { id, data },
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['shipments'] });
    },
  });

  return {
    updateShipment,
  };
}
