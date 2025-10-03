# DTDC API (Text)

## DTDC Cancellation API

(for B2C & Express Customer)
Ver. 2.0

www.dtdc.com

1

Overview:

This API allows customers to cancel consignments by providing the AWB (Airway Bill)
number(s) and the associated customer code.

Base URLs

● Staging URL:

https://alphademodashboardapi.shipsy.io/api/customer/integration/consignment/cancel

● Production URL:

http://pxapi.dtdc.in/api/customer/integration/consignment/cancel

Method

● HTTP Method: POST

Headers

● Content-Type: application/json
● api-key: <API KEY> (replace <API KEY> with the actual key provided)

Request Body:-

{

}

"AWBNo": [

"D78326386"

],
"customerCode": "<customer_code>"

Request Field Descriptions

Field

Type

Mandatory

Description

AWBNo

Array of
Strings

Yes

List of Airway Bill numbers (AWBs) that need to be canceled.

customerCode

String

Yes

The unique code assigned to the customer for identification
purposes.

www.dtdc.com

2

Example Request

curl --location '<url>' \
--header 'api-key: <API-key>' \
--header 'Content-Type: application/json' \
--data '{

"AWBNo": [

"D78326386"

],
"customerCode": "<customer_code>"

}'

Response:-

Example Request

{

"status": "OK",
"success": true,
"successConsignments": [

"success": true,
"reference_number": "7V000008715"

{

}

]

}

Detailed Explanation of Key Fields

1. status:

○ This ﬁeld shows the overall status of the API request.
○ OK indicates that the API processed the request correctly without errors.

2. success:

○ A boolean value indicating whether the entire request was successful.
○ If true, the request was processed successfully; if false, it means there was

an issue with the request.

3. successConsignments:

○ An array containing objects that provide details about each consignment that

was successfully processed.

○ Each object inside this array contains ﬁelds speciﬁc to the consignment's

processing status.

www.dtdc.com

3

4. success (inside successConsignments):

○ This boolean indicates whether the individual consignment was processed

successfully.

○ A value of true means the consignment was successfully canceled or

processed.

5. reference_number:

○ This string contains the reference number of the consignment that was

processed successfully.

○ The reference number helps identify which consignment was aﬀected by the

request.

Response

200

Code Remarks

Each consignment will be processed independently.
For each consignment, “success”key will be either true or false.
If success is true for a consignment, then the consignment is successfully entered
into the DTDC system.
If success is false, the consignment is not entered
(in case of false, the response contains an error message reason)

400

There is some validation error in the overall request format. In this case,
completerequest is rejected.

401

There is an authentication error.

www.dtdc.com

------------------------------

## DTDC Order Upload API

(for B2C & Express Customer)
Ver. 2.0

www.dtdc.com

1 Overview:

This API allows customers to create consignment requests by submitting shipment details in
JSON format. The details include the origin, destination, package speciﬁcations, and additional
relevant information.

Base URLs

●  Staging URL:

https://demodashboardapi.shipsy.in/api/customer/integration/consignment/softdata

●  Production URL:

https://dtdcapi.shipsy.io/api/customer/integration/consignment/softdata

Method

●  HTTP Method: POST

Headers

●  Content-Type: application/json
●  api-key: <API KEY> (replace <API KEY> with the actual key provided)

Request Body:-

➔  Sample request body for the Single Parcel shipments.

{
    "consignments": [
        {
            "customer_code": "customer code",
            "service_type_id": "B2C PRIORITY",
            "load_type": "NON-DOCUMENT",
            "description": "test",
            "dimension_unit": "cm",
            "length": "70.0",
            "width": "70.0",
            "height": "65.0",
            "weight_unit": "kg",
            "weight": "17.0",
            "declared_value": "5982.6",
            "num_pieces": "1",

www.dtdc.com

                       2










            "origin_details": {
                "name": "TEST ENTERPRISES",
                "phone": "0000000000",
                "alternate_phone": "0000000000",
                "address_line_1": "dummy sender",
                "address_line_2": "",
                "pincode": "110046",
                "city": "New Delhi",
                "state": "Delhi"
            },
            "destination_details": {
                "name": "TEST ",
                "phone": "0000000000",
                "alternate_phone": "0000000000",
                "address_line_1": "test receiver",
                "address_line_2": "",
                "pincode": "636010",
                "city": "SALEM",
                "state": "Tamil Nadu"
            },
            "return_details": {
                "address_line_1": "Test_Address_Return",
                "address_line_2": "Test_Address_Return line 2",
                "city_name": "DELHI",
                "name": "Test_Return",
                "phone": "0000000000",
                "pincode": "248001",
                "state_name": "DELHI",
                "email": "amisha.arora@test.co.in",
                "alternate_phone": "0000000000"
            },
            "customer_reference_number": "order_id",
            "cod_collection_mode": "",
            "cod_amount": "",
            "commodity_id": "99",
            "eway_bill" : "12345678",
            "is_risk_surcharge_applicable": “false”,
            "invoice_number": "AB001",
            "invoice_date": "14 Oct 2022",
            "reference_number": ""
        }
    ]
}

www.dtdc.com

                       3










➔  Sample request body for the Multi Parcel shipments.

{
    "consignments": [
        {
            "customer_code": "customer code",
            "service_type_id": "B2C PRIORITY",
            "load_type": "NON-DOCUMENT",
            "description": "test",
            "dimension_unit": "cm",
            "length": "70.0",
            "width": "70.0",
            "height": "65.0",
            "weight_unit": "kg",
            "weight": "17.0",
            "declared_value": "5982.6",
            "num_pieces": "1",
            "origin_details": {
                "name": "TEST ENTERPRISES",
                "phone": "0000000000",
                "alternate_phone": "0000000000",
                "address_line_1": "dummy sender",
                "address_line_2": "",
                "pincode": "110046",
                "city": "New Delhi",
                "state": "Delhi"
            },
            "destination_details": {
                "name": "TEST ",
                "phone": "0000000000",
                "alternate_phone": "0000000000",
                "address_line_1": "test receiver",
                "address_line_2": "",
                "pincode": "636010",
                "city": "SALEM",
                "state": "Tamil Nadu"
            },
            "return_details": {
                "address_line_1": "Test_Address_Return",
                "address_line_2": "Test_Address_Return line 2",
                "city_name": "DELHI",
                "name": "Test_Return",
                "phone": "0000000000",
                "pincode": "248001",

www.dtdc.com

                       4










                "state_name": "DELHI",
                "email": "amisha.arora@test.co.in",
                "alternate_phone": "0000000000"
            },
            "customer_reference_number": "order_id",
            "cod_collection_mode": "",
            "cod_amount": "",
            "commodity_id": "99",
            "eway_bill" : "12345678",
            "is_risk_surcharge_applicable": “false”,
            "invoice_number": "AB001",
            "invoice_date": "14 Oct 2022",
            "reference_number": "",
            "pieces_detail": [
                {
                    "description": "Test Product",
                    "declared_value": "200",
                    "weight": "0.5",
                    "height": "5",
                    "length": "5",
                    "width": "5"
                }
            ]
        }
    ]
}

Field Descriptions

Field

Type

Mandatory

Description

consignments

customer_code

service_type_id

load_type

description

dimension_unit

length

width

height

www.dtdc.com

Array of
Object

String

String

String

String

String

String

String

String

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

List of consignment objects, each containing details of a
shipment.

Unique code assigned to the customer.

Type of service required ( list attached below)

Type of load (e.g., NON-DOCUMENT).

Description of the consignment.

Unit for dimensions (cm). We accept only “CM”

Length of the package.

Width of the package.

Height of the package.

                       5











weight_unit

weight

declared_value

num_pieces

String

String

String

String

origin_details

Object

name

phone

alternate_phone

address_line_1

address_line_2

email

pincode

city

state

String

String

String

String

String

String

String

String

String

destination_details

Object

name

phone

alternate_phone

address_line_1

address_line_2

email

pincode

city

state

String

String

String

String

String

String

String

String

String

return_details

Object

name

address_line_1

address_line_2

email

city_name

phone

pincode

state_name

alternate_phone

String

String

String

String

String

String

String

