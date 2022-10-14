#!/bin/bash

mkdir -p build
cd build

python_version=$1
pyzstd_version=0.15.3

platforms=(
    win_amd64
    # manylinux2014_x86_64
    # manylinux2014_aarch64
    # macosx_10_9_x86_64
    # FIXME: the arm64 shared library has the same name as the x86_64 one (_zstd.cpython-39-darwin.so)
    # How to handle such situation?
    # macosx_11_0_arm64
)

# Download wheels
for platform in ${platforms[@]}; do
    pip download pyzstd==$pyzstd_version --only-binary=:all: --python-version $python_version --implementation cp --platform $platform
done

# Create a shared wheel from an arbitrary platform-specific wheel
cp pyzstd-$pyzstd_version-cp$python_version-cp$python_version-${platforms[0]}.whl pyzstd.whl

# Unzip wheels
wheels=(pyzstd-$pyzstd_version-cp$python_version-*.whl pyzstd.whl)
for wheel in ${wheels[@]}; do
    mkdir -p "${wheel%.*}"
    pushd "${wheel%.*}"
    unzip -o ../$wheel
    popd
done

# Copy platform-specific library files to the shared wheel
for dir in pyzstd-$pyzstd_version-cp$python_version-*/; do
    cp $dir/pyzstd/c/_zstd* pyzstd/pyzstd/c/
done

# Copy to vendor dir
cp -r ./pyzstd/* ../src/vendor
