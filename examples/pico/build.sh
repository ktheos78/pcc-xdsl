set -e

export PATH="/usr/bin:/usr/local/bin:/bin:/usr/sbin:/sbin"
export PICO_SDK_PATH="$(pwd)/pico-sdk"

rm -rf build
mkdir build

/usr/bin/cmake -S . -B build -DPICO_BOARD=pico2
/usr/bin/cmake --build build -j