file(GLOB_RECURSE DRIVER_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_board_specific_library(${BOARD_NAME}_drivers
		TARGET ${BOARD_NAME}
		SOURCES ${DRIVER_SOURCES}
		INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/include
		DEPENDS ${BOARD_NAME}_platform
)

# DEBUG
get_target_property(DRIVER_SRCS ${BOARD_NAME}_drivers SOURCES)
message(STATUS "[${BOARD_NAME}_drivers] sources: ${DRIVER_SRCS}")

get_target_property(PROJECT_SRCS ${BOARD_NAME} SOURCES)
message(STATUS "[${BOARD_NAME}] sources: ${PROJECT_SRCS}")