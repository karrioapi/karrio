import re
from karrio.core.utils import Enum, Flag, Spec


class PackagingType(Flag):
    easypost_envelope = "Envelope"

    """ Unified Packaging type mapping """
    envelope = easypost_envelope


class Service(Enum):
    easypost_all = "0"

    @staticmethod
    def info(serviceId, carrierId, serviceName, carrierName):
        carrier_name = CARRIER_IDS.get(str(carrierId)) or carrierName
        service = Service.map(str(serviceId))
        formatted_name = re.sub(
            r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r" \1", serviceName
        )
        service_name = (service.name or formatted_name).replace("easypost_", "")

        return carrier_name, service.name_or_key, service_name


CARRIER_IDS = {
    "1": "fedex",
}


class Option(Flag):
    easypost_option = Spec.asFlag("option")
