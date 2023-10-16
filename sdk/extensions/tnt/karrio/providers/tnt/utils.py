import karrio.schemas.tnt.label_request as tnt
import karrio.schemas.tnt.shipping_response as shipping
import base64
import urllib.parse
import karrio.lib as lib
import karrio.core as core
import karrio.core.units as units


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


def generate_label(
    activity: shipping.document,
    settings: Settings,
    ctx: dict,
) -> lib.Serializable:
    import karrio.providers.tnt.units as provider_units

    tracer = ctx.get("tracer")
    payload = ctx.get("payload")
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.parcels).single
    customs = lib.to_customs_info(payload.customs)
    payment = payload.payment or units.Payment(paid_by="sender")
    price: shipping.PRICE = next(activity.RATE.PRICE, shipping.PRICE())

    request = tnt.labelRequest(
        consignment=[
            tnt.labelConsignmentsType(
                key="1",
                consignmentIdentity=tnt.consignmentIdentityType(
                    consignmentNumber=activity.CREATE.CONNUMBER,
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
                    groupId=activity.GROUPCODE,
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
                    payment.paid_by or "sender"
                ).value,
                totalNumberOfPieces=1,
                pieceLine=[
                    tnt.pieceLineType(
                        identifier=1,
                        goodsDescription=package.parcel.description,
                        barcodeForCustomer="Y",
                        pieceMeasurements=tnt.measurementsType(
                            length=package.length.M,
                            width=package.width.M,
                            height=package.height.M,
                            weight=package.weight.M,
                        ),
                        pieces=(
                            [
                                tnt.pieceType(
                                    sequenceNumbers=(index + 1),
                                    pieceReference=piece.sku or piece.hs_code,
                                )
                                for index, piece in enumerate(
                                    customs.commodities, start=1
                                )
                            ]
                            if payload.customs is not None and any(customs.commodities)
                            else None
                        ),
                    )
                ],
            )
        ]
    )

    return lib.request(
        url=f"{settings.server_url}/expressconnect/shipping/ship",
        data=urllib.parse.urlencode(dict(xml_in=request.serialize())),
        trace=tracer,
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {settings.authorization}",
        },
        decoder=lib.encode_base64,
    )
