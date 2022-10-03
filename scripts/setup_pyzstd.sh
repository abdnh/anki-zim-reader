# TODO: handle all supported Python versions

cd build

platforms=(
    win_amd64
    manylinux2014_x86_64
    manylinux2014_aarch64
    macosx_10_9_x86_64
    # FIXME: the arm64 shared library has the same name as the x86_64 one (_zstd.cpython-39-darwin.so)
    # How to handle such situation?
    # macosx_11_0_arm64
)

# Download wheels
for platform in ${platforms[@]}; do
    echo $platform
    pip download pyzstd==0.15.3 --only-binary=:all: --python-version 39 --implementation cp --platform $platform
done

# Create a shared wheel from an arbitrary platform-specific wheel
cp pyzstd-0.15.3-cp39-cp39-win_amd64.whl pyzstd.whl

# Unzip wheels
for wheel in *.whl; do
    mkdir -p "${wheel%.*}"
    pushd "${wheel%.*}"
    unzip -o ../$wheel
    popd
done

# Copy platform-specific library files to the shared wheel
for dir in pyzstd-*/; do
    cp $dir/pyzstd/c/_zstd* pyzstd/pyzstd/c/
done

# Copy to vendor dir
cp -r ./pyzstd/* ../src/vendor
