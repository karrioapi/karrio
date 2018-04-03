# python-soap

SOAP Python Data Structure generated from [SOAP Envelope](http://schemas.xmlsoap.org/soap/envelope/) .xml file with [generateDS](http://www.davekuhlman.org/generateDS.html) library

```python
from python_soap.soap.envelope import Envelope, Body

body = soap.Body()
body.add_anytypeobjs_(ANY_PYTHON_GENERATED_DS_OBJ_TYPE)
envelop = soap.Envelope(Body=body)

```