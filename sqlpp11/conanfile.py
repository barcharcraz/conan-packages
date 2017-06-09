from conans import ConanFile, CMake, tools
import shutil
import os

class Sqlpp11Conan(ConanFile):
    name = "sqlpp11"
    version = "0.48"
    license = "BSD"
    requires = (
        ("HinnantDate/[~=2]@barcharcraz/testing")
    )
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "CMakeLists.txt"
    generators = "cmake"

    def source(self):
        zip_name = f"sqlpp-{self.version}"
        tools.download(f"https://github.com/rbock/sqlpp11/archive/{self.version}.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move(f"sqlpp11-{self.version}", "sqlpp11")
        os.unlink(zip_name)
    def build(self):
        cmake = CMake(self.settings)
        args = [f"-DBUILD_SHARED_LIBS={self.options.shared}",
                f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
                "-DENABLE_TESTS=OFF"]
        self.run(f"cmake . {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")
    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []

