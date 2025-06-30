project(example_buzzer_${BOARD_NAME} ASM C CXX)

add_arm_executable(${PROJECT_NAME}
		TARGET ${BOARD_NAME}
		SOURCES testbuzzer.cpp
)
#
#get_target_property(PROJECT_SRCS ${PROJECT_NAME}.elf SOURCES)
#message(STATUS "[Buzzer ${PROJECT_NAME}.elf] sources: ${PROJECT_SRCS}")