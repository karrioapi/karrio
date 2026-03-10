# Carrier Integration Rules

## Required Files
```
modules/connectors/<carrier>/
├── karrio/mappers/<carrier>/mapper.py    # Auto-generated, don't edit
├── karrio/mappers/<carrier>/proxy.py     # HTTP client
├── karrio/mappers/<carrier>/settings.py  # Carrier credentials
├── karrio/providers/<carrier>/rate.py    # Rate request/response
├── karrio/providers/<carrier>/shipment/  # Shipment create/cancel
├── karrio/providers/<carrier>/tracking.py # Tracking
├── karrio/providers/<carrier>/error.py   # Error parsing
├── karrio/providers/<carrier>/units.py   # Enums: services, options, statuses
├── karrio/schemas/<carrier>/             # Generated types (don't edit)
└── tests/<carrier>/test_*.py             # Test files
```

## Key Rules
- Always use `./bin/cli sdk add-extension` for scaffolding (never manual creation)
- Never edit `mapper.py` or schema files — they are auto-generated
- Never hardcode service/option strings — use enums in `units.py`
- Always use `karrio.lib as lib` utilities
- Schema generation: edit `schemas/*.json`, then `./bin/run-generate-on modules/connectors/<carrier>`

## Definition of Done
- [ ] `test_rate.py`: rate quote + error handling
- [ ] `test_shipment.py`: label generation + void/cancel
- [ ] `test_tracking.py`: delivered + in-transit with events
- [ ] All tests pass: `python -m unittest discover -v -f modules/connectors/<carrier>/tests`
- [ ] Service/Option enums defined in `units.py`

## Reference Carriers
- **SEKO**: JSON REST (simple)
- **UPS**: JSON REST (full features)
- **Canada Post**: XML REST
- **Easyship**: Hub/aggregator pattern
- **FedEx**: OAuth authentication
