###############################################################################
#
# CMake main configuration file to build GeoTIFF library and utilities.
#
# Author: Mateusz Loskot <mateusz@loskot.net>
#
###############################################################################
PROJECT(GeoTIFF)

SET(GEOTIFF_LIB_NAME geotiff)
SET(GEOTIFF_LIBRARY_TARGET geotiff_library)
SET(GEOTIFF_ARCHIVE_TARGET geotiff_archive)

##############################################################################
# CMake settings
CMAKE_MINIMUM_REQUIRED(VERSION 2.6.0)

SET(CMAKE_COLOR_MAKEFILE ON)

# Version information
set(PROJECT_VERSION_MAJOR 1)
set(PROJECT_VERSION_MINOR 4)
set(PROJECT_VERSION_PATCH 1)
set(PROJECT_VERSION
  "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")
set(GeoTIFF_VERSION ${PROJECT_VERSION})

# Set library version to match that of autoconf:
# libgeotiff.so -> libgeotiff.so.2.1.1
# libgeotiff.so.2 -> libgeotiff.so.2.1.1
# libgeotiff.so.2.1.1
set(LINK_SOVERSION "2")
set(LINK_VERSION "2.1.1")

string (TOLOWER ${PROJECT_NAME} PROJECT_NAME_LOWER)
string (TOUPPER ${PROJECT_NAME} PROJECT_NAME_UPPER)

# Allow advanced users to generate Makefiles printing detailed commands
MARK_AS_ADVANCED(CMAKE_VERBOSE_MAKEFILE)

# Path to additional CMake modules
SET(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

###############################################################################
# General build settings

IF(NOT CMAKE_BUILD_TYPE)
    SET(CMAKE_BUILD_TYPE Debug CACHE STRING
        "Choose the type of build, options are: None Debug Release RelWithDebInfo MinSizeRel"
        FORCE)
ENDIF()

SET(GEOTIFF_BUILD_PEDANTIC FALSE CACHE BOOL "Choose compilation in pedantic or relaxed mode")
IF(CMAKE_BUILD_TYPE MATCHES Debug)
    SET(GEOTIFF_BUILD_PEDANTIC TRUE)
ENDIF()

if (CMAKE_MAJOR_VERSION GREATER 2)
cmake_policy(SET CMP0022 OLD) # interface link libraries
cmake_policy(SET CMP0042 OLD) # osx rpath
endif()


# TODO: Still testing the output paths --mloskot
SET(GEOTIFF_BUILD_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)

# Output directory in which to build RUNTIME target files.
# SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${GEOTIFF_BUILD_OUTPUT_DIRECTORY})
SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)

# Output directory in which to build LIBRARY target files
# SET(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${GEOTIFF_BUILD_OUTPUT_DIRECTORY})
SET(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib)

# Output directory in which to build ARCHIVE target files.
# SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${GEOTIFF_BUILD_OUTPUT_DIRECTORY})
SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib)

###############################################################################
# Platform and compiler specific settings

IF(WIN32)
    IF(MSVC)
        ADD_DEFINITIONS(-DBUILD_AS_DLL=1)
        ADD_DEFINITIONS(/DW4)
        if (NOT (MSVC_VERSION VERSION_LESS 1400))
            ADD_DEFINITIONS(-D_CRT_SECURE_NO_DEPRECATE)
            ADD_DEFINITIONS(-D_CRT_SECURE_NO_WARNINGS)
            ADD_DEFINITIONS(-D_CRT_NONSTDC_NO_WARNING)
            ADD_DEFINITIONS(-D_SCL_SECURE_NO_WARNINGS)
        endif()
    ENDIF(MSVC)
ENDIF()

