project(example_oled_${BOARD_NAME} ASM C CXX)

add_arm_executable(${PROJECT_NAME}
		TARGET ${BOARD_NAME}
		SOURCES oled.cpp
)