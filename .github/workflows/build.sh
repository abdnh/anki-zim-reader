#!/bin/bash

pip install git+https://github.com/abdnh/ankibuild@5e346f5ddab5c783dfc35a16a1e8a5fdc7c7bed4#egg=ankibuild[qt5,qt6]

# These are the Python versions used in Anki versions we support (2.1.46 to 2.1.54+)
python_versions=(
    38
    39
)
./scripts/vendor_no_platform.sh
for python_version in ${python_versions[@]}; do
    ./scripts/vendor_pyzstd.sh $python_version
    ./scripts/vendor_libzim.sh $python_version
    # FIXME: min_point_version in manifest.json should depend on the Python version
    make zip EXTRA_ARGS="--out build/zim_reader-py$python_version.ankiaddon"
    make ankiweb EXTRA_ARGS="--out build/zim_reader-py$python_version-ankiweb.ankiaddon"
    rm -rf build/pyzstd/
    rm -rf src/vendor/pyzstd/
done