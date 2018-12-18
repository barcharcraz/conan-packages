from conans import ConanFile, CMake, tools
import platform
import os


class CyclesConan(ConanFile):
    name = "cycles"
    version = "1.9.1"
    url = "https://github.com/barcharcraz/conan-packages"
    author = "Charlies Barto <bartoc@umich.edu>"
    license = "Apache 2.0"
    exports_sources = ["CMakeLists.txt"]

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    generators = "cmake"

    settings = "os", "arch", "build_type", "compiler"

    requires = (
        "boost/[>=1.48.0]@conan/stable",
        "OpenImageIO/2.0.3@bartoc/stable"
    )

    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = {
        "shared": False,
        "fPIC": True
    }

    def source(self):
        git = tools.Git(folder=self._source_subfolder)
        git.clone("git://git.blender.org/cycles.git", branch=f"v{self.version}")
    
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake
    
    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
    
    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
