from conans import ConanFile, CMake, tools
import shutil
import os

class LibpqConan(ConanFile):
    name = "libpq"
    version = "9.6.2"
    license = "PostgreSQL"
    description = "the Postgresql client library"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "CMakeLists.txt"
    generators = "cmake"
    requires = (
        ("OpenSSL/[>=1.0.2k]@lasote/stable")
    )

    def source(self):
        zip_name = f"postgresql-{self.version}.tar.gz"
        tools.download(f"https://ftp.postgresql.org/pub/source/v{self.version}/postgresql-{self.version}.tar.gz", zip_name)
        tools.untargz(zip_name)
        shutil.move(f"postgresql-{self.version}", "postgresql")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = [
            f'-DCMAKE_INSTALL_PREFIX={self.package_folder}',
            f'-DBUILD_SHARED_LIBS={self.options.shared}'
        ]
        self.run(f"cmake {self.conanfile_directory} {cmake.command_line} {' '.join(cmake_options)}")
        self.run(f"cmake --build . {cmake.build_config}")

    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")
