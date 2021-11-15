SCHEMAS=./schemas
LIB_MODULES=./dhl_parcel_pl_lib
mkdir -p $LIB_MODULES
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

generateDS --no-namespace-defs -o "${LIB_MODULES}/services.py" "${SCHEMAS}/webapi2.xsd"
