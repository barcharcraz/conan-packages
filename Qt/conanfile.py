import conans
from conans import tools, ConanFile, CMake
from conans.tools import download, unzip, vcvars_command, untargz
import shutil
import os

class QtConan(ConanFile):
    name = "Qt"
    version = "5.9.1"
    description = "Qt GUI toolkit and library"
    license = "LGPL"
    url = "https://github.com/barcharcraz/conan-packages"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    short_paths = True

    def source(self):
        zip_name = f"{self.name}-{self.version}.zip"
        download("https://download.qt.io/official_releases/qt/5.9/5.9.1/single/qt-everywhere-opensource-src-5.9.1.tar.xz", zip_name)
        if self.settings.os == "Windows":
            download("https://download.qt.io/official_releases/jom/jom_1_1_2.zip", "jom.zip")
            unzip("jom.zip")
        #self.run("git clone -b v5.9.0-rc2 --recursive https://code.qt.io/qt/qt5.git qt")
        untargz(zip_name)

        shutil.move("qt-everywhere-opensource-src-5.9.1", "qt")
        os.unlink(zip_name)

    def build(self):
        platform = ""
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                platform = "win32-msvc"
            elif self.settings.compiler == "gcc":
                platform = "win32-g++"
        elif self.settings.os == "Linux":
            if self.settings.compiler == "gcc":
                platform = "linux-g++"
        else:
            raise "Unsupported platform"

        args = [f"-platform {platform}",
                "-shared" if self.options.shared else "-static",
                "-static-runtime" if self.settings.compiler == "Visual Studio" and (self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd") else "",
                "-opensource",
                "-debug" if self.settings.build_type=="Debug" else "-release",
                "-nomake tests",
                "-nomake examples",
                "-skip webengine",
                "-no-openssl",
                "-make libs",
                "-make tools",
                "-mp" if self.settings.compiler == "Visual Studio" else "",
                f"-prefix {self.package_folder}"]

        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            cmd = vcvars_command(self.settings)

            self.run(f"{cmd} && cd Qt && configure {' '.join(args)}")
            if self.settings.compiler == "Visual Studio":
                self.run(f"{cmd} && cd Qt && ..\jom.exe")
            else:
                self.run(f"{cmd} && cd Qt && make")
        else:
            self.run(f"cd qt && ./configure {' '.join(args)}")
            self.run(f"cd qt && make")

    def package(self):
        if self.settings.compiler == "Visual Studio":
            cmd = vcvars_command(self.settings)
            self.run(f"{cmd} && cd Qt && nmake install")
        else:
            self.run(f"cd qt && make install")

