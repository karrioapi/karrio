SCHEMAS=./schemas
LIB_MODULES=./chronopost_lib
mkdir -p $LIB_MODULES
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

generateDS --no-namespace-defs -o "${LIB_MODULES}/shippingservice.py" "${SCHEMAS}/ShippingServiceWS.xml"
generateDS --no-namespace-defs -o "${LIB_MODULES}/trackingservice.py" "${SCHEMAS}/TrackingServiceWS.xml"
generateDS --no-namespace-defs -o "${LIB_MODULES}/quickcostservice.py" "${SCHEMAS}/QuickcostServiceWS.xml"

