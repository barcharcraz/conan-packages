from conans import ConanFile, CMake, tools
import shutil
import os


class GlfwConan(ConanFile):
    name = "Eigen3"
    version = "3.3.2"
    license = "MPL2"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = None
    generators = "cmake"

    def source(self):
        zip_name = "eigen3-3.3.1.zip"
        tools.download("http://bitbucket.org/eigen/eigen/get/3.3.2.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move("eigen-eigen-da9b4e14c255", "eigen3")
        os.unlink(zip_name)

    def build(self):
        pass

    def package(self):
        self.copy("*", "include/eigen3/Eigen", "eigen3/Eigen", keep_path=True)
        self.copy("signature_of_eigen3_matrix_library", "include/eigen3", "eigen3")

    def package_info(self):
        self.cpp_info.includedirs = ["include/eigen3"]
