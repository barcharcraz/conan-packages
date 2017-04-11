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
        zip_name = f"triangle.zip"
        download(f"http://www.netlib.org/voronoi/triangle.zip", zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
    def build(self):
        cmake = CMake(self.settings)
        args = [f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
                f"-DBUILD_SHARED_LIBS={self.options.shared}"
                ]
        self.run(f"cmake . {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")
    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")