
from conans import ConanFile, CMake, tools
from conans.tools import download, unzip
import shutil
import os

class GdalConan(ConanFile):
    name = "gdal"
    version = "2.1.2"
    license = "MIT"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        zip_name = "gdal-2.1.2.zip"
        download("http://download.osgeo.org/gdal/2.1.2/gdal212.zip", zip_name)
        unzip(zip_name)
        shutil.move("gdal-2.1.2", "gdal")
        os.unlink(zip_name)
    def build(self):
        nmake_args = ["WIN64=YES" if self.settings.arch == "x64" else "WIN64=NO"]
        if self.settings.compiler == "Visual Studio":
            version = self.settings.compiler.version
            if version == "9":
                nmake_args.append(["MSVC_VER=1500"])
            elif version == "10":
                nmake_args.append(["MSVC_VER=1600"])
            elif version == "11":
                nmake_args.append(["MSVC_VER=1700"])
            elif version == "12":
                nmake_args.append(["MSVC_VER=1800"])
            else:
                # this is the highest version of msvc that
                # gdal recognises, but if compiles fine at least up
                # to VS 2017
                nmake_args.append(["MSVC_VER=1900"])
