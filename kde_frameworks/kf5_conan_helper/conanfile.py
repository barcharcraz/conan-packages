from conans import ConanFile

class Kf5ConanHelperConan(ConanFile):
    name = "Kde Frameworks 5 conan helper"
    version = "0.1"
    exports = "*"
    build_policy = "missing"