String

String

customer_reference_n

String

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

No

No

Yes

Yes

Yes

No

Yes

Yes

No

No

Yes

Yes

Yes

Yes

No

Yes

Unit for weight (kg). We accept only “KG”

Weight of the package.

Declared value of the consignment.

Number of parcels/boxes

Details about the origin of the consignment.

Name of the sender.

Phone number of the sender.

Alternate phone number of the sender.

First line of the sender's address.

Second line of the sender's address.

Email of the sender

Pincode of the sender's location.

City of the sender.

State of the sender.

Details about the destination of the consignment.

Name of the receiver.

Phone number of the receiver.

Alternate phone number of the receiver.

First line of the receiver's address.

Second line of the receiver's address.

Email of the receiver

Pincode of the receiver's location.

City of the receiver.

State of the receiver.

Details about the return address for the consignment.

Name for the return contact.

First line of the return address.

Second line of the return address.

Email for the return contact.

City of the return address.

Phone number for the return contact.

Pincode for the return address.

State of the return address.

Alternate phone number for the return contact.

Reference number assigned by the customer for tracking

www.dtdc.com

                       6










umber

purposes.

cod_collection_mode

String

cod_amount

String

No

No

The mode of COD collection will be "CASH" , if
applicable. (Mandatory for COD only)

Amount to be collected for COD shipments.
(Mandatory for COD only)

commodity_id

String

Yes

eway_bill

String

No

Identifier for the commodity type being shipped.
(list attached below)
you can pass ID from list or mention the commodity name

E-Way bill number for the shipment, if applicable.
(12 characters limit)

is_risk_surcharge_app
licable

Boolean

Yes

Indicates whether a risk surcharge applies (true or false).

invoice_number

invoice_date

String

String

reference_number

String

pieces_detail

Array of
Object

description (pieces)

String

declared_value
(pieces)

weight (pieces)

height (pieces)

length (pieces)

width (pieces)

String

String

String

String

String

Example Request

No

No

No

No

No

No

No

No

No

No

Invoice number associated with the consignment.

Date of the invoice.

Reference number for the consignment, if available. You
can pass awb number here.

Array containing detailed information about each
parcel/piece in the consignment. (mandatory for MPS)

Description of the individual piece. (mandatory for MPS)

Declared value of the individual piece. (mandatory for
MPS)

Weight of the individual piece. (mandatory for MPS)

Height of the individual piece. (mandatory for MPS)

Length of the individual piece. (mandatory for MPS)

Width of the individual piece. (mandatory for MPS)

curl -X POST <URL> \
     -H "Content-Type: application/json" \
     -H "api-key: <API KEY>" \
     -d '{...}' # JSON payload as described above

List of Commodity_id:
https://docs.google.com/spreadsheets/d/158LuKmF8mHXSQfXcSE-U_NVeUpz-O1Lu
Nlc1ualKEeI/edit?usp=sharing

www.dtdc.com

                       7










List of Service_type_id:
https://docs.google.com/spreadsheets/d/1pYajATrmH-lay_e7oS47lx_UXNvrtGcL2MoQ
693mmuk/edit?usp=sharing

Response:-

Example Request

{
    "status": "OK",
    "data": [
        {
            "success": true,
            "reference_number": "100008518801",
            "courier_partner": null,
            "courier_account": "",
            "courier_partner_reference_number": null,
            "chargeable_weight": 0.025,
            "self_pickup_enabled": true,
            "customer_reference_number": "#100001",
            "pieces": [
                {
                    "reference_number": "100008518801001",
                    "product_code": ""
                }
            ],
            "barCodeData": ""
        }
    ]
}

Explanation of Key Fields

1.  status: The status of the API call, such as "OK" for a successful request.
2.  data: Contains an array of consignment details, where each object represents a

consignment processed by the API.

3.  success: A boolean value indicating whether the consignment was processed

successfully.

www.dtdc.com

                       8












Response

200

Code Remarks

Each consignment will be processed independently.
For each consignment, “success”key will be either true or false.
If success is true for a consignment, then the consignment is successfully entered
into the DTDC system.
If success is false, the consignment is not entered
(in case of false, the response contains an error message reason)

400

There is some validation error in the overall request format. In this case, the
complete request is rejected.

401

 There is an authentication error.

www.dtdc.com

------------------------------

## DTDC Shipping Label API WS

(for E-commerce, GS, LTL &
Express based Customer)
Ver. 2.0

Introduction:

This API allows you to generate shipping labels for your packages. You can choose to receive
the label in PDF format or as a Base64 encoded string.

Base URL: Replace <API_BASE_URL> with the actual base URL provided below.

Live environment ::   https://pxapi.dtdc.in

Staging environment : https://alphademodashboardapi.shipsy.io

Endpoint : <base_url>/api/customer/integration/consignment/shippinglabel/stream

Method: GET

Authentication: Authentication is done using an API key. Include the API key in the request
headers as follows:

--header 'api-key: YOUR_API_KEY'

Request Parameters:

● reference_number (Required): The unique reference number assigned to the

shipment within Shipsy.

● label_code (Required): The speciﬁc code for the type of shipping label you want to

generate.

● label_format (Optional, defaults to pdf): The format of the downloadable label.

Supported Label Codes: The following are the supported label codes along with their
descriptions:

Label Description

Shipping Label A4

Shipping Label A6

label_code

SHIP_LABEL_A4

SHIP_LABEL_A6

Shipping Label POD

SHIP_LABEL_POD

Shipping Label 4x6

SHIP_LABEL_4X6

Routing Label A4

ROUTE_LABEL_A4

Routing Label 4x4

ROUTE_LABEL_4X4

Invoice Print (for International orders only)

INVOICE

Address Label A4 (for Document)

ADDR_LABEL_A4

Address Label 4x2 (for Document)

ADDR_LABEL_4X2

Supported Label Formats:

● pdf: Generates a downloadable PDF ﬁle containing the shipping label.
● base64: Returns the label data as a Base64 encoded string, which can be decoded

and used within your application.

Curl Examples:-

Generate PDF Label:

curl --location
'https://pxapi.dtdc.in/api/customer/integration/consignment/shippinglabel/strea
m?reference_number=<awb_no>&label_code=SHIP_LABEL_4X6&label_format=pdf' \
--header 'api-key: <api-key>

Generate Base64 Encoded Label:

curl --location
'https://pxapi.dtdc.in/api/customer/integration/consignment/shippinglabel/strea
m?reference_number=<awb_no>&label_code=SHIP_LABEL_4X6&label_format=base64' \
--header 'api-key: <api-key>'

Curl Explanation:

● reference_number=<awb_no>: This parameter speciﬁes the reference number of the
shipment for which you want to generate a label. Replace<awb_no> with your actual
AWB/shipping/reference number.

● label_code=SHIP_LABEL_4X6: This parameter speciﬁes the code for the desired
shipping label format. In this example,SHIP_LABEL_4X6 is used, indicating a 4" x 6"
label. Refer to above documentation for availablelabel_code options.

● label_format=pdf or label_format=base64: This parameter speciﬁes the format

of the downloadable label.

Response:

● PDF Format: The response will be the raw PDF data of the generated shipping label.
You will need to save this data to a.pdf ﬁle using an appropriate method depending
on your programming language or environment.

Sample_labels:-

1. SHIP_LABEL_4X6

2. SHIP_LABEL_A4 / SHIP_LABEL_A6 / SHIP_LABEL_POD

3. ROUTE_LABEL_A4 / ROUTE_LABEL_4X4

4. ADDR_LABEL_A4 / ADDR_LABEL_4X2

5. INVOICE (for international orders only)

● Base64 Format: The response will be a string containing the Base64 encoded

representation of the shipping label data. You will need to decode this string using a
Base64 decoder in your application to obtain the label data for further use.

Sample_response:-

