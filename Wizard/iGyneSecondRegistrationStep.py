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
    self.tac=0
    self.WMAX = 0
    self.L=[]
    self.divider = 1
    self.step = 1
    self.nIterations = 0
    self.timer = None
    self.pos0 = 0
    self.trianglesOutput = vtk.vtkPolyData()
    self.TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
    self.Transform=vtk.vtkTransform()
    # self.transformNode = vtk.vtkMRMLLinearTransformNode()
       
    # initialize VR stuff
    self.__roiSegmentationNode = None
    self.__roiVolume = None
    self.transform = slicer.mrmlScene.GetNodeByID("vtkMRMLLinearTransformNode4")
    

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
    
    groupbox = qt.QGroupBox()
    groupboxLayout  = qt.QFormLayout(groupbox)
    groupboxLayout.addRow(slicer.modules.editor.widgetRepresentation())
    self.__layout.addRow(groupbox)
    
    self.__secondReg = qt.QPushButton('3/ ICP Registration')
    string = 'Register Template and Model.'
    self.__registrationStatus = qt.QLabel(string)
    self.__layout.addRow(self.__registrationStatus, self.__secondReg)
    self.__secondReg.connect('toggled(bool)', self.onICPButtonToggled)
    self.__secondReg.setEnabled(0)
    self.__secondReg.checkable = True
    self.__layout.addRow(self.__secondReg)
    
    # self.fiducialButton = qt.QPushButton('Manual Registration')
    # self.fiducialButton.checkable = True
    # self.__layout.addRow(self.fiducialButton)
    # self.fiducialButton.connect('toggled(bool)', self.onRunButtonToggled)
    self.iter=0
    self.obturatorSlider = ctk.ctkSliderWidget()
    self.obturatorSlider.minimum = -10
    self.obturatorSlider.maximum = 300
    self.obturatorSlider.singleStep = 1
    self.obturatorSlider.value = 0
    self.obturatorSlider.connect('valueChanged(double)', self.pushObturator)
    self.__layout.addRow(self.obturatorSlider)
    
  def pushObturator(self):
    
    nDepth = self.obturatorSlider.value-self.pos0
    pNode=self.parameterNode()
    mrmlScene=slicer.mrmlScene  
    obturatorID = pNode.GetParameter('obturatorID')
    self.ObturatorNode = mrmlScene.GetNodeByID(obturatorID)
    if self.ObturatorNode!=None :   
      self.m_poly = vtk.vtkPolyData()  
      self.m_poly.DeepCopy(self.ObturatorNode.GetPolyData())
    
    vtkmat = vtk.vtkMatrix4x4()
    print nDepth
    vtkmat.SetElement(2,3,nDepth)

    
    self.TransformPolyDataFilter.SetInput(self.m_poly)
    self.Transform.SetMatrix(vtkmat)
    
    self.TransformPolyDataFilter.SetTransform(self.Transform)
    self.TransformPolyDataFilter.Update()

    triangles=vtk.vtkTriangleFilter()
    triangles.SetInput(self.TransformPolyDataFilter.GetOutput())
    self.ObturatorNode.SetAndObservePolyData(triangles.GetOutput())
    self.pos0 = self.obturatorSlider.value

    self.iter +=1
    print self.iter    
 
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
    self.__registrationStatus.setText('Please Wait ...')
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
      if node.GetName() == "obturator": 
        modelFromImageNode = node 
        break
    

    targetSurface = segmentationModel
    self.templateDisplayModel = segmentationModel.GetDisplayNode()
    self.obturatorDisplayModel = modelFromImageNode.GetDisplayNode()
    
    addTarget = vtk.vtkAppendPolyData()
    addTarget.AddInput(targetSurface.GetPolyData())
    addTarget.AddInput(modelFromImageNode.GetPolyData())
    addTarget.Update()
    
    obturatorID = pNode.GetParameter('obturatorID')    
    ObutratorNode = slicer.mrmlScene.GetNodeByID(obturatorID)
    if ObutratorNode!=None:   
      self.m_poly = vtk.vtkPolyData()  
      self.m_poly.DeepCopy(ObutratorNode.GetPolyData())
    TransformPolyDataFilter = vtk.vtkTransformPolyDataFilter()
    Transform = vtk.vtkTransform()
    TransformPolyDataFilter.SetInput(self.m_poly)
    Transform.SetMatrix(self.vtkMatInitial)
    TransformPolyDataFilter.SetTransform(Transform)
    TransformPolyDataFilter.Update()
    
    addSource = vtk.vtkAppendPolyData()
    addSource.AddInput( self.glyphInputData)
    addSource.AddInput(TransformPolyDataFilter.GetOutput())
    addSource.Update()
    
    
    icpTransform = vtk.vtkIterativeClosestPointTransform()
    icpTransform.SetSource(addSource.GetOutput())
    icpTransform.SetTarget(addTarget.GetOutput())
    icpTransform.SetCheckMeanDistance(0)
    icpTransform.SetMaximumMeanDistance(0.1)
    icpTransform.SetMaximumNumberOfIterations(300)
    icpTransform.SetMaximumNumberOfLandmarks(1000)
    icpTransform.SetMeanDistanceModeToRMS()
    icpTransform.GetLandmarkTransform().SetModeToRigidBody()
    icpTransform.Update()
    self.nIterations = icpTransform.GetNumberOfIterations()
    FinalMatrix = vtk.vtkMatrix4x4()

    FinalMatrix.Multiply4x4(icpTransform.GetMatrix(),self.vtkMatInitial,FinalMatrix)
    transformNode.SetAndObserveMatrixTransformToParent(FinalMatrix)

    self.processRegistrationCompletion()

  def processRegistrationCompletion(self):
    
    self.__registrationStatus.setText('Done')
    self.__secondReg.setEnabled(1)
    self.__secondReg.setChecked(0)
    self.__secondReg.text = "ICP Registration"
    Helper.SetLabelVolume('None')
    self.obturatorDisplayModel.SetVisibility(0)
    self.templateDisplayModel.SetVisibility(0)
    
    # self.removeNodes()

  # def removeNodes(self):
  
    # numNodes = slicer.mrmlScene.GetNumberOfNodesByClass( "vtkMRMLScalarVolumeNode" ) 
    
    # # for n in xrange(numNodes): 
      # # node = slicer.mrmlScene.GetNthNodeByClass( n, "vtkMRMLScalarVolumeNode" )
      # # print n      
      # # if node and node.GetAttribute('LabelMap') == "1": 
        # # slicer.mrmlScene.RemoveNode(node)
        # # print(node.GetID()," removed")
        
    # # numNodes2 = slicer.mrmlScene.GetNumberOfNodesByClass( "vtkMRMLModelNode" ) 
    # # segmentationModel = None 
    # # for n in xrange(numNodes2): 
      # # node = slicer.mrmlScene.GetNthNodeByClass( n, "vtkMRMLModelNode" ) 
      # # if node.GetName() == "baselineROI_segmentation_10_Post-Gyrus": 
        # # slicer.mrmlScene.RemoveNode(node)
      # # if node.GetName() == "obturator":
        # # slicer.mrmlScene.RemoveNode(node)      
  
  def onRunButtonToggled(self, checked):
    if checked:
      self.start()
      self.fiducialButton.text = "Stop"  
    else:
      self.stop()
      self.fiducialButton.text = "ICP Registration"
      
  def onICPButtonToggled(self,checked):
    if checked:  
      self.startICP()
      self.__secondReg.text = "Processing"
    # else:
      # self.stopICP()
      # self.__secondReg.text = "ICP Registration"
      
  def startICP(self):          
    # if self.timer:
      # self.stop()
    # self.timer = qt.QTimer()
    # self.timer.setInterval(2)
    # self.timer.connect('timeout()', self.ICPRegistration)
    # self.timer.start()
    self.ICPRegistration()
    
  # def stopICP(self):
    # if self.timer:
      # self.timer.stop()
      # self.timer = None
    
  def stop(self):
    self.removeObservers()


     
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

  def processSegmentationCompletion(self, node, event):

    print("event")
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
      self.updateWidgetFromParameters(pNode)
      self.onThresholdsCheckChanged()
      Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')

      roiVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
      self.__roiVolume = roiVolume
      self.__roiSegmentationNode = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeSegmentationID'))
      
      # setup color transfer function once
      
      baselineROIVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
      baselineROIRange = baselineROIVolume.GetImageData().GetScalarRange()
      threshRange = [self.__threshRange.minimumValue, self.__threshRange.maximumValue]
      labelsColorNode = slicer.modules.colors.logic().GetColorTableNodeID(10)
      self.__roiSegmentationNode.GetDisplayNode().SetAndObserveColorNodeID(labelsColorNode)
      Helper.SetLabelVolume(self.__roiSegmentationNode.GetID())
      self.onThresholdChanged()
      pNode.SetParameter('currentStep', self.stepid)
    
  def updateWidgetFromParameters(self, pNode):
  
    baselineROIVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
    baselineROIRange = baselineROIVolume.GetImageData().GetScalarRange()
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

  
  def removeObservers(self):
    # remove observers and reset
    for observee,tag in self.styleObserverTags:
      observee.RemoveObserver(tag)
    self.styleObserverTags = []
    self.sliceWidgetsPerStyle = {}

  def translate(self,x,y,z):
    self.m.SetElement(0,3,x)
    self.m.SetElement(1,3,y)
    self.m.SetElement(2,3,z)
    