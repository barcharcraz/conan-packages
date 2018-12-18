from conans import ConanFile, CMake, tools

import os
import sys

class EmbreeConan(ConanFile):
    name = "embree"
    version = "3.3.0"
    license = "Apache 2.0"
    description = "The embree ray tracing library"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "build_type", "compiler", "arch"
    generators = "cmake"
    exports_sources = ["CMakeLists.txt"]
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }
    default_channel = "testing"
    default_user = "bartoc"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        source_url = "https://github.com/embree/embree"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version), 
            sha256="b7afee01034544d80cce4f81eb3ead03c527728186ff96b4662a242252e224f6")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
    
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["EMBREE_STATIC_RUNTIME"] = True if "MT" in self.settings.compiler.runtime else False
        cmake.definitions["EMBREE_STATIC_LIB"] = not self.options.shared
        cmake.definitions["EMBREE_TASKING_SYSTEM"] = "INTERNAL"
        cmake.definitions["EMBREE_TUTORIALS"] = False
        cmake.definitions["EMBREE_MAX_ISA"] = "SSE2"
        cmake.definitions["EMBREE_ISPC_SUPPORT"] = False
        cmake.definitions["EMBREE_TESTING_BENCHMARK"] = False
        cmake.definitions["EMBREE_TESTING_SDE"] = False
        cmake.definitions["EMBREE_TESTING_PACKAGE"] = False
        cmake.definitions["EMBREE_STACK_PROTECTOR"] = False
        cmake.definitions["EMBREE_RAY_PACKETS"] = False
        cmake.definitions["EMBREE_RAY_MASK"] = False
        
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