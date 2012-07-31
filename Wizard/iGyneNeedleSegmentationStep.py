from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
from EditorLib import *
import math

import string

'''
TODO:
  add advanced option to specify segmentation
'''

class iGyneNeedleSegmentationStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '6. Needle Segmentation' )
    self.setDescription( 'Segment the needles' )
    self.__parent = super( iGyneNeedleSegmentationStep, self )
    

  def createUserInterface( self ):
    '''
    '''

    self.__layout = self.__parent.createUserInterface()
    
    
    needleLabel = qt.QLabel( 'Needle Label:' )
    self.__needleLabelSelector = slicer.qMRMLNodeComboBox()
    self.__needleLabelSelector.toolTip = "Choose the needle-label image"
    self.__needleLabelSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__needleLabelSelector.setMRMLScene(slicer.mrmlScene)
    self.__needleLabelSelector.addEnabled = 1
    self.__layout.addRow( needleLabel, self.__needleLabelSelector )
    # followupScanLabel = qt.QLabel( 'Followup scan:' )
    # self.__followupVolumeSelector = slicer.qMRMLNodeComboBox()
    # self.__followupVolumeSelector.toolTip = "Choose the followup scan"
    # self.__followupVolumeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    # self.__followupVolumeSelector.setMRMLScene(slicer.mrmlScene)
    # self.__followupVolumeSelector.addEnabled = 0
	
	#Load Template Button 
    self.needleButton = qt.QPushButton('Segment Needles')
    self.__layout.addRow(self.needleButton)
    self.needleButton.connect('clicked()', self.needleSegmentation)
    
    self.updateWidgetFromParameters(self.parameterNode())
    
  def needleSegmentation(self):
    scene = slicer.mrmlScene
    pNode = self.parameterNode()
    inputImage = Helper.getNodeByID(pNode.GetParameter("baselineVolumeID"))
    needleLabelID = pNode.GetParameter('needleLabelID')
    needleLabelNode = None
    
    if needleLabelID != '':
      needleLabelNode = Helper.getNodeByID(needleLabelID)
    else:
      needleLabelNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLScalarVolumeNode')
      slicer.mrmlScene.AddNode(needleLabelNode)
      pNode.SetParameter('needleLabelID', needleLabelNode.GetID())
      
    needleVolumeID = pNode.GetParameter('needleVolumeID')
    needleVolumeNode = None
    
    if needleVolumeID != '':
      needleVolumeNode = Helper.getNodeByID(needleVolumeID)
    else:
      needleVolumeNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelNode')
      slicer.mrmlScene.AddNode(needleVolumeNode)
      pNode.SetParameter('needleVolumeID', needleVolumeNode.GetID())
   
    parameters = {} 
    parameters['InputImageName'] = needleVolumeNode.getID()
    parameters["InputLabelImageName"] = needleLabelNode.GetID() 
    parameters['outputVtkName'] = needleVolumeNode
    module = slicer.modules.mainlabelneedletrackingcli 
    self.__cliNode = None
    self.__cliNode = slicer.cli.run(module, self.__cliNode, parameters)
    
  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )
    self.__parent.validationSucceeded(desiredBranchId)

  def onExit(self, goingTo, transitionType):
    if goingTo.id() != 'SecondRegistration' and goingTo.id() != 'NeedleSegmentation':
      return

    pNode = self.parameterNode()
   

    super(iGyneNeedleSegmentationStep, self).onExit(goingTo, transitionType)

  def onEntry(self,comingFrom,transitionType):
    '''
    Update GUI and visualization
    '''
    super(iGyneNeedleSegmentationStep, self).onEntry(comingFrom, transitionType)
    pNode = self.parameterNode()
    self.updateWidgetFromParameters(pNode)
    Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')
    
    # setup color transfer function once
    
    
    labelsColorNode = slicer.modules.colors.logic().GetColorTableNodeID(10)
    self.__needleSegmentationNode.GetDisplayNode().SetAndObserveColorNodeID(labelsColorNode)
    Helper.SetLabelVolume(self.__roiSegmentationNode.GetID())
    self.onThresholdChanged()
    pNode.SetParameter('currentStep', self.stepid)
    


  def updateWidgetFromParameters(self, pNode):
  
    baselineVolume = Helper.getNodeByID(pNode.GetParameter('baselineVolumeID'))

