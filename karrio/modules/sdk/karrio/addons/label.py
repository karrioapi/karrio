from jinja2 import Template
from karrio.core.utils import DP
from karrio.core.units import Package, CountryISO
from karrio.core.models import ShipmentRequest
from karrio.addons.renderer import render_label
from karrio.universal.providers.shipping import (
    ShippingMixinSettings,
)


def generate_label(
    shipment: ShipmentRequest,
    package: Package,
    service_name: str,
    tracking_number: str,
    settings: ShippingMixinSettings,
    index: int = 1,
) -> str:
    template = getattr(settings.label_template, "template", DEFAULT_SVG_LABEL_TEMPLATE)
    context = DP.to_dict(
        dict(
            package_index=index,
            items=package.parcel.items,
            total_packages=len(shipment.parcels),
            is_multi_item=len(package.parcel.items) > 1,
            master_item=next(iter(package.parcel.items), {}),
            metadata=next((item.metadata or {} for item in package.parcel.items), {}),
            total_quantity=sum(item.quantity for item in package.parcel.items) or 1,
            shipment=shipment,
            carrier=settings,
            service_name=service_name,
            tracking_number=tracking_number,
            units=dict(
                CountryISO=CountryISO.as_dict(),
            ),
        )
    )

    return render_label(
        label=Template(template).render(**context),
        label_type=getattr(shipment, "label_type", "PDF"),
        template_type=getattr(settings.label_template, "type", "SVG"),
        width=getattr(settings.label_template, "width", 4),
        height=getattr(settings.label_template, "height", 6),
    )


