from conans import ConanFile, CMake, tools
import os


class LuxcoreConan(ConanFile):
    name = "LuxCore"
    version = "2.1beta3"
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
        "boost/[>=1.56.0]@conan/stable"
    )
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        source_url = "https://github.com/LuxCoreRender/LuxCore"
        tools.get("{0}/archive/luxcorerender_v{1}.tar.gz".format(source_url, self.version), 
            sha256="4a6c9b0dea6b29a4ae758d8b120d8fd1175ec6fb5ad2a9cb1ed4306b1cc274e4")
        extracted_dir = self.name + "-" + "luxcorerender_v" + self.version

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
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

