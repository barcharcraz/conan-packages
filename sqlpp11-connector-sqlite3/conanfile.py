from conans import ConanFile, CMake, tools
import shutil
import os

class Sqlpp11ConnectorSqlite3Conan(ConanFile):
    name = "sqlpp11-connector-sqlite3"
    version = "0.24"
    description = "sqlite interface for sqlpp11"
    license = "BSD"
    requires = (
        ("HinnantDate/[~=2]@barcharcraz/testing"),
        ("sqlite3/[~3]@barcharcraz/testing"),
        ("sqlpp11/[~0]@barcharcraz/testing")
    )
    url = "https://github.com/barcharcraz/conan-packages"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "CMakeLists.txt"
    generators = "cmake"

    def source(self):
        zip_name = f"sqlpp-{self.version}"
        tools.download(f"https://github.com/rbock/sqlpp11-connector-sqlite3/archive/{self.version}.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move(f"{self.name}-{self.version}", f"{self.name}")
        os.unlink(zip_name)
    def build(self):
        cmake = CMake(self.settings)
        date_include_path = os.path.join(self.deps_cpp_info['HinnantDate'].rootpath,
                                         self.deps_cpp_info['HinnantDate'].includedirs[0])
        sqlpp11_include_path = os.path.join(self.deps_cpp_info['sqlpp11'].rootpath,
                                         self.deps_cpp_info['sqlpp11'].includedirs[0])
        self.output.info(date_include_path)
        self.output.info(sqlpp11_include_path)
        args = [f"-DBUILD_SHARED_LIBS={self.options.shared}",
                f'-DCMAKE_INSTALL_PREFIX="{self.package_folder}"',
                "-DENABLE_TESTS=OFF",
                f"-DDATE_INCLUDE_DIR={date_include_path}",
                f"-DSQLPP11_INCLUDE_DIR={sqlpp11_include_path}"]
        self.run(f"cmake . {cmake.command_line} {' '.join(args)}")
        self.run(f"cmake --build . {cmake.build_config}")
    def package(self):
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install {cmake.build_config}")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []

