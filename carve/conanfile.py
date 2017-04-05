from conans import ConanFile, CMake, tools
import shutil
import os

class CarveConanFile(ConanFile):
    name = "CARVE"
    description = "The Carve Solid modeling library"
    version = "devel"
    license = "GPLv2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = "CMakeLists.txt"

    def source(self):
        self.run("git clone https://github.com/VTREEM/Carve.git")

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = [
            f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
            f"-DBUILD_SHARED_LIBS={self.options.shared}",
            f"-DBUILD_TESTING=FALSE",
            f"-DCARVE_BOOST_COLLECTIONS=FALSE",
            f"-DCARVE_WITH_GUI=FALSE",
            f"-DCARVE_DEBUG={TRUE if self.settings.build_type=='Debug' else FALSE}"
        ]
        self.run(f"cmake . {cmake.command_line} {' '.join(cmake_options)}")
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package(self):
        pass

    