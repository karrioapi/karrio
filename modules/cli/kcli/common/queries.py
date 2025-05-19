GET_LOGS = """
  query get_logs($filter: LogFilter) {
    logs(filter: $filter) {
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
          path
          host
          data
          method
          response_ms
          remote_addr
          requested_at
          status_code
          query_params
          response
          records {
            id
            key
            timestamp
            test_mode
            created_at
            meta
            record
          }
        }
      }
    }
  }
"""

GET_LOG = """
  query get_log($id: Int!) {
    log(id: $id) {
      id
      requested_at
      response_ms
      path
      remote_addr
      host
      method
      query_params
      data
      response
      status_code
      records {
        id
        key
        timestamp
        test_mode
        created_at
        meta
        record
      }
    }
  }
"""
