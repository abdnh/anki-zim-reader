#!/bin/bash

mkdir -p build
cd build

python_version=$1
libzim_version=2.0.0

platforms=(
    # TODO: bundle for Windows too once available
    # win_amd64
    manylinux1_x86_64
    macosx_10_9_x86_64
)

# Download wheels
for platform in ${platforms[@]}; do
    pip download libzim==$libzim_version --only-binary=:all: --python-version $python_version --implementation cp --platform $platform
done

# Create a shared wheel from an arbitrary platform-specific wheel
cp libzim-$libzim_version-cp$python_version-cp$python_version-${platforms[0]}.whl libzim.whl

# Unzip wheels
wheels=(libzim-$libzim_version-cp$python_version-*.whl libzim.whl)
for wheel in ${wheels[@]}; do
    mkdir -p "${wheel%.*}"
    pushd "${wheel%.*}"
    unzip -o ../$wheel
    popd
done

# Copy platform-specific library files to the shared wheel
for dir in libzim-$libzim_version-cp$python_version-*/; do
    cp $(find $dir -maxdepth 1 -name 'libzim.*' -type f) libzim/

done

# Copy to vendor dir
cp -r ./libzim/* ../src/vendor
