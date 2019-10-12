from conans import ConanFile, CMake, tools
import os
class NtKernelErrorCategoryConan(ConanFile):
    name = 'ntkernel-error-category'
    description = "A C++ 11 std::error_category for the NT kernel's NTSTATUS error codes"
    url = 'https://github.com/barcharcraz/conan-packages'
    homepage = 'https://github.com/ned14/ntkernel-error-category'
    license = 'Apache-2.0'
    exports_sources = ["CMakeLists.txt"]
    generators = 'cmake'
    default_user = "chbarto"
    default_channel = "testing"
    version = "20191011"
    _source_subfolder = 'source_subfolder'
    _build_subfolder = 'build_subfolder'
    settings = 'os', 'arch', 'compiler', 'build_type'

    def source(self):
        tools.get(**self.conan_data[self.version]["source"])
        extracted_dir = self.conan_data[self.version]["foldername"]
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake
    
    def build(self):
        self._configure_cmake()
