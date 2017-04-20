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
    def source(self):
        self.run("git clone https://github.com/libigl/triangle.git")
        self.run("git -C triangle checkout d6761dd691e2e1318c83bf7773fea88d9437464a")
        # OK this one was a big huuuuge fuck you moment for me.
        # like can we just never do this ever again in the world
    def build(self):
        cmake = CMake(self.settings)
        args = [f'-DCMAKE_INSTALL_PREFIX="{self.package_folder}"',
                f"-DBUILD_SHARED_LIBS={self.options.shared}"
                ]
        self.run(f"cmake . {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")
    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")