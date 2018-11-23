from conans import ConanFile, CMake, tools
import platform
import os


class VulkanLoaderConan(ConanFile):
    name = "Vulkan-Loader"
    version = "1.1.85.0"
    url = "https://github.com/barcharcraz/conan-packages"
    author = "Charlies Barto <bartoc@umich.edu>"
    description = "Khronos official Vulkan ICD desktop loader for Windows, Linux, and MacOS."
    license = "Apache 2.0"
    
    exports = ["LICENSE.txt"]
    exports_sources = "CMakeLists.txt"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    generators = "cmake"

    settings = "os", "arch", "build_type", "compiler"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_wsi_xcb": [True, False],
        "with_wsi_xlib": [True, False],
        "with_wsi_wayland": [True, False],
        "with_wsi_mir": [True, False],
        "win10_onecore": [True, False],
        "build_loader": [True, False],
        "build_tests": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": False,
        "with_wsi_xcb": True,
        "with_wsi_xlib": True,
        "with_wsi_wayland": True,
        "with_wsi_mir": False,
        "win10_onecore": False,
        "build_loader": True,
        "build_tests": True
    }
    default_channel = "testing"
    default_user = "bartoc"

    def requirements(self):
        self.requires(f"Vulkan-Headers/{self.version}@{self.user}/{self.channel}")

    def source(self):
        source_url = "https://github.com/KhronosGroup/Vulkan-Loader"
        tools.get("{0}/archive/sdk-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-sdk-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
    
    def config_options(self):
        if self.settings.os != "Windows":
            del self.options.win10_onecore
        if self.settings.os != "Linux":
            del self.options.with_wsi_xcb
            del self.options.with_wsi_xlib
            del self.options.with_wsi_wayland
            del self.options.with_wsi_mir

    def _configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os == "Linux":
            cmake.definitions["BUILD_WSI_XCB_SUPPORT"] = self.options.with_wsi_xcb
            cmake.definitions["BUILD_WSI_XLIB_SUPPORT"] = self.options.with_wsi_xlib
            cmake.definitions["BUILD_WSI_WAYLAND_SUPPORT"] = self.options.with_wsi_wayland
            cmake.definitions["BUILD_WSI_MIR_SUPPORT"] = self.options.with_wsi_mir
        if self.settings.os == "Windows":
            cmake.definitions["ENABLE_WIN10_ONECORE"] = self.options.win10_onecore
        cmake.definitions["ENABLE_STATIC_LOADER"] = not self.options.shared
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
    
    

