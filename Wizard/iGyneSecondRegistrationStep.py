from __main__ import qt, ctk

from iGyneStep import *
from Helper import *

import string

'''
TODO:
  add advanced option to specify segmentation
'''

class iGyneSecondRegistrationStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '4. Register the template' )
    self.setDescription( 'Register the template based on 3 fiducial points. Choose the points counterclockwise, starting from the one in the middle' )
    self.__parent = super( iGyneSecondRegistrationStep, self )
    self.interactorObserverTags = []    
    self.styleObserverTags = []
    self.volume = None
    

  def createUserInterface( self ):
    '''
    '''
    self.__layout = self.__parent.createUserInterface()
     
    self.loadTemplateButton = qt.QPushButton('Crop Volume')
    self.loadTemplateButton.checkable = True
    self.__layout.addRow(self.loadTemplateButton)
    self.loadTemplateButton.connect('toggled(bool)', self.onRunButtonToggled)
	
    self.firstRegButton = qt.QPushButton('Second Registration')
    self.firstRegButton.checkable = True
    self.__layout.addRow(self.firstRegButton)
    self.firstRegButton.connect('clicked()', self.firstRegistration)

  def onRunButtonToggled(self, checked):
    if checked:
      self.start()
      self.loadTemplateButton.text = "Stop"  
    else:
      self.stop()
      self.loadTemplateButton.text = "Choose Fiducial Points"


  def onEntry(self,comingFrom,transitionType):
  
    super(iGyneSecondRegistrationStep, self).onEntry(comingFrom, transitionType)
    # setup the interface
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)    
    # self.updateWidgetFromParameterNode(pNode)
    # qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    if goingTo.id() != 'FirstRegistration' and goingTo.id() != 'SecondRegistration':
      return
    pNode = self.parameterNode()
    # if goingTo.id() == 'LoadDiagnosticSeries':
      # self.doStepProcessing()

    super(iGyneSecondRegistrationStep, self).onExit(goingTo, transitionType)

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )    
    self.__parent.validationSucceeded(desiredBranchId)


  # def updateWidgetFromParameters(self, pNode):
  
    # baselineROIVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
    # baselineROIRange = baselineROIVolume.GetImageData().GetScalarRange()
    # self.__threshRange.minimum = baselineROIRange[0]
    # self.__threshRange.maximum = baselineROIRange[1]

    # if pNode.GetParameter('useSegmentationThresholds') == 'True':
      # self.__useThresholds = True
      # self.__useThresholdsCheck.setChecked(1)

      # thresholdRange = pNode.GetParameter('thresholdRange')
      # if thresholdRange != '':
        # rangeArray = string.split(thresholdRange, ',')
        # self.__threshRange.minimumValue = float(rangeArray[0])
        # self.__threshRange.maximumValue = float(rangeArray[1])
      # else:
         # Helper.Error('Unexpected parameter values! Error code CT-S03-TNA. Please report')
    # else:
      # self.__useThresholdsCheck.setChecked(0)
      # self.__useThresholds = False

    # segmentationID = pNode.GetParameter('croppedBaselineVolumeSegmentationID')
    # if segmentationID != '':
      # self.__roiLabelSelector.setCurrentNode(Helper.getNodeByID(segmentationID))
    # else:
      # Helper.Error('Unexpected parameter values! Error CT-S03-SNA. Please report')
    # self.__roiSegmentationNode = Helper.getNodeByID(segmentationID)
