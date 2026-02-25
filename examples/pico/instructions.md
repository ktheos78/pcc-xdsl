# pcc Raspberry Pi Pico 2 Example

## About

This example is a small proof of concept which loads a program that uses ARM assembly produced by the compiler into a Raspberry Pi Pico 2, demonstrating a fully-functional end-to-end example of successful (pico)C code compilation and execution in a real hardware platform.

More specifically, `main-pico.c` calls a function compiled via pcc (`compiled_assembly()`) and uses its return value to tune the frequency at which the on-board LED of the Pico 2 is blinked.

This file contains instructions for building the project and flashing it onto the Pico 2.

Special thanks to [kourosh824/microc-arm-compiler](https://www.github.com/kourosh824/microc-arm-compiler) for the testing/verification idea and documentation of most of the build process.

## Instructions

### 1. Install dependencies

Install the required packages through your package manager (for example, apt):

`sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib`

### 2. Compile the picoC source file

Inside the directory containing `pcc.py`, compile the C source file:

`./pcc.py examples/pico/asm-pico.c`

### 3. Clone the Raspberry Pi Pico SDK and Initialize Submodules

Inside `examples/pico`, run the following commands:

```bash
git clone https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git submodule update --init
cd ..
```

### 4. Create Project Directory and Import SDK Configuration

`cp pico-sdk/external/pico_sdk_import.cmake .`

### 5. Build Firmware

To build the firmware with which the Pico 2 is flashed, simply run the provided build script with the following commands:

```bash
chmod +x build.sh
./build.sh
```

### 6. Flash Raspberry Pi Pico 2

To flash the device with the compiled project, follow these steps:

- Plug the Raspberry Pi Pico 2 into your computer while holding the **BOOTSEL** button.

- Identify the device using `lsblk` (`/dev/sdX1`)

- Mount the device into a directory like `/mnt/pico2` by running the following command: `sudo mount /dev/sdX1 /mnt/pico2` (make sure to replace sdX1 with the actual volume name) 

- Copy the generated firmware file into the device: `sudo cp build/<filename>.uf2 /mnt/pico2`.

- Unmount the device and unplug it from your computer to complete the flashing process: `sudo umount /dev/sdX1` 