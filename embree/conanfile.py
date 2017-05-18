
from conans import ConanFile, CMake, tools
import shutil
import os

class EmbreeConan(ConanFile):
    name = "embree"
    version = "2.15.0"
    license = "Apache 2.0"
    description = "The embree ray tracing library"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {
        "shared": [True, False]
    }
    default_options = "shared=False"
    def source(self):
        zip_name = f"{self.name}-{self.version}.zip"
        tools.download(f"https://github.com/embree/embree/archive/v{self.version}.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move(f"{self.name}-{self.version}", f"{self.name}")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        cmake_opts = [
            f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
            f"-DBUILD_SHARED_LIBS={self.options.shared}",
            f"-DEMBREE_STATIC_LIB={not self.options.shared}",
            "-DEMBREE_TUTORIALS=OFF",
            "-DEMBREE_TASKING_SYSTEM=INTERNAL",
            "-DEMBREE_ISPC_SUPPORT=OFF",
            "-DEMBREE_MAX_ISA=SSE2",
            "-DEMBREE_GEOMETRY_SUBDIV=OFF",
            "-DEMBREE_STATIC_RUNTIME=ON" if "MT" in str(self.settings.compiler.runtime) else "-DEMBREE_STATIC_RUNTIME=OFF"
        ]
        self.run(f"cmake {self.name} {' '.join(cmake_opts)} {cmake.command_line}")
        self.run(f"cmake --build . {cmake.build_config}")
    
    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
        self.copy("*.lib", ".", "lib")