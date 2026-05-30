# seed.py — provision HIGH-FIDELITY sample data for Karrio Studio.
# Run: cat apps/studio/sandbox/seed.py | karrio shell
# Idempotent & defensive. Every shipment/order gets real shipper, recipient,
# parcels, line items, and itemized charges so no Studio section renders empty.
#
# Field types on this Karrio version (verified):
#   Shipment.shipper / recipient        -> JSON dict
#   Shipment.parcels                    -> JSON list of dicts
#   Shipment.selected_rate              -> JSON dict (Rate; needs carrier_id)
#   Order.shipping_to                   -> JSON dict
#   Order.line_items                    -> JSON list of dicts
from django.contrib.auth import get_user_model

U = get_user_model()
user = U.objects.order_by("date_joined").first() or U.objects.first()
print("seeding as:", getattr(user, "email", None))


def log(section, fn):
    try:
        print(f"  ok {section}: {fn()}")
    except Exception as e:  # noqa: BLE001
        import traceback
        print(f"  FAIL {section}: {type(e).__name__}: {e}")
        traceback.print_exc()


SHIPPER = dict(person_name="Daniel Kovic", company_name="Acme Inc.", address_line1="432 Park Ave, Suite 4",
               city="Brooklyn", state_code="NY", postal_code="11201", country_code="US",
               email="ops@acme.shop", phone_number="+1 718 555 0142", residential=False)
RECIPIENTS = [
    dict(person_name="Alicia Romero", address_line1="55 Water St", city="Brooklyn", state_code="NY",
         postal_code="11201", country_code="US", email="alicia@example.com", phone_number="+1 212 555 0198", residential=True),
    dict(person_name="Jane Doe", company_name="Northwest Retail", address_line1="980 Howe St", city="Vancouver",
         state_code="BC", postal_code="V6Z 1N9", country_code="CA", email="jane@example.com", phone_number="+1 604 555 0199"),
    dict(person_name="Helmut Strauss", company_name="Strauss GmbH", address_line1="Friedrichstrasse 88", city="Berlin",
         state_code="BE", postal_code="10117", country_code="DE", email="helmut@example.de", phone_number="+49 30 5550 1234"),
    dict(person_name="Owen Wright", address_line1="700 Bay St", city="Toronto", state_code="ON",
         postal_code="M5G 1Z8", country_code="CA", email="owen@example.ca", phone_number="+1 416 555 0110", residential=True),
]


def parcel_dict(ref):
    return dict(weight=2.0, weight_unit="KG", width=30, height=20, length=25,
                dimension_unit="CM", packaging_type="BOX", reference_number=ref, is_document=False)


def rate_dict(carrier, svc, charge, cur):
    base, fuel = round(charge * 0.8, 2), round(charge * 0.15, 2)
    return {
        "id": "rate_" + carrier, "object_type": "rate", "carrier_name": carrier,
        "carrier_id": carrier + "_acct", "service": svc, "total_charge": charge, "currency": cur,
        "transit_days": 2, "test_mode": False,
        "extra_charges": [
            {"name": "Base charge", "amount": base, "currency": cur},
            {"name": "Fuel surcharge", "amount": fuel, "currency": cur},
        ],
    }


SHIPMENTS = [
    ("ups", "ups_2nd_day_air", "purchased", 12.40, "USD", "1Z999AA10123456784", "ORDER-11335", 0),
    ("canadapost", "canadapost_expedited_parcel", "delivered", 9.80, "CAD", "CP123456789CA", "ORDER-11333", 1),
    ("dhl_express", "dhl_express_worldwide", "in_transit", 42.80, "USD", "1231006943", "ORDER-11334", 2),
    ("fedex", "fedex_priority_overnight", "purchased", 28.10, "USD", "794651413733", "REF-1112", 3),
]


def seed_shipments():
    import karrio.server.manager.models as m
    created = 0
    for carrier, svc, status, charge, cur, tn, ref, ridx in SHIPMENTS:
        if m.Shipment.objects.filter(tracking_number=tn).exists():
            continue
        m.Shipment.objects.create(
            created_by=user, status=status, test_mode=False, tracking_number=tn, reference=ref,
            shipper=dict(SHIPPER), recipient=dict(RECIPIENTS[ridx]),
            parcels=[parcel_dict(ref)],
            selected_rate=rate_dict(carrier, svc, charge, cur),
        )
        created += 1
    return f"{created} created, {m.Shipment.objects.count()} total"


