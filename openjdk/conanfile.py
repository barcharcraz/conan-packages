#NOTE: inprogress

from conans import ConanFile, tools
import os
class OpenJDKConan(ConanFile):
    name = "OpenJDK"
    version = "11.0.1"
    license = "GPLv2 (classpath exception)"
    author = "Charles Barto <bartoc@umich.edu>"
    url = "https://github.com/barcharcraz/conan-packages"
    description = "java openjdk"
    topics = ("languages", "compilers", "doggos")
    settings = "os", "compiler", "build_type", "arch"
    
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        source_url= "https://hg.openjdk.java.net/jdk-updates/jdk11u/archive/8513ac27b651.tar.gz"
        source_hash = "a2622cce55c3517e2dccb2b703860029b45a58b0e9bce7a250cf3ad8a8c8af1f"
        tools.get(source_url, sha256=source_hash)
        extracted_dir = "jdk11u-8513ac27b651"
        os.rename(extracted_dir, self._source_subfolder)