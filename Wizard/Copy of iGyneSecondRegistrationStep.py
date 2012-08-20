from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
from EditorLib import *
import math
import PythonQt

import string

'''
TODO:
  add advanced option to specify segmentation
'''

class iGyneSecondRegistrationStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.skip = 1
    self.initialize( stepid )
    self.setName( '5. Second Registration' )
    self.setDescription( 'Register the template based on the volume segmentation' )
    self.__parent = super( iGyneSecondRegistrationStep, self )
    self.interactorObserverTags = []    
    self.styleObserverTags = []
    self.volume = None
    self.__threshold = [ -1, -1 ]
    self.pointId = 0
    self.vtkMatInitial = vtk.vtkMatrix4x4()
    self.glyphPoints = vtk.vtkPoints()
    self.glyphInputData= vtk.vtkPolyData()
    self.glyphBalls = vtk.vtkSphereSource()
    self.glyphPoints3D = vtk.vtkGlyph3D()
    self.pointId = 0
    self.iteration = 0
    self.position = [0, 0, 0]
    self.paintCoordinates = []
    self.x0, self.y0, self.z0 = 0,0,0
    self.tx0, self.ty0,self.tz0 = 0,0,0   
    self.m = vtk.vtkMatrix4x4()
    self.r = vtk.vtkTransform()
    self.transformNode,self.model = None, None
    self.before = 0
    self.plan = 'plan'  
    self.actionState = "idle"
    self.interactorObserverTags = []    
    self.styleObserverTags = []
    self.sliceWidgetsPerStyle = {}
    self.__roiTransformNode = None
    self.__baselineVolume = None
    self.__roi = None
    self.__roiObserverTag = None
    self.__roiSegmentationNode = None
    self.__roiVolume = None
    self.tac=0
    self.WMAX = 0
    self.L=[]
    self.divider = 1
    self.step = 1
    # self.transformNode = vtk.vtkMRMLLinearTransformNode()
       
    # initialize VR stuff
    self.__roiSegmentationNode = None
    self.__roiVolume = None
    self.transform = slicer.mrmlScene.GetNodeByID("vtkMRMLLinearTransformNode4")
    self.__roiWidget = PythonQt.qSlicerAnnotationsModuleWidgets.qMRMLAnnotationROIWidget()
    

  def createUserInterface( self ):
    '''
    '''
    self.skip = 0
    self.__layout = self.__parent.createUserInterface()

    self.__basicFrame = ctk.ctkCollapsibleButton()
    self.__basicFrame.text = "Basic settings"
    self.__basicFrame.collapsed = 0
    basicFrameLayout = qt.QFormLayout(self.__basicFrame)
    self.__layout.addRow(self.__basicFrame)

    self.__advancedFrame = ctk.ctkCollapsibleButton()
    self.__advancedFrame.text = "Advanced settings"
    self.__advancedFrame.collapsed = 1
    advFrameLayout = qt.QFormLayout(self.__advancedFrame)
    self.__layout.addRow(self.__advancedFrame)

    threshLabel = qt.QLabel('1/ Make the holes visible:')
    self.__threshRange = slicer.qMRMLRangeWidget()
    self.__threshRange.decimals = 0
    self.__threshRange.singleStep = 1

    self.__useThresholdsCheck = qt.QCheckBox()
    self.__useThresholdsCheck.setEnabled(0)
    threshCheckLabel = qt.QLabel('Use thresholds for segmentation')

    roiLabel = qt.QLabel( 'Select segmentation:' )
    self.__roiLabelSelector = slicer.qMRMLNodeComboBox()
    self.__roiLabelSelector.nodeTypes = ( 'vtkMRMLScalarVolumeNode', '' )
    self.__roiLabelSelector.addAttribute('vtkMRMLScalarVolumeNode','LabelMap','1')
    self.__roiLabelSelector.toolTip = "Choose the ROI segmentation"
    self.__roiLabelSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__roiLabelSelector.addEnabled = 0
    self.__roiLabelSelector.setMRMLScene(slicer.mrmlScene)

    self.__applyButton = qt.QPushButton('2/ Make a 3D Model')
    self.__applyButton.connect('clicked()', self.applyModelMaker)
    
    basicFrameLayout.addRow(threshLabel, self.__threshRange)
    basicFrameLayout.addRow(self.__applyButton)
    advFrameLayout.addRow(threshCheckLabel, self.__useThresholdsCheck)
    advFrameLayout.addRow( roiLabel, self.__roiLabelSelector )

    self.__threshRange.connect('valuesChanged(double,double)', self.onThresholdChanged)
    self.__useThresholdsCheck.connect('stateChanged(int)', self.onThresholdsCheckChanged)
    
    self.__secondReg = qt.QPushButton('3/ ICP Registration')
    self.__registrationStatus = qt.QLabel('Register Template and Model')
    self.__layout.addRow(self.__registrationStatus, self.__secondReg)
    self.__secondReg.connect('clicked()', self.ICPRegistration)
    self.__secondReg.setEnabled(0)
    self.__layout.addRow(self.__secondReg)
    
    self.fiducialButton = qt.QPushButton('Manual Registration')
    self.fiducialButton.checkable = True
    self.__layout.addRow(self.fiducialButton)
    self.fiducialButton.connect('toggled(bool)', self.onRunButtonToggled)

  def setPointData(self,fHoleOriginX,fHoleOriginY):
    fTipPoint,fTipPointTrans=[0,0,0,0],[0,0,0,0]
    for k in xrange(10):
      for i in xrange(36):
        
        fTipPoint[0]=fHoleOriginX+1.25*math.cos(math.pi/180.0*i*10)
        fTipPoint[1]=fHoleOriginY+1.25*math.sin(math.pi/180.0*i*10)
        fTipPoint[2]=k
        fTipPoint[3]=float(1)
        self.vtkMatInitial.MultiplyPoint(fTipPoint, fTipPointTrans)

        self.glyphPoints.InsertPoint(self.pointId, fTipPointTrans[0], fTipPointTrans[1],fTipPointTrans[2])
        self.pointId += 1
        # print(self.pointId,self.vtkMatInitial )
  
  def ICPRegistration(self):
    self.__registrationStatus.setText('Wait ...')
    self.__secondReg.setEnabled(0)
    scene = slicer.mrmlScene
    pNode= self.parameterNode()
    transformNodeID = pNode.GetParameter('followupTransformID')
    transformNode = Helper.getNodeByID(transformNodeID)
    self.vtkMatInitial = transformNode.GetMatrixTransformToParent()
    # print(self.vtkMatInitial)
    
    self.setPointData(50,28.019)
    self.setPointData(40.209,24.456)
    self.setPointData(35,14)
    self.setPointData(24.647,15.363)
    self.setPointData(15,19.359)
    self.setPointData(15,88.641)
    self.setPointData(24.647,92.637)
    self.setPointData(35,94)
    self.setPointData(45.353,92.637)
    self.setPointData(55,88.641)
    self.setPointData(55,19.359)
    self.setPointData(45.353,15.363)
    self.setPointData(30.642,4.19)
    self.setPointData(22.059,5.704)
    self.setPointData(22.059,102.296)
    self.setPointData(30.642,103.81)
    self.setPointData(39.358,103.81)
    self.setPointData(47.941,102.296)
    self.setPointData(47.941,5.704)
    self.setPointData(39.358,4.19)
    # print(self.glyphPoints)
    self.glyphInputData.SetPoints(self.glyphPoints)
    self.glyphInputData.Update()

    self.glyphBalls.SetRadius(0.05)
    self.glyphBalls.SetThetaResolution(6)
    self.glyphBalls.SetPhiResolution(10)

    self.glyphPoints3D.SetInput(self.glyphInputData)
    self.glyphPoints3D.SetSource(self.glyphBalls.GetOutput())
    self.glyphPoints3D.Update()  

    inputSurface = scene.GetNodeByID("vtkMRMLModelNode4")

    
    numNodes = slicer.mrmlScene.GetNumberOfNodesByClass( "vtkMRMLModelNode" ) 
    segmentationModel = None 
    for n in xrange(numNodes): 
      node = slicer.mrmlScene.GetNthNodeByClass( n, "vtkMRMLModelNode" ) 
      if node.GetName() == "baselineROI_segmentation_10_Post-Gyrus": 
        segmentationModel = node 
        break 
    targetSurface = segmentationModel
    
    icpTransform = vtk.vtkIterativeClosestPointTransform()
    icpTransform.SetSource(self.glyphInputData)
    icpTransform.SetTarget(targetSurface.GetPolyData())
    icpTransform.SetCheckMeanDistance(0)
    icpTransform.SetMaximumMeanDistance(0.01)
    icpTransform.SetMaximumNumberOfIterations(1000)
    icpTransform.SetMaximumNumberOfLandmarks(100)
    icpTransform.SetMeanDistanceModeToRMS()
    icpTransform.GetLandmarkTransform().SetModeToRigidBody()
    icpTransform.Update()
    nIterations = icpTransform.GetNumberOfIterations()
    FinalMatrix = vtk.vtkMatrix4x4()

    FinalMatrix.Multiply4x4(icpTransform.GetMatrix(),self.vtkMatInitial,FinalMatrix)
    transformNode.SetAndObserveMatrixTransformToParent(FinalMatrix)
    self.processRegistrationCompletion()

  def processRegistrationCompletion(self):
    
    self.__registrationStatus.setText('Done')

    self.__secondReg.setEnabled(1)
    
    pNode = self.parameterNode()
    followupNode = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('followupVolumeID'))
    obturatorNode = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('obturatorID'))
    
    df = followupNode.GetDisplayNode()
    df.SetSliceIntersectionVisibility(1)
    do = obturatorNode.GetDisplayNode()
    do.SetSliceIntersectionVisibility(1)
    
    roiNode = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('roiTransformID'))
    roiNode.SetAndObserveTransformNodeID(self.__followupTransform.GetID())

    Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),pNode.GetParameter('followupVolumeID'))

    pNode.SetParameter('followupTransformID', self.__followupTransform.GetID())
    self.onROIChanged()



     
  def onThresholdsCheckChanged(self):
    if self.__useThresholdsCheck.isChecked():
      self.__roiLabelSelector.setEnabled(0)
      self.__threshRange.setEnabled(1)
    else:
      self.__roiLabelSelector.setEnabled(1)
      self.__threshRange.setEnabled(0)
    
  def applyModelMaker(self):
    pNode = self.parameterNode()
    range0 = self.__threshRange.minimumValue
    range1 = self.__threshRange.maximumValue
    self.__roiVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
    self.__roiSegmentationNode = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeSegmentationID'))

    # update the label volume accordingly
    thresh = vtk.vtkImageThreshold()
    thresh.SetInput(self.__roiVolume.GetImageData())
    thresh.ThresholdBetween(range0, range1)
    thresh.SetInValue(10)
    thresh.SetOutValue(0)
    thresh.ReplaceOutOn()
    thresh.ReplaceInOn()
    thresh.Update()

    # self.__modelNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelNode')
    self.__roiSegmentationNode.SetAndObserveImageData(thresh.GetOutput())
    Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')
    self.__secondReg.setEnabled(1)

    # set up the model maker node 
    parameters = {} 
    parameters['Name'] = self.__roiSegmentationNode.GetName() 
    parameters["InputVolume"] = self.__roiSegmentationNode.GetID() 
    parameters['FilterType'] = "Sinc" 

    # build only the currently selected model. 
    # parameters['Labels'] = self.getPaintLabel() 
    parameters["StartLabel"] = -1 
    parameters["EndLabel"] = -1 
    parameters['GenerateAll'] = True 
    parameters["JointSmoothing"] = False 
    parameters["SplitNormals"] = True 
    parameters["PointNormals"] = True 
    parameters["SkipUnNamed"] = True 
    parameters["Decimate"] = 0.25 
    parameters["Smooth"] = 10 
  
    # output 
    # - make a new hierarchy node if needed 
    # 
    numNodes = slicer.mrmlScene.GetNumberOfNodesByClass( "vtkMRMLModelHierarchyNode" ) 
    self.segmentationModel = None 
    for n in xrange(numNodes): 
      node = slicer.mrmlScene.GetNthNodeByClass( n, "vtkMRMLModelHierarchyNode" ) 
      if node.GetName() == "Segmentation Model": 
        self.segmentationModel = node 
        break 

    if not self.segmentationModel: 
      self.segmentationModel = slicer.vtkMRMLModelHierarchyNode() 
      self.segmentationModel.SetScene( slicer.mrmlScene ) 
      self.segmentationModel.SetName( "Segmentation Model" ) 
      slicer.mrmlScene.AddNode( self.segmentationModel ) 

    parameters["ModelSceneFile"] = self.segmentationModel 
    modelMaker = slicer.modules.modelmaker 
    self.__cliNode = None
    self.__cliNode = slicer.cli.run(modelMaker, self.__cliNode, parameters) 
        
  def onThresholdChanged(self): 
    pNode = self.parameterNode()
    range0 = self.__threshRange.minimumValue
    range1 = self.__threshRange.maximumValue
    self.__roiVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
    self.__roiSegmentationNode = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeSegmentationID'))

    # update the label volume accordingly
    thresh = vtk.vtkImageThreshold()
    thresh.SetInput(self.__roiVolume.GetImageData())
    thresh.ThresholdBetween(range0, range1)
    thresh.SetInValue(10)
    thresh.SetOutValue(0)
    thresh.ReplaceOutOn()
    thresh.ReplaceInOn()
    thresh.Update()
    
    self.__roiSegmentationNode.SetAndObserveImageData(thresh.GetOutput())
    Helper.SetBgFgVolumes(pNode.GetParameter('BaselineVolumeID'),'')

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )
    self.__parent.validationSucceeded(desiredBranchId)

  def onExit(self, goingTo, transitionType):
    if self.skip == 0:
      if goingTo.id() != 'FirstRegistration' and goingTo.id() != 'NeedlePlanning':
        return

      pNode = self.parameterNode()
      pNode.SetParameter('thresholdRange', str(self.__threshRange.minimumValue)+','+str(self.__threshRange.maximumValue))
      if self.segmentationModel:
        self.segmentationModel.RemoveAllChildrenNodes()
        slicer.mrmlScene.RemoveNode(self.segmentationModel)
        
      if self.__roi != None:
        self.__roi.RemoveObserver(self.__roiObserverTag)
        self.__roi.VisibleOff()
      
      pNode = self.parameterNode()
      pNode.SetParameter('roiNodeID', self.__roiSelector.currentNode().GetID())
      
    super(iGyneSecondRegistrationStep, self).onExit(goingTo, transitionType)

  def onEntry(self,comingFrom,transitionType):
    '''
    Update GUI and visualization
    '''
    super(iGyneSecondRegistrationStep, self).onEntry(comingFrom, transitionType)
    if self.skip == 0:
    # setup the interface
      lm = slicer.app.layoutManager()
      lm.setLayout(3)
      pNode = self.parameterNode()

      
      self.__roiTransformNode = slicer.mrmlScene.GetNodeByID( pNode.GetParameter('roiTransformID'))
      self.__followupVolume = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('followupVolumeID'))
      self.__baselineVolume = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('baselineVolumeID'))
      self.__followupTransform = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('followupTransformID'))
      
      print pNode
      self.updateWidgetFromParameters(pNode)
      self.onThresholdsCheckChanged()
      #Helper.SetBgFgVolumes(self.__baselineVolume,'')

      self.__roiVolume = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
      self.__roiSegmentationNode = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('croppedBaselineVolumeSegmentationID'))
      
      # setup color transfer function once
      

      baselineROIRange = self.__roiVolume.GetImageData().GetScalarRange()
      threshRange = [self.__threshRange.minimumValue, self.__threshRange.maximumValue]
      labelsColorNode = slicer.modules.colors.logic().GetColorTableNodeID(10)
      self.__roiSegmentationNode.GetDisplayNode().SetAndObserveColorNodeID(labelsColorNode)
      Helper.SetLabelVolume(self.__roiSegmentationNode.GetID())
      self.onThresholdChanged()
      
      # use this transform node to align ROI with the axes of the baseline
      # volume
      
      # get the roiNode from parameters node, if it exists, and initialize the
      # GUI
      self.updateWidgetFromParameters(pNode)
      bounds = [0,0,0,0,0,0]
      self.__followupVolume.GetRASBounds(bounds)
      #print(bounds)
      if self.__roi != None:
        self.__roi.VisibleOn()
      self.__roi.SetRadiusXYZ(abs(bounds[0]-bounds[1])/float(2),abs(bounds[2]-bounds[3])/float(2),abs(bounds[4]-bounds[5])/float(2))
      pNode.SetParameter('currentStep', self.stepid)
    
  def updateWidgetFromParameters(self, pNode):
  
    self.__roiVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
    baselineROIRange = self.__roiVolume.GetImageData().GetScalarRange()
    self.__threshRange.minimum = baselineROIRange[0]
    self.__threshRange.maximum = baselineROIRange[1]

    if pNode.GetParameter('useSegmentationThresholds') == 'True':
      self.__useThresholds = True
      self.__useThresholdsCheck.setChecked(1)

      thresholdRange = pNode.GetParameter('thresholdRange')
      if thresholdRange != '':
        rangeArray = string.split(thresholdRange, ',')
        self.__threshRange.minimumValue = float(rangeArray[0])
        self.__threshRange.maximumValue = float(rangeArray[1])
      else:
         Helper.Error('Unexpected parameter values! Error code CT-S03-TNA. Please report')
    else:
      self.__useThresholdsCheck.setChecked(0)
      self.__useThresholds = False

    segmentationID = pNode.GetParameter('croppedBaselineVolumeSegmentationID')
    if segmentationID != '':
      self.__roiLabelSelector.setCurrentNode(Helper.getNodeByID(segmentationID))
    else:
      Helper.Error('Unexpected parameter values! Error CT-S03-SNA. Please report')
    self.__roiSegmentationNode = Helper.getNodeByID(segmentationID)
    
    roiNodeID = pNode.GetParameter('roiNodeID')
    if roiNodeID != '':
      self.__roi = slicer.mrmlScene.GetNodeByID(roiNodeID) 
    else:
      Helper.Error('RoiNodeID is missing')
    self.onROIChanged()
    self.doStepProcessing()

  def onROIChanged(self):
    pNode = self.parameterNode()
    roiID = pNode.GetParameter('roiNodeID')
    roi = slicer.mrmlScene.GetNodeByID(roiID)

    if roi != None:
    
      pNode = self.parameterNode()
      roi.SetAndObserveTransformNodeID(self.__roiTransformNode.GetID())

      if self.__roiObserverTag != None:
        self.__roi.RemoveObserver(self.__roiObserverTag)

      self.__roi = slicer.mrmlScene.GetNodeByID(roi.GetID())
      self.__roiObserverTag = self.__roi.AddObserver('ModifiedEvent', self.processROIEvents)

      roi.SetInteractiveMode(0)

      self.__roiWidget.setMRMLAnnotationROINode(roi)
      self.__roi.VisibleOff()
     
  def processROIEvents(self,node,event):
    # get the range of intensities inside the ROI

    # get the IJK bounding box of the voxels inside ROI
    roiCenter = [0,0,0]
    roiRadius = [0,0,0]
    self.__roi.GetXYZ(roiCenter)
    self.__roi.GetRadiusXYZ(roiRadius)

    roiCorner1 = [roiCenter[0]+roiRadius[0],roiCenter[1]+roiRadius[1],roiCenter[2]+roiRadius[2],1]
    roiCorner2 = [roiCenter[0]+roiRadius[0],roiCenter[1]+roiRadius[1],roiCenter[2]-roiRadius[2],1]
    roiCorner3 = [roiCenter[0]+roiRadius[0],roiCenter[1]-roiRadius[1],roiCenter[2]+roiRadius[2],1]
    roiCorner4 = [roiCenter[0]+roiRadius[0],roiCenter[1]-roiRadius[1],roiCenter[2]-roiRadius[2],1]
    roiCorner5 = [roiCenter[0]-roiRadius[0],roiCenter[1]+roiRadius[1],roiCenter[2]+roiRadius[2],1]
    roiCorner6 = [roiCenter[0]-roiRadius[0],roiCenter[1]+roiRadius[1],roiCenter[2]-roiRadius[2],1]
    roiCorner7 = [roiCenter[0]-roiRadius[0],roiCenter[1]-roiRadius[1],roiCenter[2]+roiRadius[2],1]
    roiCorner8 = [roiCenter[0]-roiRadius[0],roiCenter[1]-roiRadius[1],roiCenter[2]-roiRadius[2],1]

    ras2ijk = vtk.vtkMatrix4x4()
    self.__baselineVolume.GetRASToIJKMatrix(ras2ijk)

    roiCorner1ijk = ras2ijk.MultiplyPoint(roiCorner1)
    roiCorner2ijk = ras2ijk.MultiplyPoint(roiCorner2)
    roiCorner3ijk = ras2ijk.MultiplyPoint(roiCorner3)
    roiCorner4ijk = ras2ijk.MultiplyPoint(roiCorner4)
    roiCorner5ijk = ras2ijk.MultiplyPoint(roiCorner5)
    roiCorner6ijk = ras2ijk.MultiplyPoint(roiCorner6)
    roiCorner7ijk = ras2ijk.MultiplyPoint(roiCorner7)
    roiCorner8ijk = ras2ijk.MultiplyPoint(roiCorner8)

    lowerIJK = [0, 0, 0]
    upperIJK = [0, 0, 0]

    lowerIJK[0] = min(roiCorner1ijk[0],roiCorner2ijk[0],roiCorner3ijk[0],roiCorner4ijk[0],roiCorner5ijk[0],roiCorner6ijk[0],roiCorner7ijk[0],roiCorner8ijk[0])
    lowerIJK[1] = min(roiCorner1ijk[1],roiCorner2ijk[1],roiCorner3ijk[1],roiCorner4ijk[1],roiCorner5ijk[1],roiCorner6ijk[1],roiCorner7ijk[1],roiCorner8ijk[1])
    lowerIJK[2] = min(roiCorner1ijk[2],roiCorner2ijk[2],roiCorner3ijk[2],roiCorner4ijk[2],roiCorner5ijk[2],roiCorner6ijk[2],roiCorner7ijk[2],roiCorner8ijk[2])

    upperIJK[0] = max(roiCorner1ijk[0],roiCorner2ijk[0],roiCorner3ijk[0],roiCorner4ijk[0],roiCorner5ijk[0],roiCorner6ijk[0],roiCorner7ijk[0],roiCorner8ijk[0])
    upperIJK[1] = max(roiCorner1ijk[1],roiCorner2ijk[1],roiCorner3ijk[1],roiCorner4ijk[1],roiCorner5ijk[1],roiCorner6ijk[1],roiCorner7ijk[1],roiCorner8ijk[1])
    upperIJK[2] = max(roiCorner1ijk[2],roiCorner2ijk[2],roiCorner3ijk[2],roiCorner4ijk[2],roiCorner5ijk[2],roiCorner6ijk[2],roiCorner7ijk[2],roiCorner8ijk[2])

    image = self.__baselineVolume.GetImageData()
    clipper = vtk.vtkImageClip()
    clipper.ClipDataOn()
    clipper.SetOutputWholeExtent(int(lowerIJK[0]),int(upperIJK[0]),int(lowerIJK[1]),int(upperIJK[1]),int(lowerIJK[2]),int(upperIJK[2]))
    clipper.SetInput(image)
    clipper.Update()

    roiImageRegion = clipper.GetOutput()
    intRange = roiImageRegion.GetScalarRange()
    lThresh = 0.4*(intRange[0]+intRange[1])
    uThresh = intRange[1]
  def start(self):    
    self.removeObservers()
    # get new slice nodes
    layoutManager = slicer.app.layoutManager()
    sliceNodeCount = slicer.mrmlScene.GetNumberOfNodesByClass('vtkMRMLSliceNode')
    for nodeIndex in xrange(sliceNodeCount):
      # find the widget for each node in scene
      sliceNode = slicer.mrmlScene.GetNthNodeByClass(nodeIndex, 'vtkMRMLSliceNode')
      sliceWidget = layoutManager.sliceWidget(sliceNode.GetLayoutName())      
      if sliceWidget:     
        # add obserservers and keep track of tags
        style = sliceWidget.sliceView().interactorStyle()
        self.sliceWidgetsPerStyle[style] = sliceWidget
        events = ("LeftButtonPressEvent","LeftButtonReleaseEvent","MouseMoveEvent", "KeyPressEvent","KeyReleaseEvent","EnterEvent", "LeaveEvent")
        for event in events:
          tag = style.AddObserver(event, self.processEvent)   
          self.styleObserverTags.append([style,tag])
		  
  def stop(self):
    self.removeObservers() 
	
  def removeObservers(self):
    # remove observers and reset
    for observee,tag in self.styleObserverTags:
      observee.RemoveObserver(tag)
    self.styleObserverTags = []
    self.sliceWidgetsPerStyle = {}
	
  def processEvent(self,observee,event=None):

    ######################################  transformation  ##########################
    scene = slicer.mrmlScene
    pNode= self.parameterNode()
    transformNodeID = pNode.GetParameter('followupTransformID')
    self.transform = Helper.getNodeByID(transformNodeID)
    if self.sliceWidgetsPerStyle.has_key(observee):
      sliceWidget = self.sliceWidgetsPerStyle[observee]
      style = sliceWidget.sliceView().interactorStyle()

      if event == "KeyPressEvent":
        # self.before == 0:
        key = style.GetInteractor().GetKeySym()
        if key == 'a' and self.actionState != "translation":
          self.actionState = "translation"          
        elif key == 's' and self.actionState != "rotation":
          self.actionState = "rotation"
        elif key == 's' and self.actionState == "rotation":
          self.actionState = "idle"
          self.before = 0
        elif key == 'a' and self.actionState == "translation":
          self.actionState = "idle"
          self.before = 0

      print(self.actionState)

      global fi, theta, psi
      
      if (self.actionState == "rotation" or self.actionState == "translation"):

        ############################  rotation ########################################
        if self.actionState == "rotation" and event == "MouseMoveEvent":
          # xy = style.GetInteractor().GetEventPosition()
          # xyz = sliceWidget.convertDeviceToXYZ(xy)
          # ras = sliceWidget.convertXYZToRAS(xyz)
          # tx = 0
          # ty = 0
          # tz = 0
          # fi=0
          # theta = 0
          # psi = 0
          # x = ras[0]
          # y = ras[1]
          # z = ras[2]
          # if self.before == 0:
            # self.x0 = ras[0]
            # self.y0 = ras[1]
            # self.z0 = ras[2]
            # self.tx0 = self.m.GetElement(0,3)
            # self.ty0 = self.m.GetElement(1,3)
            # self.tz0 = self.m.GetElement(2,3)      
            # if y == 0:
              # self.plan = 'yplan'      
            # elif z == 0:
              # self.plan = 'zplan'
            # elif x == 0:
              # self.plan = 'xplan'
          # tx = x - self.x0
          # ty = y - self.y0
          # tz = z - self.z0

          # self.m =  self.transform.GetMatrixTransformToParent()

          # new_rot_point = [0,0,0]
          # new_rot_point = [self.tx0,self.ty0,self.tz0]
          # translate_back = [k * -1 for k in new_rot_point]    

          # #self.r.Translate(new_rot_point)
          # if self.plan == 'yplan':
            # self.r.RotateWXYZ(tx/float(30),0,1,0)         
          # elif self.plan == 'zplan':
            # self.r.RotateWXYZ(tx/float(30),0,0,1)  
          # elif self.plan == 'xplan':
            # self.r.RotateWXYZ(ty/float(30),1,0,0)
          # #self.r.Translate(translate_back)  
          # self.transform.ApplyTransformMatrix(self.r.GetMatrix())       
          # self.x0 = x
          # self.y0 = y
          # self.z0 = z
          
    
          # self.before += 1
          print("rotation is not supported yet - please use the transform Module")
        ######################################### translation ###########################################
        elif self.actionState == "translation" and event == "MouseMoveEvent":
          xy = style.GetInteractor().GetEventPosition()
          xyz = sliceWidget.convertDeviceToXYZ(xy);
          ras = sliceWidget.convertXYZToRAS(xyz)
          x = ras[0]
          y = ras[1]
          z = ras[2]
          self.m = self.transform.GetMatrixTransformToParent()
          if self.before == 0:
            self.x0 = ras[0]
            self.y0 = ras[1]
            self.z0 = ras[2]
            self.tx0 = self.m.GetElement(0,3)
            self.ty0 = self.m.GetElement(1,3)
            self.tz0 = self.m.GetElement(2,3)  
          tx = x - self.x0 
          ty = y - self.y0 
          tz = z - self.z0
          self.translate(self.tx0+tx,self.ty0+ty,self.tz0+tz)          
          self.before += 1

  
  def onRunButtonToggled(self, checked):
    if checked:
      self.start()
      self.fiducialButton.text = "Stop"  
    else:
      self.stop()
      self.fiducialButton.text = "ICP Registration"

  def translate(self,x,y,z):
    self.m.SetElement(0,3,x)
    self.m.SetElement(1,3,y)
    self.m.SetElement(2,3,z)
    
  def doStepProcessing(self):
    '''
    prepare roi image for the next step
    '''
    pNode = self.parameterNode()
    cropVolumeNode = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('cropVolumeNodeID'))
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
      thresholdParameter = str(0.25*(roiRange[0]+roiRange[1]))+','+str(roiRange[1])
      pNode.SetParameter('thresholdRange', thresholdParameter)
      pNode.SetParameter('useSegmentationThresholds', 'True')

    