from abc import ABC


class Client(ABC):
    """ 
    Unitied API carrier Client (Interface)
    ...

    Attributes
    ----------
    server_url : str
        a carrier server url address (can be test or prod) 
    carrier_name : str
        a custom name to identified the carrier client instance (set to carrier name by default) 
    """

    server_url: str
    carrier_name: str
