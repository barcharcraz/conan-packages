from conans import ConanFile, CMake
from conans.tools import download, unzip
import shutil
import os
class GlBindingConan(ConanFile):
    name = "glBinding"
    version = "2.1.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    def source(self):
        zip_name = "glbinding-2.1.1.zip"
        download("https://github.com/cginternals/glbinding/archive/v2.1.1.zip", zip_name)
        unzip(zip_name)
        shutil.move("glbinding-2.1.1", "glbinding")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        print(cmake.build_config)
        args = ["-DOPTION_BUILD_TESTS=OFF",
                "-DOPTION_BUILD_GPU_TESTS=OFF",
                f'-DCMAKE_INSTALL_PREFIX="{self.package_folder}"',
                f"-DBUILD_SHARED_LIBS={self.options.shared}"]
        self.run(f"cmake {self.conanfile_directory}/glbinding {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")

    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
    
    def package_info(self):
        self.cpp_info.libs = ["glbinding"]
