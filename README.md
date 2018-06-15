# python-soap

SOAP Python Data Structure generated from [SOAP Envelope](http://schemas.xmlsoap.org/soap/envelope/) .xml file with [generateDS](http://www.davekuhlman.org/generateDS.html) library

## You can play with it

### Installation

```shell
  pip install -e git://github.com/OpenShip/py-soap.git#egg=py-soap
```

```python
from pysoap.envelope import Envelope, Body

body = soap.Body()
body.add_anytypeobjs_(ANY_PYTHON_GENERATED_DS_OBJ_TYPE)
envelop = soap.Envelope(Body=body)

```