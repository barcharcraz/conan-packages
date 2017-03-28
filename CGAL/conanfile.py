from conans import ConanFile, CMake, tools
import shutil
import os

class CGALConanFile(ConanFile):
    name = "CGAL"
    description = "The Computational Geometry Algorithms Library"
    version = "4.9"
    license = "GPLv3"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "header_only": [True, False]}
    default_options = "shared=False", "header_only=False"
    requires = (
        ("Boost/1.64.0b1@barcharcraz/testing")
    )
    generators = "cmake"
    exports = "CMakeLists.txt"

    def source(self):
        zip_name = f"{self.name}-{self.version}.zip"
        download_uri = f"https://github.com/CGAL/cgal/releases/download/releases%2FCGAL-{self.version}/CGAL-{self.version}.zip"
        tools.download(download_uri, zip_name)
        shutil.move(f"{self.name}-{self.version}", f"{self.name}")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = [
            f"-DCMAKE_INSTALL_PREFIX={self.package_folder}",
            f"-DBUILD_SHARED_LIBS={self.options.shared}"
        ]
        self.run(f"cmake . {cmake.command_line} {' '.join(cmake_options)}")
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package(self):
        pass

    def package_id(self):
        if self.options.header_only:
            self.info.requires.clear()
            self.info.settings.clear()