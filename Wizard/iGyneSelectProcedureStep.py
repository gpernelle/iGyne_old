from __main__ import qt, ctk
import os.path, time
from iGyneStep import *
from Helper import *

class iGyneSelectProcedureStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.skip = 1
    self.initialize( stepid )
    self.setName( '1. Select the Procedure' )
    file = slicer.app.slicerHome + "//lib\Slicer-4.1\qt-scripted-modules\iGynePy.py"
    builddate = time.gmtime(os.path.getmtime(file))
    creationdate = int(12*365.25 + 188)# 07/07/2012
    todaydate = int((builddate.tm_year - 2000)*365.25+builddate.tm_yday)
    versionnumber = todaydate - creationdate
    self.version = str(versionnumber)
    self.setDescription( 'iGyne v2.0.' + self.version + '       Last Modified: ' + time.ctime(os.path.getmtime(file)) )
    
    self.__parent = super( iGyneSelectProcedureStep, self )

  def createUserInterface( self ):
    '''
    '''

    self.__layout = self.__parent.createUserInterface()
    
    # checkButton1 = qt.QCheckBox("EBRT")
    # radioButton2 = qt.QRadioButton("Brachy HDR Intracav")
    # radioButton3 = qt.QRadioButton("Brachy HDR Interstitial")
    # radioButton4 = qt.QRadioButton("Brachy LDR Intracav")
    # radioButton5 = qt.QRadioButton("Brachy LDR Interstitial")
    # self.__layout.addRow(checkButton1)
    # self.__layout.addRow(radioButton2)
    # self.__layout.addRow(radioButton3)
    # self.__layout.addRow(radioButton4)
    # self.__layout.addRow(radioButton5)
    self.templateButton = qt.QRadioButton("Template")
    self.templateButton.setChecked(1)
    self.noTemplateButton = qt.QRadioButton("No Template")  
    self.__layout.addRow(self.templateButton)
    self.__layout.addRow(self.noTemplateButton)
    

      
  def onEntry(self, comingFrom, transitionType):

    super(iGyneSelectProcedureStep, self).onEntry(comingFrom, transitionType)
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    pNode.SetParameter('skip', '0')

  def onExit(self, goingTo, transitionType):
  
    pNode = self.parameterNode()
    if self.templateButton.isChecked():
      self.skip = 0
    else:
      self.skip = 1
    if goingTo.id() != 'SelectApplicator' and goingTo.id() != 'NeedleSegmentation':
      return
    
    if self.skip==1:
      pNode.SetParameter('skip', '1')
      self.workflow().goForward() # 2   
    else:
      pNode.SetParameter('skip', '0')
      super(iGyneSelectProcedureStep, self).onExit(goingTo, transitionType)
    

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )    
    self.__parent.validationSucceeded(desiredBranchId)
   

