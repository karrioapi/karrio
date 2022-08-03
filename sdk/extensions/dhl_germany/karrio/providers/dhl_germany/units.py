
import karrio.core.utils as utils


class PackagingType(utils.Flag):
    """ Carrier specific packaging type """
    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingService(utils.Enum):
    """ Carrier specific services """
    dhl_germany_standard_service = "DHL Parcel Germany Standard Service"


class ShippingOption(utils.Enum):
    """ Carrier specific options """
    # dhl_germany_option = utils.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = dhl_germany_coverage  #  maps unified karrio option to carrier specific

    pass