{

"referenceNumber": "7X100761088",
"label":

"JVBERi0xLjQKJfbk/N8KMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovVmVyc2lvbiAvMS41Ci9QYWdlcyAyIDAgUgovTmFtZXMgMyAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL01vZERhdGUgKEQ6MjAyNDA0MDExN
jUxMDArMDUnMzAnKQovQ3JlYXRvciAoSmFzcGVyUmVwb3J0cyBMaWJyYXJ5IHZlcnNpb24gNi4yMC42LTVjOTZiNmFhOGEzOWFjMWRjNmI2YmVhNGI4MTE2OGUxNmRkMzkyMzEpCi9DcmVhdGlvbkRhdGUgKEQ6MjAyNDA
0MDExNjUxMDArMDUnMzAnKQovUHJvZHVjZXIgKE9wZW5QREYgMS4zLjMwLmphc3BlcnNvZnQuMykKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFs1IDAgUl0KL0NvdW50IDEKPj4KZW5kb2JqC
jMgMCBvYmoKPDwKL0Rlc3RzIDYgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9UYWJzIC9TCi9Hcm91cCA3IDAgUgovQ29udGVudHMgOCAwIFIKL1R5cGUgL1BhZ2UKL1Jlc291cmNlcyA5IDAgUgovUGFyZW50IDIgMCB
SCi9NZWRpYUJveCBbMC4wIDAuMCA0OTMuMCA3MDAuMF0KL0Nyb3BCb3ggWzAuMCAwLjAgNDkzLjAgNzAwLjBdCi9Sb3RhdGUgMAo+PgplbmRvYmoKNiAwIG9iago8PAovTmFtZXMgWygxMjIwMTQpIFs1IDAgUiAvWFlaI
DI5IDM5MS4zIDBdCiAoMzAtMDMtMjAyNCkgWzUgMCBSIC9YWVogMzgzIDYyNS4wNCAwXQogKDMwLTAzLTIwMjQgMTQ6MzQ6NTYpIFs1IDAgUiAvWFlaIDQxNy44NiA1OS44NiAwXQogKDQ3MC44MikgWzUgMCBSIC9YWVo
gMzgzIDYxMi4wNCAwXQogKDdYKSBbNSAwIFIgL1hZWiAzNDIuMiA0NzYuMDIgMF0KKDdYMTAwNzYxMDg4KSBbNSAwIFIgL1hZWiAzMjguMDcgNTAyLjYxIDBdCiAoN1gxMDA3NjEwODgwMDAwMDEwMDA5MTAyNDEyMjAxN
DAyNSkgWzUgMCBSIC9YWVogMTAzLjg5IDExNy4wOCAwXQogKEFSKSBbNSAwIFIgL1hZWiA4MyAzMjYuMTUgMF0KIDw0MTcwNkY2QzZDNkYyMDRDNkY2NzY5NzM3NDY5NjM3MzJDMjAwQTU1NkU2OTc0NjU2MzY4MjA0Mzc
5NjI2NTcyMjA1MDYxNzI2QjIwMzY3NDY4MjA0NjZDNkY2RjcyMjAzMTMyMzIzMDMyMzEwQT4gWzUgMCBSIC9YWVogMzEgNjMyLjY1IDBdCiAoQjJDIHByaW9yaXR5KSBbNSAwIFIgL1hZWiAzMiAzNTEuNDYgMF0KKEJpb
GwgU2VuZGVyICkgWzUgMCBSIC9YWVogMzI0IDU3MS4wNCAwXQogKERTVCkgWzUgMCBSIC9YWVogMzcwIDI1Ny4zMSAwXQogKERUREMpIFs1IDAgUiAvWFlaIDMwIDI3Ni43OSAwXQogPDQ0NjU2NTcwNjE2QjIwNEI3NTZ
ENjE3MjJDMjAwQTUzNjU2Mzc0NkY3MjIwMzMzOTIwMzEzMjMyMzAzMTM0MEE0NzU1NTI0NzQxNEY0RTJDMjA1MDQ5NEUzQTMxMzIzMjMwMzEzNDJDMjA0ODQxNTI1OTQxNEU0MTJDMjA0OTRFPiBbNSAwIFIgL1hZWiAzM
SA1MjEuNzkgMF0KIChEb24ndCBjb2xsZWN0IG1vbmV5KSBbNSAwIFIgL1hZWiAzMjMuNSAxOTQuOTMgMF0KKEUtV2F5IEJpbGw6ICkgWzUgMCBSIC9YWVogMzk1LjMyIDM0OS4zNSAwXQogKEZST006KSBbNSAwIFIgL1h
ZWiAzMSA2NDIuNzIgMF0KIChJbnYgRGF0ZSA6KSBbNSAwIFIgL1hZWiAzMjQgNTg2LjA0IDBdCiAoSW52IE5vIDopIFs1IDAgUiAvWFlaIDMyNCA1OTkuMDQgMF0KIChKUl9QQUdFX0FOQ0hPUl8wXzEpIFs1IDAgUiAvW
FlaIDAgNzEwIDBdCihMMDQpIFs1IDAgUiAvWFlaIDM2NC4zMiAyODkuNzIgMF0KIChMMjcpIFs1IDAgUiAvWFlaIDM2NC4zMiAyNDUuNzIgMF0KIChMViA6ICkgWzUgMCBSIC9YWVogNDM2IDg3Ljg1IDBdCiAoTW9kZTo
gKSBbNSAwIFIgL1hZWiAzMiAzMjUuOTYgMF0KIChPUkcpIFs1IDAgUiAvWFlaIDM2Ny45MiAzMDAuMzEgMF0KKFBjczogMDAxICBPRiAgMDAxKSBbNSAwIFIgL1hZWiAzNDYuODIgMzI0LjY1IDBdCiAoUHJlcGFpZCkgW
zUgMCBSIC9YWVogMzYzLjEgMjE0LjkzIDBdCiAoUHJvZHVjdCBEZXNjcmlwdGlvbjopIFs1IDAgUiAvWFlaIDMxIDMwMy4xNSAwXQogKFJlZi4gTm86IDU2ODM5OTI3MjM2ODYpIFs1IDAgUiAvWFlaIDMyIDg4LjM1IDB
dCiAoU2hpcCBEYXRlIDopIFs1IDAgUiAvWFlaIDMyNCA2MjUuMDQgMF0KKFNoaXAgdmFsdWUgOikgWzUgMCBSIC9YWVogMzI0IDYxMi4wNCAwXQogKFRPIDopIFs1IDAgUiAvWFlaIDI3IDU1OS4xNSAwXQogKFRPOiApI
Fs1IDAgUiAvWFlaIDMwIDUzNS44NiAwXQogKFdlaWdodDogMC4yLzAuMDAwKSBbNSAwIFIgL1hZWiAxOTIuMTMgNTYuNjUgMF0KXQo+PgplbmRvYmoKNyAwIG9iago8PAovUyAvVHJhbnNwYXJlbmN5Ci9UeXBlIC9Hcm9
1cAovQ1MgL0RldmljZVJHQgo+PgplbmRvYmoKOCAwIG9iago8PAovTGVuZ3RoIDE1NDgKL0ZpbHRlciAvRmxhdGVEZWNvZGUKPj4Kc3RyZWFtDQp4nM1aW1PbOBR+z6/Q23ZnQNXFkiXegBS2uy3QkG67s7MPWeNAtg6mI
W2n/36PZMmxRe04ODN1mcn5wEf6jo6lc1H6eXQyHXGJpIzQ9Gb0ajp6N2Lod/NXigj8mM+YEDRdjl6eUUQBzUcvfp3+Z3Q3KgQly+ogFiMRcUxFMZAhKs1AYh+vbkcvppfoyMxC0O0PZvr7H5A31hLghB8YQtE3  +4dijsm
5V+IxR5EgaDmKotiirEShTOwTAcZkJQplYmcsdDwKZVKyZiUKZTKaD9i2a+++rf5lxLxNWAGMBZB5UBeJ/bPU7jmAukjMPPZxIaufiePInKx+Gi/+bAt28pVmzlIAmQd1UVhK48gpGBRKa1Gh4kBdJI4rc7L66Xw2CEt28
h0n3mSDshKFsjCbM+V1AIXSmlWoOFAXiSfMPKgL58RhmbSbN5n2pjNdmqVRKJ3pwm8Cg0JZmCbcJjCgLhJPmHlQF96bgzJpN2/ClMtOZhkkIup0DAqlNa1QcaAuti9tPjyTdvKm4MqZblBWolC6oB5xH9UBhbII7FbFgbp
IPGHmQV04bw7LpGd4k1NvukehTOyTwi6PQrlXbw7FpO7e5Ao4hbA7gViUlSiUSfFEEa8DKJRJMaPV8SiUScmalSiUtpocrG077VbzypadDpFFbgncmV6XxdawKg7UxfatMx+eSaU3PyMlrf84xQLOg4pAQ2BoBpIlerlY3
hI0ztG7auNV0YHOyw6Hvu7Qg9amjVMkOcMxq3d7m6btbHL5tmvX1kIiKMGxLjtDWicZp+nD7BP648tytjqokNXniHSMtWqa4zpN1vkKcY0oY4RGzdMogWnjNOfvJ+fHlxcH6Or1xVEx0wH67Xjy1/HF8QF6fdHfFZJxLIX
3t67THz/kWZajN/nt4nG9SB6bvSEp9NpxwzTv7xfrNLlDp9//TVfoarb6hOT6Dp1lObjIrIrRvguJJFYMDCHlYsCZUd2Mq+TxCBFCEbo8Qwb0JQVCDhtdNl0xnLBT9LBa5KvF+vt+rhpcx7McMdh6riVyKJSJfeKKeYdCu
b3e39Z5zYdn0g6pwNm17NSEdmnBOq2vg5/mA7atkhwoZnGxmQ2AiEpphKPIJoePc/okN2w04MTA2XG5oUT2cHTI376Ha7tr2XbvwFruDFjLPc38p1tQ2eBNoYlqhqF2jVgltofh8EO6uL1bQ0TE7CXBhJCe4TCiMYYsH2n
z2ZC/OTkk/BACfpkQy9EcbIBtqDCz2X8zhkZHPDoS8jnmlbuJMzguMobtp9ChUmiVwosMlAXsOPKjipxB8WNHm1vUyOEM3kPzCMOmsamUDeaxxGLLCMPBY11yGNw2IopYyWHwhqNj8oIyjQpMoqZ3dX23eEDj2TrtfE/ey
kXYNq6vs+zLfsiE0i1kr++/oot8P0Tg9HaivTlQSNpCdbLIMnSd3t+kq75cpqdq3RhPD3EfqtZ9AY0i1HXPO/n7VqyGOi5RLLDalJqsbvebP/u/cy2wrTBjzBt5Xh1+mH1H5uV3o7MpmyOXsqHjU9w2Q5q6nM2e5OyKChh
BlUZF0i5Re0fHFCax7XIkLd9yXF9F/JESEktKlOrrNIIENDRKNjlsetn/LAKLxrqx6n+b36S9SSBzQ3gnEF2Y54lJ6LU99RRQ2TEh/ddbQvrvtwCFcr+VZsHlUSh9FTxM23brMhgVfg1U+DVQgUKZdFpnF/s8a1aiUJb+H
aRtHYpcLmNsSmaILXwTW0T9lFxOzvueRTh4DM5jM8f4etqXQ0Ym2DMpyssv+C0o2N+Q3gnX0UCx2ULD4p40TCMuNOaegQdB+MmV2DPjMBRfzalxks4xlHlHUDgprjWLGZfqWU1Eta8ikFygiTVFi2raDpV0Rsw/+I1oGBI
V6yZMNFtBG6p9c7tBTRw0DSK3ZX6Tqr0VoD5mOuVOq1Pc3qA1/5+Z40n/C0em4haGq1V +8yVZo3H6mKwWD+tFft87l0qOzbeIFGtevjIe0qYPs8VN7y3JoQWjasPEnjCN8/tf1ijJsyyFZS7z +7Tr1WBLzWPjhi4XF95nT
8enwyih96D4PwlAdwsNCmVuZHN0cmVhbQplbmRvYmoKOSAwIG9iago8PAovQ29sb3JTcGFjZSAxMCAwIFIKL0ZvbnQgMTEgMCBSCi9YT2JqZWN0IDw8Ci9YZjEgMTIgMCBSCi9YZjIgMTMgMCBSCi9pbWcwIDE0IDAgUgo
+Pgo+PgplbmRvYmoKMTAgMCBvYmoKPDwKL0NTIC9EZXZpY2VSR0IKPj4KZW5kb2JqCjExIDAgb2JqCjw8Ci9GMSAxNSAwIFIKL0YyIDE2IDAgUgo+PgplbmRvYmoKMTIgMCBvYmoKPDwKL0xlbmd0aCAxNTYwCi9TdWJ0e
XBlIC9Gb3JtCi9GaWx0ZXIgL0ZsYXRlRGVjb2RlCi9UeXBlIC9YT2JqZWN0Ci9NYXRyaXggWzEgMCAwIDEgMCAwXQovRm9ybVR5cGUgMQovUmVzb3VyY2VzIDw8Cj4+Ci9CQm94IFswIDAgMjY0IDQzXQo+PgpzdHJlYW0
NCnicbZlNjiRFDIX3dYo+Qjr+4wpILFixQOwQIDQgDRuuT+XE+5wj9VNLbak7vnLYYUe+dH19XR+tfvz9NtfHl1cZLe37z19ef75+fv3zio//XuXjh/eiv15xffz4+uXX6+O319f3P  +6ff//gU+I6WJyP47c+6vdvf7ju9
QFQBJRvS8XFd0i6OEvfSBVSz9qCMV6qEEUTJzrI6rw0IUPIOGsbxngZQqaQedYOjPEyD1Li/PNtr+/IabycpW9EWyg6qcB89lIUS+lC+lnbMMZLF6ItlLMjyO68EMsSss7aiTFe1kGqdl0VxMJ89lIVftU513PsImsYL1U
FU7XreoKALM6Lwq/aQj07guzOC7FsIfusXRjjZR+kqczbqXrIbbw09UvTrtsJQmRz/dIUflOZt1P1kK5fmvqlqTTaqRRI1y9NNdaUm3ZSBelqrCnJTblpJ1WQrsaaktyUm3ZSBbmcFyW5a9ddQWzMZy9d4Xftup8gRPZqv
HSF39Xl/TQ9ZHNedF107bqfICCH86Lwu3bdTxCQrsa6wh8653GOHdLV2FDBDAU6Ttwih+uXoYwNHdo4ZwjpMjZ0+kOBjhM3pDv9oYwNBTpO3JAuY0MZm+qMeRoF0mVsqsWmdj1PECKne4pNhT91zvMcO6Trl6mCmdr1PEF
Aun6ZCn9q1/MEAemeL1PhL+16KYiF+exlKfylq3Sdm1XkcjfM0p28dGjrnCGku5OXTn9p1+sEAelOfyn8pSfJOg8WSHf6S4+kpUDXiRtyOi/K2Naut4JYmM9etsLfOud9jl3kdk/krYLZCnSfuCFdv2xlbCvQfeKGdBnby
tjWrvcJAtJlbBO+LoZ97glI1y9bN0xcKfpOrcC6O0aLbyqgpH2uK +1nZ1p+c8i/SyoueVdvWn5zqLNLIit5KwOvCbfhttbPtM4fWQniC/a30xp/QXypiBG28GHjS1WcGhepmry7uCN1bgpd9GryVuum2I0Ft7R+pHX+VGB
RqJai807e9ZiW31y+KSD4r7TGXyEvhXopvC+UtM4f9YLWDWnfh7f1gnAOBG9IAD +8U4+Beo5CnRXVSfLuutLy+22IOpMUfnjbf+joqPkaxdtQpDX+KnlBBIdE8cO72ytQ1FGps6o6Sd5dYVp+c+RF8vjh3T0WaOtAE4c08
sPb/kNgB8I4JJSTb/Y9FpUdLd8xeVUsaZ0/+g+9G9K/D2/7D/EcjTprqpPkbT4bdYbyDSnhh7f3GTI6OnXWVSfJ23x26gzZHJLRyXd7n6HBoxNf1/6St/3XiQ81HFLHD2/jQ1rHoF6Gzjt59/DT8psjL0NxwQ9bL4O8II5
DYvnhbf+htIPJTGhU8/C2/0bOM3KgwVyipXX+6D+0ckg7P7ztP4R3IJhjko+V1vhDfcek/6b6B94qcC2/OfIiKf3wtv/Q4THpv6n+Sd7236T/Zk57GNr0tM4f9YmSjkVcM63xhywP5HRIXidvpXmgzWORl6W4krf9t8gLW
jykzR/e1gvCPhDkIYH+8Pb5h7oPJHZIcj+81RPo9djkc5OPldb42+QTsR0S38lvm0+Ue2zyuZWP5G3/bfKJUg8p94e3+UT2x6bOtuokeZvPTZ0hv0Ny/OGtnkDNF2R0QVcn7/REQZcXZHSRroYvlx1NosvLxTzz0lgyeZd
PLb+5ATe0vqV1/gYcY8pL08bk3X2m5fekVmVRNKN+eHefFQbchSlz0dQ5+XD3WWFkXZDfJRj01rTOH3kJhr2hmW3ydt4bDHyR7UU6/uHt0Jf3gBIbbmv9SOv8UWfI7yI9/vBOTxT0fMn5N2NseKvnS87AcwjOLDt5Wy85C
C/kpSiu5F3/afnNUWdMtZN391lhJF4qdVZVJ8m7+0zLb446kx5Pvrr7rKDnSyWfVflI3vZfJZ/I7yI9/vA2n+j5UvlmoeoLguRtvVS+XUB+l0ZcM63xh54vjfus6T6Ct3pey2+OfDblI3n/VQv5bOSlKa7kbT4beUFGF+n
qh7f1gi4vnbx04tppjb9OXpDfRXo8+W7rBT1fOn3b1XfJOz2h5TdHnWk2/vBOnxUG6/lNZH412R+b3E/vn/8BMFeWQg0KZW5kc3RyZWFtCmVuZG9iagoxMyAwIG9iago8PAovTGVuZ3RoIDg4NwovU3VidHlwZSAvRm9yb
QovRmlsdGVyIC9GbGF0ZURlY29kZQovVHlwZSAvWE9iamVjdAovTWF0cml4IFsxIDAgMCAxIDAgMF0KL0Zvcm1UeXBlIDEKL1Jlc291cmNlcyA8PAo+PgovQkJveCBbMCAwIDE1NCAxOF0KPj4Kc3RyZWFtDQp4nG2XQY5
UMQxE9/8UfYTvxEmcKyCxYMUCsUOA0IA0bLg+v8dVblCXRhpLM3ntlO2kK6/HebO4/bzCeXs5bHjF688vx/fj4/HrsNufo93eXYt+HHbe3h+fPp  +3L8fr9Y/7z+9v/BQ7E7P8OP7GR319+8N5X28EGoCWeU+GQipFLr2QD
qTn2sYgsnQgUGNQ1xlEFgcygcxc6wwiywSygKxcOxlElpVIs/znFc9/yCWy5NILwRZa7ggkP+i/LA1a2gAycq0ziCwDCLbQckckh8pCLQEkcu1iEFkikY5dd4gIhucsHfI7+tyz7SC7iSwdA9Ox654iSDaVBfI7ttBzRyS
HykItG8jOtcEgsuxEHGPuOfUkt8jiOC+OXXuKAOnqvDjkO8bcc+pJqvPiOC+O0fCcFJLqvDhmzFEbz1KRVDPmKLKjNp6lIqlmzFFkR208S0UyVBYUeWDXAyI2w3OWAfm8/HAZghxdZBmQP3DKRx56kq6y4LoY2PVIESSny
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  +0ghYe/P91uhggnTTC
ipXib3A5SeGiMyKkGpZH56ve86aHHg7MXO2/qy8Z68FO7h2eQG/RNmLdsM8dc4B/nxjbQLSwdfeD2s/vQbAidIoGTg6a4haejoN/I12BgmgSC3i/fk/WU8uXOUhgwWaHKJbSeUVrol8QxUV3TdeibyDq2W0TWmGyu222Hw
wG9J5I7yVyBKeMPHy9DzUXFWzGbhGpPf0iU+UpC+1axJDfp+Hz9ePw8x0Q79h/FUmEfG5b+4aodHGOPna6U5K4Kd4BXche1arbcugu+asI7QQxd5szlUubDdRTReSQXps9SEJQybfFa7oneWLjGYzD77RVm58ipco6xH5X
sglDSu6oekZrWG8Y20qYVuQ8W+l4Qu+eD0tZ++4MEaSCA8MKUuRMMTJ78ZhHvRMHj872jWF7CYRSU8TabjWMsPjjYB0lCjbnDNmrvcDuAvdtHlSs+g4EpFToLUQLIOH6mimR3wocXN6L5K7YImctZqfgM13oNy+EZG5SiU
IksM6ZCglOxfliVy3UWUExQiEoio+wfxyrbZRSt2S1ud2JyF5KKu2LrK7i8lFUZsVxZpbCVZM1awTG2+c8WCEgUF2HmrOinLly9k0P/bLkBj0l4IHFVH48xobHTXQh3JxCbt1j47oQBwYcFDwN45sRRG3aVCp9o1Zb9ePB
jlcVWsm4bVyvZd+iEsyMQq5P4UDMvsoak4uacv6DkkZX/7aMHDx9Fp87Fz2NNCt9UsYfO/GC98CB0BtB9LPNic/9kfgtIxAWGqae/s3RTWZXJ1YleypiHdc6u7Dmau5Vo5xRDr1hBTj59SRu7raZgJebdVSerDFemvvs5H
oxxpYKm8xq388AxV2eREPyShaEz1DRym97cUFN/7fbd+yRzXTbV68wNrPqV+lruscbaJp2pntfJastV3G9JnGzDarXhkvVOHG4zzLiV8wBGoVAoFAqFQqFQKBQKhUKhUCgUygvCf7eUWOENCmVuZHN0cmVhbQplbmRvYmo
KMTUgMCBvYmoKPDwKL1N1YnR5cGUgL1R5cGUxCi9UeXBlIC9Gb250Ci9CYXNlRm9udCAvSGVsdmV0aWNhCi9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nCj4+CmVuZG9iagoxNiAwIG9iago8PAovU3VidHlwZSAvVHlwZ
TEKL1R5cGUgL0ZvbnQKL0Jhc2VGb250IC9IZWx2ZXRpY2EtQm9sZAovRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZwo+PgplbmRvYmoKeHJlZgowIDE3CjAwMDAwMDAwMDAgNjU1MzUgZg0KMDAwMDAwMDAxNSAwMDAwMCB
uDQowMDAwMDAwMzE2IDAwMDAwIG4NCjAwMDAwMDAzNzMgMDAwMDAgbg0KMDAwMDAwMDA5MSAwMDAwMCBuDQowMDAwMDAwNDA3IDAwMDAwIG4NCjAwMDAwMDA1ODIgMDAwMDAgbg0KMDAwMDAwMjIwMiAwMDAwMCBuDQowM
DAwMDAyMjY4IDAwMDAwIG4NCjAwMDAwMDM4OTEgMDAwMDAgbg0KMDAwMDAwMzk5NiAwMDAwMCBuDQowMDAwMDA0MDMzIDAwMDAwIG4NCjAwMDAwMDQwNzcgMDAwMDAgbg0KMDAwMDAwNTgxMyAwMDAwMCBuDQowMDAwMDA
2ODc1IDAwMDAwIG4NCjAwMDAwMDg3MTUgMDAwMDAgbg0KMDAwMDAwODgxMyAwMDAwMCBuDQp0cmFpbGVyCjw8Ci9Sb290IDEgMCBSCi9JbmZvIDQgMCBSCi9JRCBbPEEwQzQ5MDhBNUM3MDdCNTlBMEZBMUFBOEZFOUQ2M

DlDPiA8QTBDNDkwOEE1QzcwN0I1OUEwRkExQUE4RkU5RDYwOUM+XQovU2l6ZSAxNwo+PgpzdGFydHhyZWYKODkxNgolJUVPRgo="
}

