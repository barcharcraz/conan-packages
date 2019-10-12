from conans import ConanFile, CMake, tools
from pathlib import Path
import re
import os
class QuickCPPLibConan(ConanFile):
    name = 'quickcpplib'
    description = 'Eliminate all the tedious hassle when making state-of-the-art C++ 14 or 17 libraries!'
    url = 'https://github.com/barcharcraz/conan-packages'
    homepage = 'https://github.com/ned14/llfio'
    license = 'Apache-2.0'
    exports_sources = ["CMakeLists.txt"]
    generators = 'cmake'
    default_user = "chbarto"
    default_channel = "testing"
    _source_subfolder = 'source_subfolder'
    _build_subfolder = 'build_subfolder'
    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {"shared": [True, False], "fPIC": [True, False], "cxx_modules": [True, False]}
    default_options = {"shared": False, "fPIC": True, "cxx_modules": False}
    requires = [
        ("optional-lite/3.2.0@nonstd-lite/stable"),
        ("byte-lite/0.2.0@nonstd-lite/stable")
    ]

    def source(self):
        
        tools.get(**self.conan_data[self.version]["source"])
        extracted_dir = self.conan_data[self.version]["foldername"]
        os.rename(extracted_dir, self._source_subfolder)
        src_path = Path(self._source_subfolder)
        headers_path = src_path / "cmake" / "headers.cmake"
        headers_path.write_text(re.sub('(?m)^.*byte/.*$|^.*gsl-lite/.*$|^.*optional/.*$', '', headers_path.read_text('UTF-8')))
        #tools.replace_in_file(src_path / "cmake/QuickCppLibBootstrap.cmake", "CMAKE_BINARY_DIR", "PROJECT_BINARY_DIR")
        for f in src_path.glob("**/*.cmake*"):
            tools.replace_in_file(f, "CMAKE_BINARY_DIR", "PROJECT_BINARY_DIR", strict=False)
        

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_VALGRIND"] = False
        cmake.definitions["ENABLE_CXX_MODULES"] = self.options.cxx_modules
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
