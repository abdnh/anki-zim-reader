#!/bin/bash

pip install git+https://github.com/abdnh/ankibuild@d986a15c247981eccad651dd7f769331ea1092ea#egg=ankibuild[qt5,qt6]

# These are the Python versions used in Anki versions we support (2.1.46 to 2.1.54+)
python_versions=(
    38
    39
)
anki_min_versions=(
    46
    50
)

./scripts/vendor_no_platform.sh
for i in $(seq 0 $(expr ${#python_versions[@]} - 1)); do
    echo $i
    python_version=${python_versions[$i]}
    anki_min_version=${anki_min_versions[$i]}
    ./scripts/vendor_pyzstd.sh $python_version
    ./scripts/vendor_libzim.sh $python_version
    make zip EXTRA_ARGS="--out build/zim_reader-py$python_version.ankiaddon --manifest \"{\\\"min_point_version\\\": $anki_min_version}\""
    make ankiweb EXTRA_ARGS="--out build/zim_reader-py$python_version-ankiweb.ankiaddon --manifest \"{\\\"min_point_version\\\": $anki_min_version}\""
    rm -rf build/pyzstd/
    rm -rf src/vendor/pyzstd*
    rm -rf build/libzim/
    rm -rf src/vendor/libzim*
done
