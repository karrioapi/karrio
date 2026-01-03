"""PostAT carrier tests fixtures."""

import karrio.sdk as karrio


gateway = karrio.gateway["postat"].create(
    dict(
        id="carrier_id",
        test_mode=True,
        carrier_id="postat",
        client_id="-1",
        org_unit_id="1461448",
        org_unit_guid="cd96848d-6552-4653-a992-f0f411710fb4",
        config=dict(
            label_format="PDF",
            label_size="SIZE_100x200",
            paper_layout="LAYOUT_2xA5inA4",
        ),
    )
)