
from conans import ConanFile, CMake, tools
import os
import shutil

class ExpatConan(ConanFile):
    name = "expat"
    version = "2.2.0"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "examples": [True, False],
               "tools": [True, False],
               "tests": [True, False]
               }
    default_options = "shared=False", "examples=False", "tools=False", "tests=False"
    generators = "cmake"

    def source(self):
        zip_name = f"expat-{self.version}.tar.bz2"
        tools.download(f"https://sourceforge.net/projects/expat/files/expat/2.2.0/expat-{self.version}.tar.bz2/download", zip_name)
        tools.untargz(zip_name)
        shutil.move(f"expat-{self.version}", "expat")
        os.unlink(zip_name)

        #expat tries to build docs in a system dependent way
        #this is fixed in HEAD but I'm patching it here so we can use the 2.2.0 release
        # TODO: remove hack with next expat update
        # we don't make this windows only because actually it fails on unix for out of source builds
        tools.replace_in_file("expat/CMakeLists.txt", "add_custom_command", "#add_custom_command")

    def build(self):
        cmake = CMake(self.settings)
        options = [f"-DBUILD_SHARED_LIBS={self.options.shared}",
                   f"-DBUILD_shared={self.options.shared}",
                   f"-DBUILD_examples={self.options.examples}",
                   f"-DBUILD_tools={self.options.tools}",
                   f"-DBUILD_tests={self.options.tests}",
                   f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
                   "-DCMAKE_DEBUG_POSTFIX=\"\""]
        self.run(f"cmake {self.name} {cmake.command_line} {' '.join(options)}")
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["expat"]
        if self.options.shared == False:
            self.cpp_info.defines = ["XML_STATIC"]
