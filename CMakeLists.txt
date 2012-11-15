cmake_minimum_required(VERSION 2.8.7)

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  set(EXTENSION_NAME iGynePy)
  set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/4.1/Extensions/iGynePy")
  set(EXTENSION_CATEGORY "IGT")
  set(EXTENSION_CONTRIBUTORS "Guillaume Pernelle")
  set(EXTENSION_DESCRIPTION "iGynePy moudle description...")
  set(EXTENSION_ICONURL "http://viewvc.slicer.org/viewvc.cgi/Slicer4/trunk/Extensions/Testing/iGynePy/Resources/Icons/iGynePy.png?revision=19437&view=co")
  set(EXTENSION_SCREENSHOTURLS "http://wiki.slicer.org/slicerWiki/images/e/e2/Slicer-r19441-iGynePy-screenshot.png")
endif()

#-----------------------------------------------------------------------------
set(MODULE_NAME iGynePy)

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  find_package(Slicer REQUIRED)
  include(${Slicer_USE_FILE})
endif()

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  iGynePy.py
  )

set(MODULE_PYTHON_RESOURCES
  )


ADD_SUBDIRECTORY(iGyneWizard)
ADD_SUBDIRECTORY(iGynePyTemplate)



#-----------------------------------------------------------------------------
ctkMacroCompilePythonScript(
  TARGET_NAME iGynePy
  SCRIPTS "${MODULE_PYTHON_SCRIPTS}"
  RESOURCES "${MODULE_PYTHON_RESOURCES}"
  DESTINATION_DIR ${CMAKE_BINARY_DIR}/${Slicer_QTSCRIPTEDMODULES_LIB_DIR}
  INSTALL_DIR ${Slicer_INSTALL_QTSCRIPTEDMODULES_LIB_DIR}
  NO_INSTALL_SUBDIR
  )

# #-----------------------------------------------------------------------------
# if(BUILD_TESTING)
#   add_subdirectory(Testing)
# endif()

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  include(${Slicer_EXTENSION_CPACK})
endif()


################################################################################
################################################################################
################################################################################

# if(BUILD_TESTING)
#   set(Launcher_Command ${Slicer_LAUNCH_COMMAND})
# endif()

# ADD_SUBDIRECTORY(iGyneWizard)
# ADD_SUBDIRECTORY(iGynePyTemplate)

# SET(iG_PYTHON_SCRIPTS
#     iGynePy.py
#   )
  
# SET(iG_PYTHON_RESOURCES
#   )
  
# ctkMacroCompilePythonScript(
#   TARGET_NAME iGynePy
#   SCRIPTS "${iG_PYTHON_SCRIPTS}"
#   RESOURCES "${iG_PYTHON_RESOURCES}"
#   DESTINATION_DIR ${CMAKE_BINARY_DIR}/${Slicer_QTSCRIPTEDMODULES_LIB_DIR}
#   INSTALL_DIR ${Slicer_INSTALL_QTSCRIPTEDMODULES_LIB_DIR}
#   NO_INSTALL_SUBDIR
#   )