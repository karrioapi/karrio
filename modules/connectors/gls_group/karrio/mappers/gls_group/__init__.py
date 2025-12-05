"""Karrio GLS Group mapper module."""
from karrio.mappers.gls_group.mapper import Mapper
from karrio.mappers.gls_group.proxy import Proxy
from karrio.mappers.gls_group.settings import Settings

# Re-export METADATA for gateway registration
from karrio.plugins.gls_group import METADATA
