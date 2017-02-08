from conans import ConanFile, CMake, tools
import shutil
import os


class GlfwConan(ConanFile):
    name = "Eigen3"
    version = "3.2.1"
    license = "zlib"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"


    def source(self):
        zip_name = "glfw-3.2.1.zip"
        tools.download("https://github.com/glfw/glfw/releases/download/3.2.1/glfw-3.2.1.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move("glfw-3.2.1", "glfw")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        args = [f"-DBUILD_SHARED_LIBS={self.options.shared}",
                f"-DCMAKE_INSTALL_PREFIX={self.package_folder}"]
        self.run(f"cmake glfw {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")

    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["glfw3dll.lib" if self.options.shared else "glfw3.lib"]
            if self.options.shared:
                self.cpp_info.bindirs = ["lib"]
