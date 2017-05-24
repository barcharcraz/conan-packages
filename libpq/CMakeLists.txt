cmake_minimum_required(VERSION 3.5)
project(libpq VERSION 9.6.2 LANGUAGES C)
include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()
find_package(OpenSSL REQUIRED)
set(CMAKE_DEBUG_POSTFIX "d")
configure_file(${CMAKE_CURRENT_LIST_DIR}/postgresql/src/include/pg_config.h.win32 ${CMAKE_CURRENT_LIST_DIR}/postgresql/src/include/pg_config.h)
configure_file(${CMAKE_CURRENT_LIST_DIR}/postgresql/src/include/pg_config_ext.h.win32 ${CMAKE_CURRENT_LIST_DIR}/postgresql/src/include/pg_config_ext.h)
configure_file(${CMAKE_CURRENT_LIST_DIR}/postgresql/src/include/port/win32.h ${CMAKE_CURRENT_LIST_DIR}/postgresql/src/include/pg_config_os.h)
file(WRITE postgresql/src/interfaces/libpq/pg_config_paths.h "#define SYSCONFDIR \"\"")
set(INSTALL_INCLUDES ON CACHE BOOL "Install include files")
set(pg_port_src
    postgresql/src/port/getaddrinfo.c
    postgresql/src/port/pgstrcasecmp.c
    postgresql/src/port/pqsignal.c
    postgresql/src/port/thread.c
    postgresql/src/port/inet_aton.c
    postgresql/src/port/crypt.c
    postgresql/src/port/noblock.c
    postgresql/src/port/chklocale.c
    postgresql/src/port/inet_net_ntop.c
    postgresql/src/port/snprintf.c
    postgresql/src/port/strlcpy.c
    postgresql/src/port/dirent.c
    postgresql/src/port/dirmod.c
    postgresql/src/port/pgsleep.c
    postgresql/src/port/open.c
    postgresql/src/port/system.c
    postgresql/src/port/win32error.c
    postgresql/src/port/win32setlocale.c
)
set(pg_backend_src
    postgresql/src/backend/libpq/md5.c
    postgresql/src/backend/libpq/ip.c
    postgresql/src/backend/utils/mb/wchar.c
    postgresql/src/backend/utils/mb/encnames.c
)
set(pg_libpq_src
    postgresql/src/interfaces/libpq/fe-auth.c
    postgresql/src/interfaces/libpq/fe-connect.c
    postgresql/src/interfaces/libpq/fe-exec.c
    postgresql/src/interfaces/libpq/fe-lobj.c
    postgresql/src/interfaces/libpq/fe-misc.c
    postgresql/src/interfaces/libpq/fe-print.c
    postgresql/src/interfaces/libpq/fe-protocol2.c
    postgresql/src/interfaces/libpq/fe-protocol3.c
    postgresql/src/interfaces/libpq/fe-secure-openssl.c
    postgresql/src/interfaces/libpq/fe-secure.c
    postgresql/src/interfaces/libpq/libpq-events.c
    postgresql/src/interfaces/libpq/pqexpbuffer.c
    postgresql/src/interfaces/libpq/pthread-win32.c
    postgresql/src/interfaces/libpq/win32.c
    postgresql/src/interfaces/libpq/libpq-dist.rc
)
set(pg_libpq_interface
    postgresql/src/include/postgres_ext.h
    postgresql/src/include/pg_config_ext.h
    postgresql/src/include/pg_config.h
    postgresql/src/interfaces/libpq/libpq-fe.h
    )
set(pg_libpq_catalog_interface
    postgresql/src/include/catalog/pg_type.h
    postgresql/src/include/catalog/genbki.h
)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_DEBUG_POSTFIX "d")
set(CMAKE_INCLUDE_CURRENT_DIR ON)
add_library(libpq ${pg_port_src} ${pg_backend_src} ${pg_libpq_src})
target_compile_definitions(libpq PRIVATE -DFRONTEND -DENABLE_THREAD_SAFETY -DUSE_OPENSSL -D_CRT_SECURE_NO_WARNINGS)
target_link_libraries(libpq PRIVATE ${OPENSSL_LIBRARIES} )
if(WIN32)
target_link_libraries(libpq PRIVATE ws2_32 secur32 advapi32 shell32 crypt32)
endif()
target_include_directories(libpq PRIVATE ${OPENSSL_INCLUDE_DIRS} postgresql/src/include postgresql/src/include/port/win32 postgresql/src/include/port/win32_msvc postgresql/src/port)
set_target_properties(libpq PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON)

install(TARGETS libpq
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
    )
if(INSTALL_INCLUDES)
    install(FILES ${pg_libpq_interface} DESTINATION include)
    install(DIRECTORY postgresql/src/include/libpq DESTINATION include)
    install(FILES ${pg_libpq_catalog_interface} DESTINATION include/catalog)
endif()