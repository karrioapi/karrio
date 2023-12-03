import gql from 'graphql-tag';


export const GET_SYSTEM_USAGE = gql`query get_system_usage {
  system_usage {
    total_errors
    order_volume
    total_requests
    total_shipments
    organization_count
    api_errors {
      label
      count
      date
    }
    api_requests {
      label
      count
      date
    }
    order_volumes {
      label
      count
      date
    }
    shipments {
      label
      count
      date
    }
    shipment_spend {
      label
      count
      date
    }
  }
}
`;
