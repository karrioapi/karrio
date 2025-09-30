// Shopify-specific types

export interface ShopifyStore {
    id: string;
    name: string;
    domain: string;
    myshopify_domain: string;
    country_code: string;
    currency: string;
    timezone: string;
    created_at: string;
    updated_at: string;
}

export interface ShopifyOrder {
    id: string;
    order_number: string;
    email: string;
    created_at: string;
    updated_at: string;
    total_price: string;
    currency: string;
    financial_status: string;
    fulfillment_status: string;
    shipping_address?: ShopifyAddress;
    billing_address?: ShopifyAddress;
    line_items: ShopifyLineItem[];
}

export interface ShopifyAddress {
    address1: string;
    address2?: string;
    city: string;
    province: string;
    province_code: string;
    country: string;
    country_code: string;
    zip: string;
    name: string;
    phone?: string;
    company?: string;
}

export interface ShopifyLineItem {
    id: string;
    title: string;
    quantity: number;
    price: string;
    grams: number;
    width?: number;
    height?: number;
    length?: number;
    requires_shipping: boolean;
}

export interface ShopifyCarrierService {
    id: string;
    name: string;
    callback_url: string;
    service_discovery: boolean;
    carrier_service_type: string;
    format: string;
    active: boolean;
}

export interface ShopifyRateRequest {
    rate: {
        origin: ShopifyAddress;
        destination: ShopifyAddress;
        items: ShopifyLineItem[];
        currency: string;
    };
}

export interface ShopifyRate {
    service_name: string;
    service_code: string;
    total_price: number; // in cents
    currency: string;
    min_delivery_date?: string;
    max_delivery_date?: string;
    description?: string;
}

export interface ShopifyRateResponse {
    rates: ShopifyRate[];
}

// OAuth related types
export interface ShopifyOAuthTokenResponse {
    access_token: string;
    scope: string;
}

export interface ShopifyAppInstallation {
    shop_domain: string;
    access_token: string;
    carrier_service_id?: string;
    scopes: string[];
    installed_at: string;
}

// Configuration types
export interface ShopifyAppConfig {
    default_packaging?: string;
    insurance_enabled?: boolean;
    signature_confirmation?: boolean;
    excluded_carriers?: string[];
    webhook_url?: string;
}
