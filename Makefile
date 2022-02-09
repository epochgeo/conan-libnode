
local: justsource justinstall justbuild justexport

_force:

clean: _force
	rm -rf cmake-build-release
	rm -rf build
	rm -rf package

create: _force
	conan create . test/debug

justsource: build
build:
	conan source . --source-folder=build

justinstall:
	conan install . --install-folder=build

justbuild:
	conan build . --build-folder=build --source-folder=build

package: justpackage
justpackage: build
	conan package . --build-folder=build --source-folder=build --package-folder=package

justexport: package
	conan export-pkg --force . test/debug --package-folder=package

