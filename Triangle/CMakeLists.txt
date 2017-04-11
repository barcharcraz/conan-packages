cmake_minimum_required(VERSION 3.7)
project(Triangle VERSION 1.6 LANGUAGES C)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_library(triangle triangle.h triangle.c)
target_compile_definitions(triangle PRIVATE TRILIBRARY NO_TIMER)
add_library(Triangle::triangle ALIAS triangle)
target_include_directories(triangle INTERFACE
    $<INSTALL_INTERFACE:include>
    )

install(TARGETS triangle EXPORT triangle-config
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
    )

install(EXPORT triangle-config NAMESPACE Triangle:: DESTINATION share/Triangle)
install(FILES triangle.h DESTINATION include)