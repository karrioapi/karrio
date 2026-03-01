# OSP-COMMERCE-INTEGRATION: Commerce Platform Integration Guide

**Version**: 0.1 (Draft)
**License**: Apache 2.0
**Audience**: Commerce platform developers and plugin authors
**Prerequisite**: [OSP-CORE.md](./OSP-CORE.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Shopify](#2-shopify)
3. [WooCommerce](#3-woocommerce)
4. [MedusaJS](#4-medusajs)
5. [Saleor](#5-saleor)
6. [Magento / Adobe Commerce](#6-magento--adobe-commerce)
7. [Generic OSP Commerce Hook](#7-generic-osp-commerce-hook)

---

## 1. Overview

Commerce platforms are the primary adoption vector for OSP. When a platform's shipping integration speaks OSP, every carrier implementing OSP becomes instantly available to every merchant on that platform.

### Integration Pattern

All commerce platform integrations follow the same core pattern:

```
┌──────────────────────────┐
│    Commerce Platform     │
│                          │
│  Checkout / Cart         │
│         │                │
│         ▼                │
│  Shipping Rate Callback  │──── POST /osp/v1/rates ────┐
│         │                │                              │
│         ▼                │                              ▼
│  Order Fulfillment       │     ┌──────────────────────────┐
│         │                │     │   OSP-Compliant Server   │
│         ▼                │     │   (e.g., karrio Cloud)   │
│  Create Shipment         │──── POST /osp/v1/shipments ──│
│         │                │     │                          │
│         ▼                │     │   Webhooks ──────────────│──┐
│  Track Shipment          │──── GET /osp/v1/tracking/{n} ─│  │
│                          │     └──────────────────────────┘  │
│  ◄───────────────────────│───────────────────────────────────┘
│  Update order status     │     tracking.delivered webhook
└──────────────────────────┘
```

### Required OSP Configuration

Every integration needs these configuration values:

| Setting | Example | Description |
|---------|---------|-------------|
| `osp_api_url` | `https://api.karrio.io` | OSP server base URL |
| `osp_api_key` | `osp_key_xxxxx` | API key for authentication |
| `osp_webhook_secret` | `whsec_xxxxx` | Webhook signing secret |
| `default_shipper` | `{address object}` | Default ship-from address |

---

## 2. Shopify

### 2.1 CarrierService Integration

Shopify uses the [CarrierService API](https://shopify.dev/docs/api/admin-rest/2024-10/resources/carrierservice) to fetch real-time shipping rates during checkout.

**Registration**:
```json
POST /admin/api/2024-10/carrier_services.json
{
  "carrier_service": {
    "name": "OSP Shipping",
    "callback_url": "https://your-app.example.com/shopify/rates",
    "service_discovery": true,
    "format": "json"
  }
}
```

**Rate callback handler** — translates Shopify's rate request to OSP:

```javascript
// POST /shopify/rates — Shopify calls this during checkout
async function handleShopifyRateRequest(shopifyRequest) {
  // Translate Shopify → OSP
  const ospRequest = {
    shipper: {
      postal_code: shopifyRequest.rate.origin.postal_code,
      country_code: shopifyRequest.rate.origin.country,
      state_code: shopifyRequest.rate.origin.province,
      city: shopifyRequest.rate.origin.city,
      company_name: shopifyRequest.rate.origin.company_name,
    },
    recipient: {
      postal_code: shopifyRequest.rate.destination.postal_code,
      country_code: shopifyRequest.rate.destination.country,
      state_code: shopifyRequest.rate.destination.province,
      city: shopifyRequest.rate.destination.city,
      person_name: shopifyRequest.rate.destination.name,
      company_name: shopifyRequest.rate.destination.company_name,
    },
    parcels: shopifyRequest.rate.items.map(item => ({
      weight: item.grams / 1000,
      weight_unit: "KG",
      description: item.name,
      items: [{
        title: item.name,
        sku: item.sku,
        quantity: item.quantity,
        value_amount: item.price / 100,
        value_currency: shopifyRequest.rate.currency,
      }]
    })),
  };

  // Call OSP
  const response = await fetch(`${OSP_API_URL}/osp/v1/rates`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${OSP_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(ospRequest),
  });
  const ospResponse = await response.json();

  // Translate OSP → Shopify
  return {
    rates: ospResponse.rates.map(rate => ({
      service_name: rate.service_name || rate.service,
      service_code: rate.service,
      total_price: Math.round(rate.total_charge * 100), // Shopify uses cents
      currency: rate.currency,
      min_delivery_date: rate.estimated_delivery,
      max_delivery_date: rate.estimated_delivery,
    })),
  };
}
```

### 2.2 Fulfillment on Order Creation

When an order is placed, create a shipment via OSP:

```javascript
// Shopify order webhook → create shipment
async function fulfillOrder(order) {
  const shipment = await fetch(`${OSP_API_URL}/osp/v1/shipments`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${OSP_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      service: order.shipping_lines[0].code, // OSP service code from checkout
      shipper: DEFAULT_SHIPPER,
      recipient: {
        person_name: `${order.shipping_address.first_name} ${order.shipping_address.last_name}`,
        address_line1: order.shipping_address.address1,
        address_line2: order.shipping_address.address2,
        city: order.shipping_address.city,
        state_code: order.shipping_address.province_code,
        postal_code: order.shipping_address.zip,
        country_code: order.shipping_address.country_code,
        phone_number: order.shipping_address.phone,
      },
      parcels: [{ weight: totalWeight(order), weight_unit: "LB" }],
      reference: order.name,
      metadata: { shopify_order_id: order.id.toString() },
    }),
  });

  const result = await shipment.json();

  // Create fulfillment in Shopify with the tracking number
  await createShopifyFulfillment(order.id, result.tracking_number, result.carrier_name);
}
```

---

## 3. WooCommerce

### 3.1 Shipping Method Plugin

WooCommerce uses shipping method classes to provide rates at checkout.

```php
<?php
/**
 * Plugin Name: OSP Shipping for WooCommerce
 * Description: Open Shipping Protocol integration for WooCommerce
 */

class WC_OSP_Shipping_Method extends WC_Shipping_Method {

    public function __construct($instance_id = 0) {
        $this->id = 'osp_shipping';
        $this->instance_id = absint($instance_id);
        $this->method_title = __('OSP Shipping');
        $this->method_description = __('Real-time rates via Open Shipping Protocol');
        $this->supports = ['shipping-zones', 'instance-settings'];
        $this->init();
    }

    public function calculate_shipping($package = []) {
        $osp_request = [
            'shipper' => [
                'postal_code' => get_option('woocommerce_store_postcode'),
                'country_code' => get_option('woocommerce_default_country'),
                'city' => get_option('woocommerce_store_city'),
                'state_code' => get_option('woocommerce_store_state', ''),
            ],
            'recipient' => [
                'postal_code' => $package['destination']['postcode'],
                'country_code' => $package['destination']['country'],
                'state_code' => $package['destination']['state'],
                'city' => $package['destination']['city'],
            ],
            'parcels' => [
                [
                    'weight' => $this->get_package_weight($package),
                    'weight_unit' => get_option('woocommerce_weight_unit') === 'kg' ? 'KG' : 'LB',
                ],
            ],
        ];

        $response = wp_remote_post($this->get_option('osp_api_url') . '/osp/v1/rates', [
            'headers' => [
                'Authorization' => 'Bearer ' . $this->get_option('osp_api_key'),
                'Content-Type' => 'application/json',
            ],
            'body' => wp_json_encode($osp_request),
            'timeout' => 30,
        ]);

        if (is_wp_error($response)) return;

        $body = json_decode(wp_remote_retrieve_body($response), true);

        foreach ($body['rates'] as $rate) {
            $this->add_rate([
                'id' => $this->id . '_' . $rate['service'],
                'label' => $rate['service_name'] ?? $rate['service'],
                'cost' => $rate['total_charge'],
                'meta_data' => [
                    'osp_service' => $rate['service'],
                    'osp_carrier' => $rate['carrier_name'],
                    'transit_days' => $rate['transit_days'],
                ],
            ]);
        }
    }
}
```

### 3.2 Order Fulfillment Hook

```php
// Hook into WooCommerce order status change
add_action('woocommerce_order_status_processing', 'osp_create_shipment_on_order');

function osp_create_shipment_on_order($order_id) {
    $order = wc_get_order($order_id);
    $shipping_method = $order->get_shipping_methods();
    $osp_service = reset($shipping_method)->get_meta('osp_service');

    $response = wp_remote_post(get_option('osp_api_url') . '/osp/v1/shipments', [
        'headers' => [
            'Authorization' => 'Bearer ' . get_option('osp_api_key'),
            'Content-Type' => 'application/json',
        ],
        'body' => wp_json_encode([
            'service' => $osp_service,
            'shipper' => osp_get_store_address(),
            'recipient' => osp_map_wc_address($order),
            'parcels' => osp_map_wc_parcels($order),
            'reference' => $order->get_order_number(),
            'metadata' => ['woocommerce_order_id' => (string) $order_id],
        ]),
        'timeout' => 30,
    ]);

    $result = json_decode(wp_remote_retrieve_body($response), true);

    // Store tracking number on the order
    $order->update_meta_data('_osp_tracking_number', $result['tracking_number']);
    $order->update_meta_data('_osp_shipment_id', $result['id']);
    $order->update_meta_data('_osp_carrier', $result['carrier_name']);
    $order->save();
}
```

---

## 4. MedusaJS

### 4.1 FulfillmentProvider

MedusaJS v2 uses a FulfillmentProvider interface for shipping integrations.

```typescript
import {
  AbstractFulfillmentProviderService,
  MedusaContainer,
} from "@medusajs/framework/utils";

class OspFulfillmentProvider extends AbstractFulfillmentProviderService {
  static identifier = "osp";

  private ospApiUrl: string;
  private ospApiKey: string;

  constructor(container: MedusaContainer, options: Record<string, unknown>) {
    super(container, options);
    this.ospApiUrl = (options.api_url as string) || process.env.OSP_API_URL!;
    this.ospApiKey = (options.api_key as string) || process.env.OSP_API_KEY!;
  }

  async getFulfillmentOptions(): Promise<Record<string, unknown>[]> {
    const response = await this.ospFetch("/osp/v1/rates", "POST", {
      shipper: await this.getDefaultShipper(),
      recipient: { postal_code: "10001", country_code: "US" },
      parcels: [{ weight: 1, weight_unit: "LB" }],
    });

    return response.rates.map((rate: any) => ({
      id: rate.service,
      name: rate.service_name || rate.service,
      carrier: rate.carrier_name,
      price: rate.total_charge,
      currency: rate.currency,
    }));
  }

  async calculatePrice(
    optionData: Record<string, unknown>,
    data: Record<string, unknown>,
    context: Record<string, unknown>
  ): Promise<number> {
    const cart = context.cart as any;

    const response = await this.ospFetch("/osp/v1/rates", "POST", {
      shipper: await this.getDefaultShipper(),
      recipient: {
        postal_code: cart.shipping_address.postal_code,
        country_code: cart.shipping_address.country_code,
        state_code: cart.shipping_address.province,
        city: cart.shipping_address.city,
      },
      parcels: this.mapCartToParcels(cart),
      services: [optionData.id as string],
    });

    const rate = response.rates?.[0];
    return rate ? rate.total_charge * 100 : 0; // Medusa uses cents
  }

  async createFulfillment(
    data: Record<string, unknown>,
    items: Record<string, unknown>[],
    order: Record<string, unknown>,
    fulfillment: Record<string, unknown>
  ): Promise<Record<string, unknown>> {
    const result = await this.ospFetch("/osp/v1/shipments", "POST", {
      service: data.service_code,
      shipper: await this.getDefaultShipper(),
      recipient: this.mapOrderRecipient(order),
      parcels: this.mapItemsToParcels(items),
      reference: (order as any).display_id,
      metadata: { medusa_order_id: (order as any).id },
    });

    return {
      tracking_number: result.tracking_number,
      shipment_id: result.id,
      carrier_name: result.carrier_name,
      label_url: result.label_url,
    };
  }

  async cancelFulfillment(fulfillment: Record<string, unknown>): Promise<void> {
    const shipmentId = (fulfillment as any).data?.shipment_id;
    if (shipmentId) {
      await this.ospFetch(`/osp/v1/shipments/${shipmentId}/cancel`, "POST");
    }
  }

  async createReturnFulfillment(
    fromData: Record<string, unknown>
  ): Promise<Record<string, unknown>> {
    const shipmentId = (fromData as any).shipment_id;
    const result = await this.ospFetch(`/osp/v1/shipments/${shipmentId}/return`, "POST", {
      label_type: "PDF",
    });

    return {
      tracking_number: result.tracking_number,
      return_shipment_id: result.id,
      label_url: result.label_url,
    };
  }

  private async ospFetch(path: string, method: string, body?: any): Promise<any> {
    const response = await fetch(`${this.ospApiUrl}${path}`, {
      method,
      headers: {
        Authorization: `Bearer ${this.ospApiKey}`,
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    return response.json();
  }

  private mapCartToParcels(cart: any) { /* ... */ }
  private mapOrderRecipient(order: any) { /* ... */ }
  private mapItemsToParcels(items: any[]) { /* ... */ }
  private async getDefaultShipper() { /* ... */ }
}

export default OspFulfillmentProvider;
```

---

## 5. Saleor

### 5.1 Shipping Plugin

Saleor uses webhooks and plugins for shipping rate calculation and fulfillment.

**Webhook subscription** (Saleor Dashboard → Configuration → Webhooks):

| Event | Target URL | Purpose |
|-------|------------|---------|
| `SHIPPING_LIST_METHODS_FOR_CHECKOUT` | `/saleor/shipping-methods` | Provide rates at checkout |
| `ORDER_FULFILLED` | `/saleor/fulfill` | Create shipment on fulfillment |

**Shipping methods handler**:

```python
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.post("/saleor/shipping-methods")
async def shipping_methods(request: Request):
    payload = await request.json()
    checkout = payload["checkout"]

    osp_request = {
        "shipper": get_default_shipper(),
        "recipient": {
            "postal_code": checkout["shipping_address"]["postal_code"],
            "country_code": checkout["shipping_address"]["country"]["code"],
            "city": checkout["shipping_address"]["city"],
            "state_code": checkout["shipping_address"]["country_area"],
        },
        "parcels": [{
            "weight": sum(
                line["variant"]["weight"]["value"]
                * line["quantity"]
                for line in checkout["lines"]
            ),
            "weight_unit": "KG",
        }],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OSP_API_URL}/osp/v1/rates",
            json=osp_request,
            headers={"Authorization": f"Bearer {OSP_API_KEY}"},
        )
        osp_response = response.json()

    return {
        "shipping_methods": [
            {
                "id": rate["service"],
                "name": rate.get("service_name", rate["service"]),
                "amount": rate["total_charge"],
                "currency": rate["currency"],
                "maximum_delivery_days": rate.get("transit_days"),
            }
            for rate in osp_response.get("rates", [])
        ]
    }

@app.post("/saleor/fulfill")
async def fulfill_order(request: Request):
    payload = await request.json()
    order = payload["order"]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OSP_API_URL}/osp/v1/shipments",
            json={
                "service": order["shipping_method_name"],
                "shipper": get_default_shipper(),
                "recipient": map_saleor_address(order["shipping_address"]),
                "parcels": map_saleor_lines(order["lines"]),
                "reference": order["number"],
                "metadata": {"saleor_order_id": order["id"]},
            },
            headers={"Authorization": f"Bearer {OSP_API_KEY}"},
        )
        return response.json()
```

---

## 6. Magento / Adobe Commerce

### 6.1 Carrier Model

Magento uses a Carrier model class to provide shipping rates and create shipments.

```php
<?php
namespace Osp\Shipping\Model\Carrier;

use Magento\Quote\Model\Quote\Address\RateRequest;
use Magento\Shipping\Model\Carrier\AbstractCarrier;
use Magento\Shipping\Model\Carrier\CarrierInterface;
use Magento\Shipping\Model\Rate\ResultFactory;
use Magento\Quote\Model\Quote\Address\RateResult\MethodFactory;

class OspCarrier extends AbstractCarrier implements CarrierInterface
{
    protected $_code = 'osp';
    protected $_isFixed = false;

    public function collectRates(RateRequest $request)
    {
        if (!$this->getConfigFlag('active')) {
            return false;
        }

        $ospRequest = [
            'shipper' => [
                'postal_code' => $request->getOrigPostcode(),
                'country_code' => $request->getOrigCountryId(),
                'state_code' => $request->getOrigRegionCode(),
                'city' => $request->getOrigCity(),
            ],
            'recipient' => [
                'postal_code' => $request->getDestPostcode(),
                'country_code' => $request->getDestCountryId(),
                'state_code' => $request->getDestRegionCode(),
                'city' => $request->getDestCity(),
            ],
            'parcels' => [
                [
                    'weight' => $request->getPackageWeight(),
                    'weight_unit' => $this->getWeightUnit(),
                ],
            ],
        ];

        $ospResponse = $this->callOsp('/osp/v1/rates', 'POST', $ospRequest);

        $result = $this->rateResultFactory->create();

        foreach ($ospResponse['rates'] as $rate) {
            $method = $this->rateMethodFactory->create();
            $method->setCarrier($this->_code);
            $method->setCarrierTitle($rate['carrier_name']);
            $method->setMethod($rate['service']);
            $method->setMethodTitle($rate['service_name'] ?? $rate['service']);
            $method->setPrice($rate['total_charge']);
            $method->setCost($rate['total_charge']);
            $result->append($method);
        }

        return $result;
    }

    public function getAllowedMethods()
    {
        return ['osp' => $this->getConfigData('name')];
    }

    private function callOsp(string $path, string $method, array $body = []): array
    {
        $apiUrl = $this->getConfigData('api_url');
        $apiKey = $this->getConfigData('api_key');

        $ch = curl_init($apiUrl . $path);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_POSTFIELDS => json_encode($body),
            CURLOPT_HTTPHEADER => [
                'Authorization: Bearer ' . $apiKey,
                'Content-Type: application/json',
            ],
            CURLOPT_TIMEOUT => 30,
        ]);

        $response = curl_exec($ch);
        curl_close($ch);
        return json_decode($response, true);
    }
}
```

---

## 7. Generic OSP Commerce Hook

For platforms not listed above, or for custom commerce applications, use this generic pattern.

### 7.1 Rate Hook

The rate hook is called during checkout to fetch available shipping options.

```
Checkout Flow:
  Customer enters address → Platform calls rate hook → OSP returns rates → Customer selects rate
```

**Interface**:
```typescript
interface OspCommerceHook {
  // Called during checkout to get shipping rates
  getRates(context: CheckoutContext): Promise<ShippingOption[]>;

  // Called when an order is fulfilled
  createShipment(context: FulfillmentContext): Promise<ShipmentResult>;

  // Called to track a shipment
  trackShipment(trackingNumber: string, carrier?: string): Promise<TrackingResult>;

  // Called to create a return label
  createReturn(shipmentId: string): Promise<ShipmentResult>;

  // Called to cancel a shipment
  cancelShipment(shipmentId: string): Promise<CancelResult>;
}

interface CheckoutContext {
  origin: OspAddress;       // Ship-from address
  destination: OspAddress;  // Ship-to address
  items: CartItem[];        // Cart items
  currency: string;         // Cart currency
}

interface FulfillmentContext {
  service: string;          // OSP service code selected at checkout
  origin: OspAddress;
  destination: OspAddress;
  parcels: OspParcel[];
  order_reference: string;
  metadata: Record<string, string>;
}
```

### 7.2 Reference Implementation

```typescript
class OspCommerceClient implements OspCommerceHook {
  constructor(
    private apiUrl: string,
    private apiKey: string,
  ) {}

  async getRates(context: CheckoutContext): Promise<ShippingOption[]> {
    const response = await this.request("POST", "/osp/v1/rates", {
      shipper: context.origin,
      recipient: context.destination,
      parcels: this.itemsToParcels(context.items, context.currency),
    });

    return response.rates.map((rate: any) => ({
      id: rate.service,
      name: rate.service_name || rate.service,
      carrier: rate.carrier_name,
      price: rate.total_charge,
      currency: rate.currency,
      estimated_days: rate.transit_days,
      estimated_delivery: rate.estimated_delivery,
    }));
  }

  async createShipment(context: FulfillmentContext): Promise<ShipmentResult> {
    const response = await this.request("POST", "/osp/v1/shipments", {
      service: context.service,
      shipper: context.origin,
      recipient: context.destination,
      parcels: context.parcels,
      reference: context.order_reference,
      metadata: context.metadata,
    });

    return {
      shipment_id: response.id,
      tracking_number: response.tracking_number,
      carrier: response.carrier_name,
      label_url: response.label_url,
      label_base64: response.label,
      label_type: response.label_type,
    };
  }

  async trackShipment(trackingNumber: string, carrier?: string): Promise<TrackingResult> {
    const params = carrier ? `?carrier_name=${carrier}` : "";
    return this.request("GET", `/osp/v1/tracking/${trackingNumber}${params}`);
  }

  async createReturn(shipmentId: string): Promise<ShipmentResult> {
    return this.request("POST", `/osp/v1/shipments/${shipmentId}/return`, {
      label_type: "PDF",
    });
  }

  async cancelShipment(shipmentId: string): Promise<CancelResult> {
    return this.request("POST", `/osp/v1/shipments/${shipmentId}/cancel`);
  }

  private async request(method: string, path: string, body?: any): Promise<any> {
    const response = await fetch(`${this.apiUrl}${path}`, {
      method,
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new OspError(error.errors || [{ code: "unknown", message: response.statusText }]);
    }

    return response.json();
  }

  private itemsToParcels(items: CartItem[], currency: string) {
    return [{
      weight: items.reduce((sum, item) => sum + (item.weight || 0) * item.quantity, 0),
      weight_unit: "LB" as const,
      items: items.map(item => ({
        title: item.name,
        sku: item.sku,
        quantity: item.quantity,
        value_amount: item.price,
        value_currency: currency,
      })),
    }];
  }
}
```

### 7.3 Webhook Handler

Handle OSP webhook events to keep order status in sync:

```typescript
import { createHmac, timingSafeEqual } from "crypto";

async function handleOspWebhook(req: Request): Promise<Response> {
  // Verify signature
  const signature = req.headers.get("X-OSP-Signature")!;
  const timestamp = req.headers.get("X-OSP-Timestamp")!;
  const body = await req.text();

  if (!verifySignature(body, signature, timestamp, WEBHOOK_SECRET)) {
    return new Response("Invalid signature", { status: 401 });
  }

  const event = JSON.parse(body);

  switch (event.type) {
    case "tracking.delivered":
      await markOrderDelivered(event.data.tracking_number);
      break;
    case "tracking.exception":
      await flagOrderForReview(event.data.tracking_number, event.data.events[0]?.description);
      break;
    case "shipment.cancelled":
      await handleShipmentCancellation(event.data.id);
      break;
  }

  return new Response("OK", { status: 200 });
}

function verifySignature(payload: string, signature: string, timestamp: string, secret: string): boolean {
  const signedContent = `${timestamp}.${payload}`;
  const expected = `sha256=${createHmac("sha256", secret).update(signedContent).digest("hex")}`;
  return timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
}
```
