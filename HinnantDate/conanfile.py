from conans import ConanFile, CMake, tools
import shutil
import os

class QuinceConan(ConanFile):
    name = "HinnantDate"
    version = "2.1"
    license = "MIT"
    url = "https://github.com/barcharcraz/conan-packages"
    settings = None
    #options = {"shared": [True, False]}
    #default_options = "shared=False"
    generators = "cmake"

    def source(self):
        zip_name = f"date-{self.version}"
        tools.download(f"https://github.com/HowardHinnant/date/archive/2.1.0.zip", zip_name)
        tools.unzip(zip_name)
        shutil.move(f"date-2.1.0", "date")
        os.unlink(zip_name)

    def build(self):
        pass

    def package(self):
        self.copy("date.h", src="date", dst="include")
        self.copy("iso_week.h", src="date", dst="include")
        self.copy("islamic.h", src="date", dst="include")
        self.copy("julian.h", src="date", dst="include")
        self.copy("chrono_io.h", src="date", dst="include")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []