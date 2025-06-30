cmake_minimum_required(VERSION 3.22)

add_definitions(-DSTM32F103xB)
add_definitions(-DCMSIS_device_header="stm32f1xx.h")

include(cmake/gcc-arm-none-eabi.cmake)
include(cmake/build-helper.cmake)

set(DCMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_SOURCE_DIR}/cmake/gcc-arm-none-eabi.cmake")
project(myrtos)
enable_language(C ASM)

set(CMAKE_EXPORT_COMPILE_COMMANDS 1)

add_subdirectory(broads)
add_subdirectory(examples)


