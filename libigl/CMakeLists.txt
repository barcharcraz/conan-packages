cmake_minimum_required(VERSION 3.7)
project(libigl)

include(conanbuildinfo.cmake)
conan_basic_setup()

install(DIRECTORY libigl/include/ DESTINATION include)