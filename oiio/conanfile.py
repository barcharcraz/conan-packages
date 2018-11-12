from conans import ConanFile, CMake, tools
import os

class OpenimageioConan(ConanFile):
    name = "OpenImageIO"
    version = "1.8.16"
    license = "BSD 3-clause"
    author = "Charles Barto <bartoc@umich.edu>"
    url = "https://github.com/barcharcraz/conan-packages"
    description = "Open Image IO library"
    topics = ("graphics", "images", "IO")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }
    generators = "cmake"

    requires = (
        "libtiff/4.0.9@bincrafters/stable",
        "libpng/1.6.34@bincrafters/stable",
        "openexr/2.3.0@conan/stable"
    )

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"


    def source(self):
        source_url = f"https://github.com/OpenImageIO/oiio/archive/Release-{self.version}.tar.gz"
        tools.get(source_url, sha256='a67bb2800805bce10c055bc3f5ed32ce31498381fc1cf8e42e24d4193f3f935f')
        extracted_dir = f"oiio-Release-{self.version}"
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        cmake.definitions["BUILDSTATIC"] = self.options.shared
        cmake.definitions["EMBEDPLUGINS"] = False
        cmake.definitions["USE_DICOM"] = False
        cmake.definitions["USE_FFMPEG"] = False
        cmake.definitions["USE_EXTERNAL_PUGIXML"] = True
        cmake.definitions["USE_GIF"] = False
        cmake.definitions["USE_FIELD3D"] = False
        cmake.definitions["USE_JPEGTURBO"] = False
        cmake.definitions["USE_FREETYPE"] = False
        cmake.definitions["USE_LIBRAW"] = False
        cmake.definitions["USE_NUKE"] = False
        cmake.definitions["USE_OPENCV"] = False
        cmake.definitions["USE_OPENJPEG"] = False
        cmake.definitions["USE_OPENSSL"] = False
        cmake.definitions["USE_OPENGL"] = False
        cmake.definitions["USE_PTEX"] = False
        cmake.definitions["USE_PYTHON"] = False
        cmake.definitions["USE_QT"] = False
        cmake.definitions["USE_SIMD"] = "0"
        cmake.definitions["USE_fPIC"] = self.options.fPIC
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["hello"]

