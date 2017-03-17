from conans import ConanFile, CMake, tools
import shutil
import os

class LibodbConan(ConanFile):
    name = "libodb"
    version = "2.4.0"
    license = "GPL"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = ("CMakeLists.txt", "odbConfig.cmake")

    def source(self):
        zip_name = f"libodb-{self.version}.zip"
        tools.download(f"http://www.codesynthesis.com/download/odb/2.4/libodb-{self.version}.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move(f"libodb-{self.version}", "libodb")
        os.unlink(zip_name)
        shutil.copy("CMakeLists.txt", "libodb/CMakeLists.txt")

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = [
            f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
            f"-DBUILD_SHARED_LIBS={self.options.shared}"
        ]
        self.run(f"cmake {self.conanfile_directory}/libodb {cmake.command_line} {' '.join(cmake_options)}")
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
        self.copy(pattern="odbConfig.cmake", src="", dst="share/odb")
    def package_info(self):
        self.cpp_info.libs = ["libodb"]




