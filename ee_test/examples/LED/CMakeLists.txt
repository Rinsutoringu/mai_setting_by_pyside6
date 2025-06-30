project(example_led_${BOARD_NAME} ASM C CXX)
file(GLOB_RECURSE src ${CMAKE_CURRENT_SOURCE_DIR}/Src/*.cpp)

add_arm_executable(${PROJECT_NAME}
		TARGET ${BOARD_NAME}
		SOURCES ${src}
		INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/Inc
)
