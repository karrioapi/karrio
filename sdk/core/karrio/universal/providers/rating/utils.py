import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.core.settings as settings

PackageRates = typing.Tuple[
    typing.List[models.RateDetails], typing.List[models.Message]
]


@attr.s(auto_attribs=True)
class RatingMixinSettings(settings.Settings):
    """Universal rating settings mixin."""

    # Additional properties
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel]

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        return self.services
