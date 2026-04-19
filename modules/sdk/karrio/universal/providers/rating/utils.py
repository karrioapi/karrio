import attr
import jstruct

import karrio.core.models as models
import karrio.core.settings as settings

PackageRates = tuple[list[models.RateDetails], list[models.Message]]


@attr.s(auto_attribs=True)
class RatingMixinSettings(settings.Settings):
    """Universal rating settings mixin."""

    # Additional properties
    services: list[models.ServiceLevel] = jstruct.JList[models.ServiceLevel]

    @property
    def shipping_services(self) -> list[models.ServiceLevel]:
        return self.services
