from conans import ConanFile, CMake, tools
import shutil
import os

class LibosmiumConan(ConanFile):
    name = "libosmium"
    version = "2.11.1"
    license = "Boost"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "Boost/devel@barcharcraz/testing"
    exports = "CMakeLists.txt"

    def source(self):
        zip_name = f"libosmium-{self.version}.zip"
        tools.download(f"https://github.com/osmcode/libosmium/archive/v{self.version}.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move(f"libosmium-{self.version}", "libosmium")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = [
            f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
            f"-DBUILD_SHARED_LIBS={self.options.shared}"
        ]
        self.run(f"cmake {self.conanfile_directory} {cmake.command_line} {' '.join(cmake_options)}")
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