IF(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
    SET(COMPILE_FLAGS "-fPIC -Wall -Wno-long-long")
    SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${COMPILE_FLAGS} -std=c99")
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${COMPILE_FLAGS} -std=c++98")
    IF(GEOTIFF_BUILD_PEDANTIC)
        SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -pedantic")
        SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pedantic")
    ENDIF()
ENDIF()

# Check required standard headers
INCLUDE(CheckIncludeFiles)
CHECK_INCLUDE_FILES(stdio.h HAVE_STDIO_H)
CHECK_INCLUDE_FILES(stdlib.h HAVE_STDLIB_H)
CHECK_INCLUDE_FILES(string.h HAVE_STRING_H)

###############################################################################
# User-defined build settings

SET(GEOTIFF_CSV_NAMES area.csv codes.csv datum.csv gcs.csv pcs.csv)
FIND_PATH(GEOTIFF_CSV_DATA_DIR NAMES ${GEOTIFF_CSV_NAMES}
    PATHS "${CMAKE_SOURCE_DIR}/csv"
    DOC "Default location of GeoTIFF CSV files"
    NO_DEFAULT_PATH)

IF(IS_DIRECTORY ${GEOTIFF_CSV_DATA_DIR} AND EXISTS "${GEOTIFF_CSV_DATA_DIR}/gcs.csv")
    MESSAGE(STATUS "Found GeoTIFF CSV files in: ${GEOTIFF_CSV_DATA_DIR}")
    ADD_DEFINITIONS(-DCSV_DATA_DIR="${GEOTIFF_CSV_DATA_DIR}")
ELSE()
    MESSAGE(FATAL_ERROR "Failed to find GeoTIFF CSV files in: ${GEOTIFF_CSV_DATA_DIR}")
ENDIF()

SET(WITH_UTILITIES TRUE CACHE BOOL "Choose if GeoTIFF utilities should be built")

###############################################################################
# Search for dependencies

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR})
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/libxtiff)

# TIFF support - required, default=ON
SET(WITH_TIFF TRUE CACHE BOOL "Choose if TIFF support should be built")

# PROJ.4 support - optional, default=ON
SET(WITH_PROJ4 TRUE CACHE BOOL "Choose if PROJ.4 support should be built")

IF(WITH_PROJ4)
    FIND_PACKAGE(PROJ4 NO_MODULE QUIET)
    if (NOT PROJ4_FOUND)
      FIND_PACKAGE(PROJ4)
    endif ()

    IF(PROJ4_FOUND)
        ADD_DEFINITIONS(-DHAVE_LIBPROJ=1)
        INCLUDE_DIRECTORIES(${PROJ4_INCLUDE_DIR})
    ENDIF()
ENDIF()

# Zlib support - optional, default=OFF
SET(WITH_ZLIB FALSE CACHE BOOL "Choose if zlib support should be built")

IF(WITH_ZLIB)
    FIND_PACKAGE(ZLIB NO_MODULE QUIET)
    if (NOT ZLIB_FOUND)
      FIND_PACKAGE(ZLIB)
    endif ()

    IF(ZLIB_FOUND)
        SET(HAVE_ZIP 1)
        INCLUDE_DIRECTORIES(${ZLIB_INCLUDE_DIR})
        ADD_DEFINITIONS(-DHAVE_ZIP=${HAVE_ZIP})
    ENDIF()
ENDIF()

# JPEG support - optional, default=OFF
SET(WITH_JPEG FALSE CACHE BOOL "Choose if JPEG support should be built")

IF(WITH_JPEG)
    FIND_PACKAGE(JPEG NO_MODULE QUIET)
    if (NOT JPEG_FOUND)
      FIND_PACKAGE(JPEG)
    endif ()

    IF(JPEG_FOUND)
        SET(HAVE_JPEG 1)
        INCLUDE_DIRECTORIES(${JPEG_INCLUDE_DIR})
        ADD_DEFINITIONS(-DHAVE_JPEG=${HAVE_JPEG})
    ENDIF()
ENDIF()

IF(WITH_TIFF)
    FIND_PACKAGE(TIFF NO_MODULE QUIET)
    if (NOT TIFF_FOUND)
      FIND_PACKAGE(TIFF REQUIRED)
    endif ()

    IF(TIFF_FOUND)
        # Confirm required API is available
        INCLUDE(CheckFunctionExists)
        SET(CMAKE_REQUIRED_LIBRARIES ${TIFF_LIBRARIES})

        CHECK_FUNCTION_EXISTS(TIFFOpen HAVE_TIFFOPEN)
        IF(NOT HAVE_TIFFOPEN)
            SET(TIFF_FOUND) # ReSET to NOT found for TIFF library
            MESSAGE(FATAL_ERROR "Failed to link with libtiff - TIFFOpen function not found")
        ENDIF()

        CHECK_FUNCTION_EXISTS(TIFFMergeFieldInfo HAVE_TIFFMERGEFIELDINFO)
        IF(NOT HAVE_TIFFMERGEFIELDINFO)
            SET(TIFF_FOUND) # ReSET to NOT found for TIFF library
            MESSAGE(FATAL_ERROR "Failed to link with libtiff - TIFFMergeFieldInfo function not found. libtiff 3.6.0 Beta or later required. Please upgrade or use an older version of libgeotiff")
        ENDIF()

        INCLUDE_DIRECTORIES(${TIFF_INCLUDE_DIR})
        ADD_DEFINITIONS(-DHAVE_TIFF=1)
    ENDIF(TIFF_FOUND)
