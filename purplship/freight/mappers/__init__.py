try:
    import purplship.freight.mappers.dhl as dhl
except ImportError:
    pass
try:
    import purplship.freight.mappers.fedex as fedex
except ImportError:
    pass
try:
    import purplship.freight.mappers.ups as ups
except ImportError:
    pass
