import conans
from conans import tools, ConanFile, CMake
from conans.tools import download, unzip
import os
import shutil

class TriangleConan(ConanFile):
    name = "Triangle"
    version = "1.6"
    description = "Triangle triangulation library"
    author = "Jonathan Richard Shewchuk"
    license = "Custom/Non-Commercial"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    exports = "CMakeLists.txt"
    default_options = "shared=False"
    generators = "cmake"

    _source_subfolder = "triangle"
    _build_subfolder = "triangle_build"

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def source(self):
        self.run("git clone https://github.com/libigl/triangle.git")
        self.run("git -C triangle checkout d6761dd691e2e1318c83bf7773fea88d9437464a")
        # OK this one was a big huuuuge fuck you moment for me.
        # like can we just never do this ever again in the world
    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)