Response

200

Code Remarks

Each consignment will be processed independently.
For each consignment, “success”key will be either true or false.
If success is true for a consignment, then the consignment is successfully entered
into the DTDC system.
If success is false, the consignment is not entered
(in case of false, the response contains an error message reason)

400

There is some validation error in the overall request format. In this case,
completerequest is rejected.

401

There is an authentication error.

------------------------------

## Reference Document

DTDC API version 2.2

Introduction

Representational state transfer (REST) or RESTful web service are one way of providing interoperability
between computer systems on the Internet. REST-compliant web services allow requesting systems to
access and manipulate textual representations of web services using a uniform and predefined set
of stateless operations. Other forms of web service exist, which expose their own arbitrary sets of
operations such as WSDL and SOAP.

To make a web API call from a client application, you must supply an authentication token on the call.
The token acts like an electronic key that lets you access the API.

DTDC Tracking services allow third party provider to integrate DTDC tracking services into a platform or
website. Once integrated your application will access DTDC servers over REST style architecture using
XML/JSON.

Authentication token request

To request an authentication token for a user for the REST web API:

Staging :
http://dtdcstagingapi.dtdc.com/dtdc-tracking-api/dtdc-api/api/dtdc/authenticate?username=<userna
me>&password=<password>

Production : https://blktracksvc.dtdc.com/dtdc-api/api/dtdc/authenticate?username=<username>
&password=<password>

