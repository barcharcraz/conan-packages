from conans import ConanFile, CMake, tools
import shutil
import os

class LibodbConan(ConanFile):
    name = "libodb-pgsql"
    version = "2.4.0"
    license = "GPL"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = (
        ("libodb/2.4.0@barcharcraz/testing"),
        ("libpq/[>=9.6]@barcharcraz/testing")
                )
    exports = ("CMakeLists.txt", "config.h.in")

    def source(self):
        zip_name = f"libodb-sqlite-{self.version}.zip"
        tools.download(f"http://www.codesynthesis.com/download/odb/2.4/libodb-pgsql-{self.version}.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move(f"libodb-pgsql-{self.version}", "libodb-pgsql")
        os.unlink(zip_name)
        shutil.copy("CMakeLists.txt", "libodb-pgsql/CMakeLists.txt")

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = [
            f'-DCMAKE_INSTALL_PREFIX="{self.package_folder}"',
            f"-DBUILD_SHARED_LIBS={self.options.shared}"
        ]
        self.run(f"cmake {self.conanfile_directory}/libodb-pgsql {cmake.command_line} {' '.join(cmake_options)}")
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
        #self.copy(pattern="odbConfig.cmake", src="libodb", dst="share/odb")
    def package_info(self):
        self.cpp_info.libs = ["libodb-pgsql"]




