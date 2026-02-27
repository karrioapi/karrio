import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { KarrioClient } from "../../src/client.js";

describe("KarrioClient", () => {
  let client: KarrioClient;
  let originalFetch: typeof global.fetch;

  beforeEach(() => {
    originalFetch = global.fetch;
    client = new KarrioClient({
      apiUrl: "https://api.karrio.io",
      apiKey: "test_key_123",
    });
  });

  afterEach(() => {
    global.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  it("constructs with correct base URL (strips trailing slash)", () => {
    const c = new KarrioClient({
      apiUrl: "https://api.karrio.io/",
      apiKey: "key",
    });
    // Access private apiUrl via any cast for testing
    const result = (c as any).apiUrl;

    expect(result).toBe("https://api.karrio.io");
  });

  it("strips multiple trailing slashes from URL", () => {
    const c = new KarrioClient({
      apiUrl: "https://api.karrio.io///",
      apiKey: "key",
    });
    const result = (c as any).apiUrl;

    expect(result).toBe("https://api.karrio.io");
  });

  it("preserves URL without trailing slash", () => {
    const c = new KarrioClient({
      apiUrl: "https://api.karrio.io",
      apiKey: "key",
    });
    const result = (c as any).apiUrl;

    expect(result).toBe("https://api.karrio.io");
  });

  it("stores API key correctly", () => {
    const result = (client as any).apiKey;

    expect(result).toBe("test_key_123");
  });

  it("makes GET requests with correct headers", async () => {
    const mockResponse = { results: [{ id: "carrier_1" }] };
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const result = await client.listCarriers();


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/carriers",
      expect.objectContaining({
        method: "GET",
        headers: expect.objectContaining({
          Authorization: "Token test_key_123",
          "Content-Type": "application/json",
        }),
      }),
    );
    expect(result).toEqual(mockResponse);
  });

  it("makes POST requests with JSON body", async () => {
    const mockResponse = { rates: [] };
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const payload = { shipper: {}, recipient: {}, parcels: [] };
    const result = await client.fetchRates(payload);


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/proxy/rates",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(payload),
      }),
    );
    expect(result).toEqual(mockResponse);
  });

  it("throws descriptive error on API failure", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
      json: () => Promise.resolve({ detail: "Invalid API key" }),
    });

    await expect(client.listCarriers()).rejects.toThrow(/401/);
  });

  it("includes error detail from JSON response body", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 403,
      statusText: "Forbidden",
      json: () => Promise.resolve({ detail: "Permission denied" }),
    });

    await expect(client.listCarriers()).rejects.toThrow(/Permission denied/);
  });

  it("falls back to text error when JSON parsing fails", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      statusText: "Internal Server Error",
      json: () => Promise.reject(new Error("not json")),
      text: () => Promise.resolve("Server Error"),
    });

    await expect(client.listCarriers()).rejects.toThrow(/500/);
  });

  it("builds query string for GET requests", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ results: [] }),
    });

    await client.listShipments({ status: "purchased", limit: "10" });

    const calledUrl = (fetch as any).mock.calls[0][0];

    expect(calledUrl).toContain("status=purchased");
    expect(calledUrl).toContain("limit=10");
  });

  it("omits query string when no params provided", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ results: [] }),
    });

    await client.listShipments();

    const calledUrl = (fetch as any).mock.calls[0][0];

    expect(calledUrl).toBe("https://api.karrio.io/v1/shipments");
    expect(calledUrl).not.toContain("?");
  });

  it("calls correct URL for createShipment", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: "shp_123" }),
    });

    const payload = { shipper: {}, recipient: {}, parcels: [] };
    const result = await client.createShipment(payload);


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/shipments",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(payload),
      }),
    );
  });

  it("calls correct URL for purchaseShipment", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: "shp_123", status: "purchased" }),
    });

    const payload = { selected_rate_id: "rate_456" };
    const result = await client.purchaseShipment("shp_123", payload);


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/shipments/shp_123/purchase",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(payload),
      }),
    );
  });

  it("calls correct URL for getShipment", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: "shp_123" }),
    });

    const result = await client.getShipment("shp_123");


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/shipments/shp_123",
      expect.objectContaining({ method: "GET" }),
    );
  });

  it("calls correct URL for cancelShipment", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: "shp_123", status: "cancelled" }),
    });

    const result = await client.cancelShipment("shp_123");


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/shipments/shp_123/cancel",
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("calls correct URL for createTracker", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ tracking_number: "1Z999AA10123456784" }),
    });

    const payload = { tracking_number: "1Z999AA10123456784", carrier_name: "ups" };
    const result = await client.createTracker(payload);


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/trackers",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(payload),
      }),
    );
  });

  it("calls correct URL for getTracker", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ tracking_number: "1Z999AA10123456784" }),
    });

    const result = await client.getTracker("1Z999AA10123456784");


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/trackers/1Z999AA10123456784",
      expect.objectContaining({ method: "GET" }),
    );
  });

  it("calls correct URL for validateAddress", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ valid: true }),
    });

    const payload = { address: { postal_code: "10001", country_code: "US" } };
    const result = await client.validateAddress(payload);


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/addresses/validate",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(payload),
      }),
    );
  });

  it("calls correct URL for getReferences", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ countries: {} }),
    });

    const result = await client.getReferences();


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/references",
      expect.objectContaining({ method: "GET" }),
    );
  });

  it("calls correct URL for listOrders", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ results: [] }),
    });

    const result = await client.listOrders({ limit: "5" });


    const calledUrl = (fetch as any).mock.calls[0][0];
    expect(calledUrl).toContain("/v1/orders");
    expect(calledUrl).toContain("limit=5");
  });

  it("calls correct URL for getOrder", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: "ord_123" }),
    });

    const result = await client.getOrder("ord_123");


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/orders/ord_123",
      expect.objectContaining({ method: "GET" }),
    );
  });

  it("calls correct URL for schedulePickup", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: "pck_123" }),
    });

    const payload = { pickup_date: "2026-03-01" };
    const result = await client.schedulePickup(payload);


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/pickups",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(payload),
      }),
    );
  });

  it("calls correct URL for createManifest", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: "mnf_123" }),
    });

    const payload = { carrier_name: "fedex", shipment_ids: ["shp_1"] };
    const result = await client.createManifest(payload);


    expect(fetch).toHaveBeenCalledWith(
      "https://api.karrio.io/v1/manifests",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(payload),
      }),
    );
  });
});
