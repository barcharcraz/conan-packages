from conans import ConanFile, CMake, tools
import os

class RobinMapConan(ConanFile):
    name = "robin-map"
    version = "0.5.0"
    license = "MIT"
    author = "Charles Barto <bartoc@umich.edu>"
    url = "https://github.com/barcharcraz/conan-packages"
    description = "robin map, a fast hashmap for c++"
    
    exports_sources = ["CMakeLists.txt"]

    generators = "cmake"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    default_channel = "testing"
    default_user = "bartoc"

    def source(self):
        source_url = "https://github.com/Tessil/robin-map"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        #turn off C/C++ we just want cmake for the install features
        tools.replace_in_file(f"{self._source_subfolder}/CMakeLists.txt",
            "project(tsl_robin_map",
            "project(tsl_robin_map LANGUAGES")
    
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
        self.info.header_only()