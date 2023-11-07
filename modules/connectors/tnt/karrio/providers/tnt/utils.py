import karrio.schemas.tnt.label_request as tnt
import karrio.schemas.tnt.shipping_response as shipping
import typing
import base64
import karrio.lib as lib
import karrio.core as core
import karrio.core.models as models


class Settings(core.Settings):
    """TNT connection settings."""

    username: str
    password: str

    account_number: str = None
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "tnt"

    @property
    def server_url(self):
        return "https://express.tnt.com"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.tnt.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def create_label_request(
    shipment_response: str,
    settings: Settings,
    ctx: dict,
) -> typing.Optional[lib.Serializable]:
    import karrio.providers.tnt.units as provider_units

    payload: models.ShipmentRequest = ctx.get("payload")
    response = lib.to_element(shipment_response)
    consignment = lib.find_element("CONNUMBER", response, first=True)
    groupcode = lib.find_element("GROUPCODE", response, first=True)
    price: shipping.document = lib.find_element(
        "PRICE", response, shipping.PRICE, first=True
    )

    if consignment is None or groupcode is None or price is None:
        return None

    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    customs = lib.to_customs_info(payload.customs)

    request = tnt.labelRequest(
        consignment=[
            tnt.labelConsignmentsType(
                key="1",
                consignmentIdentity=tnt.consignmentIdentityType(
                    consignmentNumber=getattr(consignment, "text", None),
                    customerReference=payload.reference,
                ),
                collectionDateTime=None,
                sender=tnt.nameAndAddressRequestType(
                    name=recipient.contact,
                    addressLine1=shipper.street,
                    addressLine2=shipper.address_line2,
                    addressLine3=None,
                    town=shipper.city,
                    exactMatch=None,
                    province=shipper.state_code,
                    postcode=shipper.postal_code,
                    country=shipper.country_code,
                ),
                delivery=tnt.nameAndAddressRequestType(
                    name=recipient.contact,
                    addressLine1=recipient.street,
                    addressLine2=recipient.address_line2,
                    addressLine3=None,
                    town=recipient.city,
                    exactMatch=None,
                    province=recipient.state_code,
                    postcode=recipient.postal_code,
                    country=recipient.country_code,
                ),
                contact=tnt.contactType(
                    name=shipper.person_name,
                    telephoneNumber=shipper.phone_number,
                    emailAddress=shipper.email,
                ),
                product=tnt.productType(
                    lineOfBusiness=None,
                    groupId=getattr(groupcode, "text", None),
                    subGroupId=None,
                    id=price.SERVICE,
                    type_=price.SERVICEDESC,
                    option=price.OPTION,
                ),
                account=tnt.accountType(
                    accountNumber=settings.account_number,
                    accountCountry=settings.account_country_code,
                ),
                cashAmount=price.RATE,
                cashCurrency=price.CURRENCY,
                cashType=None,
                ncolNumber=None,
                specialInstructions=None,
                bulkShipment="N",
                customControlled=("N" if payload.customs is None else "Y"),
                termsOfPayment=provider_units.PaymentType.map(
                    getattr(payload.payment, "paidby", "sender")
                ).value,
                totalNumberOfPieces=len(packages),
                pieceLine=[
                    tnt.pieceLineType(
                        identifier=1,
                        goodsDescription=package.parcel.description,
                        barcodeForCustomer="Y",
                        pieceMeasurements=tnt.measurementsType(
                            length=package.length.M,
                            width=package.width.M,
                            height=package.height.M,
                            weight=package.weight.KG,
                        ),
                        pieces=(
                            [
                                tnt.pieceType(
                                    sequenceNumbers=(index + 1),
                                    pieceReference=piece.sku or piece.hs_code,
                                )
                                for index, piece in enumerate(
                                    (
                                        package.items
                                        if len(package.items) > 0
                                        else customs.commodities
                                    ),
                                    start=1,
                                )
                            ]
                            if len(package.items) > 0 or len(customs.commodities) > 0
                            else None
                        ),
                    )
                    for package in packages
                ],
            )
        ]
    )

    return lib.Serializable(request, lib.to_xml)
