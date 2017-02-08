from conans import ConanFile, CMake
from conans.tools import download, unzip
import shutil
import os
import os.path
class GlBindingConan(ConanFile):
    name = "sqlite3"
    version = "3.16.2"
    description = "sqlite3 embedded database"
    license = "Public Domain"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    exports = "CMakeLists.txt"
    default_options = "shared=False"
    def source(self):
        zip_name = "sqlite-amalgamation-3160200.zip"
        download("https://sqlite.org/2017/sqlite-amalgamation-3160200.zip", zip_name)
        unzip(zip_name)
        shutil.move("sqlite-amalgamation-3160200", "sqlite")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        print(cmake.build_config)
        args = [f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
                f"-DBUILD_SHARED_LIBS={self.options.shared}"]
        self.run(f"cmake {self.conanfile_directory} {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")

    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
    
    def package_info(self):
        self.cpp_info.libs = ["sqlite3"]
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        