import conans
from conans import tools, ConanFile, CMake
from conans.tools import download, unzip
import os
import shutil

class OpenMeshConan(ConanFile):
    name = "OpenMesh"
    version = "6.3"
    description = "openmesh mesh processing library"
    license = "BSD"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    #exports = "CMakeLists.txt"
    default_options = "shared=False"
    def source(self):
        zip_name = f"{self.name}-{self.version}.zip"
        download(f"https://www.openmesh.org/media/Releases/{self.version}/OpenMesh-{self.version}.zip", zip_name)
        unzip(zip_name)
        shutil.move(f"{self.name}-{self.version}", "openmesh")
        os.unlink(zip_name)
    def build(self):
        cmake = CMake(self.settings)
        args = [f'-DCMAKE_INSTALL_PREFIX="{self.package_folder}"',
                f"-DBUILD_SHARED_LIBS={self.options.shared}",
                "-DBUILD_APPS=OFF",
                "-DOPENMESH_BUILD_PYTHON_BINDINGS=OFF",
                f"-DOPENMESH_BUILD_SHARED={self.options.shared}"]
        self.run(f"cmake openmesh {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")
    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")