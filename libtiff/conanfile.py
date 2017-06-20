import os
from conans import ConanFile, CMake
from conans.tools import download, unzip

class LibtiffConan(ConanFile):
    name = "libtiff"
    version = "4.0.8"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "jpeg": [True, False]
               }
    default_options = "shared=False", "jpeg=False", "libjpeg-turbo:shared=True"
    requires = "zlib/[>=1.2.8]@lasote/stable"
    exports = ["CMakeLists.txt", "FindTIFF.cmake"]
    url="http://github.com/bilke/conan-tiff"
    license="http://www.remotesensing.org/libtiff/"

    ZIP_FOLDER_NAME = "tiff-%s" % version
    INSTALL_DIR = "_install"

    def source(self):
        zip_name = self.ZIP_FOLDER_NAME + ".zip"
        download("https://github.com/vadz/libtiff/archive/Release-v4-0-8.zip", zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def requirements(self):
        if self.options.jpeg == True:
            self.requires("libjpeg-turbo/1.5.1@barcharcraz/testing")

    def build(self):
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        CMAKE_OPTIONALS = f"-Dlzma=OFF -Djpeg={self.options.jpeg} "
        if self.settings.os == "Linux":
            CMAKE_OPTIONALS += "-DCMAKE_POSITION_INDEPENDENT_CODE=ON "
        if self.options.shared == False:
            CMAKE_OPTIONALS += "-DBUILD_SHARED_LIBS=OFF "
        else:
            CMAKE_OPTIONALS += "-DBUILD_SHARED_LIBS=ON "
        self.run("%s && cmake .. -DCMAKE_INSTALL_PREFIX=../%s %s %s" % (cd_build, self.INSTALL_DIR, cmake.command_line, CMAKE_OPTIONALS))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))
        self.run("%s && cmake --build . --target install %s" % (cd_build, cmake.build_config))

    def package(self):
        self.copy("FindTIFF.cmake", ".", ".")
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["tiffd", "tiffxxd"]
        else:
            self.cpp_info.libs = ["tiff", "tiffxx"]
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
