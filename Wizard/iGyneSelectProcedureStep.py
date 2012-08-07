from __main__ import qt, ctk

from iGyneStep import *
from Helper import *

class iGyneSelectProcedureStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '1. Select the Procedure' )
    self.setDescription( 'Select the procedure used in this iGyne case.' )
    self.__parent = super( iGyneSelectProcedureStep, self )

  def createUserInterface( self ):
    '''
    '''

    self.__layout = self.__parent.createUserInterface()
    
    checkButton1 = qt.QCheckBox("EBRT")
    radioButton2 = qt.QRadioButton("Brachy HDR Intracav")
    radioButton3 = qt.QRadioButton("Brachy HDR Interstitial")
    radioButton4 = qt.QRadioButton("Brachy LDR Intracav")
    radioButton5 = qt.QRadioButton("Brachy LDR Interstitial")
    self.__layout.addRow(checkButton1)
    self.__layout.addRow(radioButton2)
    self.__layout.addRow(radioButton3)
    self.__layout.addRow(radioButton4)
    self.__layout.addRow(radioButton5)

      
  def onEntry(self, comingFrom, transitionType):

    super(iGyneSelectProcedureStep, self).onEntry(comingFrom, transitionType)
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)


  def onExit(self, goingTo, transitionType):

    super(iGyneSelectProcedureStep, self).onExit(goingTo, transitionType) 

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )    
    self.__parent.validationSucceeded(desiredBranchId)
   

