cmake_minimum_required(VERSION 3.1)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

include_directories(BEFORE ${CONAN_ICU_ROOT}/include)
link_directories(BEFORE ${CONAN_ICU_ROOT}/lib)
set(CMAKE_PREFIX_PATH ${CONAN_ICU_ROOT}/bin ${CMAKE_PREFIX_PATH})

message(${CONAN_ICU_ROOT})

add_subdirectory("source_subfolder/cpp")
