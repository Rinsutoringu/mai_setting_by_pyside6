file(GLOB_RECURSE DRIVER_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_board_specific_library(stm32c8t6-standard_drivers
		TARGET stm32c8t6-standard
		SOURCES ${DRIVER_SOURCES}
		INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/include
		DEPENDS stm32c8t6-standard_platform
)