ENDIF(WITH_TIFF)

# Turn off TOWGS84 support
SET(WITH_TOWGS84 TRUE CACHE BOOL "Build with TOWGS84 support")
IF (NOT WITH_TOWGS84)
   SET(GEO_NORMALIZE_DISABLE_TOWGS84 1)
endif()

###############################################################################
# Generate geo_config.h with compile-time configuration

MESSAGE(STATUS "Generating geo_config.h header")

CONFIGURE_FILE (${CMAKE_CURRENT_SOURCE_DIR}/cmake/geo_config.h.in
  geo_config.h)
INCLUDE_DIRECTORIES(BEFORE ${CMAKE_CURRENT_BINARY_DIR})

MESSAGE(STATUS "Generating geo_config.h header - done")


###############################################################################
# Installation settings

SET(GEOTIFF_CSV_DATA
    csv/alias.csv
    csv/area.csv
    csv/change.csv
    csv/compdcs.csv
    csv/coordinate_axis.csv
    csv/coordinate_axis_name.csv
    csv/coordinate_operation.csv
    csv/coordinate_operation_method.csv
    csv/coordinate_operation_parameter.csv
    csv/coordinate_operation_parameter_value.csv
    csv/coordinate_operation_path.csv
    csv/coordinate_reference_system.csv
    csv/coordinate_system.csv
    csv/datum.csv
    csv/datum_shift.csv
    csv/datum_shift_pref.csv
    csv/deprecation.csv
    csv/ellipsoid.csv
    csv/esri_datum_override.csv
    csv/gcs.csv
    csv/gcs.override.csv
    csv/geoccs.csv
    csv/naming_system.csv
    csv/pcs.csv
    csv/pcs.override.csv
    csv/prime_meridian.csv
    csv/projop_wparm.csv
    csv/stateplane.csv
    csv/supersession.csv
    csv/unit_of_measure.csv
    csv/version_history.csv
    csv/vertcs.csv
    csv/vertcs.override.csv )

SET(GEOTIFF_LIB_HEADERS
    geotiff.h
    geotiffio.h
    geovalues.h
    geonames.h
    geokeys.h
    ${CMAKE_CURRENT_BINARY_DIR}/geo_config.h
    geo_tiffp.h
    geo_keyp.h
    geo_normalize.h
    cpl_serv.h
    geo_simpletags.h
    epsg_datum.inc
    epsg_gcs.inc
    epsg_pm.inc
    epsg_units.inc
    geo_ctrans.inc
    epsg_ellipse.inc
    epsg_pcs.inc
    epsg_proj.inc
    epsg_vertcs.inc
    geokeys.inc
    libxtiff/xtiffio.h)

#    ${PROJECT_BINARY_DIR}/geotiff_version.h

IF(WIN32)
    SET(DEFAULT_LIB_SUBDIR lib)
    SET(DEFAULT_DATA_SUBDIR .)
    SET(DEFAULT_INCLUDE_SUBDIR include)

    IF(MSVC)
        SET(DEFAULT_BIN_SUBDIR bin)
    ELSE()
        SET(DEFAULT_BIN_SUBDIR .)
    ENDIF()
ELSE()
    # Common locatoins for Unix and Mac OS X
    SET(DEFAULT_BIN_SUBDIR bin)
    SET(DEFAULT_LIB_SUBDIR lib)
    SET(DEFAULT_DATA_SUBDIR share)
    SET(DEFAULT_INCLUDE_SUBDIR include)
ENDIF()

# Locations are changeable by user to customize layout of GeoTIFF installation
# (default values are platform-specIFic)
SET(GEOTIFF_BIN_SUBDIR ${DEFAULT_BIN_SUBDIR} CACHE STRING
    "Subdirectory where executables will be installed")
SET(GEOTIFF_LIB_SUBDIR ${DEFAULT_LIB_SUBDIR} CACHE STRING
    "Subdirectory where libraries will be installed")
SET(GEOTIFF_INCLUDE_SUBDIR ${DEFAULT_INCLUDE_SUBDIR} CACHE STRING
    "Subdirectory where header files will be installed")
SET(GEOTIFF_DATA_SUBDIR ${DEFAULT_DATA_SUBDIR} CACHE STRING
    "Subdirectory where data will be installed")