Page 1 | 25

Query request parameters

Http Method : GET

Parameter Name

Parameter Value

Remarks

username*
password*

username
password

Response Status

Status: 200 - Will send `Token Access key` if authentication is successful,
Status: 201 – `Partial content` (validation failed for request parameters)
Status: 400 - `Bad Request ` (wrong data passed as request parameter)
Status: 401 - `Unauthorized`
Status: 500 - `Error Occurred `

XML Format Response

Staging :
http://dtdcstagingapi.dtdc.com/dtdc-tracking-api/dtdc-api/rest/XMLCnTrk/getDetails?strcnno=<AWB
No>&TrkType=cnno&addtnlDtl=Y&apikey=<Token Key>

Production : https://blktracksvc.dtdc.com/dtdc-api/rest/XMLCnTrk/getDetails?strcnno=<AWB
No>&TrkType=cnno&addtnlDtl=Y&apikey=<Token Key>

Query request parameters

Http Method : GET

Parameter Name

Parameter Value

Remarks

TrkType*

strcnno*

addtnlDtl*

apikey*

cnno (or) reference

Consignment number (9 chars with
first char as alphabet and the
remaining 8 chars in digits) or
reference number
Y (or) N

Application key to be passed in
each request to make the
authenticate the API request

Consignment number tracking
(cnno) or Reference number
tracking (reference).