DEFAULT_SVG_LABEL_TEMPLATE = """
<svg viewBox="0 0 1200 1800" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin" width="4in" height="6in"
    style="border: 1px solid #ddd;">

    <!--  Part 1 -->

    <text x="30" y="60" fill="black" style="font-size: 50; font-weight: bold">FROM:</text>
    <text x="30" y="110" fill="black" style="font-size: 40; font-weight: bold">{{ shipment.shipper.get('company_name', '').upper() }}</text>
    <text x="30" y="160" fill="black" style="font-size: 30;">{{ shipment.shipper.get('address_line1', '').upper() }}</text>
    <text x="30" y="210" fill="black" style="font-size: 30;">{{ [shipment.shipper.city, [shipment.shipper.state_code, shipment.shipper.postal_code]|join(" ")]|join(", ") }}</text>

    <line x1="450" y1="20" x2="450" y2="270" stroke="black" stroke-width="3" />

    <text x="470" y="60" fill="black" style="font-size: 50; font-weight: bold">CARR: {{ carrier.get('display_name', '').upper() }}</text>
    <text x="470" y="140" fill="black" style="font-size: 45; font-weight: bold">PRO#: {{ metadata.get('RFF_CN', '') }}</text>
    <text x="470" y="220" fill="black" style="font-size: 45; font-weight: bold">BOL#: {{ metadata.get('BGM', '') }}</text>

    <line x1="20" y1="270" x2="1170" y2="270" stroke="black" stroke-width="3" />

    <!--  Part 2 -->

    <text x="30" y="310" fill="black" style="font-size: 50; font-weight: bold">TO: {{ shipment.recipient.get('address_line1', '').upper() }}</text>
    <text x="110" y="370" fill="black" style="font-size: 40; font-weight: bold">{{ shipment.recipient.get('company_name', '').upper() }}</text>


    <text x="110" y="470" fill="black" style="font-size: 40; font-weight: bold">{{ [shipment.recipient.get('city', '').upper(), [shipment.recipient.get('state_code', '').upper(), shipment.recipient.get('postal_code', '').upper()]|join(" ")]|join(", ") }}</text>

    <line x1="20" y1="500" x2="1170" y2="500" stroke="black" stroke-width="3" />

    <!--  Part 3 -->

    <text x="100" y="550" fill="black" style="font-size: 35; font-weight: bold">SHIP TO POSTAL CODE</text>

    <text data-type="barcode-text" x="60" y="620" fill="black" style="font-size: 40">(421) {{ units.CountryISO.get(shipment.recipient.country_code)  }}{{ shipment.recipient.get('postal_code', '').upper() }}</text>
    <g data-type="barcode" data-value="(421) {{ units.CountryISO.get(shipment.recipient.country_code)  }}{{ shipment.recipient.get('postal_code', '').upper() }}"
        data-module-width="3" data-width-ratio="2" x="30" y="660"
        width="460" height="150" style="font-size: 60; font-weight: bold">
        <text x="80" y="640" fill="black" style="font-size: 40; font-weight: bold">(421) {{ units.CountryISO.get(shipment.recipient.country_code)  }}{{ shipment.recipient.get('postal_code') }}</text>
        <rect x="30" y="660" width="460" height="100" fill="transparent" stroke="black"></rect>
    </g>

    <line x1="550" y1="500" x2="550" y2="840" stroke="black" stroke-width="3" />

    <text x="600" y="570" fill="black" style="font-size: 75; font-weight: bold">PO#: {{ metadata.get('RFF_ON', '') }}</text>
    <text x="600" y="700" fill="black" style="font-size: 35">DEPT#: {{ metadata.get('DEPT', '') }}</text>
    <text x="600" y="780" fill="black" style="font-size: 35">CTL#: {{ metadata.get('CTL', '') }}</text>

    <line x1="20" y1="840" x2="1170" y2="840" stroke="black" stroke-width="3" />

    <!--  Part 4 -->

    <text x="110" y="940" fill="black" style="font-size: 50; font-weight: bold">CARTON: {{ package_index }} OF {{ total_packages }}</text>

    <text x="30" y="1080" fill="black" style="font-size: 40; font-weight: bold">SKU: {% if is_multi_item %}{{ master_item.get('sku', '') }}{% else %}MIXED{% endif %}</text>
    <text x="30" y="1140" fill="black" style="font-size: 40; font-weight: bold">XXNC: {{ metadata.get('XXNC', '') }}</text>

    <text x="460" y="1080" fill="black" style="font-size: 40; font-weight: bold">CUST#: {{ metadata.get('NAD_UD', '') }}</text>
    <text x="460" y="1140" fill="black" style="font-size: 40; font-weight: bold">QTY: {{ total_quantity }}</text>


    <text x="850" y="1000" fill="black" style="font-size: 90; font-weight: bold">{{ metadata.get('RFF_AJY', '') }}</text>
    <text x="850" y="1100" fill="black" style="font-size: 90; font-weight: bold">{{ metadata.get('RFF_AEM', '') }}</text>

    <line x1="20" y1="1230" x2="1170" y2="1230" stroke="black" stroke-width="3" />

    <!--  Part 4 -->

    <text x="100" y="1300" fill="black" style="font-size: 35; font-weight: bold">(00) SERIAL SHIPPING CONTAINER</text>

    <text data-type="barcode-text" x="90" y="1360" fill="black" style="font-size: 45">({{ carrier['metadata'].get('APP_ID', '00') }}){{ carrier['metadata'].get('EXTENSION_DIGIT', '0') }}{{ carrier['metadata'].get('GS1_PREFIX', '0000000000') }}{{ tracking_number[-6:] }}{{ carrier['metadata'].get('CHECK_DIGIT', 5) }}</text>
    <g data-type="barcode" data-value="({{ carrier['metadata'].get('APP_ID', '00') }}){{ carrier['metadata'].get('EXTENSION_DIGIT', '0') }}{{ carrier['metadata'].get('GS1_PREFIX', '0000000000') }}{{ tracking_number[-6:] }}{{ carrier['metadata'].get('CHECK_DIGIT', 5) }}"
        data-module-width="5" data-width-ratio="3" x="60" y="1410" width="900" height="250" style="font-size: 65;">
        <text x="80" y="1380" fill="black" style="font-size: 60; font-weight: bold">({{ carrier['metadata'].get('APP_ID', '00') }}){{ carrier['metadata'].get('EXTENSION_DIGIT', '0') }}{{ carrier['metadata'].get('GS1_PREFIX', '0000000000') }}{{ tracking_number[-6:] }}{{ carrier['metadata'].get('CHECK_DIGIT', 5) }}</text>
        <rect x="60" y="1400" width="750" height="200" fill="transparent" stroke="black"></rect>
    </g>


    <text x="740" y="1720" fill="black" style="font-size: 30; font-weight: bold">xxxxxxxxxxxxxxxxxxxxxxxxx</text>

</svg>
"""


