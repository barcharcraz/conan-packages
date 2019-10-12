from conans import ConanFile, CMake, tools
from pathlib import Path
import os
class OutcomeConan(ConanFile):
    name = 'outcome'
    description = 'Provides very lightweight outcome<T> and result<T> (non-Boost edition) '
    url = 'https://github.com/barcharcraz/conan-packages'
    homepage = 'https://github.com/ned14/outcome'
    license = 'Apache-2.0'
    exports_sources = ["CMakeLists.txt"]
    generators = 'cmake'
    default_user = "chbarto"
    default_channel = "testing"
    version = "2.1.1"
    _source_subfolder = 'source_subfolder'
    _build_subfolder = 'build_subfolder'
    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {"cxx_modules": [True, False]}
    default_options = {"cxx_modules": False}
    
    def build_requirements(self):
        self.build_requires(f"quickcpplib/20191011-master@{self.user}/{self.channel}")

    def source(self):
        tools.get(**self.conan_data[self.version]["source"])
        extracted_dir = self.conan_data[self.version]["foldername"]
        os.rename(extracted_dir, self._source_subfolder)
        src_path = Path(self._source_subfolder)
        tools.replace_in_file(src_path / "CMakeLists.txt", "find_quickcpplib_library(quickcpplib 1.0 REQUIRED)", "")
        

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_VALGRIND"] = False
        cmake.definitions["ENABLE_CXX_CONCEPTS"] = False
        cmake.definitions["ENABLE_CXX_MODULES"] = self.options.cxx_modules
        cmake.definitions["ENABLE_CLANG_STATIC_ANALYZER"] = False
        cmake.definitions["BUILD_TESTING"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake
    
    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.cmake*", src=os.path.join(self._source_subfolder, "cmakelib"), dst="lib/cmake/quickcpplib/cmakelib")
        cmake = self._configure_cmake()
        cmake.install()
    
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.builddirs.append("lib/cmake/quickcpplib/cmakelib")
    
    def package_id(self):
        if not self.options.cxx_modules:
            self.info.header_only()
