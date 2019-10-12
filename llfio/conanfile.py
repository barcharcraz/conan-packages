from conans import ConanFile, CMake, tools
import os
import pathlib
class LLFIOConanfile(ConanFile):
    name = 'llfio'
    description = 'P1031 low level file i/o and filesystem library for the C++ standard'
    url = 'https://github.com/barcharcraz/conan-packages'
    homepage = 'https://github.com/ned14/llfio'
    license = 'Apache-2.0'
    exports_sources = ["CMakeLists.txt"]
    generators = 'cmake'
    default_user = "chbarto"
    default_channel = "testing"
    version = "20191011"
    _source_subfolder = 'source_subfolder'
    _build_subfolder = 'build_subfolder'
    settings = 'os', 'arch', 'compiler', 'build_type'
    def requirements(self):
        self.requires(f"quickcpplib/20191011-master@{self.user}/{self.channel}")
        self.requires(f"outcome/2.1.1@{self.user}/{self.channel}")
        self.requires(f"ntkernel-error-category/20191011@{self.user}/{self.channel}")
    def source(self):
        tools.get(**self.conan_data[self.version]["source"])
        extracted_dir = self.conan_data[self.version]["foldername"]
        os.rename(extracted_dir, self._source_subfolder)
        src_path = pathlib.Path(self._source_subfolder)
        tools.replace_in_file(src_path / "CMakeLists.txt", 'add_subdirectory("include/llfio/ntkernel-error-category" EXCLUDE_FROM_ALL)', '')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake
    
    def build(self):
        self._configure_cmake()