DEFAULT_ZPL_LABEL_TEMPLATE = """
^XA

^FX Top section.

^FX Top Left section.
^CF0,50
^FO30,30^FDFROM:^FS
^CF0,40
^FO30,90^FD{{ shipment.shipper.get('company_name', '').upper() }}^FS

^CFA,30
^FO30,150^FD{{ shipment.shipper.get('address_line1', '').upper() }}^FS
^FO30,200^FD{{ [shipment.shipper.city, [shipment.shipper.state_code, shipment.shipper.postal_code]|join(" ")]|join(", ") }}^FS

^FO520,20^GB4,260,4^FS

^FX Top Right section.
^CF0,50
^FO540,30^FDCARR: {{ carrier.get('display_name', '').upper() }}^FS
^CF0,45
^FO540,120^FDPRO#: {{ metadata.get('RFF_CN', '') }}^FS
^FO540,200^FDBOL#: {{ metadata.get('BGM', '') }}^FS

^FO20,280^GB1170,4,4^FS

^FX Second section with recipient address
^CF0,60
^FO30,320^FDTO: {{ shipment.recipient.get('address_line1', '') }}^FS
^CF0,50
^FO110,380^FD{{ shipment.recipient.get('company_name', '').upper() }}^FS

^FO110,500^FD{{ [shipment.recipient.get('city', '').upper(), [shipment.recipient.get('state_code', '').upper(), shipment.recipient.get('postal_code', '').upper()]|join(" ")]|join(", ") }}^FS

^FO20,560^GB1170,4,4^FS

^FX Third section with bar code.
^CF0,35
^FO100,600^FDSHIP TO POSTAL CODE^FS

^CFA,40
^FO70,620^FD(421) {{ units.CountryISO.get(shipment.recipient.country_code)  }}{{ shipment.recipient.get('postal_code', '').upper() }}^FS
^BY3,2,150
^FO30,660^BCN,150,N,Y,Y,D^FD(421) {{ units.CountryISO.get(shipment.recipient.country_code)  }}{{ shipment.recipient.get('postal_code', '').upper() }}^FS

^FO580,560^GB4,340,4^FS

^CF0,90
^FO630,600^FDPO#: {{ metadata.get('RFF_ON', '') }}^FS
^CF0,40
^FO630,740^FDDEPT#: {{ metadata.get('DEPT', '') }}^FS
^FO630,820^FDCTL#: {{ metadata.get('CTL', '') }}^FS

^FO20,900^GB1170,4,4^FS

^FX Fourth section.
^CF0,60
^FO110,940^FDCARTON: {{ package_index }} OF {{ total_packages }}^FS

^CF0,40
^FO30,1080^FDSKU: {% if is_multi_item %}{{ master_item.get('sku', '') }}{% else %}MIXED{% endif %}^FS
^FO30,1140^FDXXNC: {{ metadata.get('XXNC', '') }}^FS

^FO460,1080^FDCUST#: {{ metadata.get('NAD_UD', '') }}^FS
^FO460,1140^FDQTY: {{ total_quantity }}^FS

^CF0,90
^FO850,1000^FD{{ metadata.get('RFF_AJY', '') }}^FS
^FO850,1100^FD{{ metadata.get('RFF_AEM', '') }}^FS

^FO20,1230^GB1170,4,4^FS

^FX Fifth section.
^CF0,35
^FO100,1280^FD(00) SERIAL SHIPPING CONTAINER^FS

^CFA,45
^FO80,1360^FD({{ carrier['metadata'].get('APP_ID', '00') }}){{ carrier['metadata'].get('EXTENSION_DIGIT', '0') }}{{ carrier['metadata'].get('GS1_PREFIX', '0000000000') }}{{ tracking_number[-6:] }}{{ carrier['metadata'].get('CHECK_DIGIT', 5) }}^FS
^BY5,3,200
^FO60,1410^BCN,250,N,Y,Y,D^FD({{ carrier['metadata'].get('APP_ID', '00') }}){{ carrier['metadata'].get('EXTENSION_DIGIT', '0') }}{{ carrier['metadata'].get('GS1_PREFIX', '0000000000') }}{{ tracking_number[-6:] }}{{ carrier['metadata'].get('CHECK_DIGIT', 5) }}^FS

^CF0,30
^FO760,1720^FDxxxxxxxxxxxxxxxxxxxxxxxxx^FS

^XZ
"""
