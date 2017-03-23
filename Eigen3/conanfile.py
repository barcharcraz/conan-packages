from conans import ConanFile, CMake, tools
import shutil
import os


class GlfwConan(ConanFile):
    name = "Eigen3"
    version = "3.3.2"
    license = "MPL2"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def source(self):
        zip_name = "eigen3-3.3.2.zip"
        tools.download("http://bitbucket.org/eigen/eigen/get/3.3.2.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move("eigen-eigen-da9b4e14c255", "eigen3")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        self.run(f"cmake eigen3 -DCMAKE_INSTALL_PREFIX={self.package_folder} {cmake.command_line}")
        self.run(f"cmake --build . {cmake.build_config}")

    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
        #self.copy("*", "include/eigen3/Eigen", "eigen3/Eigen", keep_path=True)
        #self.copy("signature_of_eigen3_matrix_library", "include/eigen3", "eigen3")

    def package_info(self):
        self.cpp_info.includedirs = ["include/eigen3"]
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
