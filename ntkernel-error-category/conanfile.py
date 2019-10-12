from conans import ConanFile, CMake, tools
import os
import pathlib
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
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data[self.version]["source"])
        extracted_dir = self.conan_data[self.version]["foldername"]
        os.rename(extracted_dir, self._source_subfolder)
        src_path = pathlib.Path(self._source_subfolder)
        for f in src_path.glob("**/CMakeLists.txt"):
            tools.replace_in_file(f, "CMAKE_BINARY_DIR", "PROJECT_BINARY_DIR", strict=False)
        for f in src_path.glob("**/*.cmake*"):
            tools.replace_in_file(f, "CMAKE_BINARY_DIR", "PROJECT_BINARY_DIR", strict=False)
        tools.replace_in_file(src_path / "CMakeLists.txt", 'install(SCRIPT "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}FixupInstall.cmake")', "")

    def _configure_cmake(self):
        cmake = CMake(self, generator="Ninja")
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
