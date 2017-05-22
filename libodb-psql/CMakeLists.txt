cmake_minimum_required(VERSION 3.0)
project(libodb-sqlite VERSION 2.4.0 LANGUAGES CXX)
include(../conanbuildinfo.cmake)
conan_basic_setup()
find_package(odb_libodb 2.4.0 REQUIRED COMPONENTS libodb)
find_package(PostgreSQL REQUIRED)
set(LIBODB_INSTALL_HEADERS ON CACHE BOOL "Install the header files (a debug install)")
file(GLOB_RECURSE libodb_src LIST_DIRECTORIES False
    RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}
    *.cxx)
list(FILTER libodb_src EXCLUDE REGEX /posix/.*)
add_library(libodb-pgsql ${libodb_src})
target_include_directories(libodb-pgsql
    PUBLIC
        ${PostgreSQL_INCLUDE_DIRS} 
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>

)

target_link_libraries(libodb-pgsql PRIVATE odb::libodb ${PostgreSQL_LIBRARIES})
if(NOT MSVC)
    configure_file("${CMAKE_BINARY_DIR}/config.h.in" "${CMAKE_CURRENT_SOURCE_DIR}/odb/pgsql/details/config.h")
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()
if(BUILD_SHARED_LIBS)
    target_compile_definitions(libodb-pgsql PRIVATE
        -DLIBODB_PGSQL_DYNAMIC_LIB)
else()
    target_compile_definitions(libodb-pgsql PRIVATE
        -DLIBODB_PGSQL_STATIC_LIB)
endif()
install(TARGETS libodb-pgsql EXPORT odb_pgsqlConfig
    COMPONENT pgsql
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)
if(LIBODB_INSTALL_HEADERS)
install(DIRECTORY odb DESTINATION include/
        COMPONENT pgsql
        FILES_MATCHING
        PATTERN "*.h"
        PATTERN "*.hxx"
        PATTERN "*.ixx"
        PATTERN "*.txx"
)
endif()
install(EXPORT odb_pgsqlConfig NAMESPACE odb:: COMPONENT pgsql DESTINATION share/odb)
export(TARGETS libodb-pgsql NAMESPACE odb:: FILE odb_pgsqlConfig.cmake)