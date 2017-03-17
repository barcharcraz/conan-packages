from conans import ConanFile
from conans.tools import download, unzip, replace_in_file
import os
import shutil
from conans import CMake


class PocoConan(ConanFile):
    name = "Poco"
    version = "devel"
    url = "https://github.com/barcharcraz/conan-packages"
    license = "BOOST"
    description = "POCO C++ libraries"
    exports = "CMakeLists.txt"
    generators = "cmake", "txt"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "enable_xml": [True, False],
               "enable_json": [True, False],
               "enable_mongodb": [True, False],
               "enable_pdf": [True, False],
               "enable_util": [True, False],
               "enable_net": [True, False],
               "enable_netssl": [True, False],
               "enable_netssl_win": [True, False],
               "enable_crypto": [True, False],
               "enable_data": [True, False],
               "enable_data_sqlite": [True, False],
               "enable_data_mysql": [True, False],
               "enable_data_postgresql": [True, False],
               "enable_data_odbc": [True, False],
               "enable_sevenzip": [True, False],
               "enable_zip": [True, False],
               "enable_apacheconnector": [True, False],
               "enable_cppparser": [True, False],
               "enable_pocodoc": [True, False],
               "enable_pagecompiler": [True, False],
               "enable_pagecompiler_file2page": [True, False],
               "force_openssl": [True, False],  # "Force usage of OpenSSL even under windows"
               "enable_tests": [True, False],
               "poco_unbundled": [True, False],
               "cxx_14": [True, False]
               }
    default_options = '''
shared=False
enable_xml=True
enable_json=True
enable_mongodb=True
enable_pdf=False
enable_util=True
enable_net=True
enable_netssl=True
enable_netssl_win=True
enable_crypto=True
enable_data=True
enable_data_sqlite=True
enable_data_mysql=False
enable_data_postgresql=False
enable_data_odbc=False
enable_sevenzip=False
enable_zip=True
enable_apacheconnector=False
enable_cppparser=False
enable_pocodoc=False
enable_pagecompiler=False
enable_pagecompiler_file2page=False
force_openssl=True
enable_tests=False
poco_unbundled=False
cxx_14=False
'''

    def source(self):
        self.run("git clone https://github.com/barcharcraz/poco.git")
        """
        zip_name = "poco-%s-release.zip" % self.version
        download("https://github.com/pocoproject/poco/archive/develop.zip", zip_name)
        unzip(zip_name)
        shutil.move("poco-develop", "poco")
        os.unlink(zip_name)
        """

    def config(self):
        if self.options.enable_netssl or self.options.enable_crypto or self.options.force_openssl:
            # self.output.warn("ENABLED OPENSSL DEPENDENCY!!")
            self.requires.add("OpenSSL/1.0.2i@lasote/stable", private=False)
            self.options["OpenSSL"].shared = self.options.shared
            if self.options.shared and self.settings.compiler == "apple-clang" \
                    and self.settings.compiler.version == "7.3":
                self.options["OpenSSL"].shared = False
        else:
            if "OpenSSL" in self.requires:
                del self.requires["OpenSSL"]

        if self.options.enable_data_mysql:
            self.requires.add("MySQLClient/6.1.6@hklabbers/stable")
        else:
            if "MySQLClient" in self.requires:
                del self.requires["MySQLClient"]

    def build(self):
        cmake = CMake(self.settings)
        # Wrap original CMakeLists.txt for be able to include and call CONAN_BASIC_SETUP
        # It will allow us to set architecture flags, link with the requires etc
        cmake_options = []
        for option_name in self.options.values.fields:
            activated = getattr(self.options, option_name)
            the_option = "%s=" % option_name.upper()
            if option_name == "shared":
                the_option = "POCO_STATIC=OFF" if activated else "POCO_STATIC=ON"
            else:
                the_option += "ON" if activated else "OFF"
            cmake_options.append(the_option)

        options_poco = " -D".join(cmake_options)

        if self.settings.os == "Windows":
            if self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd":
                options_poco += " -DPOCO_MT=ON"
            else:
                options_poco += " -DPOCO_MT=OFF"
        options_poco += f" -DCMAKE_INSTALL_PREFIX={self.package_folder}"
        conf_command = 'cmake . %s -D%s' % (cmake.command_line, options_poco)

        self.output.warn(conf_command)
        self.run(conf_command)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        """ Copy required headers, libs and shared libs from the build folder to the package
        """
        # Typically includes we want to keep_path=True (default)
        """
        packages = ["CppUnit", "Crypto", "Data", "Data/MySQL", "Data/ODBC", "Data/SQLite",
                    "Foundation", "JSON", "MongoDB", "Net", "Util",
                    "XML", "Zip"]
        if self.settings.os == "Windows":
            packages.append("NetSSL_Win")
        else:
            packages.append("NetSSL_OpenSSL")

        for header in packages:
            self.copy(pattern="*.h", dst="include", src="poco/%s/include" % header)

        # But for libs and dlls, we want to avoid intermediate folders
        self.copy(pattern="*.lib", dst="lib", src="poco/lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="poco/lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="poco/bin", keep_path=False)
        # in linux shared libs are in lib, not bin
        self.copy(pattern="*.so*", dst="lib", src="poco/lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="poco/lib", keep_path=False)
        """
        cmake = CMake(self.settings)
        self.run(f"cmake --build . --target install -DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=ON {cmake.build_config}")
    def package_info(self):
        """ Define the required info that the consumers/users of this package will have
        to add to their projects
        """
        libs = [("enable_util", "PocoUtil"),
                ("enable_mongodb", "PocoMongoDB"),
                ("enable_pdf", "PocoPDF"),
                ("enable_net", "PocoNet"),
                ("enable_netssl", "PocoNetSSL"),
                ("enable_netssl_win", "PocoNetSSLWin"),
                ("enable_crypto", "PocoCrypto"),
                ("enable_data", "PocoData"),
                ("enable_data_sqlite", "PocoDataSQLite"),
                ("enable_data_mysql", "PocoDataMySQL"),
                ("enable_data_odbc", "PocoDataODBC"),
                ("enable_sevenzip", "PocoSevenZip"),
                ("enable_util", "PocoUtil"),
                ("enable_zip", "PocoZip"),
                ("enable_apacheconnector", "PocoApacheConnector"),
                ("enable_xml", "PocoXML"),
                ("enable_json", "PocoJSON")]
        for flag, lib in libs:
            if getattr(self.options, flag):
                if self.settings.os == "Windows" and flag == "enable_netssl":
                    continue
                if self.settings.os != "Windows" and flag == "enable_netssl_win":
                    continue
                self.cpp_info.libs.append(lib)

        self.cpp_info.libs.append("PocoFoundation")

        if self.settings.compiler == "Visual Studio" and self.options.shared == False:
            if self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd":
                self.cpp_info.libs = ["%smt" % lib for lib in self.cpp_info.libs]
            else:
                self.cpp_info.libs = ["%smd" % lib for lib in self.cpp_info.libs]

        # Debug library names has "d" at the final
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["%sd" % lib for lib in self.cpp_info.libs]

        # in linux we need to link also with these libs
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread", "dl", "rt"])

        if not self.options.shared:
            self.cpp_info.defines.extend(["POCO_STATIC=ON", "POCO_NO_AUTOMATIC_LIBS"])
            if self.settings.compiler == "Visual Studio":
                self.cpp_info.libs.extend(["ws2_32", "Iphlpapi.lib"])