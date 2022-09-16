
import os

from conans import ConanFile, tools, AutoToolsBuildEnvironment


class LibNodeConan(ConanFile):
    name = "libnode"
    version = "14.18.2"
    #version = "14.16.1"

    # Optional metadata
    license = "MIT"
    homepage = "https://github.com/nodejs/node"
    url = "https://github.com/conan-io/conan-center-index"
    description = "Node.js JavaScript runtime"

    # Binary configuration
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {
        "shared": False,
        "fPIC": True,
        "icu:shared": True,
    }

    requires = [
        "openssl/1.1.1l",
        "icu/69.1",
    ]

    def source(self):
        url = f"https://github.com/nodejs/node/archive/refs/tags/v{self.version}.tar.gz"
        tools.get(url=url, strip_root=True)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)

        cflags = []
        args=[
            "--without-dtrace",
            "--with-intl=small-icu",
            "--openssl-use-def-ca-store",
        ]

        if self.options.fPIC:
            cflags.append("-fPIC")
        if self.options.shared:
            args.append("--shared")

        cflags.append("-fvisibility=default")

        cflags_str = " ".join(cflags)
        
        build_vars = {
            "CFLAGS": cflags_str,
            "CXXFLAGS": cflags_str,
        }
        print(build_vars)

        autotools.configure(args=args, vars=build_vars)
        autotools.make(vars=build_vars)

    def package(self):
        self.copy("node", dst="bin", src="out/Release/")
        self.copy("*.h", dst="include/node", src="src")
        self.copy("*.h", dst="include", src="deps/v8/include/")
        self.copy("libnode.lib", src="out/Release/obj.target/", dst="lib", keep_path=False)
        self.copy("libnode.a", src="out/Release/obj.target/", dst="lib", keep_path=False)

        if self.options.shared:
            self.run("cd out/Release/obj.target/; ln -s libnode.so.83 libnode.so")
            self.copy("libnode.so*", src="out/Release/obj.target/", dst="lib", keep_path=False, symlinks=True)

        self.copy("libuv.*", src="out/Release/obj.target/deps/uv/", dst="lib", keep_path=False)
        self.copy("libuvwasi.*", src="out/Release/obj.target/deps/uvwasi/", dst="lib", keep_path=False)
        self.copy("libhistogram.*", src="out/Release/obj.target/deps/histogram/", dst="lib", keep_path=False)
        self.copy("*", src="out/Release/obj.target/deps/brotli/", dst="lib", keep_path=False)
        self.copy("*", src="out/Release/obj.target/deps/cares/", dst="lib", keep_path=False)
        self.copy("*", src="out/Release/obj.target/deps/googletest/", dst="lib", keep_path=False)
        self.copy("*", src="out/Release/obj.target/deps/llhttp/", dst="lib", keep_path=False)
        self.copy("*", src="out/Release/obj.target/deps/nghttp2/", dst="lib", keep_path=False)
        self.copy("*", src="out/Release/obj.target/deps/openssl/", dst="lib", keep_path=False)
        self.copy("*", src="out/Release/obj.target/deps/zlib/", dst="lib", keep_path=False)
        self.copy("*", src="out/Release/obj.target/tools/icu/", dst="lib", keep_path=False)
        self.copy("*.a", src="out/Release/obj.target/tools/v8_gypfiles/", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["node"]
