import { request, APIRequestContext } from "@playwright/test";
import { env } from "./env";

/**
 * Thin REST client around Playwright's `request` fixture.
 *
 * Uses JWT bearer auth — the smoke suite hits `/api/token` once, caches
 * the access token, and reuses it for all subsequent calls.  This matches
 * what the dashboard does internally and avoids touching the DB directly.
 */
export class KarrioApi {
  private ctx: APIRequestContext | null = null;
  private token: string | null = null;

  constructor(
    private readonly baseURL: string = env.apiUrl,
    private readonly email: string = env.email,
    private readonly password: string = env.password,
  ) {}

  private async context(): Promise<APIRequestContext> {
    if (!this.ctx) {
      this.ctx = await request.newContext({ baseURL: this.baseURL });
    }
    return this.ctx;
  }

  /** Obtain + cache a JWT access token. */
  async login(): Promise<string> {
    if (this.token) return this.token;
    const ctx = await this.context();
    const res = await ctx.post("/api/token", {
      data: { email: this.email, password: this.password },
    });
    if (!res.ok()) {
      throw new Error(`karrio login failed: ${res.status()} ${await res.text()}`);
    }
    const body = (await res.json()) as { access: string };
    this.token = body.access;
    return this.token;
  }

  private async authHeaders(): Promise<Record<string, string>> {
    const token = await this.login();
    return { Authorization: `Bearer ${token}` };
  }

  async get<T = unknown>(path: string): Promise<T> {
    const ctx = await this.context();
    const res = await ctx.get(path, { headers: await this.authHeaders() });
    if (!res.ok()) throw new Error(`GET ${path} failed: ${res.status()} ${await res.text()}`);
    return (await res.json()) as T;
  }

  async post<T = unknown>(path: string, data: unknown): Promise<T> {
    const ctx = await this.context();
    const res = await ctx.post(path, {
      headers: await this.authHeaders(),
      data,
    });
    if (!res.ok()) throw new Error(`POST ${path} failed: ${res.status()} ${await res.text()}`);
    return (await res.json()) as T;
  }

  async delete(path: string): Promise<void> {
    const ctx = await this.context();
    const res = await ctx.delete(path, { headers: await this.authHeaders() });
    if (!res.ok() && res.status() !== 404) {
      throw new Error(`DELETE ${path} failed: ${res.status()} ${await res.text()}`);
    }
  }

  /** Create a reusable shipping address. */
  createAddress(overrides: Partial<Record<string, unknown>> = {}) {
    return this.post<{ id: string }>("/v1/addresses", {
      address_line1: "5840 Oak Street",
      city: "Los Angeles",
      state_code: "CA",
      postal_code: "90001",
      country_code: "US",
      person_name: "Karrio E2E",
      company_name: "Karrio E2E",
      phone_number: "4151234567",
      ...overrides,
    });
  }

  /** Create a reusable parcel template. */
  createParcel(overrides: Partial<Record<string, unknown>> = {}) {
    return this.post<{ id: string }>("/v1/parcels", {
      weight: 1.0,
      weight_unit: "KG",
      package_preset: "canadapost_corrugated_small_box",
      ...overrides,
    });
  }

  /** Release the underlying request context (call in afterAll hooks). */
  async dispose() {
    if (this.ctx) {
      await this.ctx.dispose();
      this.ctx = null;
    }
  }
}
