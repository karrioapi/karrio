# seed.py — provision sample data for Karrio Studio. Run via: cat seed.py | karrio shell
# Idempotent and defensive: each section is independent and safe to re-run.
from django.contrib.auth import get_user_model

U = get_user_model()
user = U.objects.order_by("date_joined").first() or U.objects.first()
print("seeding as:", getattr(user, "email", None))


def log(section, fn):
    try:
        n = fn()
        print(f"  ✓ {section}: {n}")
    except Exception as e:  # noqa: BLE001
        print(f"  ✗ {section}: {type(e).__name__}: {e}")


# --- Trackers ---------------------------------------------------------------
def seed_trackers():
    import karrio.server.manager.models as m
    samples = [
        ("1Z999AA10123456784", "ups", "in_transit", "2026-06-01", "Departed facility", "Newark, NJ"),
        ("794651413733", "fedex", "delivered", "2026-05-27", "Delivered", "Vancouver, BC"),
        ("1231006943", "dhl_express", "in_transit", "2026-05-30", "Customs cleared", "Leipzig, DE"),
        ("CP123456789CA", "canadapost", "pending", None, "Shipment info received", "Toronto, ON"),
    ]
    created = 0
    for tn, carrier, status, eta, desc, loc in samples:
        if m.Tracking.objects.filter(tracking_number=tn).exists():
            continue
        m.Tracking.objects.create(
            created_by=user, tracking_number=tn, status=status, test_mode=False,
            estimated_delivery=eta,
            events=[{"description": desc, "location": loc, "date": "2026-05-28", "time": "11:02"}],
            meta={"carrier_name": carrier},
        )
        created += 1
    return f"{created} created, {m.Tracking.objects.count()} total"


# --- Addresses (shipper/recipient) -----------------------------------------
def make_address(**kw):
    import karrio.server.manager.models as m
    return m.Address.objects.create(created_by=user, **kw)


# --- Shipments --------------------------------------------------------------
def seed_shipments():
    import karrio.server.manager.models as m
    samples = [
        ("ups", "UPS 2nd Day Air", "purchased", 12.40, "USD", "1Z999AA10123456784", "ORDER-11335", "Alicia Romero", "Brooklyn", "NY", "US"),
        ("fedex", "FedEx Priority Overnight", "delivered", 28.10, "USD", "794651413733", "REF-1112", "Jane Doe", "Vancouver", "BC", "CA"),
        ("dhl_express", "DHL Express Worldwide", "in_transit", 42.80, "USD", "1231006943", "ORDER-11334", "Helmut Strauss", "Berlin", "", "DE"),
        ("canadapost", "Expedited Parcel", "purchased", 9.80, "CAD", "CP123456789CA", "ORDER-11333", "Owen Wright", "Toronto", "ON", "CA"),
    ]
    created = 0
    for carrier, svc, status, charge, cur, tn, ref, name, city, state, country in samples:
        if m.Shipment.objects.filter(tracking_number=tn).exists():
            continue
        # Recipient/shipper enrichment is left to the API path; core fields here
        # avoid a Karrio event-signal serialization quirk with Address FKs.
        m.Shipment.objects.create(
            created_by=user, status=status, test_mode=False, tracking_number=tn, reference=ref,
            selected_rate={
                "id": "rate_" + tn[-6:], "object_type": "rate",
                "carrier_name": carrier, "carrier_id": carrier + "_acct",
                "service": svc, "total_charge": charge, "currency": cur,
                "transit_days": 2, "extra_charges": [], "test_mode": False,
            },
        )
        created += 1
    return f"{created} created, {m.Shipment.objects.count()} total"


# --- Address & parcel templates (GraphQL-backed screens) --------------------
def seed_templates():
    import karrio.server.graph.models as g
    n = 0
    addrs = [("Acme Brooklyn HQ", "Daniel K", "Acme Inc.", "Brooklyn", "NY", "US", True),
             ("Vancouver Warehouse", "Mei Tanaka", "Acme Inc.", "Vancouver", "BC", "CA", False)]
    for label, person, company, city, state, country, default in addrs:
        if g.Template.objects.filter(label=label).exists():
            continue
        a = g.Address.objects.create(created_by=user, person_name=person, company_name=company,
                                     address_line1="100 Example St", city=city, state_code=state,
                                     postal_code="00000", country_code=country)
        g.Template.objects.create(created_by=user, label=label, is_default=default, address=a)
        n += 1
    parcels = [("Small Box", 20, 15, 10, 0.5, True), ("Medium Box", 35, 25, 20, 2.0, False)]
    for label, l, w, h, wt, default in parcels:
        if g.Template.objects.filter(label=label).exists():
            continue
        p = g.Parcel.objects.create(created_by=user, length=l, width=w, height=h,
                                    dimension_unit="CM", weight=wt, weight_unit="KG", packaging_type="BOX")
        g.Template.objects.create(created_by=user, label=label, is_default=default, parcel=p)
        n += 1
    return f"{n} created, {g.Template.objects.count()} total"


# --- Orders -----------------------------------------------------------------
def seed_orders():
    import karrio.server.orders.models as om
    import karrio.server.manager.models as m
    created = 0
    samples = [("#11335", "unfulfilled", "shopify", "Alicia Romero", "Brooklyn", "US"),
               ("#11334", "fulfilled", "medusa", "Jane Doe", "Vancouver", "CA")]
    for oid, status, source, name, city, country in samples:
        if om.Order.objects.filter(order_id=oid).exists():
            continue
        o = om.Order.objects.create(created_by=user, order_id=oid, status=status, source=source, test_mode=False)
        try:
            c = om.Commodity.objects.create(created_by=user, title="Widget", quantity=2, sku="ACM-1",
                                            value_amount=84, value_currency="USD")
            o.line_items.add(c)
        except Exception:
            pass
        created += 1
    return f"{created} created, {om.Order.objects.count()} total"


log("trackers", seed_trackers)
log("shipments", seed_shipments)
log("templates (addresses/parcels)", seed_templates)
log("orders", seed_orders)
print("seed complete.")