Y – the additional details will be
sent in the XML. N – No additional
details will be sent.

Page 2 | 25

Response XML Consignment Data

Node Name

Attribute “NAME” for
the FIELD node

Remarks

Sample Data

(Node value or the
value of the attribute
‘VALUE’ for FIELD
node)

DTDCREPLY

Root Header

CONSIGNMENT

Consignment Node

CNHEADER

CNTRACK

FIELD

strShipmentNo

Consignment details
header

True / False.
Availability of the
consignment details.

The consignment
number

‘True’ / ‘False’

V01197967

strRefNo

The reference Number N/A

strCNType

Booked by Direct Party,
Walk-in, etc

DP, WI

strCNTypeCode

Direct Party Code

LL676

strCNTypeName

Direct Party Name

BMP E-GROUP
SOLUTION PVT. LTD

strCNProduct

Consignment Product

LITE, PTP, etc.

Page 3 | 25

strModeCode

strMode

The billing mode of the
consignment Code

AR1/SF1/AC1

The billing mode of the
consignment

AIR / SURFACE / AIR
CARGO

strCNProdCODFOD

The product code

COD/FOD/CUD

AHMEDABAD
(VEJALPUR),
AHMEDABAD

Booked At

strOrigin

Consignment booked
by or at the office

strOriginRemarks

This field tells about
the strOrigin node. The
values will be

‘Booked By’

‘Received From’

‘Scanned At’

‘Booked At’

strBookedOn

strPieces

Consignment booked
on date (DDMMYYYY)

15062009

The number of pieces
in the consignment

1

strWeightUnit

Unit of the Weight

Kg

strWeight

strDestination

strStatus

Weight of the
consignment in Kg

0.020 Kg

The destination place
of the consignment

Bangalore

DELIVERED

The status of the
consignment.

DELIVERED

Page 4 | 25

strStatusTransOn

strStatusTransTime

DELIVERY PROCESS IN
PROGRESS

ATTEMPTED

HELDUP

RTO

Delivered / Attempted
/ Heldup / Out for
Delivery /
Consignment Returned
On / FDM Prepared On
date

(DDMMYYYY)

Delivered / Attempted
/ Heldup / Out for
Delivery /
Consignment Returned
On / FDM Prepared
time

(HHMM)

16062009

1234

strStatusRelCode

Relationship Code

BRO/DAU/EMP

strStatusRelName

Relationship Name

strRemarks

The receiver details /
Heldup due to reason /
not delivered due to
reason

Brother, Daughter,
Employee

Shakthi

PARTY NOT AVAILABLE

strNoOfAttempts

The number of
attempts for the
consignment delivery

1

strRtoNumber

RTO consignment
number will be

000000339085

Page 5 | 25

available if shipment is
RTO'ed

strActualServiceType

Consignment Product

LITE, PTP, etc.

strExpectedAgent

Expected connection
Agent

TNT

strActualAgent

Actual Connection
Agent

FEDEX

strConnectionDateTim
e

Connection Date and
Time

2019/08/04 14:38:10

strAltReferenceNumbe
r

Alt Ref number

564000857151

strAgentConnectionLoc
ation

Agent Connection
location

DELHI APEX

strBookingType

strError

DOM

Shipment
Identification:Domestic
“DOM“ or
International ”INT”

NO DATA FOUND FOR
THIS CNNO NUMBER

True / False

Error Description (if
consignment is not
found)

Body Node

Node for each Action

True / False.
Availability of the
consignment
additional details.

strCode

strAction

Action Code

BKD

Action Details.

BOOKED

Ex:

DISPATCHED

Page 6 | 25

CNBODY

CNACTION

CNACTIONTRACK

RECEIVED

OUT FOR DELIVERY

DELIVERED

NOT DELIVERED

HELDUP

CONSIGNMENT
RELEASED

CONSIGNMENT HAS
RETURNED

POD DISPATCHED

ARRIVAL AT AIRPORT

CUSTOMS CLEARED

HELDUP AT CUSTOMS

https://docs.google.co
m/spreadsheets/d/10K
olSYlWhN4eFZsVSPUxk
3YEBsxJvELNpWt-CWx
GcFM/edit?usp=drive_
web&ouid=113448660
306017136829

strManifestNo

Manifest Number

O0154799

strOrigin

SALEM BRANCH,
SALEM

Manifest is dispatched
from / Consignment is
not delivered at / Out
for delivery from /
Consignment is
released from /
Consignment is

Page 7 | 25

strDestination

strActionDate

strRemarks

strError

returned from /Heldup
at

Manifest is dispatched
to / Consignment is
released to /
Consignment is
returned to / Out for
delivery by

Manifest dispatch date
/ manifest received
date / Out for delivery
on / not delivered on /
Heldup on /
Consignment has
returned on /
Consignment released
on (DDMMYYYY)

Non–delivery reason /
Heldup reason

Error Description (if
additional details are
not found)

TRICHY BRANCH,
TRICHY

16062009

ADDRESS NOT FOUND

NO DATA FOUND FOR
THIS CNNO NUMBER.

Sample Data for XML output

<DTDCREPLY xmlns="http://dtdc.com">

<CONSIGNMENT xmlns="">

<CNHEADER>

<CNTRACK>true</CNTRACK>

<FIELD name="strShipmentNo" value="V34070628"/>

Page 8 | 25

<FIELD name="strRefNo"/>

<FIELD name="strCNType" value="CC"/>

<FIELD name="strCNTypeCode" value="OC014"/>

<FIELD name="strCNTypeName" value="COCHIN APEX - CO. OWNED CCC"/>

