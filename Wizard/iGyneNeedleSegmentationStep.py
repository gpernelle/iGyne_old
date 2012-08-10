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
    self.skip = 1
    self.initialize( stepid )
    self.setName( '6. Needle Segmentation' )
    self.setDescription( 'Segment the needles' )
    self.__parent = super( iGyneNeedleSegmentationStep, self )
    

  def createUserInterface( self ):
    '''
    '''
    self.skip = 0
    pNode = self.parameterNode()
    self.__layout = self.__parent.createUserInterface()
    
    groupbox = qt.QGroupBox()
    groupboxLayout  = qt.QFormLayout(groupbox)
    groupboxLayout.addRow(slicer.modules.editor.widgetRepresentation())
    self.__layout.addRow(groupbox)
    
    needleLabel = qt.QLabel( 'Needle Label:' )
    self.__needleLabelSelector = slicer.qMRMLNodeComboBox()
    self.__needleLabelSelector.toolTip = "Choose the needle-label image"
    self.__needleLabelSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__needleLabelSelector.setMRMLScene(slicer.mrmlScene)
    self.__needleLabelSelector.addEnabled = 1
    self.__layout.addRow( needleLabel, self.__needleLabelSelector )
    if Helper.getNodeByID(pNode.GetParameter("baselineVolumeID")) == None:
      volumeLabel = qt.QLabel( 'Volume:' )
      self.__volumeSelector = slicer.qMRMLNodeComboBox()
      self.__volumeSelector.toolTip = "Choose the Volume"
      self.__volumeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
      self.__volumeSelector.setMRMLScene(slicer.mrmlScene)
      self.__volumeSelector.addEnabled = 1
      self.__layout.addRow( volumeLabel, self.__volumeSelector )

	
	#Segment Needle Button 
    self.needleButton = qt.QPushButton('Segment Needles')
    self.__layout.addRow(self.needleButton)
    self.needleButton.connect('clicked()', self.needleSegmentation)
    
    self.updateWidgetFromParameters(self.parameterNode())
    
  def needleSegmentation(self):
    scene = slicer.mrmlScene
    pNode = self.parameterNode()
    if Helper.getNodeByID(pNode.GetParameter("baselineVolumeID")) == None:
      inputVolumeID = self.__volumeSelector.currentNode().GetID()
    else:
      inputVolumeID = Helper.getNodeByID(pNode.GetParameter("baselineVolumeID")).GetID()
    inputLabelID = self.__needleLabelSelector.currentNode().GetID()
    
    self.outputVolumeNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelNode')
    self.outputVolumeNode.SetName("Output Needle Model")
    outputVolumeStorageNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelStorageNode')
    #outputVolumeName = inputImageName.replace(".nrrd","-OutputNeedleModel.vtk")
    #outputVolumeStorageNode.SetFileName(outputVolumeName)
    slicer.mrmlScene.AddNode(self.outputVolumeNode)
    slicer.mrmlScene.AddNode(outputVolumeStorageNode)
    self.outputVolumeNode.AddAndObserveStorageNodeID(outputVolumeStorageNode.GetID())
    outputVolumeStorageNode.WriteData(self.outputVolumeNode)
    
    outputID = self.outputVolumeNode.GetID()
    
    # Set the parameters for the CLI module    
    parameters = {} 
    parameters['inputVolume'] = inputVolumeID
    parameters['inputLabel'] = inputLabelID
    parameters['outputVtk'] = outputID
    module = slicer.modules.mainlabelneedletrackingcli 
    self.__cliNode = None
    self.__cliNode = slicer.cli.run(module, None, parameters, wait_for_completion=True)
    
    d = slicer.mrmlScene.GetNodeByID(outputID).GetDisplayNode()
    # l = slicer.vtkMRMLColorLogic()
    # d.SetAndObserveColorNodeID(l.GetDefaultEditorColorNodeID())
    dd = slicer.mrmlScene.GetNodeByID(inputLabelID).GetDisplayNode()
    color = dd.GetColorNodeID()
    
    
    d.SetScalarVisibility(1)
    d.SetActiveScalarName('NeedleLabel')
    d.SetAndObserveColorNodeID(color)
    
  def validate( self, desiredBranchId ):
    '''
    '''
    if self.skip == 1:
      self.__parent.validationFailed(desiredBranchId, 'Error','Ready to start the needle segmentation!')
    
    else:
      self.__parent.validate( desiredBranchId )
      self.__parent.validationSucceeded(desiredBranchId)

  def onExit(self, goingTo, transitionType):
    if goingTo.id() != 'NeedlePlanning' and goingTo.id() != 'NeedleSegmentation':
      return

    pNode = self.parameterNode()
   

    super(iGyneNeedleSegmentationStep, self).onExit(goingTo, transitionType)

  def onEntry(self,comingFrom,transitionType):
    '''
    Update GUI and visualization
    '''
    super(iGyneNeedleSegmentationStep, self).onEntry(comingFrom, transitionType)
    if self.skip == 0:
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

