SCHEMAS=./schemas
LIB_MODULES=./dhl_ecom_de_lib
mkdir -p $LIB_MODULES
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

generateDS --no-namespace-defs -o "${LIB_MODULES}/business_interface.py" "${SCHEMAS}/geschaeftskundenversand-api-3.1.8-schema-bcs_base.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/customer_interface.py" "${SCHEMAS}/geschaeftskundenversand-api-3.1.8-schema-cis_base.xsd"