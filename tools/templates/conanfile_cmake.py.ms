
from conans import ConanFile, CMake, tools
import shutil
import os

class {{name}}Conan(ConanFile):
    name = {{name}}
    version = {{version}}
    license = {{license}}
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        {{#options}}
        "{{name}}": [True, False]
        {{/options}}
    }
    default_options = (
        {{#options}}
        "{{name}}={{default}}"
        {{/options}}
    )
    generators = "cmake"

    def source(self):
        zip_name = f"{self.name}-{self.version}.{{extension}}"
        tools.download(f"{{download_uri}}", zip_name)
        tools.unzip(zip_name)
        shutil.move(f"{self.name}-{self.version}", "{self.name}")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        args = [
            {{#options}}
            f"-D{{cmake_var}}={self.options.{{name}}}",
            {{/options}}
            f"-DCMAKE_INSTALL_PREFIX={self.package_folder}"
        ]
        self.run(f"cmake glfw {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
    
