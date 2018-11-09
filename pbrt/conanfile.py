from conans import ConanFile, CMake, tools
import os

class PbrtConan(ConanFile):
    name = "pbrt"
    version = "20181109"
    license = "BSD 2-Clause"
    author = "Charles Barto <bartoc@umich.edu>"
    url = "https://github.com/barcharcraz/conan-packages"
    description = "the pbrt renderer,"
    topics = ("rendering", "simulation", "graphics")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {
        "shared": False
    }
    generators = "cmake"
    exports_sources = ["CMakeLists.txt"]
    exports = ["LICENSE.txt", "*.patch"]
    default_user = "bartoc"
    default_channel = "testing"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    def source(self):
        git = tools.Git(folder=self._source_subfolder)
        git.clone(url ="https://github.com/mmp/pbrt-v3.git", branch="master")
        git.checkout("master", submodule="recursive")
        # fix the project using source dir to set the module path
        # this doesn't work with conan since we include the cmakelists file
        # in our dependency enabling superproject
        tools.patch(base_path=self._source_subfolder, patch_file="cmake_patch.patch")
        tools.patch(base_path=os.path.join(self._source_subfolder, "src/ext/openexr"), patch_file="openexr_cmake_patch.patch")

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
        self.cpp_info.libs = ["hello"]

