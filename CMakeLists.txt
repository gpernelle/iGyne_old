cmake_minimum_required(VERSION 2.8.7)

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  set(EXTENSION_NAME iGyne)
  set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/4.3/Extensions/iGyne")
  set(EXTENSION_CATEGORY "IGT")
  set(EXTENSION_CONTRIBUTORS "Guillaume Pernelle, Xiaojun Chen, Yi Gao, Carolina Vale, Jan Egger, Tobias Penzkofer, Sandy Wells, Sam Song, Antonio Damato, Tina Kapur, Akila Viswanathan")

  set(EXTENSION_DESCRIPTION "iGyne is an open source software for MR-Guided Interstitial Gynecologic Brachytherapy. It enables on-time processing of the intra-operative MRI data via a DICOM connection to the scanner followed by a multi-stage registration of CAD models of the template and the obturator to the patient images. This allows the virtual placement of interstitial needles during the intervention, as well as the detection/labeling of needles in MR images")

  set(EXTENSION_ICONURL "http://www.slicer.org/slicerWiki/images/9/90/IGynePyIcon.png")
  set(EXTENSION_SCREENSHOTURLS "http://www.slicer.org/slicerWiki/images/5/5d/IGyne-labelingResult.png")
endif()

#-----------------------------------------------------------------------------
set(MODULE_NAME iGyne)

#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  find_package(Slicer REQUIRED)
  include(${Slicer_USE_FILE})
endif()

#-----------------------------------------------------------------------------
add_subdirectory(iGyneWizard)

file(COPY ${CMAKE_SOURCE_DIR}/Resources DESTINATION ${Slicer_QTSCRIPTEDMODULES_LIB_DIR}) 

set(MODULE_PYTHON_SCRIPTS
  iGyne.py)

set(MODULE_PYTHON_RESOURCES
  )

#-----------------------------------------------------------------------------
# Build
#-----------------------------------------------------------------------------
ctkMacroCompilePythonScript(
  TARGET_NAME iGyne 
  SCRIPTS "${MODULE_PYTHON_SCRIPTS}"
  RESOURCES "${MODULE_PYTHON_RESOURCES}"
  DESTINATION_DIR ${CMAKE_BINARY_DIR}/${Slicer_QTSCRIPTEDMODULES_LIB_DIR}
  INSTALL_DIR ${Slicer_INSTALL_QTSCRIPTEDMODULES_LIB_DIR}  NO_INSTALL_SUBDIR
  NO_INSTALL_SUBDIR
  )

#-----------------------------------------------------------------------------
# Testing
#-----------------------------------------------------------------------------
#if(BUILD_TESTING)
# add_subdirectory(Testing)
#endif()

#-----------------------------------------------------------------------------
# Packaging
#-----------------------------------------------------------------------------
if(NOT Slicer_SOURCE_DIR)
  include(${Slicer_EXTENSION_CPACK})
endif()
