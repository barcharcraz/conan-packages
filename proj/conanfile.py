# forked from proj@bilke

import os
from conans import ConanFile, CMake
from conans.tools import download, unzip, patch

class ProjConan(ConanFile):
    name = "proj"
    version = "4.9.3"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", "FindPROJ4.cmake"]
    license="https://github.com/OSGeo/proj.4"
    description = "The Proj library for projecting things"
    url = "https://github.com/barcharcraz/conan-packages"

    ZIP_FOLDER_NAME = "proj.4-%s" % version
    INSTALL_DIR = "_install"

    def source(self):
        zip_name = self.version + ".zip"
        download("https://github.com/OSGeo/proj.4/archive/%s" % zip_name , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        # produced with `diff -U 1 -p Proj4Config.cmake tmp.cmake`

        patch_content1 = '''--- cmake/Proj4Config.cmake	2016-04-25 09:27:06.000000000 +0200
+++ cmake/Proj4Config.cmake	2016-04-25 09:27:02.000000000 +0200
@@ -38,2 +38,2 @@ set(PACKAGE_VERSION "${${PROJECT_INTERN_

-configure_file(cmake/proj_config.cmake.in src/proj_config.h)
+configure_file(${PROJ4_SOURCE_DIR}/cmake/proj_config.cmake.in ${CMAKE_SOURCE_DIR}/_build/%s/src/proj_config.h)
''' % self.ZIP_FOLDER_NAME
        patch(patch_string=patch_content1, base_path=self.ZIP_FOLDER_NAME)
        patch_content2 = '''--- cmake/Proj4InstallPath.cmake	2016-04-25 09:27:06.000000000 +0200
+++ cmake/Proj4InstallPath.cmake	2016-04-25 09:28:02.000000000 +0200
@@ -24,3 +24,3 @@ ENDIF(CMAKE_INSTALL_PREFIX_INITIALIZED_T

-if(WIN32)
+if(FALSE)
   set(DEFAULT_BIN_SUBDIR bin)
'''

        patch(patch_string=patch_content2, base_path=self.ZIP_FOLDER_NAME)
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        CMAKE_OPTIONALS = "-DBUILD_CS2CS=ON -DBUILD_PROJ=ON -DBUILD_GEOD=ON -DBUILD_NAD2BIN=ON "
        if self.options.shared == False:
            CMAKE_OPTIONALS += "-DBUILD_LIBPROJ_SHARED=OFF "
        else:
            CMAKE_OPTIONALS += "-DBUILD_LIBPROJ_SHARED=ON "
        self.run("%s && cmake .. -DPROJ4_TESTS=OFF -DCMAKE_INSTALL_PREFIX=../%s %s %s" % (cd_build, self.INSTALL_DIR, cmake.command_line, CMAKE_OPTIONALS))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))
        self.run("%s && cmake --build . --target install %s" % (cd_build, cmake.build_config))

    def package(self):
        #self.copy("FindPROJ4.cmake", ".", ".")
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["proj_4_9_d"]
            else:
                self.cpp_info.libs = ["proj_4_9"]
        else:
            self.cpp_info.libs = ["proj"]
