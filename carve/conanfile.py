
from conans import ConanFile, CMake, tools
import shutil
import os
# this uses the version of carve in the blender source tree because that seems
# to be the one that's maintained
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
        zip_name = f"{self.name}-{self.version}.zip"
        download_uri = f"https://git.blender.org/gitweb/gitweb.cgi/blender.git/snapshot/d85b2ca04619f5a451862099c5f10834ec8eab1f.tar.gz"
        tools.download(download_uri, zip_name)
        tools.untargz(zip_name)
        shutil.move(f"blender-d85b2ca", f"{self.name}")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = [
            f'-DCMAKE_INSTALL_PREFIX="{self.package_folder}"',
            f"-DBUILD_SHARED_LIBS={self.options.shared}",
            f"-DBUILD_TESTING=FALSE"
        ]
        self.run(f"cmake . {cmake.command_line} {' '.join(cmake_options)}")
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package(self):
        pass

    