# Mark *_SUBDIR variables as advanced and dedicated to use by power-users only.
MARK_AS_ADVANCED(GEOTIFF_BIN_SUBDIR GEOTIFF_LIB_SUBDIR GEOTIFF_INCLUDE_SUBDIR GEOTIFF_DATA_SUBDIR)

# Full paths for the installation
SET(GEOTIFF_BIN_DIR ${GEOTIFF_BIN_SUBDIR})
SET(GEOTIFF_LIB_DIR ${GEOTIFF_LIB_SUBDIR})
SET(GEOTIFF_INCLUDE_DIR ${GEOTIFF_INCLUDE_SUBDIR})
SET(GEOTIFF_DATA_DIR ${GEOTIFF_DATA_SUBDIR})

# Install doc files
INSTALL(FILES
    AUTHORS ChangeLog COPYING INSTALL LICENSE README README_BIN README.WIN
    DESTINATION doc)
#    DESTINATION ${GEOTIFF_DATA_DIR}/doc)

# Install CSV data files
# INSTALL(FILES ${GEOTIFF_CSV_DATA} DESTINATION ${GEOTIFF_DATA_DIR}/epsg_csv)
INSTALL(FILES ${GEOTIFF_CSV_DATA} DESTINATION share/epsg_csv)

# Install header files for development distribution
# INSTALL(FILES ${GEOTIFF_LIB_HEADERS} DESTINATION ${GEOTIFF_INCLUDE_DIR})
INSTALL(FILES ${GEOTIFF_LIB_HEADERS} DESTINATION include)

###############################################################################
# Build libxtiff library

ADD_SUBDIRECTORY(libxtiff)

###############################################################################
# Build libgeotiff library

SET(GEOTIFF_LIB_SOURCES
    cpl_serv.c
    cpl_csv.c
    geo_extra.c
    geo_free.c
    geo_get.c
    geo_names.c
    geo_new.c
    geo_normalize.c
    geo_print.c
    geo_set.c
    geo_simpletags.c
    geo_tiffp.c
    geo_trans.c
    geo_write.c
    geotiff_proj4.c)

SET(INCODE_EPSG_FROM_CSV FALSE CACHE BOOL "Build source-encoded EPSG data files")

FOREACH(epsg_csv_file ${GEOTIFF_CSV_DATA})
    # We cannot use NAME_WE without string-replace, because that would
    # give "gcs.csv" and "gcs.override.csv" the same epsg_csv_name
    GET_FILENAME_COMPONENT(epsg_csv_name "${epsg_csv_file}" NAME)
    STRING(REPLACE ".csv" "" epsg_csv_basename "${epsg_csv_name}")
    # SET(INCODE_EPSG_FROM_CSV_${epsg_csv_basename} FALSE CACHE BOOL "Build ${epsg_csv_basename} file target")

    # IF(INCODE_EPSG_FROM_CSV_${epsg_csv_basename})
    if( INCODE_EPSG_FROM_CSV)
        SET(epsg_source_name "${CMAKE_CURRENT_BINARY_DIR}/incode_epsg_${epsg_csv_basename}.c")
        LIST(APPEND GEOTIFF_LIB_CSV_SOURCES "${epsg_source_name}")

        # sanitize .'s out of struct names
        STRING(REGEX REPLACE "\\." "_" STRUCT_NAME ${epsg_csv_basename})
        LIST(APPEND epsg_includefile_externconst "\nextern const datafile_rows_t *${STRUCT_NAME}_rows[]")
        LIST(APPEND epsg_includefile_pointer_list "  { \"${STRUCT_NAME}\", ${STRUCT_NAME}_rows },")
        MESSAGE(STATUS "Creating buildrule to convert ${epsg_csv_basename}.csv to ${epsg_csv_basename}.c and include it in code.")
        ADD_CUSTOM_COMMAND(OUTPUT "${epsg_source_name}"
            COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/csv/csv2c.py" "${CMAKE_CURRENT_SOURCE_DIR}/${epsg_csv_file}" "${epsg_source_name}"
            DEPENDS "${epsg_csv_file}"
            WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
            VERBATIM)
    ENDIF()
ENDFOREACH()

