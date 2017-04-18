import conans
from conans import tools, ConanFile, CMake
from conans.tools import download, unzip
import os
import shutil

class GeographicLibConan(ConanFile):
    name = "GeographicLib"
    version = "1.48"
    description = "Geographic lib geography library"
    author = "Charles Barto"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False]
    
    }
    default_options = "shared=False"
    exports = "CMakeLists.txt"
    generators = "cmake"
    def source(self):
        download("https://sourceforge.net/projects/geographiclib/files/distrib/GeographicLib-1.48.zip/download", "GeographicLib-1.48.zip")
        unzip("GeographicLib-1.48.zip")
        shutil.move("GeographicLib-1.48", "GeographicLib")
        #stop building the wrappers. These are not packaged well and break things like x64 builds
        tools.replace_in_file("GeographicLib/CMakeLists.txt", "add_subdirectory (js)", "#add_subdirectory (js)")
        tools.replace_in_file("GeographicLib/CMakeLists.txt", "add_subdirectory (python/geographiclib)", "#add_subdirectory (python/geographiclib)")
        tools.replace_in_file("GeographicLib/CMakeLists.txt", "add_subdirectory (matlab)", "#add_subdirectory (matlab)")


        os.unlink("GeographicLib-1.48.zip")
    def build(self):
        cmake = CMake(self.settings)
        args = [f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
                f"-DBUILD_SHARED_LIBS={self.options.shared}",
                f"-DGEOGRAPHICLIB_LIB_TYPE={'SHARED' if self.options.shared else 'STATIC'}",
                "-DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=ON",
                "-DJS_BUILD=OFF"
                ]
        self.run(f"cmake . {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")
    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
    
    #def package_id(self):
    #    self.info.settings.clear()