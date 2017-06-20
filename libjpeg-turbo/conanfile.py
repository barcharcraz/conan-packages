from conans import ConanFile, ConfigureEnvironment
import os
from conans.tools import download
from conans.tools import unzip, replace_in_file
from conans import CMake


class LibJpegTurboConan(ConanFile):
    name = "libjpeg-turbo"
    version = "1.5.1"
    ZIP_FOLDER_NAME = "%s-%s" % (name, version)
    generators = "cmake", "txt"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "SSE": [True, False]}
    default_options = "shared=False", "fPIC=True", "SSE=True"
    exports = "CMakeLists.txt"
    url="http://github.com/lasote/libjpeg-turbo"
    license="https://github.com/libjpeg-turbo/libjpeg-turbo/blob/%s/LICENSE.txt" % version
    
    def config(self):
        
        if self.settings.os == "Windows":
            self.requires.add("nasm/2.12.02@lasote/stable", private=True)
            self.options.remove("fPIC")
       
    def source(self):
        zip_name = "%s.tar.gz" % self.ZIP_FOLDER_NAME
        download("http://downloads.sourceforge.net/project/libjpeg-turbo/%s/%s" % (self.version, zip_name), zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """

            
        # Don't mess with runtime conan already set
        replace_in_file("%s/CMakeLists.txt" % self.ZIP_FOLDER_NAME, 'string(REGEX REPLACE "/MD" "/MT" ${var} "${${var}}")', "")
        replace_in_file("%s/sharedlib/CMakeLists.txt" % self.ZIP_FOLDER_NAME, 'string(REGEX REPLACE "/MT" "/MD" ${var} "${${var}}")', "")
        
        cmake_options = []
        if self.options.shared == True:
            cmake_options.append("-DENABLE_STATIC=0 -DENABLE_SHARED=1")
        else:
            cmake_options.append("-DENABLE_SHARED=0 -DENABLE_STATIC=1")
        cmake_options.append("-DWITH_SIMD=%s" % "1" if self.options.SSE else "0")

        cmake = CMake(self.settings)
        self.run("cd %s && mkdir _build" % self.ZIP_FOLDER_NAME)
        cd_build = "cd %s/_build" % self.ZIP_FOLDER_NAME

        self.run('%s && cmake .. %s %s' % (cd_build, cmake.command_line, " ".join(cmake_options)))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))
                
    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        # Copying headers
        self.copy("*.h", "include", "%s" % (self.ZIP_FOLDER_NAME), keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
                self.copy(pattern="*turbojpeg.lib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
                self.copy(pattern="*jpeg.lib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*jpeg-static.lib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.options.shared:
                self.cpp_info.libs = ['jpeg', 'turbojpeg']
            else:
                self.cpp_info.libs = ['jpeg-static', 'turbojpeg-static']
        else:
            self.cpp_info.libs = ['jpeg', 'turbojpeg']
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