SET(EPSG_INCODE_EXPLANATION
    "This file is autogenerated by CMake, based on the INCODE_EPSG_* options specified during configure.\n
    Choosing an EPSG CSV file for inclusion into code will run csv/csv2c.py on the file and include the\n
    resulting c-source as a build target, as opposed to using GDAL_DATA-dir to find the EPSG codes at runtime.")
STRING(REPLACE ";" "\n" EPSG_INCLUDEFILE_POINTER_STRING "${epsg_includefile_pointer_list}")
FILE(WRITE "${CMAKE_CURRENT_BINARY_DIR}/epsg_incode_header.h"
    "/* ${EPSG_INCODE_EXPLANATION} */\n${epsg_includefile_externconst}; \n\n/* Pointers to csv data included in code */\nstatic const datafile_t files[] = {\n${EPSG_INCLUDEFILE_POINTER_STRING}\n  { NULL, NULL }};")

SET(XTIFF_SOURCES libxtiff/xtiff.c)

#---
# Static libgeotiff archive
# NOTE: Did not put XTIFF_SOURCES in static lib because libxtiff.a is written out
#       currently.
#---
if (MSVC OR CMAKE_CONFIGURATION_TYPES)
  # For multi-config systems and for Visual Studio, the debug versions
  # of the libraries have a _d suffix.
  set (CMAKE_DEBUG_POSTFIX _d)
endif ()

ADD_LIBRARY(${GEOTIFF_ARCHIVE_TARGET} STATIC
    ${GEOTIFF_LIB_SOURCES} ${GEOTIFF_LIB_CSV_SOURCES})
SET_TARGET_PROPERTIES(${GEOTIFF_ARCHIVE_TARGET} PROPERTIES
    OUTPUT_NAME ${GEOTIFF_LIB_NAME})

# Shared libgeotiff library
ADD_LIBRARY(${GEOTIFF_LIBRARY_TARGET} SHARED
    ${GEOTIFF_LIB_SOURCES} ${GEOTIFF_LIB_CSV_SOURCES} ${XTIFF_SOURCES})

# Windows:
IF(WIN32 AND MSVC)
    SET_TARGET_PROPERTIES(${GEOTIFF_LIBRARY_TARGET} PROPERTIES IMPORT_SUFFIX "_i.lib")
ENDIF(WIN32 AND MSVC)


# Unix, linux:
IF(UNIX)
   SET_TARGET_PROPERTIES(
      ${GEOTIFF_LIBRARY_TARGET}
      PROPERTIES
      OUTPUT_NAME ${GEOTIFF_LIB_NAME}
      VERSION ${LINK_VERSION}
      SOVERSION ${LINK_SOVERSION}
      CLEAN_DIRECT_OUTPUT 1 )
   if (APPLE)
      set_target_properties(
        ${GEOTIFF_LIBRARY_TARGET}
        PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib")
   endif()

ELSE(UNIX)
# Default:
   SET_TARGET_PROPERTIES(${GEOTIFF_LIBRARY_TARGET} PROPERTIES
   OUTPUT_NAME ${GEOTIFF_LIB_NAME})
ENDIF(UNIX)

SET_TARGET_PROPERTIES(${GEOTIFF_LIBRARY_TARGET} PROPERTIES
   OUTPUT_NAME ${GEOTIFF_LIB_NAME})

TARGET_LINK_LIBRARIES(${GEOTIFF_LIBRARY_TARGET}
    ${TIFF_LIBRARIES}
    ${PROJ4_LIBRARIES}
    ${ZLIB_LIBRARIES}
    ${JPEG_LIBRARIES})

# INSTALL(TARGETS ${GEOTIFF_ARCHIVE_TARGET} ${GEOTIFF_LIBRARY_TARGET}
#	RUNTIME DESTINATION ${GEOTIFF_BIN_DIR}
#   LIBRARY DESTINATION ${GEOTIFF_LIB_DIR}
#   ARCHIVE DESTINATION ${GEOTIFF_LIB_DIR})

INSTALL( TARGETS ${GEOTIFF_ARCHIVE_TARGET} ${GEOTIFF_LIBRARY_TARGET}
	 EXPORT depends
	 RUNTIME DESTINATION bin
         LIBRARY DESTINATION lib
	 ARCHIVE DESTINATION lib )

# Define grouping of source files in PROJECT file (e.g. Visual Studio)
SOURCE_GROUP("CMake Files" FILES CMakeLists.txt)
SOURCE_GROUP("Header Files" FILES ${GEOTIFF_LIB_HEADERS})
SOURCE_GROUP("Source Files" FILES ${GEOTIFF_LIB_SOURCES})

###############################################################################
# Build GeoTIFF utilities

IF(WITH_UTILITIES)
    ADD_SUBDIRECTORY(bin)
ENDIF()

ADD_SUBDIRECTORY(cmake)
