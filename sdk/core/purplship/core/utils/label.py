from jinja2 import Template
from purplship.core.utils import DP, convert_label
from purplship.core.units import Package
from purplship.core.models import ShipmentRequest
from purplship.universal.providers.shipping import (
    ShippingMixinSettings,
)


def generate_label(
    shipment: ShipmentRequest,
    package: Package,
    settings: ShippingMixinSettings,
    index: int = 1,
) -> str:
    template = getattr(settings.label_template, "template", DEFAULT_LABEL_TEMPLATE)
    context = DP.to_dict(
        dict(
            sku=(
                next((item.sku or "" for item in package.parcel.items), "")
                if len(package.parcel.items) == 1
                else "MIXED"
            ),
            package_index=index,
            total_packages=len(shipment.parcels),
            quantity=sum(item.quantity for item in package.parcel.items) or 1,
            shipper=shipment.shipper,
            recipient=shipment.recipient,
            metadata=shipment.metadata,
            carrier_name=f"{getattr(settings, 'name', settings.carrier_id)}".upper(),
        )
    )

    return convert_label(
        label=Template(template).render(**context),
        label_type=getattr(shipment, "label_type", "PDF"),
        template_type=getattr(settings.label_template, "type", "ZPL"),
        width=getattr(settings.label_template, "width", 4),
        height=getattr(settings.label_template, "height", 6),
    )


DEFAULT_LABEL_TEMPLATE = """
^XA

^FX Top section.

^FX Top Left section.
^CF0,50
^FO30,30^FDFROM:^FS
^CF0,40
^FO30,90^FD{{ shipper.get('company_name') }}^FS

^CFA,30
^FO30,150^FD{{ shipper.get('address_line1') }}^FS
^FO30,200^FD{{ [shipper.city, [shipper.state_code, shipper.postal_code]|join(" ")]|join(", ") }}^FS

^FO520,20^GB4,260,4^FS

^FX Top Right section.
^CF0,50
^FO540,30^FDCARR: {{ carrier_name }}^FS
^CF0,45
^FO540,120^FDPRO#: {{ metadata.get('RFF_CN', '') }}^FS
^FO540,200^FDBOL#: {{ metadata.get('BGM', '') }}^FS

^FO20,280^GB1170,4,4^FS

^FX Second section with recipient address
^CF0,60
^FO30,320^FDTO: {{ recipient.get('address_line1') }}^FS
^CF0,50
^FO130,380^FD{{ recipient.get('company_name') }}^FS

^FO130,500^FD{{ [recipient.get('city'), [recipient.get('state_code'), recipient.get('postal_code')]|join(" ")]|join(", ") }}^FS

^FO20,560^GB1170,4,4^FS

^FX Third section with bar code.
^CF0,35
^FO100,600^FDSHIP TO POSTAL CODE^FS
^BY3,2,100
^FO30,750^BCN,100,Y,Y,Y,D^FD(421) 124{{ recipient.get('postal_code') }}^FS

^FO580,560^GB4,340,4^FS

^CF0,90
^FO630,600^FDPO#: {{ metadata.get('RFF_ON', '') }}^FS
^CF0,45
^FO630,740^FDDEPT#: {{ metadata.get('DEPT', '') }}^FS
^FO630,820^FDCTL#: {{ metadata.get('CTL', '') }}^FS

^FO20,900^GB1170,4,4^FS

^FX Fourth section.
^CF0,60
^FO130,940^FDCARTON: {{ package_index }} OF {{ total_packages }}^FS

^CF0,40
^FO30,1080^FDSKU: {{ sku  }}^FS
^FO30,1140^FDXXNC: {{ metadata.get('XXNC', '') }}^FS

^FO460,1080^FDCUST#: {{ metadata.get('NAD_UD', '') }}^FS
^FO460,1140^FDQTY: {{ quantity }}^FS

^CF0,90
^FO850,1000^FD{{ metadata.get('RFF_AJY', '') }}^FS
^FO850,1100^FD{{ metadata.get('RFF_AEM', '') }}^FS

^FO20,1230^GB1170,4,4^FS

^FX Fifth section.
^CF0,35
^FO90,1280^FD(00) SERIAL SHIPPING CONTAINER^FS
^BY5,3,200
^FO60,1420^BCN,200,Y,Y,Y,D^FD({{ metadata.get('app_id', '00') }}){{ metadata.get('serial', '000999990002975565') }}^FS

^CF0,30
^FO760,1720^FDxxxxxxxxxxxxxxxxxxxxxxxxx^FS

^XZ
"""