def seed_trackers():
    import karrio.server.manager.models as m
    samples = [
        ("1Z999AA10123456784", "ups", "in_transit", "2026-06-01",
         [("Order processed", "Brooklyn, NY", "2026-05-28", "10:02"),
          ("Departed facility", "Newark, NJ", "2026-05-28", "23:48"),
          ("In transit", "Philadelphia, PA", "2026-05-29", "06:22")]),
        ("794651413733", "fedex", "delivered", "2026-05-27",
         [("Picked up", "Seattle, WA", "2026-05-26", "09:44"),
          ("Out for delivery", "Toronto, ON", "2026-05-27", "08:10"),
          ("Delivered — front desk", "Toronto, ON", "2026-05-27", "15:48")]),
        ("1231006943", "dhl_express", "in_transit", "2026-05-30",
         [("Shipment picked up", "Berlin, DE", "2026-05-28", "07:48"),
          ("Customs cleared", "Leipzig, DE", "2026-05-29", "02:14")]),
        ("CP123456789CA", "canadapost", "delivered", "2026-05-27",
         [("Item processed", "Vancouver, BC", "2026-05-25", "06:03"),
          ("Delivered", "Vancouver, BC", "2026-05-27", "11:20")]),
    ]
    created = 0
    for tn, carrier, status, eta, evs in samples:
        if m.Tracking.objects.filter(tracking_number=tn).exists():
            continue
        m.Tracking.objects.create(
            created_by=user, tracking_number=tn, status=status, test_mode=False, estimated_delivery=eta,
            events=[{"description": d, "location": loc, "date": dt, "time": tm} for d, loc, dt, tm in evs],
            meta={"carrier_name": carrier},
        )
        created += 1
    return f"{created} created, {m.Tracking.objects.count()} total"


def seed_templates():
    import karrio.server.graph.models as g
    n = 0
    addrs = [("Acme Brooklyn HQ", "Daniel Kovic", "Acme Inc.", "432 Park Ave", "Brooklyn", "NY", "11201", "US", True),
             ("Vancouver Warehouse", "Mei Tanaka", "Acme Inc.", "980 Powell St", "Vancouver", "BC", "V6A 1H9", "CA", False),
             ("Berlin Hub", "Helmut Strauss", "Acme GmbH", "Friedrichstrasse 88", "Berlin", "BE", "10117", "DE", False)]
    for label, person, company, line1, city, state, postal, country, default in addrs:
        if g.Template.objects.filter(label=label).exists():
            continue
        a = g.Address.objects.create(created_by=user, person_name=person, company_name=company, address_line1=line1,
                                     city=city, state_code=state, postal_code=postal, country_code=country)
        g.Template.objects.create(created_by=user, label=label, is_default=default, address=a)
        n += 1
    parcels = [("Small Box", 20, 15, 10, 0.5, True), ("Medium Box", 35, 25, 20, 2.0, False), ("Poly Mailer", 30, 25, 5, 0.3, False)]
    for label, l, w, h, wt, default in parcels:
        if g.Template.objects.filter(label=label).exists():
            continue
        p = g.Parcel.objects.create(created_by=user, length=l, width=w, height=h, dimension_unit="CM",
                                    weight=wt, weight_unit="KG", packaging_type="BOX")
        g.Template.objects.create(created_by=user, label=label, is_default=default, parcel=p)
        n += 1
    return f"{n} created, {g.Template.objects.count()} total"


def seed_orders():
    import karrio.server.orders.models as om
    created = 0
    samples = [
        ("#11335", "unfulfilled", "shopify", 0, [("Wireless Headphones", "ACM-1001", 1, 84.00), ("USB-C Cable 2m", "ACM-2410", 2, 12.00)]),
        ("#11334", "fulfilled", "medusa", 1, [("Widget Pro 2026", "WDG-PRO-001", 1, 199.00)]),
        ("#11333", "partial", "bigcommerce", 3, [("Sticker Pack", "ACM-3300", 5, 4.00)]),
    ]
    for oid, status, source, ridx, items in samples:
        if om.Order.objects.filter(order_id=oid).exists():
            continue
        line_items = [
            {"title": title, "sku": sku, "quantity": qty, "value_amount": val, "value_currency": "USD",
             "weight": 0.4, "weight_unit": "KG", "origin_country": "US", "hs_code": "8518.30"}
            for title, sku, qty, val in items
        ]
        om.Order.objects.create(created_by=user, order_id=oid, status=status, source=source,
                                test_mode=False, shipping_to=dict(RECIPIENTS[ridx]), line_items=line_items)
        created += 1
    return f"{created} created, {om.Order.objects.count()} total"


def selfcheck():
    # Fail loudly if any shipment is missing addresses/parcels/charges.
    import karrio.server.manager.models as m
    issues = []
    for s in m.Shipment.objects.all():
        r = s.selected_rate or {}
        if not s.shipper or not s.recipient:
            issues.append(f"{s.tracking_number}: missing address")
        if not s.parcels:
            issues.append(f"{s.tracking_number}: no parcels")
        if not (r.get("extra_charges")):
            issues.append(f"{s.tracking_number}: no charges")
        if not r.get("carrier_id"):
            issues.append(f"{s.tracking_number}: rate missing carrier_id")
    return "all shipments complete" if not issues else "ISSUES: " + "; ".join(issues)


log("shipments", seed_shipments)
log("trackers", seed_trackers)
log("templates (addresses/parcels)", seed_templates)
log("orders", seed_orders)
log("selfcheck", selfcheck)
print("seed complete.")
