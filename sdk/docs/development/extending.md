## Custom Carrier

The question we are most asked is: **How to add a custom carrier?**

We have experimented and studied approximately ~25 shipping carriers API/web services to design the purplship structure as is.

The good news is that making adding a custom carrier easy fits perfectly in purplship vision.

!!! caution
    To integrate a custom carrier at this stage, you will need:
    
    - A minimal knowledge of Python
    - Write code to extend the abstract classes
    - Use the plugin/extension structure available
    - Read and Understand the carrier API documentation

---


### Steps to integrate a custom carrier

1. Generate Python data types from the carrier API schemas
    1. Generate Python data types from the carrier API schemas using the type generators bellow
    2. Package the generated data types as a library in [purplship-carriers](https://github.com/PurplShip/purplship-carriers)
    
1. Create a purplship extension package
    1. Create a new purplship extension by copying [.templates/carrier](https://github.com/PurplShip/purplship/tree/main/.templates/carrier)
        into [extensions/[carrier-name]](https://github.com/PurplShip/purplship/tree/main/extensions)
    
    2. Rename all instance for [carrier] to the appropriate carrier name you are integrating. This must be done for files
        and directories
    3. Uncomment all methods you intend to integrate  in `extensions/[carrier-name]/purplship/mappers/[carrier-name]/mapper.py`
        and `extensions/[carrier-name]/purplship/providers/[carrier-name]/__init__.py`
    4. Implement all enabled mapping functions across the module
    5. Uncomment all methods you intend to integrate `extensions/[carrier-name]/purplship/mappers/[carrier-name]/proxy`
        and implement the right HTTP calls

!!! info
    The package naming convention for extensions is `purplship.[carrier_name]`

---

### Extension anatomy 

Considering the vision we aimed to achieve with purplship, the codebase has been modularized with a clear separation of
concerns to decouple clearly the carrier integration from the integration abstraction. Additionally, each carrier
integration is done in an isolated self-contained package.

As a result, we have a very modular ecosystem where one can only select the carrier integrations of interest without
carrying the whole codebase.

**Most importantly, this flexibility allows the integration of additional carrier services under the purplship umbrella.**

!!! info
    purplship makes shipping API integration easy for a single carrier and in a multi-carrier scenario, the benefit
    is exponential.
 

#### Module convention

Two modules are required to create a purplship extension.

!!! abstract "`purplship.mappers.[carrier_name]`"
    This is where the purplship abstract classes are implemented. Also, the Metadata require to identified
    the extension is also provided there.
    
    > on runtime, purplship retrieves all mappers by going trought the `purplship.mappers` modules

!!! abstract "`purplship.providers.[carrier_name]`"
    This is where the mapping between purplship Unified API data is mapped on the carrier data type corresponding requests
    
#### extension signature

The Mapper is the cornerstone of purplship's abstraction. A `Metadata` declared at `purplship.mappers.[carrier_name].__init__`
specifies the integration classes required to define a purplship compatible extension.

```text
from purplship.core.metadata import Metadata

from purplship.mappers.[carrier_name].mapper import Mapper
from purplship.mappers.[carrier_name].proxy import Proxy
from purplship.mappers.[carrier_name].settings import Settings
import purplship.providers.[carrier_name].units as units


METADATA = Metadata(
    id="[carrier_name]",
    label="[Carrier Name]",

    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,

    # Data Units (Optional...)
    options=units.OptionCode,  # Enum of Shipping options supported by the carrier
    package_presets=units.PackagePresets, # Enum of parcel presets/templates
    services=units.ServiceType,  # Enum of Shipping services supported by the carrier
)
``` 


#### file structure

The carrier extension package folder structure looks like this

```text
extensions/carrier
├── purplship
│   ├── mappers
│   │   └── carrier
│   │       ├── __init__.py
│   │       ├── mapper.py
│   │       ├── proxy.py
│   │       └── settings.py
│   └── providers
│       └── carrier
│           ├── __init__.py
│           ├── address.py
│           ├── error.py
│           ├── pickup
│           │   ├── __init__.py
│           │   ├── cancel.py
│           │   ├── create.py
│           │   └── update.py
│           ├── rate.py
│           ├── shipment
│           │   ├── __init__.py
│           │   ├── cancel.py
│           │   └── create.py
│           ├── tracking.py
│           ├── units.py
│           └── utils.py
└── setup.py
```

!!! info
    Note that `pickup` and `shipment` modules are directories since there are often many sub to integrate such as 
    **create**, **cancel**...

!!! warning
    You don't need to create the file structure from scratch. start of by copying the template available
    at the root of the project under [.templates/carrier](https://github.com/PurplShip/purplship/tree/main/.templates/carrier)

---

#### Mappers implementation

The mapper function implementations consists of instantiating carrier specific request data types assigning

=== "Mapper"

    ```python
    # Import purplship unified API models
    from purplship.core.models import PickupRequest
    
    # Import requirements from the DHL generated data types library (py-dhl) 
    from pydhl.book_pickup_global_req_3_0 import BookPURequest, MetaData
    from pydhl.pickupdatatypes_global_3_0 import (
        Requestor,
        Place,
        Pickup,
        WeightSeg,
        RequestorContact,
    )
    
    def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable[BookPURequest]:
        weight = 0.00  # Total weight calculated from the sum of `payload.parcels[].weights`
        # ...
        request = BookPURequest(
            Request=settings.Request(
                MetaData=MetaData(SoftwareName="XMLPI", SoftwareVersion=3.0)
            ),
            schemaVersion=3.0,
            RegionCode="AM",
            Requestor=Requestor(
                AccountNumber=settings.account_number,
                AccountType="D",
                RequestorContact=RequestorContact(
                    PersonName=payload.address.person_name,
                    Phone=payload.address.phone_number,
                    PhoneExtension=None,
                ),
                CompanyName=payload.address.company_name,
            ),
            Place=Place(
                City=payload.address.city,
                StateCode=payload.address.state_code,
                PostalCode=payload.address.postal_code,
                CompanyName=payload.address.company_name,
                CountryCode=payload.address.country_code,
                PackageLocation=payload.package_location,
                LocationType="R" if payload.address.residential else "B",
                Address1=payload.address.address_line1,
                Address2=payload.address.address_line2,
            ),
            PickupContact=RequestorContact(
                PersonName=payload.address.person_name, Phone=payload.address.phone_number
            ),
            Pickup=Pickup(
                Pieces=len(payload.parcels),
                PickupDate=payload.pickup_date,
                ReadyByTime=f"{payload.ready_time}:00",
                CloseTime=f"{payload.closing_time}:00",
                SpecialInstructions=[payload.instruction],
                RemotePickupFlag="Y",
                weight=WeightSeg(
                    Weight=sum(p.weight for p in payload.parcel),
                    WeightUnit="LB"
                ),
            ),
            ShipmentDetails=None,
            ConsigneeDetails=None,
        )
    
        return Serializable(request)
    ```
    
=== "Carrier request output"
    
    ```xml
    <req:BookPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com book-pickup-global-req_EA.xsd" schemaVersion="3.">
        <Request>
            <ServiceHeader>
                
                <MessageReference>1234567890123456789012345678901</MessageReference>
                <SiteID>site_id</SiteID>
                <Password>password</Password>
            </ServiceHeader>
            <MetaData>
                <SoftwareName>XMLPI</SoftwareName>
                <SoftwareVersion>3.0</SoftwareVersion>
            </MetaData>
        </Request>
        <RegionCode>AM</RegionCode>
        <Requestor>
            <AccountType>D</AccountType>
            <AccountNumber>123456789</AccountNumber>
            <RequestorContact>
                <PersonName>Subhayu</PersonName>
                <Phone>4801313131</Phone>
            </RequestorContact>
        </Requestor>
        <Place>
            <City>Montreal</City>
            <CountryCode>CA</CountryCode>
            <PostalCode>H8Z2Z3</PostalCode>
        </Place>
        <Pickup>
            <PickupDate>2013-10-19</PickupDate>
            <ReadyByTime>10:20</ReadyByTime>
            <CloseTime>09:20</CloseTime>
            <Pieces>1</Pieces>
            <RemotePickupFlag>Y</RemotePickupFlag>
            <weight>
                <Weight>20.</Weight>
                <WeightUnit>L</WeightUnit>
            </weight>
            <SpecialInstructions>behind the front desk</SpecialInstructions>
        </Pickup>
        <PickupContact>
            <PersonName>Subhayu</PersonName>
            <Phone>4801313131</Phone>
        </PickupContact>
    </req:BookPURequest>
    ```


!!! info
    The mapping function instantiates the carrier data types like a tree to allow a global view and simplify the 
    mental relation between the `code` and the formatted data output `schema`.

### Generated schema data types

To keep to robustness and simplify the maintenance of the codebase, In purplship, we use Python data types reflecting
the schemas of carriers we want to integrate.
That said, defining every schema object's structure can be tedious, long and unproductive. Therefore, code generators
are used to generate Python data types based of the schema format definition.

- For `XML` and `SOAP` services, [generateDs](https://pypi.org/project/generateDS/) is used to generate `.xsd` files
into Python data types

!!! info ""
    Check the [generate.sh](https://github.com/PurplShip/purplship-carriers/blob/main/py-canadapost/generate.sh) file 
    to see how genereDs is used.

- For `JSON` services, [quicktype](https://github.com/quicktype/quicktype) is used to generate `.json` files
into Python data types. We then use [jstruct](https://github.com/PurplShip/jstruct) as a replacement 
for python dataclass to add automated nested object instantiation.


#### Data types libraries

We have a dedicated repo for all carriers generated data types. You can submit a PR there for a new carrier.
Check the [py-canadapost](https://github.com/PurplShip/purplship-carriers/tree/main/py-canadapost) package structure
to define yours.

!!! info
    The package naming convention for carrier data types library is `carrier.[carrier_name]`

---

### Advanced


#### Multi requests

Generally, the carrier web services expose one API endpoint to accomplish most operations describe supported by
the purplship unified interface. In some case, more than one API call are required to fulfil certain operation.

##### Abstraction

!!! abstract "Pipeline"

    - The `Pipeline` instance is like an ordered dictionary where the keys are jobs identifier and the values are 
    functions returning a `Job`.
    - The `Pipeline` exposes an `apply()` method that can be called to run sequentially the jobs provided following the
    definition order.
    
    > every job receives the response of the job runned before as first argument. This allow jobs to check the state
    > and determine if the current job should be executed or not.
    >
    > the first job receive `None`

!!! abstract "Job"

    - The `Job` is a flexible structure that accept by default an `id`, a `data` and optionally a `fallback` value
    > The `id` correspond to the job name used with a Pipeline
    >
    > The `data` is often a Serializable carrier request data.
    > 
    > When a `data` is not provided, the `fallback` is returned without further action.

##### Example

By example, the `FedEx` **Pickup** service doesn't expose a way to `Update` a pickup scheduled previously. 
In such case updating a pickup is done by cancelling **the former** and **create a new one**.
That means two calls needs to be made to update a pickup.

- Implement the `pickup_update_request` mapping function using the Pipeline typeclass

```python
from functools import partial

# Import the the requests types from the carrier generated data types
from carrier_datatypes.pickup import CarrierPickupRequest, CarrierPickupCancelRequest

from purplship.core.settings import Settings
from purplship.core.models import PickupUpdateRequest
from purplship.core.utils import Pipeline, Job, Serializable

def pickup_update_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable[Pipeline]:
    """
    Create a pickup request
    Steps
        1 - create a new pickup
        3 - cancel the old pickup
    """
    request: Pipeline = Pipeline(
        create_pickup=partial(_create_pickup, payload=payload, settings=settings),
        cancel_pickup=partial(_cancel_pickup_request, payload=payload, settings=settings),
    )
    return Serializable(request)

def _create_pickup(*args, payload, settings) -> Job:
    # create a carrier pickup request using the generated data types mapping with the PickupUpdateRequest payload
    pickup_request = Serializable(CarrierPickupRequest(...))

    return Job(id="create_pickup", data=pickup_request)

def _cancel_pickup_request(create_pickup_response: str, payload, settings) -> Job:
    # create a carrier pickup request using the generated data types mapping with the PickupUpdateRequest payload
    pickup_cancel_request = Serializable(CarrierPickupRequest(...))

    return Job(id="cancel_pickup", data=pickup_cancel_request, fallback="")
```

- Implement the `modify_pickup` proxy function by applying the pipeline

```python
from purplship.core.utils import Deserializable, Serializable, request as http, Job, Pipeline

def modify_pickup(self, request: Serializable[Pipeline]) -> Deserializable[str]:
    def process(job: Job):
        if job.data is None:
            return job.fallback

        return http(
            url=f"{self.settings.server_url}/pickup",
            data=bytearray(job.data.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )

    pipeline: Pipeline = request.serialize()
    response = pipeline.apply(process)

    return Deserializable(response)
```


#### Code reuse

Remember that extensions are distributed as Python packages. Therefore, in order to reuse a carrier integration that 
has many different services with a lot of shared functionality, it is recommended to package separately 
the `purplship.provider.carrier` module that can be used as a dependency to many variation 
of `purplship.mappers.carrier_service` modules in their own respective packages.

!!! info ""
    By example, there are two `FedEx` related extension `purplship.fedex` and `purplship.fedex_express` because we can
    reuse most of the `purplship.fedex` package implementation in a `purplship.fedex_freight` extension later on.


#### Helpers

After integrating and experimenting with multiple carriers services, some data structure manipulation lead to the 
implementation of utilities functions located in `purplship.core.utils` module.

- `DICTPARSE`

Usage: 
```python
from purplship.core.utils import DP
```

```text
Python Library Documentation: class DICTPARSE in module purplship.core.utils.dict

class DICTPARSE(builtins.object)
 |  Static methods defined here:
 |  
 |  jsonify(entity: Union[dict, ~T]) -> str
 |      Return a JSON.
 |      
 |      recursively parse a data type using __dict__ into a JSON
 |  
 |  to_dict(entity: Any) -> dict
 |      Return a python dictionary.
 |      
 |      recursively parse a data type using __dict__ into a JSON

```


- `XMLPARSER`

Usage: 
```python
from purplship.core.utils import XP
```

```text
Python Library Documentation: class XMLPARSER in module purplship.core.utils.xml

class XMLPARSER(builtins.object)
 |  Static methods defined here:
 |  
 |  build(element_type: Type[~T], xml_node: purplship.core.utils.xml.Element = None) -> Union[~T, NoneType]
 |      Build xml element node into type class
 |      
 |      :param element_type: The xml node corresponding type (class)
 |      :param xml_node: the xml node source
 |      :return: None if the node is None else an instance of GenerateDS XML Element class
 |  
 |  bundle_xml(xml_strings: List[str]) -> str
 |      Bundle a list of XML string into a single one.
 |      => <wrapper>{all the XML trees concatenated}</wrapper>
 |      
 |      :param xml_strings:
 |      :return: a bundled XML text containing all the micro XML string
 |  
 |  export(typed_xml_element: Type[purplship.core.utils.xml.GenerateDSAbstract], **kwds) -> str
 |      Serialize a class instance into XML string.
 |      => Invoke the export method of generated type to return the subsequent XML represented
 |      
 |      :param typed_xml_element: a GeneratedDS XML Element instance
 |      :param kwds: exporting method arguments
 |      :return: an XML text
 |  
 |  jsonify_xml(xml_str: str) -> dict
 |      Turn a XML string into a Python Dictionary
 |      
 |      :param xml_str:
 |      :return: a dictionary
 |  
 |  to_xml(xml_str: str) -> purplship.core.utils.xml.Element
 |      Turn a XML text into an (lxml) XML Element.
 |      
 |      :param xml_str:
 |      :return: Node Element
 |  
 |  xml_tostring(xml_element: purplship.core.utils.xml.Element, encoding: str = 'utf-8') -> str
 |      Turn a XML Element into a XML text.
 |      
 |      :param xml_element: XML ELement
 |      :param encoding: the string format encoding
 |      :return: Node Element

```

- `DATEFORMAT`

Usage: 
```python
from purplship.core.utils import DF
```

```text
Python Library Documentation: class DATEFORMAT in module purplship.core.utils.datetime

class DATEFORMAT(builtins.object)
 |  Static methods defined here:
 |  
 |  date(date_str: str = None, current_format: str = '%Y-%m-%d')
 |  
 |  fdate(date_str: str = None, current_format: str = '%Y-%m-%d')
 |  
 |  fdatetime(date_str: str = None, current_format: str = '%Y-%m-%d %H:%M:%S', output_format: str = '%Y-%m-%d %H:%M:%S')
 |  
 |  ftime(time_str: str, current_format: str = '%H:%M:%S', output_format: str = '%H:%M')
 |  
 |  ftimestamp(timestamp: Union[str, int] = None)

 
```

- `STRINGFORMAT`

Usage: 
```python
from purplship.core.utils import SF
```

```text
Python Library Documentation: class STRINGFORMAT in module purplship.core.utils.string

class STRINGFORMAT(builtins.object)
 |  Static methods defined here:
 |  
 |  concat_str(*args, join: bool = False)


```

- `Other`

Usage: 
```python
from purplship.core.utils import [function]
```

```text
FUNCTIONS
    exec_async(action: Callable[[~S], ~T], sequence: List[~S]) -> List[~T]
    
    exec_parrallel(function: Callable, sequence: List[~S], max_workers: int = None) -> List[~T]
        Return a list of result for function execution on each element of the sequence.
    
    gif_to_pdf(gif_str: str) -> str
    
    request(decoder: Callable = <function decode_bytes at 0x7f99cc71c3a0>, on_error: Callable[[urllib.error.HTTPError], str] = None, **args) -> str
        Return an HTTP response body.
        
        make a http request (wrapper around Request method from built in urllib)
```
