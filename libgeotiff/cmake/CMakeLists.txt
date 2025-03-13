#############################################################################
# Config file generation and installation
#############################################################################


set (INSTALL_CMAKE_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")

include(CMakePackageConfigHelpers)
configure_package_config_file(
    project-config.cmake.in
    ${PROJECT_NAME_LOWER}Config.cmake
    PATH_VARS CMAKE_INSTALL_LIBDIR CMAKE_INSTALL_INCLUDEDIR CMAKE_INSTALL_BINDIR
    INSTALL_DESTINATION ${INSTALL_CMAKE_DIR}
)
write_basic_package_version_file(
    ${PROJECT_NAME_LOWER}ConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY AnyNewerVersion
)
install (FILES
  "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME_LOWER}Config.cmake"
  "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME_LOWER}ConfigVersion.cmake"
  DESTINATION "${INSTALL_CMAKE_DIR}"
)
install (EXPORT depends
  FILE ${PROJECT_NAME_LOWER}Targets.cmake
  DESTINATION "${INSTALL_CMAKE_DIR}")


#  ------------------------------------------------------------------------------
  # CPACK controls
  #------------------------------------------------------------------------------


  SET(CPACK_PACKAGE_VERSION_MAJOR ${PROJECT_VERSION_MAJOR})
  SET(CPACK_PACKAGE_VERSION_MINOR ${PROJECT_VERSION_MINOR})
  SET(CPACK_PACKAGE_VERSION_PATCH ${PROJECT_VERSION_PATCH})
  SET(CPACK_PACKAGE_NAME "GeoTIFF")

  SET(CPACK_SOURCE_GENERATOR "TBZ2;TGZ;ZIP")
  SET(CPACK_PACKAGE_VENDOR "GeoTIFF Development Team")
  SET(CPACK_RESOURCE_FILE_LICENSE    "${PROJECT_SOURCE_DIR}/LICENSE")

  set(CPACK_SOURCE_PACKAGE_FILE_NAME
      "lib${PROJECT_NAME_LOWER}-${GeoTIFF_VERSION}")

  set(CPACK_SOURCE_IGNORE_FILES
    "/\\\\.gitattributes"
    "/\\\\.DS_Store"
    "/\\\\.git/"
    "\\\\.swp$"
    "~$"
    "\\\\.\\\\#"
    "/\\\\#"
    "CMakeScripts/"
    "COPYING-CMAKE-SCRIPTS"
    "_CPack_Packages"
    "cmake_install.cmake"
    ".gitignore"
    ".ninja"
    ".deps"
    "HOWTORELEASE.txt"
    "README"
    "build/"
    "CMakeFiles"
    "CTestTestfile.cmake"
    ".gz"
    ".bz2"
  )

  include(CPack)
  add_custom_target(dist COMMAND ${CMAKE_MAKE_PROGRAM} package_source)
