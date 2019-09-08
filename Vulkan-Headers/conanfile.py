#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, CMake
import os


class VulkanHeadersConan(ConanFile):
    name = "Vulkan-Headers"
    version = "1.1.114.0"
    url = "https://github.com/barcharcraz/conan-packages"
    author = "Charles Barto <bartoc@umich.edu>"
    description = "Headers for Vulkan"
    no_copy_source = False

    # Indicates License type of the packaged library
    license = "Apache 2.0"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.txt"]

    exports_sources = ["CMakeLists.txt"]

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    generators = "cmake"

    def source(self):
        source_url = "https://github.com/KhronosGroup/Vulkan-Headers"
        tools.get("{0}/archive/sdk-{1}.tar.gz".format(source_url, self.version),
            sha256="701cc5391c5c757b48f0b8bc6944586c3d479cff7e1803acac9f59c11e9cebf2")
        extracted_dir = "Vulkan-Headers-sdk-" + self.version
        

        #Rename to "source_folder" is a convention to simplify later steps
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


    def package_id(self):
        self.info.header_only()
