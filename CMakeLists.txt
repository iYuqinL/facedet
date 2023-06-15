cmake_minimum_required(VERSION 2.8.12)
project(libfacedetection)


option(ENABLE_NEON "whether use neon, if use arm please set it on" OFF)
option(ENABLE_AVX512 "use avx512" OFF)
option(ENABLE_AVX2 "use avx2" OFF)
option(DEMO "build the demo" OFF)
option(USE_OPENMP "Use OpenMP" ON)
option(BUILD_PYTHONLIB "Build python exporting" OFF)

if (BUILD_SHARED_LIBS)
	add_definitions(-DBUILD_SHARED_LIBS)
    if (CMAKE_COMPILER_IS_GNUCXX AND NOT MINGW)
       # Just setting CMAKE_POSITION_INDEPENDENT_CODE should be enough to set
       # -fPIC for GCC but sometimes it still doesn't get set, so make sure it
       # does.
       add_definitions("-fPIC")
    endif()
    set(CMAKE_POSITION_INDEPENDENT_CODE ON)
endif()

SET(BUILD_VERSION "v0.0.3")
# Find Git Version Patch
IF(EXISTS "${CMAKE_SOURCE_DIR}/.git")
    if(NOT GIT)
        SET(GIT $ENV{GIT})
    endif()
    if(NOT GIT)
        FIND_PROGRAM(GIT NAMES git git.exe git.cmd)
    endif()
    IF(GIT)
        EXECUTE_PROCESS(
            WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
            COMMAND ${GIT} describe --tags
            OUTPUT_VARIABLE GIT_VERSION  OUTPUT_STRIP_TRAILING_WHITESPACE
        )
        if(NOT GIT_VERSION)
            EXECUTE_PROCESS(
                WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
                COMMAND ${GIT} rev-parse --short HEAD
                OUTPUT_VARIABLE GIT_VERSION OUTPUT_STRIP_TRAILING_WHITESPACE
            )
        endif()
        IF(NOT GIT_VERSION)
            SET(BUILD_VERSION ${GIT_VERSION})
	ENDIF()
    ENDIF()
ENDIF()
message("BUILD_VERSION:${BUILD_VERSION}")

SET(fdt_base_dir   ${PROJECT_SOURCE_DIR})
SET(fdt_src_dir    ${fdt_base_dir}/facedet)
SET(fdt_inc_dir    ${fdt_base_dir}/facedet)

SET(fdt_lib_name   facedet)

FILE(GLOB_RECURSE fdt_source_files ${fdt_src_dir}/facedetcnn*.cc)
LIST(SORT         fdt_source_files)

SET(INSTALLHEADER_FILES ${fdt_inc_dir}/facedetcnn.h)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

IF(CMAKE_CXX_COMPILER_ID STREQUAL "GNU"
    OR CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    #use -O3 to speedup
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")
ENDIF()

if(ENABLE_AVX512)
	add_definitions(-D_ENABLE_AVX512)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mavx512bw")
endif()

if(ENABLE_AVX2)
	add_definitions(-D_ENABLE_AVX2)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mavx2 -mfma")
endif()

if(ENABLE_NEON)
	message("Using ENON")
	add_definitions(-D_ENABLE_NEON)
endif()

if(USE_OPENMP)
    FIND_PACKAGE(OpenMP)
    if(OPENMP_FOUND)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
    endif()
endif()

INCLUDE_DIRECTORIES(${fdt_inc_dir})

include(CMakePackageConfigHelpers)
include(GenerateExportHeader)
include(GNUInstallDirs)

# Create a library
ADD_LIBRARY(${fdt_lib_name} ${fdt_source_files} ${INSTALLHEADER_FILES})
set_target_properties(${fdt_lib_name} PROPERTIES
    PUBLIC_HEADER "${INSTALLHEADER_FILES}" # Install head files
    VERSION ${BUILD_VERSION}
   )

# Install target
INSTALL(TARGETS ${fdt_lib_name}
    EXPORT ${fdt_lib_name}Config
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/facedetection
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    )
export(TARGETS ${fdt_lib_name}
       APPEND FILE ${CMAKE_BINARY_DIR}/${fdt_lib_name}Config.cmake
)
# Install cmake configure files
install(EXPORT ${fdt_lib_name}Config
        DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/${fdt_lib_name}"
        )
write_basic_package_version_file(
    "${CMAKE_BINARY_DIR}/${fdt_lib_name}ConfigVersion.cmake"
    VERSION ${BUILD_VERSION}
    COMPATIBILITY AnyNewerVersion)
install(FILES "${CMAKE_BINARY_DIR}/${fdt_lib_name}ConfigVersion.cmake" DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/${fdt_lib_name}")

# Python binding
if (BUILD_PYTHONLIB)
    find_package(pybind11 CONFIG REQUIRED)
    pybind11_add_module(pyfacedet
        ${fdt_base_dir}/facedet/facedetbinding.cc
        ${fdt_source_files}
        ${INSTALLHEADER_FILES}
    )
    target_link_libraries(pyfacedet PUBLIC)
    install(TARGETS pyfacedet
            COMPONENT python
            RUNTIME DESTINATION "${PYTHON_LIBRARY_DIR}"
            LIBRARY DESTINATION "${PYTHON_LIBRARY_DIR}"
            ARCHIVE DESTINATION "${PYTHON_LIBRARY_DIR}")
endif()


# Create demo. OpenCV is requred.
if (DEMO)
    find_package(OpenCV REQUIRED)
    include_directories(${OpenCV_INCLUDE_DIRS})

    add_executable(testfacedet ${fdt_base_dir}/testfacedet.cc)
    target_link_libraries(testfacedet ${fdt_lib_name} ${OpenCV_LIBS})
endif()



message("CXX_FLAGS: ${CMAKE_CXX_FLAGS}")
message("LINKER_FLAGS: ${CMAKE_EXE_LINKER_FLAGS}")
message("AVX512 = ${ENABLE_AVX512}")
message("AVX2 = ${ENABLE_AVX2}")
message("NEON = ${ENABLE_NEON}")
message("OpenMP = ${OPENMP_FOUND}")
message("DEMO = ${DEMO}")