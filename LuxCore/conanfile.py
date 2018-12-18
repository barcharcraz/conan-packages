from conans import ConanFile, CMake, tools
import os
import sys

class LuxcoreConan(ConanFile):
    name = "LuxCore"
    version = "2.1beta4"
    license = "Apache 2.0"
    author = "Charles Barto <bartoc@umich.edu>"
    url = "https://github.com/barcharcraz/conan-packages"
    description = "The LuxRenderCore 2.1 API"
    topics = ("rendering", "graphics")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = (
        "boost/[>=1.56.0]@conan/stable",
        "OpenImageIO/2.0.3@bartoc/stable",
        "openexr/2.3.0@conan/stable",
        "embree/3.3.0@bartoc/stable",
        "TBB/2019_U3@conan/stable",
        "c-blosc/1.15.1@francescalted/stable"
    )
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def configure(self):
        self.options["boost"].without_python = False

    def source(self):
        source_url = "https://github.com/LuxCoreRender/LuxCore"
        tools.get("{0}/archive/luxcorerender_v{1}.tar.gz".format(source_url, self.version), 
            sha256="ae7c20bb504b431e58dc82d2dfff9f819c6a9706115d2bbfc866a98eeacc1eb1")
        extracted_dir = self.name + "-" + "luxcorerender_v" + self.version

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["PYTHON_V"] = f"{sys.version_info.major}{sys.version_info.minor}"
        cmake.definitions["LUXRAYS_DISABLE_OPENCL"] = True
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

