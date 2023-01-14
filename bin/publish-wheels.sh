#!/usr/bin/env bash

source "bin/activate-env.sh" > /dev/null 2>&1

echo 'uploading wheels...'
pip install twine &&

# Install requirements
cd "${ROOT}"
if [[ "$*" != *--ee* ]];
then
    twine upload "${DIST}/*"
else
    twine upload --repository gitlab "${EE_DIST}/*"
fi
cd -
