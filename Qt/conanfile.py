import conans
from conans import tools, ConanFile, CMake
from conans.tools import download, unzip, vcvars_command
import shutil
import os

class QtConan(ConanFile):
    name = "Qt"
    version = "5.9.0b3"
    description = "Qt GUI toolkit and library"
    license = "LGPL"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    short_paths = True

    def source(self):
        zip_name = f"{self.name}-{self.version}.zip"
        download("https://download.qt.io/development_releases/qt/5.9/5.9.0-beta3/single/qt-everywhere-opensource-src-5.9.0-beta3.zip", zip_name)
        unzip(zip_name)
        shutil.move("qt-everywhere-opensource-src-5.9.0-beta3", "qt")
        os.unlink(zip_name)

    def build(self):
        platform = ""
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                platform = "win32-msvc"
            elif self.settings.compiler == "gcc":
                platform = "win32-g++"
        else:
            raise "Unsupported platform"

        args = [f"-platform {platform}",
                "-shared" if self.options.shared else "-static",
                "-static-runtime" if self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd" else "",
                "-opensource",
                "-debug" if self.settings.build_type=="Debug" else "-release",
                "-nomake tests",
                "-nomake examples",
                "-skip webengine",
                "-make libs",
                "-make tools",
                "-mp" if self.settings.compiler == "Visual Studio" else "",
                f"-prefix {self.package_folder}"]

        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            cmd = vcvars_command(self.settings)
            self.run(f"{cmd} && cd Qt && configure {' '.join(args)}")
            self.run(f"{cmd} && cd Qt && nmake")

    def package(self):
        if self.settings.compiler == "Visual Studio":
            cmd = vcvars_command(self.settings)
            self.run(f"{cmd} && cd Qt && nmake install")