<FIELD name="strCNProduct" value="PREMIUM EXPRESS PRODUCT"/>

<FIELD name="strModeCode"/>

<FIELD name="strMode" value=""/>

<FIELD name="strCNProdCODFOD"/>

<FIELD name="strOrigin" value="COCHIN"/>

<FIELD name="strOriginRemarks" value="Booked By"/>

<FIELD name="strBookedDate" value="08022017"/>

<FIELD name="strBookedTime" value="19:26:21"/>

<FIELD name="strPieces" value="1"/>

<FIELD name="strWeightUnit" value="KG"/>

<FIELD name="strWeight" value="0.1000"/>

<FIELD name="strDestination" value="DELHI"/>

<FIELD name="strStatus" value="Delivered"/>

<FIELD name="strStatusTransOn" value="09022017"/>

<FIELD name="strStatusTransTime" value="1845"/>

<FIELD name="strStatusRelCode" value="RNM"/>

<FIELD name="strStatusRelName" value=""/>

<FIELD name="strRemarks" value="Documents"/>

<FIELD name="strNoOfAttempts" value="1"/>

<FIELD name="strRtoNumber"/>

<FIELD name="strActualServiceType" value="STANDARD"/>

<FIELD name="strExpectedAgent" value=""/>

Page 9 | 25

<FIELD name="strActualAgent" value=""/>

<FIELD name="strConnectionDateTime" value=""/>

<FIELD name="strAltReferenceNumber" value=""/>

<FIELD name="strAgentConnectionLocation" value=""/>

<FIELD name="strBookingType" value="DOM"/>

</CNHEADER>

<CNBODY>

<CNACTIONTRACK>true</CNACTIONTRACK>

<CNACTION>

<FIELD name="strCode" value="BKD"/>

<FIELD name="strAction" value="Booked"/>

<FIELD name="strManifestNo" value=""/>

<FIELD name="strOrigin" value="COCHIN APEX"/>

<FIELD name="strDestination" value=""/>

<FIELD name="strActionDate" value="08022017"/>

<FIELD name="strActionTime" value="1926"/>

<FIELD name="sTrRemarks" value=""/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="CDOUT"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value=""/>

<FIELD name="strOrigin" value="PUNE APEX"/>

<FIELD name="strDestination" value="COCHIN APEX"/>

<FIELD name="strActionDate" value="26042016"/>

<FIELD name="strActionTime" value="0002"/>

Page 10 | 25

<FIELD name="sTrRemarks" value=""/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="OBMD"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value="P7660991"/>

<FIELD name="strOrigin" value="PUNE APEX"/>

<FIELD name="strDestination" value="COCHIN APEX"/>

<FIELD name="strActionDate" value="26042016"/>

<FIELD name="strActionTime" value="1409"/>

<FIELD name="sTrRemarks"/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="CDIN"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value="1236"/>

<FIELD name="strOrigin" value="DELHI APEX"/>

<FIELD name="strDestination"/>

<FIELD name="strActionDate" value="26012017"/>

<FIELD name="strActionTime" value="1325"/>

<FIELD name="sTrRemarks" value=""/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="OPMF"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value="V8191377"/>

Page 11 | 25

<FIELD name="strOrigin" value="COCHIN APEX"/>

<FIELD name="strDestination" value="DELHI AIRPORT APEX"/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="0050"/>

<FIELD name="sTrRemarks"/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="OBMD"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value="V4492715"/>

<FIELD name="strOrigin" value="COCHIN APEX"/>

<FIELD name="strDestination" value="DELHI AIRPORT APEX"/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="0050"/>

<FIELD name="sTrRemarks"/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="OMBM"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value="O8726956"/>

<FIELD name="strOrigin" value="COCHIN APEX"/>

<FIELD name="strDestination" value="DELHI AIRPORT APEX"/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="0435"/>

<FIELD name="sTrRemarks"/>

</CNACTION>

Page 12 | 25

<CNACTION>

<FIELD name="strCode" value="CDOUT"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value="08762261"/>

<FIELD name="strOrigin" value="COCHIN APEX"/>

<FIELD name="strDestination" value="DELHI AIRPORT APEX"/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="1001"/>

<FIELD name="sTrRemarks" value=""/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="IPMF"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value="V6016486"/>

<FIELD name="strOrigin" value="COCHIN APEX"/>

<FIELD name="strDestination" value="DELHI AIRPORT APEX"/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="1409"/>

<FIELD name="sTrRemarks" value="0.00"/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="OBMD"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value="N9642591"/>

<FIELD name="strOrigin" value="DELHI AIRPORT APEX"/>

<FIELD name="strDestination" value="VIJAYANAGAR BRANCH"/>

Page 13 | 25

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="1435"/>

<FIELD name="sTrRemarks"/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="CDOUT"/>

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo"/>

<FIELD name="strOrigin" value="DELHI AIRPORT APEX"/>

<FIELD name="strDestination" value="VIJAYANAGAR BRANCH"/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="1436"/>

<FIELD name="sTrRemarks" value=""/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="inscan"/>

<FIELD name="strAction" value="Recieved At Destination"/>

<FIELD name="strManifestNo" value="V6933762"/>

<FIELD name="strOrigin" value="VIJAYANAGAR BRANCH"/>

<FIELD name="strDestination" value="VIJAYANAGAR BRANCH"/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="1503"/>

<FIELD name="sTrRemarks" value="0.00"/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="IPMF"/>

Page 14 | 25

<FIELD name="strAction" value="In Transit"/>

<FIELD name="strManifestNo" value="V6933762"/>

<FIELD name="strOrigin" value="DELHI APEX"/>

<FIELD name="strDestination" value="VIJAYANAGAR BRANCH"/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="1503"/>

<FIELD name="sTrRemarks" value="0.00"/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="OUTDLV"/>

<FIELD name="strAction" value="Out For Delivery"/>

<FIELD name="strManifestNo" value=""/>

<FIELD name="strOrigin" value="VIJAYANAGAR BRANCH"/>

<FIELD name="strDestination" value=""/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="1514"/>

<FIELD name="sTrRemarks" value=""/>

</CNACTION>

<CNACTION>

<FIELD name="strCode" value="DLV"/>

<FIELD name="strAction" value="Delivered"/>

<FIELD name="strManifestNo" value=""/>

<FIELD name="strOrigin" value="VIJAYANAGAR BRANCH"/>

<FIELD name="strDestination" value=""/>

<FIELD name="strActionDate" value="09022017"/>

<FIELD name="strActionTime" value="1845"/>

Page 15 | 25

<FIELD name="sTrRemarks" value="SIGNTURE"/>

</CNACTION>

</CNBODY>

</CONSIGNMENT>

</DTDCREPLY>

JSON Format Response:

Staging : http://dtdcstagingapi.dtdc.com/dtdc-tracking-api/dtdc-api/rest/JSONCnTrk/getTrackDetails

Production : https://blktracksvc.dtdc.com/dtdc-api/rest/JSONCnTrk/getTrackDetails

Query request parameters

Http Method : POST

Parameter Name

Parameter Value

Remarks

trkType*

cnno (or) reference

Consignment number tracking
(cnno) or Reference number
tracking (reference).

strcnno*

Consignment number (9 chars with first char as
alphabet and the remaining 8 chars in digits) or
reference number

addtnlDtl*

Y (or) N

X-Access-Token*

Token key to be passed in header request to
make the authenticate the API request

Response JSON Consignment Data

Y – the additional details will be
sent in the XML. N – No additional
details will be sent.

Node Name

Sub Node Name

Remarks

Sample Data

(Node value or the value
of the attribute ‘VALUE’
for FIELD node)

Page 16 | 25

statusCode

Standard Http request code

Status: 200 - Will send
Success and tracking
details
Status: 206 – `Partial
content` (validation failed
for request parameters)
Status: 400 - `Bad Request
` (wrong data passed as
request parameter)

Status: 401 -
`Unauthorized`
Status: 500 - `Error
Occurred `

statusFlag

status

errorDetails

True / False. Availability of the
consignment details.

True / False

Tracking status type SUCCESS/FAILED

SUCCESS

Availability of the consignment details.

Will contain error details with error
field Name and the error message

