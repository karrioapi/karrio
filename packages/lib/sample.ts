export const DEFAULT_SVG_LABEL_TEMPLATE = `
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
`;


export const DEFAULT_DOCUMENT_TEMPLATE = `
<div>
  <h1>Document</h1>
</div>
<style type="text/css">
  @page { size: A4; margin: 1cm };
</style>
`;
