cmake_minimum_required(VERSION 2.8.7)

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  set(EXTENSION_NAME iGynePy)
  set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/4.1/Extensions/iGynePy")
  set(EXTENSION_CATEGORY "IGT")
  set(EXTENSION_CONTRIBUTORS "Guillaume Pernelle, Xiaojun Chen, Yi Gao, Carolina Vale, Jan Egger, Tobias Penzkofer, Sandy Wells, Sam Song, Antonio Damato, Tina Kapur, Akila Viswanathan")
  set(EXTENSION_DESCRIPTION "iGyne is an open source software for MR-Guided Interstitial Gynecologic Brachytherapy. It enables on-time processing of the intra-operative MRI data via a DICOM connection to the scanner followed by a multi-stage registration of CAD models of the template and the obturator to the patient images. This allows the virtual placement of interstitial needles during the intervention.")
  set(EXTENSION_ICONURL "http://viewvc.slicer.org/viewvc.cgi/Slicer4/trunk/Extensions/Testing/iGynePy/Resources/Icons/iGynePy.png?revision=19437&view=co")
  set(EXTENSION_SCREENSHOTURLS "http://www.slicer.org/slicerWiki/images/9/94/IGyne_1.0_needle_visualization.png")
endif()

#-----------------------------------------------------------------------------
set(MODULE_NAME iGynePy)

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  find_package(Slicer REQUIRED)
  include(${Slicer_USE_FILE})
endif()

#-----------------------------------------------------------------------------
ADD_SUBDIRECTORY(iGyneWizard)

set(MODULE_PYTHON_SCRIPTS
  iGynePy.py)

set(MODULE_PYTHON_RESOURCES
  )

add_custom_command(TARGET MyTest POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        "${CMAKE_SOURCE_DIR}/iGynePyTemplate"
        ${Slicer_DIR}/lib/qt-scripted)

#-----------------------------------------------------------------------------
# Build
#-----------------------------------------------------------------------------
ctkMacroCompilePythonScript(
  TARGET_NAME iGynePy
  SCRIPTS "${MODULE_PYTHON_SCRIPTS}"
  RESOURCES "${MODULE_PYTHON_RESOURCES}"
  DESTINATION_DIR ${Slicer_DIR}/${Slicer_QTSCRIPTEDMODULES_LIB_DIR}
  INSTALL_DIR ${Slicer_INSTALL_QTSCRIPTEDMODULES_LIB_DIR}
  NO_INSTALL_SUBDIR
  )

#-----------------------------------------------------------------------------
# Testing
#-----------------------------------------------------------------------------
if(BUILD_TESTING)
  add_subdirectory(Testing)
endif()

#-----------------------------------------------------------------------------
# Packaging
#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  include(${Slicer_EXTENSION_CPACK})
endif()
