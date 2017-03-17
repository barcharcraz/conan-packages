
from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, vcvars_command
import shutil
import os

class GdalConan(ConanFile):
    name = "gdal"
    version = "2.1.3"
    license = "MIT"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {}

    def _getargs(self):
        nmake_args = ["WIN64=YES" if self.settings.arch == "x86_64" else "WIN64=NO"]
        if self.settings.compiler == "Visual Studio":
            version = self.settings.compiler.version
            if version == "9":
                nmake_args.append("MSVC_VER=1500")
            elif version == "10":
                nmake_args.append("MSVC_VER=1600")
            elif version == "11":
                nmake_args.append("MSVC_VER=1700")
            elif version == "12":
                nmake_args.append("MSVC_VER=1800")
            else:
                # this is the highest version of msvc that
                # gdal recognises, but if compiles fine at least up
                # to VS 2017
                nmake_args.append("MSVC_VER=1900")
        nmake_args.append(f"GDAL_HOME={self.package_folder}")
        return nmake_args

    def source(self):
        zip_name = "gdal-2.1.2.zip"
        download("http://download.osgeo.org/gdal/2.1.3/gdal213.zip", zip_name)
        unzip(zip_name)
        shutil.move("gdal-2.1.3", "gdal")
        os.unlink(zip_name)
    def build(self):
        nmake_args = self._getargs()
        cmd = vcvars_command(self.settings)
        self.run(f"{cmd} && cd gdal && nmake /f makefile.vc {' '.join(nmake_args)}")
    def package(self):
        nmake_args = self._getargs()
        cmd = vcvars_command(self.settings)
        self.run(f"{cmd} && cd gdal && nmake /f makefile.vc {' '.join(nmake_args)} devinstall")

    def package_info(self):
        self.cpp_info.libs = ["gdal"]
