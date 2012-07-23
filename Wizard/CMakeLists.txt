SET(iGWizard_PYTHON_SCRIPTS
  __init__.py
  Helper.py
  iGyneStep.py
  iGyneSelectProcedureStep.py
  iGyneSelectApplicatorStep.py
  iGyneSegmentROIStep.py
  iGyneRegistrationStep.py
  iGyneLoadDiagnosticSeriesStep.py
  iGyneRegisterStep.py
 )

SET(iGWizard_PYTHON_RESOURCES
  )
  
ctkMacroCompilePythonScript(
  TARGET_NAME iGyneWizard  SCRIPTS "${iGWizard_PYTHON_SCRIPTS}"
  RESOURCES "${iGWizard_PYTHON_RESOURCES}"
  DESTINATION_DIR ${Slicer_BINARY_DIR}/bin/Python/iGyneWizard
  INSTALL_DIR ${Slicer_INSTALL_BIN_DIR}/Python
  )

#-----------------------------------------------------------------------------
# Testing
#
if(BUILD_TESTING)
endif(BUILD_TESTING)
