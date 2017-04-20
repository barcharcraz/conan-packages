import conans
from conans import tools, ConanFile, CMake
from conans.tools import download, unzip
import os
import shutil

class LibiglConan(ConanFile):
    name = "libigl"
    version = "2bc57eb"
    description = "libigl geometry library"
    author = "Charles Barto"
    license = "MPL"
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    exports = "CMakeLists.txt"
    generators = "cmake"
    def source(self):
        self.run("git clone https://github.com/libigl/libigl.git")
        self.run(f"git -C libigl checkout {self.version}")
    def build(self):
        cmake = CMake(self.settings)
        args = [f'-DCMAKE_INSTALL_PREFIX="{self.package_folder}"'
                ]
        self.run(f"cmake . {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")
    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
    
    def package_id(self):
        self.info.settings.clear()