from conans import ConanFile, CMake, tools
import shutil
import os

class LibpqConan(ConanFile):
    name = "libpq"
    version = "9.6.2"
    license = "PostgreSQL"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
