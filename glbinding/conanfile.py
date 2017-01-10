from conans import ConanFile, CMake
from conans.tools import download, unzip
import shutil
import os
class GlBindingConan(ConanFile):
    name = "glBinding"
    version = "2.1.1"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        zip_name = "glbinding-2.1.1.zip"
        download("https://github.com/cginternals/glbinding/archive/v2.1.1.zip", zip_name)
        unzip(zip_name)
        shutil.move("glbinding-2.1.1", "glbinding")
        os.unlink(zip_name)
