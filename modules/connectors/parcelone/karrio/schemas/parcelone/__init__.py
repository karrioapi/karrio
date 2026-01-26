"""ParcelOne API schema types."""

# Import shipping request types
from karrio.schemas.parcelone.shipping_request import (
    CepSpecialType,
    FormatType,
    MaxChargesType,
    CustomDetailType,
    IntDocDataType,
    PackageDimensionsType,
    PackageVolumeClassType,
    ServiceType,
    PackageType,
    BankAccountType,
    ShipmentAddressType,
    ShipmentContactType,
    ShipFromDataType,
    ShipToDataType,
    ShippingDataType,
    ShippingRequestType,
)

# Import shipping response types with prefixes to avoid collision
from karrio.schemas.parcelone.shipping_response import (
    ErrorType as ShipmentErrorType,
    WarningType as ShipmentWarningType,
    ActionResultType as ShipmentActionResultType,
    TotalChargesType,
    FormatType as ResponseFormatType,
    DocumentsResultType as ShipmentDocumentsResultType,
    PackageResultType as ShipmentPackageResultType,
    ResultsType as ShipmentResultType,
    ShippingResponseType,
)

# Import tracking response types
from karrio.schemas.parcelone.tracking_response import (
    EventType as TrackingEventType,
    ResultsType as TrackingResultType,
    TrackingResponseType,
)

# Import cancel response types
from karrio.schemas.parcelone.cancel_response import (
    ErrorType as CancelErrorType,
    WarningType as CancelWarningType,
    ResultsType as CancelResultType,
    CancelResponseType,
)

# Import error types
from karrio.schemas.parcelone.error import (
    ErrorType as ErrorDetailType,
    ErrorResponseType,
)

# Backwards compatibility aliases for shipping request types
ShippingDataRequestType = ShippingRequestType
ShipmentType = ShippingDataType
AddressType = ShipmentAddressType
ContactType = ShipmentContactType
ShipToType = ShipToDataType
ShipFromType = ShipFromDataType
MeasurementType = PackageVolumeClassType
DimensionsType = PackageDimensionsType
AmountType = MaxChargesType
ShipmentServiceType = ServiceType
ShipmentPackageType = PackageType
CEPSpecialType = CepSpecialType