[

{

"name":

"strShipmentNo",

"value": "11111"

},

{

"name": "strError",

"value": "NO DATA

FOUND FOR THIS CNNO
NUMBER"

}

]

trackHeader

strShipmentNo

The consignment number

V01197967

strRefNo

The reference Number

N/A

strCNType

Booked by Direct Party, Walk-in, etc

DP, WI

Page 17 | 25

strCNTypeCode

Direct Party Code

LL676

strCNTypeName

Direct Party Name

BMP E-GROUP SOLUTION
PVT. LTD

strCNProduct

Consignment Product

LITE, PTP, etc.

strModeCode

The billing mode of the consignment
Code

AR1/SF1/AC1

strMode

The billing mode of the consignment

AIR / SURFACE / AIR
CARGO

strCNProdCODFOD

The product code

COD/FOD/CUD

strOrigin

Consignment booked by or at the office

AHMEDABAD (VEJALPUR),
AHMEDABAD

strOriginRemarks

This field tells about the strOrigin node.
The values will be

Booked At

‘Booked By’

‘Received From’

‘Scanned At’

‘Booked At’

Consignment booked on date
(DDMMYYYY)

15062009

The number of pieces in the
consignment

1

Kg

strBookedOn

strPieces

strWeightUnit

Unit of the Weight

strWeight

Weight of the consignment in Kg

0.020 Kg

strDestination

The destination place of the
consignment

Bangalore

strStatus

The status of the consignment.

DELIVERED

1. DELIVERED

Page 18 | 25

2. DELIVERY PROCESS IN

PROGRESS

3. ATTEMPTED
4. HELDUP
5. RTO

strStatusTransOn

Delivered / Attempted / Heldup / Out
for Delivery / Consignment Returned
On / FDM Prepared On date

16062009

(DDMMYYYY)

strStatusTransTime

Delivered / Attempted / Heldup / Out
for Delivery / Consignment Returned
On / FDM Prepared time

1234

(HHMM)

strStatusRelCode

Relationship Code

BRO/DAU/EMP

strStatusRelName

Relationship Name

Brother, Daughter,
Employee

strRemarks

The receiver details / Heldup due to
reason / not delivered due to reason

Shakthi

PARTY NOT AVAILABLE

strNoOfAttempts

The number of attempts for the
consignment delivery

1

strRtoNumber

RTO consignment number will be
available if shipment is RTO'ed

000000339085

strError

Error Description (if consignment is not
found)

NO DATA FOUND FOR
THIS CNNO NUMBER

trackDetails

True / False. Availability of the
consignment additional details.

True / False

strCode

strAction

Action Code

Action Details.

Ex:

BKD

BOOKED

6. DISPATCHED
7. RECEIVED
8. OUT FOR DELIVERY
9. DELIVERED
10. NOT DELIVERED

Page 19 | 25

11. HELDUP
12. CONSIGNMENT RELEASED
13. CONSIGNMENT HAS

RETURNED
14. POD DISPATCHED
15. ARRIVAL AT AIRPORT
16. CUSTOMS CLEARED
17. HELDUP AT CUSTOMS

strManifestNo

Manifest Number

O0154799

strOrigin

strDestination

strActionDate

Manifest is dispatched from /
Consignment is not delivered at / Out
for delivery from / Consignment is
released from / Consignment is
returned from /Heldup at

Manifest is dispatched to /
Consignment is released to /
Consignment is returned to / Out for
delivery by

SALEM BRANCH, SALEM

TRICHY BRANCH, TRICHY

Manifest dispatch date / manifest
received date / Out for delivery on / not
delivered on / Heldup on /
Consignment has returned on /
Consignment released on (DDMMYYYY)

16062009

strRemarks

Non–delivery reason / Heldup reason

ADDRESS NOT FOUND

Sample Data For JSON Output

{

"statusCode": 200,

"statusFlag": true,

"status": "SUCCESS",

"errorDetails": null,

Page 20 | 25

"trackHeader": {

"strShipmentNo": "B32242001",

"strRefNo": "",

"strCNType": "CP",

"strCNTypeCode": "BF014",

"strCNTypeName": "AVENUE ROAD",

"strCNProduct": "LITE",

"strModeCode": "",

"strMode": "",

"strCNProdCODFOD": "",

"strOrigin": "BANGALORE",

"strOriginRemarks": "Booked By",

"strBookedDate": "21062017",

"strBookedTime": "15:30:25",

"strPieces": "1",

"strWeightUnit": "KG",

"strWeight": "0.1000",

"strDestination": "MUMBAI",

"strStatus": "Delivered",

"strStatusTransOn": "21062017",

"strStatusTransTime": "1614",

"strStatusRelCode": "",

"strStatusRelName": "",

"strRemarks": "SIGN",

"strNoOfAttempts": "1",

"strRtoNumber": ""

},

"trackDetails": [

{

"strCode": "BKD",

"strAction": "Booked",

"strManifestNo": "",

Page 21 | 25

},

{

},

{

},

{

"strOrigin": "BANGALORE SURFACE APEX",

"strDestination": "",

"strActionDate": "21062017",

"strActionTime": "1530",

"sTrRemarks": ""

"strCode": "OBMD",

"strAction": "In Transit",

"strManifestNo": "B7701202",

"strOrigin": "BANGALORE SURFACE APEX",

"strDestination": "MUMBAI APEX",

"strActionDate": "21062017",

"strActionTime": "1533",

"sTrRemarks": ""

"strCode": "OPMF",

"strAction": "In Transit",

"strManifestNo": "B7701203",

"strOrigin": "BANGALORE SURFACE APEX",

"strDestination": "MUMBAI APEX",

"strActionDate": "21062017",

"strActionTime": "1533",

"sTrRemarks": ""

"strCode": "IBMD",

"strAction": "In Transit",

"strManifestNo": "B7701202",

"strOrigin": "BANGALORE SURFACE APEX",

"strDestination": "MUMBAI APEX",

Page 22 | 25

"strActionDate": "21062017",

"strActionTime": "1533",

"sTrRemarks": ""

},

{

},

{

},

{

"strCode": "CDOUT",

"strAction": "In Transit",

"strManifestNo": "",

"strOrigin": "BANGALORE SURFACE APEX",

"strDestination": "MUMBAI APEX",

"strActionDate": "21062017",

"strActionTime": "1546",

"sTrRemarks": ""

"strCode": "CDIN",

"strAction": "In Transit",

"strManifestNo": "",

"strOrigin": "BANGALORE SURFACE APEX",

"strDestination": "MUMBAI APEX",

"strActionDate": "21062017",

"strActionTime": "1555",

"sTrRemarks": ""

"strCode": "IPMF",

"strAction": "In Transit",

"strManifestNo": "B7701203",

"strOrigin": "BANGALORE SURFACE APEX",

"strDestination": "MUMBAI APEX",

"strActionDate": "21062017",

"strActionTime": "1603",

Page 23 | 25

"sTrRemarks": "0.00"

"strCode": "IBMD",

"strAction": "In Transit",

"strManifestNo": "B7701202",

"strOrigin": "BANGALORE SURFACE APEX",

"strDestination": "MUMBAI APEX",

"strActionDate": "21062017",

"strActionTime": "1603",

"sTrRemarks": ""

"strCode": "OBMD",

"strAction": "In Transit",

"strManifestNo": "B7701202",

"strOrigin": "BANGALORE SURFACE APEX",

"strDestination": "MUMBAI APEX",

"strActionDate": "21062017",

"strActionTime": "1603",

"sTrRemarks": ""

"strCode": "OUTDLV",

"strAction": "Out For Delivery",

"strManifestNo": "",

"strOrigin": "MUMBAI APEX",

"strDestination": "",

"strActionDate": "21062017",

"strActionTime": "1611",

"sTrRemarks": ""

},

{

},

{

},

{

},

Page 24 | 25

"strCode": "DLV",

"strAction": "Delivered",

"strManifestNo": "",

"strOrigin": "MUMBAI APEX",

"strDestination": "",

"strActionDate": "21062017",

"strActionTime": "1614",

"sTrRemarks": "SIGN"

{

}

]

}

Page 25 | 25

