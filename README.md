# python-soap

SOAP Python Data Structure generated from [SOAP Envelope](http://schemas.xmlsoap.org/soap/envelope/) .xml file with [generateDS](http://www.davekuhlman.org/generateDS.html) library

## Installation

```bash
pip install -f https://git.io/purplship py-soap
```


```python
from pysoap.envelope import Envelope, Body

body = soap.Body()
body.add_anytypeobjs_(ANY_PYTHON_GENERATED_DS_OBJ_TYPE)
envelop = soap.Envelope(Body=body)

```