cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)

project(pico2_asm_demo C CXX ASM)

pico_sdk_init()

add_executable(pico2_asm_demo
    main-pico.c
    asm-pico.s
)

target_link_libraries(pico2_asm_demo
    pico_stdlib
)

pico_add_extra_outputs(pico2_asm_demo)