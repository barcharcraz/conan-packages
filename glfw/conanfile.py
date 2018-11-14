from conans import ConanFile, CMake, tools
import shutil
import os


class GlfwConan(ConanFile):
    name = "glfw"
    version = "3.2.1"
    license = "zlib"
    description = "an Open Source, multi-platform library for OpenGL, OpenGL ES and Vulkan development on the desktop"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "compiler_launcher": [None, "sccache", "ccache"]
    }
    default_options = {
        "shared": False,
        "compiler_launcher": None
    }
    generators = "cmake"

    default_user = "bartoc"
    default_channel = "testing"

    exports_sources = ["CMakeLists.txt"]


    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"


    def package_id(self):
        del self.info.options.compiler_launcher

    def source(self):
        source_url = "https://github.com/glfw/glfw/releases/download/3.2.1/glfw-3.2.1.zip"
        tools.get(source_url, sha256="b7d55e13e07095119e7d5f6792586dd0849c9fcdd867d49a4a5ac31f982f7326")
        extracted_dir = f"{self.name}-{self.version}"
        os.rename(extracted_dir, self._source_subfolder)


    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_VERBOSE_MAKEFILE"] = True
        if(self.options.compiler_launcher):
            cmake.definitions["CMAKE_CXX_COMPILER_LAUNCHER"] = self.options.compiler_launcher
            cmake.definitions["CMAKE_C_COMPILER_LAUNCHER"] = self.options.compiler_launcher
        cmake.configure(build_folder=self._build_subfolder)
        return cmake
    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
