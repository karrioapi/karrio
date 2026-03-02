export interface KarrioClientConfig {
  apiUrl: string;
  apiKey: string;
}

export class KarrioClient {
  private apiUrl: string;
  private apiKey: string;

  constructor(config: KarrioClientConfig) {
    this.apiUrl = config.apiUrl.replace(/\/+$/, "");
    this.apiKey = config.apiKey;
  }

  private buildQueryString(params?: Record<string, string>): string {
    if (!params || Object.keys(params).length === 0) return "";
    const query = new URLSearchParams(params).toString();
    return `?${query}`;
  }

  private async request<T>(
    method: string,
    path: string,
    options?: { body?: unknown; params?: Record<string, string> },
  ): Promise<T> {
    const queryString = this.buildQueryString(options?.params);
    const url = `${this.apiUrl}${path}${queryString}`;
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      Authorization: `Token ${this.apiKey}`,
    };

    const response = await fetch(url, {
      method,
      headers,
      ...(options?.body ? { body: JSON.stringify(options.body) } : {}),
    });

    if (!response.ok) {
      let errorDetail: string;
      try {
        const errorJson = await response.json();
        errorDetail = JSON.stringify(errorJson);
      } catch {
        errorDetail = await response.text();
      }
      throw new Error(
        `Karrio API error ${response.status} ${response.statusText}: ${errorDetail}`,
      );
    }

    return response.json() as Promise<T>;
  }

  // Rate shopping
  async fetchRates(payload: Record<string, unknown>): Promise<any> {
    return this.request("POST", "/v1/proxy/rates", { body: payload });
  }

  // Shipments
  async createShipment(payload: Record<string, unknown>): Promise<any> {
    return this.request("POST", "/v1/shipments", { body: payload });
  }

  async purchaseShipment(
    id: string,
    payload: Record<string, unknown>,
  ): Promise<any> {
    return this.request("POST", `/v1/shipments/${id}/purchase`, {
      body: payload,
    });
  }

  async getShipment(id: string): Promise<any> {
    return this.request("GET", `/v1/shipments/${id}`);
  }

  async listShipments(params?: Record<string, string>): Promise<any> {
    return this.request("GET", "/v1/shipments", { params });
  }

  async cancelShipment(id: string): Promise<any> {
    return this.request("POST", `/v1/shipments/${id}/cancel`);
  }

  // Tracking
  async createTracker(payload: Record<string, unknown>): Promise<any> {
    return this.request("POST", "/v1/trackers", { body: payload });
  }

  async getTracker(idOrTrackingNumber: string): Promise<any> {
    return this.request("GET", `/v1/trackers/${idOrTrackingNumber}`);
  }

  async listTrackers(params?: Record<string, string>): Promise<any> {
    return this.request("GET", "/v1/trackers", { params });
  }

  // Address validation
  async validateAddress(payload: Record<string, unknown>): Promise<any> {
    return this.request("POST", "/v1/addresses/validate", { body: payload });
  }

  // Carriers
  async listCarriers(params?: Record<string, string>): Promise<any> {
    return this.request("GET", "/v1/carriers", { params });
  }

  // Reference data
  async getReferences(): Promise<any> {
    return this.request("GET", "/v1/references");
  }

  // Orders
  async listOrders(params?: Record<string, string>): Promise<any> {
    return this.request("GET", "/v1/orders", { params });
  }

  async getOrder(id: string): Promise<any> {
    return this.request("GET", `/v1/orders/${id}`);
  }

  // Pickups
  async schedulePickup(payload: Record<string, unknown>): Promise<any> {
    return this.request("POST", "/v1/pickups", { body: payload });
  }

  // Manifests
  async createManifest(payload: Record<string, unknown>): Promise<any> {
    return this.request("POST", "/v1/manifests", { body: payload });
  }

  // GraphQL
  async queryGraphQL(
    query: string,
    variables?: Record<string, unknown>,
  ): Promise<any> {
    return this.request("POST", "/graphql", {
      body: { query, variables },
    });
  }

  // Logs
  async listLogs(filter?: Record<string, unknown>): Promise<any> {
    const query = `query get_logs($filter: LogFilter) {
      logs(filter: $filter) {
        page_info { count has_next_page has_previous_page start_cursor end_cursor }
        edges {
          node {
            id path host data method response_ms remote_addr
            requested_at status_code query_params response
            records { id key timestamp test_mode created_at meta record }
          }
        }
      }
    }`;
    const result = await this.queryGraphQL(query, { filter });
    return result?.data?.logs;
  }

  async getLog(id: number): Promise<any> {
    const query = `query get_log($id: Int!) {
      log(id: $id) {
        id requested_at response_ms path remote_addr host method
        query_params data response status_code
        records { id key timestamp test_mode created_at meta record }
      }
    }`;
    const result = await this.queryGraphQL(query, { id });
    return result?.data?.log;
  }

  async listTracingRecords(filter?: Record<string, unknown>): Promise<any> {
    const query = `query get_tracing_records($filter: TracingRecordFilter) {
      tracing_records(filter: $filter) {
        page_info { count has_next_page start_cursor end_cursor }
        edges {
          node {
            id key timestamp test_mode created_at meta record
          }
        }
      }
    }`;
    const result = await this.queryGraphQL(query, { filter });
    return result?.data?.tracing_records;
  }
}
