

from conans import ConanFile, CMake, tools
import shutil
import os

class FmtConan(ConanFile):
    name = "fmt"
    version = "3.0.1"
    license = "BSD"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "tests": [True, False],
               "docs": [True, False]}
    default_options = "shared=False", "tests=False", "docs=False"
    generators = "cmake"
    
    def source(self):
        zip_name = f"{self.name}-{self.version}.zip"
        tools.download(f"https://github.com/fmtlib/fmt/archive/{self.version}.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move(f"{self.name}-{self.version}", f"{self.name}")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = [
            f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
            f"-DBUILD_SHARED_LIBS={self.options.shared}",
            f"-DFMT_INSTALL=ON",
            f"-DFMT_TEST={self.options.tests}",
            f"-DFMT_DOCS={self.options.docs}"
        ]
        self.run(f"cmake {self.name} {cmake.command_line} {' '.join(cmake_options)}")
        self.run(f"cmake --build . --target install {cmake.build_config}")
    
    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")