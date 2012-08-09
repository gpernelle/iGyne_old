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
    inputVolumeID = self.__volumeSelector.currentNode().GetID()
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
    parameters['InputImageName'] = inputVolumeID
    parameters['InputLabelImageName'] = inputLabelID
    parameters['outputVtkName'] = outputID
    module = slicer.modules.mainlabelneedletrackingcli 
    self.__cliNode = None
    self.__cliNode = slicer.cli.run(module, None, parameters, wait_for_completion=True)
    
    
    # # input Image
    # # if  Helper.getNodeByID(pNode.GetParameter("baselineVolumeID")) !=None:
      # # inputImage = Helper.getNodeByID(pNode.GetParameter("baselineVolumeID"))
      # # inputImageName = inputImage.GetStorageNode().GetFileName()
    # # else:
    # inputImage = self.__volumeSelector.currentNode()
    # inputImageName = inputImage.GetStorageNode().GetFileName()
    
    # # input Label
    # # needleLabelID = pNode.GetParameter('needleLabelID')
    # # needleLabelNode = None
    # # if needleLabelID != '':
      # # needleLabelNode = Helper.getNodeByID(needleLabelID)
    # # else:
    
    # sliceNodeCount = slicer.mrmlScene.GetNumberOfNodesByClass('vtkMRMLScalarVolumeNode')
    # for nodeIndex in xrange(sliceNodeCount):
      # # find the widget for each node in scene
      # sliceNode = slicer.mrmlScene.GetNthNodeByClass(nodeIndex, 'vtkMRMLScalarVolumeNode')
      # labelName = inputImage.GetName() + '-label'
      # if sliceNode.GetName() == labelName:
        # needleLabelNode = sliceNode
            
    # # pNode.SetParameter('needleLabelID', needleLabelNode.GetID())
    
    # needleLabelName = inputImageName.replace(".nrrd","-label.nrrd")
    # # needleLabelStorageNodeID = pNode.GetParameter('needleLabelStorageNodeID')
    # # if needleLabelStorageNodeID =='' :
    # needleLabelStorageNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLNRRDStorageNode')
    # needleLabelStorageNode.SetFileName(needleLabelName)
    # slicer.mrmlScene.AddNode(needleLabelStorageNode)
    
    # # pNode.SetParameter('needleLabelStorageNodeID', needleLabelStorageNode.GetID())
    
    # needleLabelNode.AddAndObserveStorageNodeID(needleLabelStorageNode.GetID())
    # needleLabelStorageNode.WriteData(needleLabelNode)

    # # output Volume    
    # # outputVolumeID = pNode.GetParameter('outputVolumeID')
    # # self.outputVolumeNode = None
    # # if outputVolumeID != '':
      # # self.outputVolumeNode = Helper.getNodeByID(outputVolumeID)
    # # else:
    # self.outputVolumeNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelNode')
    # self.outputVolumeNode.SetName("Output Needle Model")
    # outputVolumeStorageNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelStorageNode')
    # outputVolumeName = inputImageName.replace(".nrrd","-OutputNeedleModel.vtk")
    # outputVolumeStorageNode.SetFileName(outputVolumeName)
    # slicer.mrmlScene.AddNode(self.outputVolumeNode)
    # slicer.mrmlScene.AddNode(outputVolumeStorageNode)
    # self.outputVolumeNode.AddAndObserveStorageNodeID(outputVolumeStorageNode.GetID())
    # outputVolumeStorageNode.WriteData(self.outputVolumeNode)
    
    # slicer.mrmlScene.AddNode(self.outputVolumeNode)
    # pNode.SetParameter('outputVolumeID', self.outputVolumeNode.GetID())
      
    # # Set the parameters for the CLI module    
    # parameters = {} 
    # parameters['InputImageName'] = inputImageName
    # parameters['InputLabelImageName'] = needleLabelName
    # parameters['outputVtkName'] = outputVolumeName
    # module = slicer.modules.mainlabelneedletrackingcli 
    # self.__cliNode = None
    # self.__cliNode = slicer.cli.run(module, self.__cliNode, parameters)
    # # print inputImage
    # # print needleLabelNode
    # # print self.outputVolumeNode
    # # print parameters
    
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

