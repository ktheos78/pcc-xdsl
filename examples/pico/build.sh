set -e

export PATH="/usr/bin:/usr/local/bin:/bin:/usr/sbin:/sbin"
export PICO_SDK_PATH="$(pwd)/pico-sdk"

rm -rf build
mkdir build

cmake -S . -B build -DPICO_BOARD=pico2
cmake --build build -j