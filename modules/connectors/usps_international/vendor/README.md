# USPS International vendor specs

Official USPS OpenAPI specifications for the international APIs, vendored for
reference and schema generation. Captured **2026-06-23** from the USPS Developer
Portal (<https://developers.usps.com>).

Shared base hosts (same platform as domestic):

- Production: `https://apis.usps.com`
- Test (TEM — Testing Environment for Mailers): `https://apis-tem.usps.com`

| File | API | Version | Server base | Portal page |
| --- | --- | --- | --- | --- |
| `international-prices.yaml` | International Prices | 3.3.11 | `/international-prices/v3` | [internationalpricesv3](https://developers.usps.com/internationalpricesv3) |
| `international-labels.yaml` | International Labels | 3.3.7 | `/international-labels/v3` | [internationallabelsv3](https://developers.usps.com/internationallabelsv3) |

OAuth, addresses, tracking and payments are shared with the domestic platform —
see `modules/connectors/usps/vendor/`.

See `modules/connectors/usps/vendor/README.md` for refresh instructions.
