from conans import ConanFile, CMake, tools
import os

class VulkanHppConan(ConanFile):
    name = "Vulkan-Hpp"
    version = "20181125"
    commit_id = "f99407cf28d0baa0b480f284fa175594ff65d1d9"
    license = "Apache 2.0"
    url = "https://github.com/barcharcraz/conan-packages"
    author = "Charles Barto <bartoc@umich.edu>"
    description = "C++ Bindings for Vulkan"
    no_copy_source = True

    exports = ["LICENSE.txt"]

    _source_subfolder = "source_subfolder"

    generators = "cmake"

    def source(self):
        source_url = "https://github.com/KhronosGroup/Vulkan-Hpp/"
        tools.get("{0}/archive/{1}.zip".format(source_url, self.commit_id),
            sha256="9eb9b682300aa51a3dd3549eef4fea978f4ead3036590b4014a7da5d4b3bc602")
        extracted_dir = f"{self.name}-{self.commit_id}"
        os.rename(extracted_dir, self._source_subfolder)
        
    def package(self):
        include_folder = os.path.join(self._source_subfolder, "vulkan")
        self.copy(pattern="LICENSE.txt", dst="license", src=self._source_subfolder)
        self.copy(pattern="*", dst="include/vulkan", src=include_folder)
    
    def package_id(self):
        self.info.header_only()