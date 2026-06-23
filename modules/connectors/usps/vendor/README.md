# USPS vendor specs

Official USPS OpenAPI specifications, vendored for reference and schema generation.
Captured **2026-06-23** from the USPS Developer Portal (<https://developers.usps.com>).

All v3 APIs share the base hosts:

- Production: `https://apis.usps.com`
- Test (TEM — Testing Environment for Mailers): `https://apis-tem.usps.com`

| File | API | Version | Server base | Portal page |
| --- | --- | --- | --- | --- |
| `domestic-prices.yaml` | Domestic Prices | 3.4.30 | `/prices/v3` | [domesticpricesv3](https://developers.usps.com/domesticpricesv3) |
| `domestic-labels.yaml` | Labels | 3.9.13 | `/labels/v3` | [domesticlabelsv3](https://developers.usps.com/domesticlabelsv3) |
| `tracking.yaml` | Package Tracking & Notification | 3.2.6 | `/tracking/v3` | [trackingv3](https://developers.usps.com/trackingv3) |
| `addresses.yaml` | Addresses | 3.2.3 | `/addresses/v3` | [addressesv3](https://developers.usps.com/addressesv3) |
| `locations.yaml` | Locations | 3.5.6 | `/locations/v3` | [locationsv3](https://developers.usps.com/locationsv3) |
| `carrier-pickup.yaml` | Carrier Pickup | 3.1.8 | `/pickup/v3` | [carrierpickupv3](https://developers.usps.com/carrierpickupv3) |
| `payments.yaml` | Payments | 3.1.20 | `/payments/v3` | [paymentsv3](https://developers.usps.com/paymentsv3) |
| `shipping-options.yaml` | Shipping Options | 3.1.29 | `/shipments/v3` | [shippingoptionsv3](https://developers.usps.com/shippingoptionsv3) |
| `scan-forms.yaml` | SCAN Forms | 3.1.14 | `/scan-forms/v3` | [scanv3](https://developers.usps.com/scanv3) |

OAuth 2.0 (`/oauth2/v3/token`) has no standalone spec — see the portal
[Getting Started](https://developers.usps.com/getting-started) guide.

## Refreshing

Each portal page embeds a Redoc `spec-url` pointing at the raw YAML under
`https://developers.usps.com/sites/default/files/apidoc_specs/<name>_<n>.yaml`
(the `_<n>` suffix increments per revision). To refresh, open the portal page,
read its `spec-url`, and re-download:

```bash
# example
curl -sS "https://developers.usps.com/domesticpricesv3" \
  | grep -oiE '/sites/default/files/apidoc_specs/[^" ]*\.yaml' | head -1
```
