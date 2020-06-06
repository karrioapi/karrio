"""PurplShip eshipper connection settings."""

import attr
from purplship.carriers.eshipper.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """eshipper connection settings."""

    username: str
    password: str
    id: str = None
    test: bool = False
    carrier_id: str = "eshipper"
