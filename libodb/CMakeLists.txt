cmake_minimum_required(VERSION 3.3)
project(libodb VERSION 2.4.0 LANGUAGES CXX)
set(LIBODB_INSTALL_HEADERS ON CACHE BOOL "Install the header files (a debug install)")
file(GLOB_RECURSE libodb_src LIST_DIRECTORIES False
    RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}
    *.cxx)
if(WIN32)
list(FILTER libodb_src EXCLUDE REGEX /posix/.*)
else()
list(FILTER libodb_src EXCLUDE REGEX /win32/.*)
endif()
message(INFO ${libodb_src})
add_library(libodb ${libodb_src})

target_include_directories(libodb
    PUBLIC 
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>

)
set_property(TARGET libodb PROPERTY VERSION 2.4.0)
include(CMakePackageConfigHelpers)
write_basic_package_version_file(${CMAKE_CURRENT_BINARY_DIR}/odb_libodbConfigVersion.cmake
    VERSION 2.4.0
    COMPATIBILITY AnyNewerVersion)
if(NOT MSVC)
    if("cxx_thread_local" IN_LIST CMAKE_CXX_COMPILE_FEATURES)
        set(ODB_THREADS_TLS_KEYWORD ON)
        set(ODB_THREADS_DECLSPEC OFF)
    endif()
    if(WIN32)
        set(ODB_THREADS_WIN32 ON)
    else()
        set(ODB_THREADS_POSIX ON)
    endif()
    configure_file("${CMAKE_BINARY_DIR}/config.h.in" "${CMAKE_CURRENT_SOURCE_DIR}/odb/details/config.h")
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()
if(BUILD_SHARED_LIBS)
    target_compile_definitions(libodb PRIVATE
        -DLIBODB_DYNAMIC_LIB)
else()
    target_compile_definitions(libodb PRIVATE
        -DLIBODB_STATIC_LIB)
endif()
install(TARGETS libodb EXPORT odb_libodbConfig
    COMPONENT libodb
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)
if(LIBODB_INSTALL_HEADERS)
install(DIRECTORY odb DESTINATION include/
        COMPONENT libodb
        FILES_MATCHING
        PATTERN "*.h"
        PATTERN "*.hxx"
        PATTERN "*.ixx"
        PATTERN "*.txx"
)
endif()
install(EXPORT odb_libodbConfig NAMESPACE odb:: COMPONENT libodb DESTINATION share/odb_libodb)
export(TARGETS libodb NAMESPACE odb:: FILE odb_libodbConfig.cmake)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/odb_libodbConfigVersion.cmake
        DESTINATION share/odb_libodb)
