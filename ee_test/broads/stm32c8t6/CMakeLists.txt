cmake_minimum_required(VERSION 3.22)

enable_language(C ASM)

# 这个cmake脚本分为多个阶段
# 它先创建一个名为board_interface的INTERFACE库，
# 这个库包含了一些编译选项和链接选项，这些选项适用于所有使用这个库的项目。
# 它创建一个名为stm32c8t6_interface的INTERFACE库，
# 这个库包含了特定于STM32F103xB微控制器的编译选项和源代码。
# 它创建一个名为stm32c8t6的OBJECT库，
# 这个库包含了STM32F103xB微控制器的具体实现代码和头文件。

# 基本接口库
add_library(board_interface INTERFACE)
target_compile_definitions(board_interface INTERFACE USE_HAL_DRIVER)
target_compile_options(board_interface INTERFACE
		$<$<COMPILE_LANGUAGE:ASM>:-x assembler-with-cpp>
		-ffunction-sections -fdata-sections -fmessage-length=0)
target_link_options(board_interface INTERFACE
		-specs=nano.specs -specs=nosys.specs -Wl,--gc-sections
		-Wl,--wrap=malloc -Wl,--wrap=free -Wl,--wrap=calloc -Wl,--wrap=realloc)
target_link_libraries(board_interface INTERFACE c m)

# stm32c8t6基本接口库
set(PROJECT_NAME stm32c8t6)

project(${PROJECT_NAME})
add_library(${PROJECT_NAME}_interface INTERFACE)

target_compile_definitions(${PROJECT_NAME}_interface INTERFACE
		USE_HAL_DRIVER
		STM32F103xB
		$<$<CONFIG:Debug>:DEBUG>
)

target_include_directories(${PROJECT_NAME}_interface INTERFACE
		Core/Inc
		Drivers/STM32F1xx_HAL_Driver/Inc/Legacy
		Drivers/STM32F1xx_HAL_Driver/Inc
		Middlewares/Third_Party/FreeRTOS/Source/include
		Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2
		Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3
		Drivers/CMSIS/Device/ST/STM32F1xx/Include
		Drivers/CMSIS/Include
)

#target_sources(${PROJECT_NAME}_interface INTERFACE)

target_link_directories(${PROJECT_NAME}_interface INTERFACE
)

target_link_libraries(${PROJECT_NAME}_interface INTERFACE board_interface
)

# 创建OBJECT库，使用stm32c8t6_interface库的编译选项和链接选项


add_library(${PROJECT_NAME} OBJECT
		Core/Src/main.c
		Core/Src/gpio.c
		Core/Src/freertos.c
		Core/Src/tim.c
		Core/Src/usart.c
		Core/Src/stm32f1xx_it.c
		Core/Src/stm32f1xx_hal_msp.c
		Core/Src/stm32f1xx_hal_timebase_tim.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio_ex.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc_ex.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_dma.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_cortex.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_pwr.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash_ex.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_exti.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim_ex.c
		Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_uart.c
		Core/Src/system_stm32f1xx.c
		Middlewares/Third_Party/FreeRTOS/Source/croutine.c
		Middlewares/Third_Party/FreeRTOS/Source/event_groups.c
		Middlewares/Third_Party/FreeRTOS/Source/list.c
		Middlewares/Third_Party/FreeRTOS/Source/queue.c
		Middlewares/Third_Party/FreeRTOS/Source/stream_buffer.c
		Middlewares/Third_Party/FreeRTOS/Source/tasks.c
		Middlewares/Third_Party/FreeRTOS/Source/timers.c
		Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.c
		Middlewares/Third_Party/FreeRTOS/Source/portable/MemMang/heap_4.c
		Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3/port.c
		Core/Src/sysmem.c
		Core/Src/syscalls.c
		startup_stm32f103xb.s
)
target_compile_options(${PROJECT_NAME} PRIVATE
		-Wno-maybe-uninitialized -Wno-unused-parameter -Wno-sign-compare -Wno-int-conversion)
# link against board specific arm dsp library and interface
target_link_libraries(${PROJECT_NAME}
		PUBLIC ${PROJECT_NAME}_interface)

# DEBUG
get_target_property(PROJECT_SRCS ${PROJECT_NAME} SOURCES)
message(STATUS "[${PROJECT_NAME}] sources: ${PROJECT_SRCS}")

# Validate that STM32CubeMX code is compatible with C standard
if(CMAKE_C_STANDARD LESS 11)
	message(ERROR "Generated code requires C11 or higher")
endif()


