from conans import ConanFile, tools, CMake, MSBuild
import os


class PythonConan(ConanFile):
    name = "python"
    version = "3.7.1"
    author = "Charles Barto <bartoc@umich.edu>"
    url = "https://github.com/barcharcraz/conan-packages"
    description = "The python programming language"
    settings = "os", "build_type", "arch", "compiler"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        source_url = f"https://www.python.org/ftp/python/{self.version}/Python-{self.version}.tgz"
        tools.get(
            source_url, sha256="36c1b81ac29d0f8341f727ef40864d99d8206897be96be73dc34d4739c9c9f06")
        extracted_dir = f"Python-{self.version}"
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        if self.settings.compiler == "Visual Studio":
            msbuild = MSBuild(self)
            msbuild.build(f"{self._source_subfolder}/PCBuild/pythoncore.vcxproj",
                          targets=["Build"],
                          upgrade_project=False,
                          properties={
                              "IncludeExternals": "false",
                              "IncludeSSL": "false",
                              "IncludeTkinter": "false"})
