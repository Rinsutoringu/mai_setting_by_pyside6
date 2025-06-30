file(GLOB_RECURSE PLATFORM_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_board_specific_library(stm32c8t6-standard_platform
		TARGET stm32c8t6-standard
		SOURCES ${PLATFORM_SOURCES}
		INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/include
)
MESSAGE("!!!!!!Building platform library for ${BOARD_NAME} with sources: ${PLATFORM_SOURCES}")