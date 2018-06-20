from .datatypes import *

class Quotes():
    """ manage quotes operations """

    def create(**args) -> QuoteRequest:
        """ Create a quote request payload """
        return QuoteRequest(**QuoteRequestType(**args)._asdict())
