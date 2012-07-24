from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
import PythonQt

class iGyneSelectApplicatorStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '2. Choose Applicator' )
    self.setDescription( 'Choose the applicator you are using. It will load the right template.' )

    self.__parent = super( iGyneSelectApplicatorStep, self )


    qt.QTimer.singleShot(0, self.killButton)

  def killButton(self):
    # hide useless button
    bl = slicer.util.findChildren(text='LoadDiagnosticSeries')
    if len(bl):
      bl[0].hide()

  def createUserInterface( self ):
    '''
    '''
    self.__layout = self.__parent.createUserInterface()

    

    # the ROI parameters
    voiGroupBox = qt.QGroupBox()
    voiGroupBox.setTitle( 'Define Applicator' )
    self.__layout.addRow( voiGroupBox )

    voiGroupBoxLayout = qt.QFormLayout( voiGroupBox )

    voiGroupBoxLayout.addRow( self.__roiWidget )


    # self.updateWidgetFromParameters(self.parameterNode())
    qt.QTimer.singleShot(0, self.killButton)

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )
    roi = self.__roiSelector.currentNode()
    if roi == None:
      self.__parent.validationFailed(desiredBranchId, 'Error', 'Please choose an applicator!')
      
    self.__parent.validationSucceeded(desiredBranchId)

  def onEntry(self,comingFrom,transitionType):
    super(iGyneDefineROIStep, self).onEntry(comingFrom, transitionType)

    # setup the interface
    lm = slicer.app.layoutManager()
    lm.setLayout(3)
    pNode = self.parameterNode()
    Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),pNode.GetParameter('followupVolumeID'))

    # use this transform node to align ROI with the axes of the baseline
    # volume
    roiTfmNodeID = pNode.GetParameter('roiTransformID')
    if roiTfmNodeID != '':
      self.__roiTransformNode = Helper.getNodeByID(roiTfmNodeID)
    else:
      Helper.Error('Internal error! Error code CT-S2-NRT, please report!')
    
    baselineVolume = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('baselineVolumeID'))
    self.__baselineVolume = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('baselineVolumeID'))

    # get the roiNode from parameters node, if it exists, and initialize the
    # GUI
    self.updateWidgetFromParameterNode(pNode)

    if self.__roi != None:
      self.__roi.VisibleOn()

    pNode.SetParameter('currentStep', self.stepid)
    
    qt.QTimer.singleShot(0, self.killButton)

# setup interface
  def onExit(self, goingTo, transitionType):
    if goingTo.id() != 'SegmentROI' and goingTo.id() != 'SelectScans':
      return
    # TODO: add storeWidgetStateToParameterNode() -- move all pNode-related stuff
    # there?
    if self.__roi != None:
      self.__roi.RemoveObserver(self.__roiObserverTag)
      self.__roi.VisibleOff()
    
    pNode = self.parameterNode()
    if self.__vrDisplayNode != None:
      self.__vrDisplayNode.VisibilityOff()
      pNode.SetParameter('vrDisplayNodeID', self.__vrDisplayNode.GetID())

    pNode.SetParameter('roiNodeID', self.__roiSelector.currentNode().GetID())

    if goingTo.id() == 'SegmentROI':
      self.doStepProcessing()

    super(iGyneDefineROIStep, self).onExit(goingTo, transitionType)

  def updateWidgetFromParameterNode(self, parameterNode):
    roiNodeID = parameterNode.GetParameter('roiNodeID')

    if roiNodeID != '':
      self.__roi = slicer.mrmlScene.GetNodeByID(roiNodeID)
      self.__roiSelector.setCurrentNode(Helper.getNodeByID(self.__roi.GetID()))
    else:
      roi = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationROINode')
      slicer.mrmlScene.AddNode(roi)
      parameterNode.SetParameter('roiNodeID', roi.GetID())
      self.__roiSelector.setCurrentNode(roi)
    
    self.onROIChanged()
      

  def doStepProcessing(self):
    '''
    prepare roi image for the next step
    '''
    pNode = self.parameterNode()
    cropVolumeNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLCropVolumeParametersNode')
    cropVolumeNode.SetScene(slicer.mrmlScene)
    cropVolumeNode.SetName('iGyne_CropVolume_node')
    cropVolumeNode.SetIsotropicResampling(True)
    cropVolumeNode.SetSpacingScalingConst(0.5)
    slicer.mrmlScene.AddNode(cropVolumeNode)
    # TODO hide from MRML tree

    cropVolumeNode.SetInputVolumeNodeID(pNode.GetParameter('baselineVolumeID'))
    cropVolumeNode.SetROINodeID(pNode.GetParameter('roiNodeID'))
    # cropVolumeNode.SetAndObserveOutputVolumeNodeID(outputVolume.GetID())

    cropVolumeLogic = slicer.modules.cropvolume.logic()
    cropVolumeLogic.Apply(cropVolumeNode)

    # TODO: cropvolume error checking
    outputVolume = slicer.mrmlScene.GetNodeByID(cropVolumeNode.GetOutputVolumeNodeID())
    outputVolume.SetName("baselineROI")
    pNode.SetParameter('croppedBaselineVolumeID',cropVolumeNode.GetOutputVolumeNodeID())

    roiSegmentationID = pNode.GetParameter('croppedBaselineVolumeSegmentationID') 
    if roiSegmentationID == '':
      roiRange = outputVolume.GetImageData().GetScalarRange()

      # default threshold is half-way of the range
      thresholdParameter = str(0.5*(roiRange[0]+roiRange[1]))+','+str(roiRange[1])
      pNode.SetParameter('thresholdRange', thresholdParameter)
      pNode.SetParameter('useSegmentationThresholds', 'True')

    # even if the seg. volume exists, it needs to be updated, because ROI
    # could have changed
    vl = slicer.modules.volumes.logic()
    roiSegmentation = vl.CreateLabelVolume(slicer.mrmlScene, outputVolume, 'baselineROI_segmentation')
    pNode.SetParameter('croppedBaselineVolumeSegmentationID', roiSegmentation.GetID())
