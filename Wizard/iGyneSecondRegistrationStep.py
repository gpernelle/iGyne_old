from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
from EditorLib import *
import math
import Queue, threading

import string

'''
TODO:
  add advanced option to specify segmentation
'''

class iGyneSecondRegistrationStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '5. Second Registration' )
    self.setDescription( 'Register the template based on the volume segmentation' )
    self.__parent = super( iGyneSecondRegistrationStep, self )
    self.interactorObserverTags = []    
    self.styleObserverTags = []
    self.volume = None
    self.__threshold = [ -1, -1 ]
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
    self.__roiSegmentationNode = None
    self.regIter = 0
    self.initialTransformMatrix = None
    self.status = None
    self.fullAutoRegOn = 0
    self.ICP = 0
    self.previousmodelID = None
    self.lastModelNode = None
    self.stringRMS = ""
    self.processingTime = "not calculated"
    

  def createUserInterface( self ):
    '''
    The user interface is composed from:
    - fully auto seg/reg button + restore initial regI
    - frame with semi manual operations
    - frame with the embedded editor modules
    - frame with parameters for segmentation/registration
    '''
    self.__layout = self.__parent.createUserInterface()
    
    ###Basic Settings Frame
    basicFrame = ctk.ctkCollapsibleButton()
    basicFrame.text = "Basic settings"
    basicFrame.collapsed = 0
    basicFrameLayout = qt.QFormLayout(basicFrame)
    
    ###Advanced Settings Frame
    advancedFrame = ctk.ctkCollapsibleButton()
    advancedFrame.text = "Advanced settings"
    advancedFrame.collapsed = 1
    advFrameLayout = qt.QFormLayout(advancedFrame)
    
    ###Evaluation Settings Frame
    evaluationFrame = ctk.ctkCollapsibleButton()
    evaluationFrame.text = "Evaluation settings"
    evaluationFrame.collapsed = 1
    evalFrameLayout = qt.QFormLayout(evaluationFrame)
    
    ### Editor Frame
    editorFrame = ctk.ctkCollapsibleButton()
    editorFrame.text = "Editor Tools (GrowCut Segmentation)"
    editorFrame.collapsed = 1
    editorFrameLayout = qt.QFormLayout(editorFrame)
    
    ###Threshold slider for template segmentation
    threshLabel = qt.QLabel('Make the holes visible:')
    self.__threshRange = slicer.qMRMLRangeWidget()
    self.__threshRange.decimals = 0
    self.__threshRange.singleStep = 1

    ###disabled...
    self.__useThresholdsCheck = qt.QCheckBox()
    self.__useThresholdsCheck.setEnabled(0)
    threshCheckLabel = qt.QLabel('Use thresholds for segmentation')
    self.__threshRange.connect('valuesChanged(double,double)', self.onThresholdChanged)
    self.__useThresholdsCheck.connect('stateChanged(int)', self.onThresholdsCheckChanged)

    ###Select segmentation button (disabled)
    roiLabel = qt.QLabel( 'Select segmentation:' )
    self.__roiLabelSelector = slicer.qMRMLNodeComboBox()
    self.__roiLabelSelector.nodeTypes = ( 'vtkMRMLScalarVolumeNode', '' )
    self.__roiLabelSelector.addAttribute('vtkMRMLScalarVolumeNode','LabelMap','1')
    self.__roiLabelSelector.toolTip = "Choose the ROI segmentation"
    self.__roiLabelSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__roiLabelSelector.addEnabled = 0
    self.__roiLabelSelector.setMRMLScene(slicer.mrmlScene)
    
    ###Make a 3D Model Button 
    make3DModelButton = qt.QPushButton('Make a 3D Model')
    make3DModelButton.connect('clicked()', self.applyModelMaker)
     
    ###Auto Segmentation of Obturator Button     
    autoSegmentationButton = qt.QPushButton('Automatic Obturator Segmentation')
    autoSegmentationButton.connect('clicked()', self.obturatorSegmentation)
    
    ### Line separator
    line = qt.QFrame()
    line.setFrameShape(qt.QFrame.HLine)
    line.setFrameShape(qt.QFrame.Sunken)
    
    ###Editor Widget
    groupbox = qt.QGroupBox()
    groupboxLayout  = qt.QFormLayout(groupbox)
    groupboxLayout.addRow(slicer.modules.editor.widgetRepresentation())
    editorFrameLayout.addRow(groupbox)
    
    ###Start ICP reg button
    self.ICPRegistrationButton = qt.QPushButton('ICP Registration')
    string = 'Register Template and Model'
    self.__registrationStatus = qt.QLabel(string)
    self.ICPRegistrationButton.connect('toggled(bool)', self.onICPButtonToggled)
    self.ICPRegistrationButton.setEnabled(0)
    self.ICPRegistrationButton.checkable = True 
    
    ###Start ICP reg button with no template
    self.ICPRegistrationButton2 = qt.QPushButton('ICP Registration w/o obturator')
    string = 'Register Template and Model'
    self.__registrationStatus = qt.QLabel(string)
    self.ICPRegistrationButton2.connect('toggled(bool)', self.onICPButtonToggled2)
    self.ICPRegistrationButton2.setEnabled(0)
    self.ICPRegistrationButton2.checkable = True 
    
    ###I Feel Lucky Button
    IFeelLuckyButton = qt.QPushButton('I am Feeling Lucky')
    IFeelLuckyButton.connect('clicked()',self.IFeelLucky)
    
    ###Restore Initial Registration Button
    backToInitialRegistrationButton = qt.QPushButton('Restore Initial Registration')
    backToInitialRegistrationButton.connect('clicked()',self.backToInitialRegistration)
    

    ###Obturator SpinBox
    self.pullObturatorValueButton = qt.QSpinBox()
    self.pullObturatorValueButton.setMinimum(-500)
    self.pullObturatorValueButton.setMaximum(500)
    fLabel = qt.QLabel("Pull Obturator: ")
    self.pullObturatorValueButton.connect('valueChanged(int)', self.pullObturator)
    
    
    
    ###ICP registration settings groupbox
    ICPGroupBox = qt.QGroupBox()
    ICPGroupBox.setTitle( 'ICP Registration Settings' )
    advFrameLayout.addRow( ICPGroupBox )
    ICPGroupBoxLayout = qt.QFormLayout( ICPGroupBox )
    
    ###Segment Template groupbox
    segTemplateGroupBox = qt.QGroupBox()
    segTemplateGroupBox.setTitle( '1. Segmentation of the template' )
    basicFrameLayout.addRow( segTemplateGroupBox )
    segTemplateGroupBoxLayout = qt.QFormLayout( segTemplateGroupBox )
    
    ###Segment Obturator groupbox
    segObturatorGroupBox = qt.QGroupBox()
    segObturatorGroupBox.setTitle( '2. Segmentation of the Obturator' )
    basicFrameLayout.addRow( segObturatorGroupBox )
    segObturatorGroupBoxLayout = qt.QFormLayout( segObturatorGroupBox )
    
    ###Registration groupbox
    registrationGroupBox = qt.QGroupBox()
    registrationGroupBox.setTitle( '3. Registration: Choose one of the following registration methods' )
    basicFrameLayout.addRow( registrationGroupBox )
    registrationGroupBoxLayout = qt.QFormLayout( registrationGroupBox )
    
    ###Evaluation groupbox
    evaluationGroupBox = qt.QGroupBox()
    evaluationGroupBox.setTitle( '4. Evaluation' )
    basicFrameLayout.addRow( evaluationGroupBox )
    evaluationGroupBoxLayout = qt.QFormLayout( evaluationGroupBox )
    
    
    ###Evaluation settings 4,5,7
    pNode = self.parameterNode()
    transformNodeID = pNode.GetParameter('followupTransformID')
    print("transfo id:" , transformNodeID)
    self.templateIDButton = qt.QSpinBox()
    self.templateIDButton.setMinimum(0)
    self.templateIDButton.setMaximum(1000)
    self.templateIDButton.setValue(4)
    templateIDButtonLabel = qt.QLabel('Template ID')
    evalFrameLayout.addRow( templateIDButtonLabel, self.templateIDButton)
    self.obturatorIDButton = qt.QSpinBox()
    self.obturatorIDButton.setMinimum(0)
    self.obturatorIDButton.setMaximum(1000)
    self.obturatorIDButton.setValue(5)
    obturatorIDButtonLabel = qt.QLabel('Obturator ID')
    evalFrameLayout.addRow( obturatorIDButtonLabel, self.obturatorIDButton)
    self.t1IDButton = qt.QSpinBox()
    self.t1IDButton.setMinimum(0)
    self.t1IDButton.setMaximum(1000)
    self.t1IDButton.setValue(6)
    t1IDButton = qt.QLabel('Transformation ID')
    evalFrameLayout.addRow( t1IDButton, self.t1IDButton)
    self.t2IDButton = qt.QSpinBox()
    self.t2IDButton.setMinimum(0)
    self.t2IDButton.setMaximum(1000)
    self.t2IDButton.setValue(7)
    t2IDButtonLabel = qt.QLabel('Optimal transformation ID')
    evalFrameLayout.addRow( t2IDButtonLabel, self.t2IDButton)
    self.result = qt.QLabel(self.stringRMS)
    chronoButton = qt.QPushButton('Start chrono')
    chronoButton.connect('clicked()',self.chrono)
    evaluationButton = qt.QPushButton('Evaluation')
    evaluationButton.connect('clicked()',self.RMS)
    evalFrameLayout.addRow( chronoButton)
    #evalFrameLayout.addRow( evaluationButton)
    
    ###CP Registration Settings -> Advanced Settings group
    self.nbIterButton = qt.QSpinBox()
    self.nbIterButton.setMinimum(0)
    self.nbIterButton.setMaximum(1000)
    self.nbIterButton.setValue(20)
    nbIterButtonLabel = qt.QLabel('Nb Iterations')
    ICPGroupBoxLayout.addRow( nbIterButtonLabel, self.nbIterButton)
    self.checkMeandist = qt.QSpinBox()
    self.checkMeandist.setMinimum(0)
    self.checkMeandist.setMaximum(1)
    self.checkMeandist.setValue(0)
    checkMeandistLabel = qt.QLabel('Check Mean Distance')
    ICPGroupBoxLayout.addRow( checkMeandistLabel, self.checkMeandist)
    self.Meandist = qt.QSpinBox()
    self.Meandist.setMinimum(0)
    self.Meandist.setMaximum(10000)
    self.Meandist.setValue(20)
    meandistLabel = qt.QLabel('Mean Distance Stop (/10000)')
    ICPGroupBoxLayout.addRow( meandistLabel, self.Meandist)
    self.landmarksNb = qt.QSpinBox()
    self.landmarksNb.setMinimum(0)
    self.landmarksNb.setMaximum(10000)
    self.landmarksNb.setValue(1000)
    landmarksNbLabel = qt.QLabel('LandMarksNb')
    ICPGroupBoxLayout.addRow( landmarksNbLabel, self.landmarksNb)
    
    ###Segmentation settings groupbox
    SegGroupBox = qt.QGroupBox()
    SegGroupBox.setTitle( 'Segmentation Settings' )
    advFrameLayout.addRow( SegGroupBox )
    SegGroupBoxLayout = qt.QFormLayout( SegGroupBox )
    
    ###Segmentation Settings
    self.medianFilterRadioButton = qt.QRadioButton('Median Filter')
    self.fourierFilterRadioButton =  qt.QRadioButton('LowPass filter in frequency domain')
    self.medianFilterRadioButton.setChecked(1)
    SegGroupBoxLayout.addRow(self.fourierFilterRadioButton)
    SegGroupBoxLayout.addRow(self.medianFilterRadioButton)
    self.thresholdFilteredOnImage = qt.QSpinBox()
    self.thresholdFilteredOnImage.setMinimum(0)
    self.thresholdFilteredOnImage.setMaximum(100)
    self.thresholdFilteredOnImage.setValue(20)
    thresholdFilteredOnImageLabel = qt.QLabel('Threshold Max Median Filter')
    SegGroupBoxLayout.addRow( thresholdFilteredOnImageLabel, self.thresholdFilteredOnImage)
    self.cutOffLowPassFilter = qt.QSpinBox()
    self.cutOffLowPassFilter.setMinimum(0)
    self.cutOffLowPassFilter.setMaximum(10000)
    self.cutOffLowPassFilter.setValue(30)
    self.cutOffLowPassFilter.toolTip = "Bigger the value, bigger the Model (default 30)"
    cutOffLowPassFilterLabel = qt.QLabel('Cut Off Low Pass Fourier Filter (/1000)')
    SegGroupBoxLayout.addRow( cutOffLowPassFilterLabel, self.cutOffLowPassFilter)
    self.xRoi = qt.QSpinBox()
    self.xRoi.setMinimum(0)
    self.xRoi.setMaximum(30)
    self.xRoi.setValue(3)
    self.xRoi.toolTip = "x median"
    xRoiLabel = qt.QLabel('x median filter')
    SegGroupBoxLayout.addRow( xRoiLabel, self.xRoi)
    self.yRoi = qt.QSpinBox()
    self.yRoi.setMinimum(0)
    self.yRoi.setMaximum(30)
    self.yRoi.setValue(8)
    self.yRoi.toolTip = "y median"
    yRoiLabel = qt.QLabel('y median filter value')
    SegGroupBoxLayout.addRow( yRoiLabel, self.yRoi)
    self.zRoi = qt.QSpinBox()
    self.zRoi.setMinimum(0)
    self.zRoi.setMaximum(30)
    self.zRoi.setValue(1)
    self.zRoi.toolTip = "z median"
    zRoiLabel = qt.QLabel('y median filter value')
    SegGroupBoxLayout.addRow( zRoiLabel, self.zRoi)
    
    ### Add button to Basic Frame
    segTemplateGroupBoxLayout.addRow(threshLabel, self.__threshRange)
    segTemplateGroupBoxLayout.addRow(make3DModelButton)
    segObturatorGroupBoxLayout.addRow(autoSegmentationButton)
    segObturatorGroupBoxLayout.addRow(editorFrame)
    registrationGroupBoxLayout.addRow(self.ICPRegistrationButton)
    registrationGroupBoxLayout.addRow(self.ICPRegistrationButton2)
    evaluationGroupBoxLayout.addRow(fLabel,self.pullObturatorValueButton)
    evaluationGroupBoxLayout.addRow(evaluationButton)
    evaluationGroupBoxLayout.addRow(self.result)
    
    
    ###Buttons Full Auto Seg + Reg and Restore Registration
    widget = qt.QWidget()
    hlay = qt.QHBoxLayout(widget)
    hlay.addWidget(IFeelLuckyButton)
    hlay.addWidget(backToInitialRegistrationButton)
    
    ###Processing Status
    self.__layout.addRow(self.__registrationStatus)
    
    ### Add 'I Feel Lucky' and 'Restore Initial Registration Button'
    self.__layout.addRow( widget )
    
    ### Basic Frame
    self.__layout.addRow(basicFrame)
    
    ###Add Editor and Advanced Settings for segmentation
    
    self.__layout.addRow(advancedFrame)
    self.__layout.addRow(evaluationFrame)
    
    # reset module
    
    resetButton = qt.QPushButton( 'Reset Module' )
    resetButton.connect( 'clicked()', self.onResetButton )
    self.__layout.addRow(resetButton)
  
  def onResetButton( self ):
    '''
    '''
    
    self.workflow().goBackward() # 4
    self.workflow().goBackward() # 3
    self.workflow().goBackward() # 2
    self.workflow().goBackward() # 1

  def pullObturator(self):
    '''
    Move the obturator along its z-axis. Positive value to pull.
    '''
    ###give the step size
    nDepth = self.pullObturatorValueButton.value-self.pos0
    pNode=self.parameterNode()
    mrmlScene=slicer.mrmlScene  
    obturatorID = pNode.GetParameter('obturatorID')
    self.ObturatorNode = mrmlScene.GetNodeByID(obturatorID)
    if self.ObturatorNode!=None :   
      self.m_poly = vtk.vtkPolyData()  
      self.m_poly.DeepCopy(self.ObturatorNode.GetPolyData())
    
    ### 4x4 transformation matrix. Only z (2,3) is to be modified
    vtkmat = vtk.vtkMatrix4x4()
    vtkmat.SetElement(2,3,nDepth)
    
    self.TransformPolyDataFilter.SetInput(self.m_poly)
    self.Transform.SetMatrix(vtkmat)
    
    self.TransformPolyDataFilter.SetTransform(self.Transform)
    self.TransformPolyDataFilter.Update()
    
    ###Apply the transformation
    triangles=vtk.vtkTriangleFilter()
    triangles.SetInput(self.TransformPolyDataFilter.GetOutput())
    self.ObturatorNode.SetAndObservePolyData(triangles.GetOutput())
    self.pos0 = self.pullObturatorValueButton.value
 
  def setPointData(self,fHoleOriginX,fHoleOriginY):
    '''
    Create a list of points used for the ICP registration
    '''
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
  
  def ICPRegistration(self):
    '''
    ICP Registration based on vtk.vtkIterativeClosestPointTransform()
    '''
    ### Initialisation
    self.__registrationStatus.setText('ICP registration running...')
    segmentationModel = None 
    modelFromImageNode = None
    modelFromImageNodeManu = None
    modelFromImageNodeAuto = None
    self.glyphPoints = vtk.vtkPoints()
    self.glyphInputData= vtk.vtkPolyData()
    self.glyphBalls = vtk.vtkSphereSource()
    self.glyphPoints3D = vtk.vtkGlyph3D()
    self.pointId=0
    ### Scroll all the model nodes. Keep the CAD template and CAD Obturator
    numNodes = slicer.mrmlScene.GetNumberOfNodesByClass( "vtkMRMLModelNode" ) 
    for n in xrange(numNodes): 
      node = slicer.mrmlScene.GetNthNodeByClass( n, "vtkMRMLModelNode" ) 
      if node.GetName() == "templateSegmentedModel": 
        segmentationModel = node 
      if node.GetName() == "obturator": 
        modelFromImageNodeManu = node 
    
    ### Scroll all the model nodes. Keep nodes from automatic segmentation and from manual/growCut Segmentation. Keep in priority these last one.
    modelnodes = slicer.util.getNodes('modelobturator')
    for node in modelnodes.values():
      modelFromImageNodeAuto=node
    
    if modelFromImageNodeManu != None and modelFromImageNodeAuto !=None :
      modelFromImageNode = modelFromImageNodeManu
    elif modelFromImageNodeAuto !=None:
      modelFromImageNode = modelFromImageNodeAuto
    else:
      modelFromImageNode = modelFromImageNodeManu
    
    ### Need segmented obturator to continue
    if modelFromImageNode != None:
          
      self.__registrationStatus.setText('Please Wait ...')
      ###Block the ICP Registration button to avoid user to click during the process
      self.ICPRegistrationButton.setEnabled(0)
      scene = slicer.mrmlScene
      pNode= self.parameterNode()
      
      ### Get the transformation matrix
      pNode=self.parameterNode()
      transformNodeID = pNode.GetParameter('followupTransformID')
      self.transform = Helper.getNodeByID(transformNodeID)
      self.vtkMatInitial = self.transform.GetMatrixTransformToParent()
      
      ### Set a list of known points from template CAD Model
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
 
      self.glyphInputData.SetPoints(self.glyphPoints)
      self.glyphInputData.Update()

      self.glyphBalls.SetRadius(0.05)
      self.glyphBalls.SetThetaResolution(6)
      self.glyphBalls.SetPhiResolution(10)

      self.glyphPoints3D.SetInput(self.glyphInputData)
      self.glyphPoints3D.SetSource(self.glyphBalls.GetOutput())
      self.glyphPoints3D.Update()  
      
      ### Get CAD Template 
      template = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('templateID'))
      inputSurface = template
      
      ### Get Segmented Template
      targetSurface = segmentationModel
      self.templateDisplayModel = segmentationModel.GetDisplayNode()
      self.obturatorDisplayModel = modelFromImageNode.GetDisplayNode()
      
      ### Define target : segmented obturator (modelFromImageNode) + segmented template (targetSurface)
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
      
      ### Define source: list of known points on the CAD template (the holes) + polydata filter on the CAD obturator
      addSource = vtk.vtkAppendPolyData()
      addSource.AddInput( self.glyphInputData)
      addSource.AddInput(TransformPolyDataFilter.GetOutput())
      addSource.Update()
      
      ### Set parameters to the ICP transformation
      icpTransform = vtk.vtkIterativeClosestPointTransform()
      icpTransform.SetSource(addSource.GetOutput())
      icpTransform.SetTarget(addTarget.GetOutput())
      icpTransform.SetCheckMeanDistance(self.checkMeandist.value)
      icpTransform.SetMaximumMeanDistance(self.Meandist.value/10000)
      icpTransform.SetMaximumNumberOfIterations(self.nbIterButton.value)
      icpTransform.SetMaximumNumberOfLandmarks(self.landmarksNb.value)
      icpTransform.SetMeanDistanceModeToRMS()
      icpTransform.GetLandmarkTransform().SetModeToRigidBody()
      icpTransform.Update()
      self.nIterations = icpTransform.GetNumberOfIterations()
      FinalMatrix = vtk.vtkMatrix4x4()
      
      ### Apply the transformation: Multiply the transformation matrix
      FinalMatrix.Multiply4x4(icpTransform.GetMatrix(),self.vtkMatInitial,FinalMatrix)
      ### Update the linear transform with the computed transformation matrix  
      self.transform.SetAndObserveMatrixTransformToParent(FinalMatrix)

      ### post registration stuffs
      self.processRegistrationCompletion()
    
    ### In case the user try the ICP without having a manually segmented obturator named 'obturator' 
    ### or an auto segmented obturator named 'modelobturator'
    
      ### evaluates processing time
      self.processingTime = time.clock()-self.t0
      
    elif self.fullAutoRegOn == 0:
      messageBox = qt.QMessageBox.warning( self, 'Error','Please make a model named "obturator"')
      self.ICPRegistrationButton.setChecked(0)
      self.ICPRegistrationButton.text = "3/ ICP Registration"
      
  def ICPRegistration2(self):
    '''
    ICP Registration based on vtk.vtkIterativeClosestPointTransform()
    '''
    ### Initialisation
    
    segmentationModel = None 
    modelFromImageNode = None
    modelFromImageNodeManu = None
    modelFromImageNodeAuto = None
    self.glyphPoints = vtk.vtkPoints()
    self.glyphInputData= vtk.vtkPolyData()
    self.glyphBalls = vtk.vtkSphereSource()
    self.glyphPoints3D = vtk.vtkGlyph3D()
    self.pointId=0
    
    ### Scroll all the model nodes. Keep the CAD template and CAD Obturator
    numNodes = slicer.mrmlScene.GetNumberOfNodesByClass( "vtkMRMLModelNode" ) 
    for n in xrange(numNodes): 
      node = slicer.mrmlScene.GetNthNodeByClass( n, "vtkMRMLModelNode" ) 
      if node.GetName() == "templateSegmentedModel": 
        segmentationModel = node 

    self.__registrationStatus.setText('Please Wait ...')
    ###Block the ICP Registration button to avoid user to click during the process
    self.ICPRegistrationButton.setEnabled(0)
    scene = slicer.mrmlScene
    pNode= self.parameterNode()
    
    ### Get the transformation matrix
    self.vtkMatInitial = self.transform.GetMatrixTransformToParent()
    
    ### Set a list of known points from template CAD Model
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

    self.glyphInputData.SetPoints(self.glyphPoints)
    self.glyphInputData.Update()

    self.glyphBalls.SetRadius(0.05)
    self.glyphBalls.SetThetaResolution(6)
    self.glyphBalls.SetPhiResolution(10)

    self.glyphPoints3D.SetInput(self.glyphInputData)
    self.glyphPoints3D.SetSource(self.glyphBalls.GetOutput())
    self.glyphPoints3D.Update()  
    
    ### Get CAD Template 
    template = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('templateID'))
    inputSurface = template
    
    ### Get Segmented Template
    targetSurface = segmentationModel
    self.templateDisplayModel = segmentationModel.GetDisplayNode()
    
    
    ### Define target : segmented obturator (modelFromImageNode) + segmented template (targetSurface)
    addTarget = vtk.vtkAppendPolyData()
    addTarget.AddInput(targetSurface.GetPolyData())
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
    
    ### Define source: list of known points on the CAD template (the holes) + polydata filter on the CAD obturator
    addSource = vtk.vtkAppendPolyData()
    addSource.AddInput( self.glyphInputData)
    addSource.Update()
    
    ### Set parameters to the ICP transformation
    icpTransform = vtk.vtkIterativeClosestPointTransform()
    icpTransform.SetSource(addSource.GetOutput())
    icpTransform.SetTarget(addTarget.GetOutput())
    icpTransform.SetCheckMeanDistance(self.checkMeandist.value)
    icpTransform.SetMaximumMeanDistance(self.Meandist.value/10000)
    icpTransform.SetMaximumNumberOfIterations(300)
    icpTransform.SetMaximumNumberOfLandmarks(self.landmarksNb.value)
    icpTransform.SetMeanDistanceModeToRMS()
    icpTransform.GetLandmarkTransform().SetModeToRigidBody()
    icpTransform.Update()
    self.nIterations = icpTransform.GetNumberOfIterations()
    FinalMatrix = vtk.vtkMatrix4x4()
    
    ### Apply the transformation: Multiply the transformation matrix
    FinalMatrix.Multiply4x4(icpTransform.GetMatrix(),self.vtkMatInitial,FinalMatrix)
    ### Update the linear transform with the computed transformation matrix  
    self.transform.SetAndObserveMatrixTransformToParent(FinalMatrix)

    ### post registration stuffs
    self.processRegistrationCompletion()
  
    ### In case the user try the ICP without having a manually segmented obturator named 'obturator' 
    ### or an auto segmented obturator named 'modelobturator'
    ### evaluates processing time
    self.processingTime = time.clock()-self.t0
      
      
  def processRegistrationCompletion(self):
    '''
    Once the ICP is completed, display a message telling so, uncheck the ICP button, restore default view
    '''
    
    self.__registrationStatus.setText('ICP Registration Completed')
    self.updateROItemplate()
    self.ICPRegistrationButton.setEnabled(1)
    self.ICPRegistrationButton.setChecked(0)
    Helper.SetLabelVolume('None')
    pNode =self.parameterNode()
    ### restore the default view
    Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')
    
    
  def onICPButtonToggled(self,checked):
    '''
    Run ICP reg when ICP button is toogled
    Possibility to watch the registration evolving but takes more time, so commented
    '''
    if checked:  
      self.startICP()
      self.regIter += 1
    # else:
      # self.stopICP()
      # self.ICPRegistrationButton.text = "ICP Registration"
  
  def onICPButtonToggled2(self,checked):
    '''
    Run ICP reg when ICP button is toogled
    Possibility to watch the registration evolving but takes more time, so commented
    '''
    if checked:  
      self.ICPRegistration2()
          
  def startICP(self, node=None, event=None):          
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
    '''
    Create a model (vtkMRMLModelNode) for labelmap done with threshold the volume cropped by a box adjusted around the CAD templated 
    '''
    
    ### Scroll all the model nodes. Keep the Segmented templated if existing, then delete it, because we're going to make a new one!
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      if modelNode.GetName()=='templateSegmentedModel':
        slicer.mrmlScene.RemoveNode(modelNode)
    
    ### Parameters used from on step to another
    pNode = self.parameterNode()
    range0 = self.__threshRange.minimumValue
    range1 = self.__threshRange.maximumValue
    roiVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
    roiSegmentationNode = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeSegmentationID'))

    ### threshold segmentation. 
    thresh = vtk.vtkImageThreshold()
    thresh.SetInput(roiVolume.GetImageData())
    thresh.ThresholdBetween(range0, range1)
    thresh.SetInValue(10)
    thresh.SetOutValue(0)
    thresh.ReplaceOutOn()
    thresh.ReplaceInOn()
    thresh.Update()

    ### Adjust the labelmap accordingly
    roiSegmentationNode.SetAndObserveImageData(thresh.GetOutput())
    Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')
    

    ### set up the model maker node 
    parameters = {} 
    parameters['Name'] = 'templateSegmentedModel' 
    parameters["InputVolume"] = roiSegmentationNode.GetID() 
    parameters['FilterType'] = "Sinc" 

    ### build only the currently selected model. 
    parameters['Labels'] = 10
    parameters["StartLabel"] = -1 
    parameters["EndLabel"] = -1 
    parameters['GenerateAll'] = False 
    parameters["JointSmoothing"] = False 
    parameters["SplitNormals"] = True 
    parameters["PointNormals"] = True 
    parameters["SkipUnNamed"] = True 
    parameters["Decimate"] = 0.25 
    parameters["Smooth"] = 10 
  
    ### output 
    ### - make a new hierarchy node if needed 
    ### 
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
    self.__registrationStatus.setText('Template Segmented...')  

    ### We have a segmented templated, we can allow the user to start an ICP registration
    self.ICPRegistrationButton.setEnabled(1)   
    self.ICPRegistrationButton2.setEnabled(1)     
        
  def onThresholdChanged(self):
    '''
    Every time the threshold slicer is moved, adjust the labelmap
    '''    
    pNode = self.parameterNode()
    range0 = self.__threshRange.minimumValue
    range1 = self.__threshRange.maximumValue
    roiVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
    self.__roiSegmentationNode = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeSegmentationID'))

    thresh = vtk.vtkImageThreshold()
    thresh.SetInput(roiVolume.GetImageData())
    thresh.ThresholdBetween(range0, range1)
    thresh.SetInValue(10)
    thresh.SetOutValue(0)
    thresh.ReplaceOutOn()
    thresh.ReplaceInOn()
    thresh.Update()
    
    ### update the label volume accordingly
    self.__roiSegmentationNode.SetAndObserveImageData(thresh.GetOutput())
    Helper.SetBgFgVolumes(pNode.GetParameter('BaselineVolumeID'),'')
    Helper.SetLabelVolume(self.__roiSegmentationNode.GetID())

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )
    self.__parent.validationSucceeded(desiredBranchId)

  def onExit(self, goingTo, transitionType):
    pNode = self.parameterNode()
    if pNode.GetParameter('skip') != '1':
      pNode.SetParameter('thresholdRange', str(self.__threshRange.minimumValue)+','+str(self.__threshRange.maximumValue))
      if self.segmentationModel:
        self.segmentationModel.RemoveAllChildrenNodes()
        slicer.mrmlScene.RemoveNode(self.segmentationModel)
      self.obturatorDisplayModel.SetVisibility(0)
      self.templateDisplayModel.SetVisibility(0)
      numNodes = slicer.mrmlScene.GetNumberOfNodesByClass( "vtkMRMLAnnotationROINode" ) 
      for n in xrange(numNodes):
        node = slicer.mrmlScene.GetNthNodeByClass( n, "vtkMRMLAnnotationROINode" )     
        slicer.mrmlScene.RemoveNode(node)
    if goingTo.id() != 'FirstRegistration' and goingTo.id() != 'NeedlePlanning':
      return      
    super(iGyneSecondRegistrationStep, self).onExit(goingTo, transitionType)
    

  def onEntry(self,comingFrom,transitionType):
    '''
    Update GUI and visualization
    '''
    super(iGyneSecondRegistrationStep, self).onEntry(comingFrom, transitionType)
    pNode = self.parameterNode()
    if pNode.GetParameter('skip') != '1':
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
      self.saveInitialRegistration()
      pNode.SetParameter('currentStep', self.stepid)
      
      ###chrono start
      self.t0 = time.clock()
    else:
      self.workflow().goForward() # 3      
    
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
    transformNodeID = pNode.GetParameter('followupTransformID')
    self.transform = Helper.getNodeByID(transformNodeID)

 
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
    
  def obturatorSegmentation(self):
    x=  (46.1749-23.8251)/2+23.8251
    y = (65.1951-42.9222)/2+42.9222
    z = 150/2-110
    pNode = self.parameterNode()
    volume = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('baselineVolumeID'))
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      if modelNode.GetName()=='Obturator_reg':
        obturator = modelNode
    
    coord=[0,0,0]
    polydata = obturator.GetPolyData()
    polydata.GetPoint(polydata.GetNumberOfPoints()-1,coord)
    
    
    # create ROI
    roi = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationROINode')
    slicer.mrmlScene.AddNode(roi)
    roi.VisibleOn()
    # Transform ROI to match the obturator after the first (fiducial) registration
    transform = slicer.vtkMRMLLinearTransformNode()
    slicer.mrmlScene.AddNode(transform)
    transformID = obturator.GetTransformNodeID()
    transform = slicer.mrmlScene.GetNodeByID(transformID)
    M = transform.GetMatrixTransformToParent()
    m = vtk.vtkMatrix4x4()
    t = slicer.mrmlScene.CreateNodeByClass('vtkMRMLLinearTransformNode')
    slicer.mrmlScene.AddNode(t)
    # obturator in initial position to get the boundaries of the model -> boundaries of ROI
    obturator.SetAndObserveTransformNodeID(t.GetID())
    bounds = [0,0,0,0,0,0]
    obturator.GetRASBounds(bounds)
    roi.SetRadiusXYZ(abs(bounds[0]-bounds[1])*float(105)/100,abs(bounds[2]-bounds[3])*float(105)/100,abs(bounds[4]-bounds[5])*float(30)/100)
    # move again obturator in previous position (after first registration)
    obturator.SetAndObserveTransformNodeID(transform.GetID())
    m.DeepCopy(M)
    m0=vtk.vtkMatrix4x4()
    m0.SetElement(0,3,x)
    m0.SetElement(1,3,y)
    m0.SetElement(2,3,z)
    m.Multiply4x4(m,m0,m)
    t.SetAndObserveMatrixTransformToParent(m)
    roi.SetAndObserveTransformNodeID(t.GetID())
    roi.SetLocked(1)
    
    roi.SetXYZ([0,0,-50+self.pullObturatorValueButton.value])
    #crop volume
    cropVolumeNode =slicer.mrmlScene.CreateNodeByClass('vtkMRMLCropVolumeParametersNode')
    cropVolumeNode.SetScene(slicer.mrmlScene)
    cropVolumeNode.SetName('obturator_CropVolume_node')
    cropVolumeNode.SetIsotropicResampling(True)
    cropVolumeNode.SetSpacingScalingConst(0.5)
    slicer.mrmlScene.AddNode(cropVolumeNode)
    cropVolumeNode.SetInputVolumeNodeID(volume.GetID())
    cropVolumeNode.SetROINodeID(roi.GetID())
    cropVolumeLogic = slicer.modules.cropvolume.logic()
    cropVolumeLogic.Apply(cropVolumeNode)
    outputVolume = slicer.mrmlScene.GetNodeByID(cropVolumeNode.GetOutputVolumeNodeID())
    outputVolume.SetName("obturatorROI")
    
    if self.medianFilterRadioButton.checked :
      self.__registrationStatus.setText('Median Filter Running...')
      self.imagefiltered = slicer.mrmlScene.CreateNodeByClass('vtkMRMLScalarVolumeNode')
      self.imagefiltered.SetName('Median Filter Output')
      slicer.mrmlScene.AddNode(self.imagefiltered)
      #median filter processing
      parameters = {}
      parameters["inputVolume"] = outputVolume
      parameters["outputVolume"] = self.imagefiltered
      parameters["neighborhood"] = self.xRoi.value,self.yRoi.value,self.zRoi.value
      medianfiltercli = slicer.modules.medianimagefilter
      __cliNode = None
      __cliNode = slicer.cli.run(medianfiltercli, __cliNode, parameters)
      
      self.__cliObserverTag = __cliNode.AddObserver('ModifiedEvent', self.medianFilterCompleted)

    
    else:
      self.__registrationStatus.setText('FFT and Low Pass filter running...')
      self.imagefiltered = self.outputLowPassFilter(outputVolume.GetID())
      self.thresholdObturator() 

   
  def medianFilterCompleted(self, node, event):
    
    status = node.GetStatusString()

    if status == 'Completed':
      self.thresholdObturator()
      self.__registrationStatus.setText('Median Filter Completed. Threshold Running...')


  def thresholdObturator(self):
    pNode = self.parameterNode()
   
    vl = slicer.modules.volumes.logic()
    roiSegmentation = vl.CreateLabelVolume(slicer.mrmlScene, self.imagefiltered, 'obturator_segmentation')
    # roiRange = outputVolume.GetImageData().GetScalarRange()
    # default threshold is half-way of the range
    # thresholdParameter = str(0)+','+str(roiRange[1])
    
    labelsColorNode = slicer.modules.colors.logic().GetColorTableNodeID(10)
    roiSegmentation.GetDisplayNode().SetAndObserveColorNodeID(labelsColorNode)
    
    thresh = vtk.vtkImageThreshold()
    thresh.SetInput(self.imagefiltered.GetImageData())
    thresh.ThresholdBetween(0, self.thresholdFilteredOnImage.value)
    thresh.SetInValue(30)
    thresh.SetOutValue(0)
    thresh.ReplaceOutOn()
    thresh.ReplaceInOn()
    thresh.Update()
    roiSegmentation.SetAndObserveImageData(thresh.GetOutput())

    Helper.SetLabelVolume(roiSegmentation.GetID())   

    editUtil = EditorLib.EditUtil.EditUtil()
    parameterNode = editUtil.getParameterNode()
    sliceLogic = editUtil.getSliceLogic()
    lm = slicer.app.layoutManager()
    sliceWidget = lm.sliceWidget('Red')
    islandsEffect = EditorLib.IdentifyIslandsEffectOptions()
    islandsEffect.setMRMLDefaults()
    islandsEffect.__del__()
    
    islandTool = EditorLib.IdentifyIslandsEffectLogic(sliceLogic)
    parameterNode.SetParameter("IslandEffect,minimumSize",'100000')
    islandTool.removeIslands()
    self.__registrationStatus.setText('Threshold, island effect applied. Model Maker Running...')
    
    #make model from segmented labelmap
   # set up the model maker node 
    parameters = {} 
    parameters['Name'] = 'modelobturator'
    parameters["InputVolume"] = roiSegmentation.GetID() 
    parameters['FilterType'] = "Sinc" 
    # build only the currently selected model. 
    parameters['Labels'] = 1
    parameters["StartLabel"] = -1 
    parameters["EndLabel"] = -1 
    parameters['GenerateAll'] = False 
    parameters["JointSmoothing"] = False 
    parameters["SplitNormals"] = True 
    parameters["PointNormals"] = True 
    parameters["SkipUnNamed"] = True 
    parameters["Decimate"] = 0.25 
    parameters["Smooth"] = 10 
    # output 
    # - make a new hierarchy node if needed 
    #
    Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')
 
    numNodes = slicer.mrmlScene.GetNumberOfNodesByClass( "vtkMRMLModelHierarchyNode" ) 
    segmentationModel = None 
    for n in xrange(numNodes): 
      node = slicer.mrmlScene.GetNthNodeByClass( n, "vtkMRMLModelHierarchyNode" ) 
      if node.GetName() == "Obturator Segmentation Model": 
        segmentationModel = node
        self.segmentationModelID = segmentationModel.GetID()         
        break  
    if not segmentationModel: 
      segmentationModel = slicer.vtkMRMLModelHierarchyNode()  
      slicer.mrmlScene.AddNode( segmentationModel )
      self.segmentationModelID = segmentationModel.GetID() 
    # if self.fullAutoRegOn == 1 :
      # slicer.mrmlScene.AddObserver(8193,self.startICP)  
      # print self.segmentationModelID
    parameters["ModelSceneFile"] = segmentationModel 
    modelMaker = slicer.modules.modelmaker 
    __cliNode = None
    __cliNode = slicer.cli.run(modelMaker, __cliNode, parameters) 
    
    self.__cliObserverTag = __cliNode.AddObserver('ModifiedEvent', self.updateStatus)
    
    Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')
    

  def updateStatus(self, node, event):
    slicer.mrmlScene.Modified()
    status = node.GetStatusString()
    if status == 'Completed':
      self.__registrationStatus.setText('Segmented obturator model built.')
      self.status = 'Segmentation Completed'

      if self.fullAutoRegOn == 1 :
        slicer.mrmlScene.Modified()
        time.sleep(1)
        slicer.mrmlScene.Modified()
        self.updatedNbModelNodes = slicer.mrmlScene.GetNumberOfNodesByClass('vtkMRMLModelNode')
        
        self.startICP()        
      self.fullAutoRegOn = 0
  
      
  def updateROItemplate(self):
    x=  (46.1749-23.8251)/2+23.8251
    y = (65.1951-42.9222)/2+42.9222
    z = 0
    pNode = self.parameterNode()
    ### remove old nodes cropped volume and labelmap
    roiVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
    roiSegmentationNode = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeSegmentationID'))
    if roiVolume != None:
      slicer.mrmlScene.RemoveNode(roiVolume)
    if roiSegmentationNode != None:
      slicer.mrmlScene.RemoveNode(roiSegmentationNode)
      
    template = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('templateID'))
    volume = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('baselineVolumeID'))
    
    # create ROI
    roi = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationROINode')
    slicer.mrmlScene.AddNode(roi)
    roi.VisibleOn()
    # Transform ROI to match the template after the first (fiducial) registration
    transform = slicer.vtkMRMLLinearTransformNode()
    slicer.mrmlScene.AddNode(transform)
    transformID = template.GetTransformNodeID()
    transform = slicer.mrmlScene.GetNodeByID(transformID)
    M = transform.GetMatrixTransformToParent()
    m = vtk.vtkMatrix4x4()
    t = slicer.mrmlScene.CreateNodeByClass('vtkMRMLLinearTransformNode')
    slicer.mrmlScene.AddNode(t)
    # template in initial position to get the boundaries of the model -> boundaries of ROI
    template.SetAndObserveTransformNodeID(t.GetID())
    bounds = [0,0,0,0,0,0]
    template.GetRASBounds(bounds)
    roi.SetRadiusXYZ(abs(bounds[0]-bounds[1])/2,abs(bounds[2]-bounds[3])/2,abs(bounds[4]-bounds[5])/2)
    # move again template in previous position (after first registration)
    template.SetAndObserveTransformNodeID(transform.GetID())
    m.DeepCopy(M)
    m0=vtk.vtkMatrix4x4()
    m0.SetElement(0,3,x)
    m0.SetElement(1,3,y)
    m0.SetElement(2,3,z)
    m.Multiply4x4(m,m0,m)
    t.SetAndObserveMatrixTransformToParent(m)
    roi.SetAndObserveTransformNodeID(t.GetID())

    roi.SetLocked(1)
    #crop volume
    cropVolumeNode =slicer.mrmlScene.CreateNodeByClass('vtkMRMLCropVolumeParametersNode')
    cropVolumeNode.SetScene(slicer.mrmlScene)
    cropVolumeNode.SetName('obturator_CropVolume_node')
    cropVolumeNode.SetIsotropicResampling(True)
    cropVolumeNode.SetSpacingScalingConst(0.5)
    slicer.mrmlScene.AddNode(cropVolumeNode)
    cropVolumeNode.SetInputVolumeNodeID(volume.GetID())
    cropVolumeNode.SetROINodeID(roi.GetID())
    cropVolumeLogic = slicer.modules.cropvolume.logic()
    cropVolumeLogic.Apply(cropVolumeNode)
    roiVolume = slicer.mrmlScene.GetNodeByID(cropVolumeNode.GetOutputVolumeNodeID())
    
    
    roiVolume.SetName("baselineROI")
    pNode.SetParameter('croppedBaselineVolumeID',cropVolumeNode.GetOutputVolumeNodeID())
    pNode.SetParameter('cropVolumeNodeID',cropVolumeNode.GetID())
    
    vl = slicer.modules.volumes.logic()
    roiSegmentationNode = vl.CreateLabelVolume(slicer.mrmlScene, roiVolume, 'baselineROI_segmentation')
    pNode.SetParameter('croppedBaselineVolumeSegmentationID', roiSegmentationNode.GetID())
    
    
    baselineROIVolume = Helper.getNodeByID(pNode.GetParameter('croppedBaselineVolumeID'))
    baselineROIRange = baselineROIVolume.GetImageData().GetScalarRange()
    
    labelsColorNode = slicer.modules.colors.logic().GetColorTableNodeID(10)
    roiSegmentationNode.GetDisplayNode().SetAndObserveColorNodeID(labelsColorNode)
    Helper.SetLabelVolume(roiSegmentationNode.GetID())
    self.onThresholdChanged()
    
    Helper.SetBgFgVolumes(pNode.GetParameter('BaselineVolumeID'),'')
    
    
  def outputLowPassFilter(self, inputImageID):

    self.__registrationStatus.setText('Low Pass Filter running...')
    inputImage = slicer.mrmlScene.GetNodeByID(inputImageID)
    fftFilter = vtk.vtkImageFFT()
    fftFilter.SetInput(inputImage.GetImageData())
    fftFilter.Update()

    fftCastFilter = vtk.vtkImageCast()
    fftCastFilter.SetOutputScalarTypeToDouble()
    fftCastFilter.SetInputConnection(fftFilter.GetOutputPort())
    fftCastFilter.Update()

    lowPassFilter = vtk.vtkImageIdealLowPass()
    lowPassFilter.SetInputConnection(fftCastFilter.GetOutputPort())
    lowPassFilter.SetXCutOff(float(self.cutOffLowPassFilter.value)/1000)
    lowPassFilter.SetYCutOff(float(self.cutOffLowPassFilter.value)/1000)
    lowPassFilter.SetZCutOff(float(self.cutOffLowPassFilter.value)/1000)
    lowPassFilter.Update()

    rfftFilter = vtk.vtkImageRFFT()
    rfftFilter.SetInputConnection(lowPassFilter.GetOutputPort())
    rfftFilter.Update()

    rfftCastFilter = vtk.vtkImageCast()
    rfftCastFilter.SetOutputScalarTypeToDouble()
    rfftCastFilter.SetInputConnection(rfftFilter.GetOutputPort())
    rfftCastFilter.Update()

    real = vtk.vtkImageExtractComponents()
    real.SetInputConnection(rfftCastFilter.GetOutputPort())
    real.SetComponents(0)
    real.Update()

    imagefiltered = slicer.mrmlScene.CreateNodeByClass('vtkMRMLScalarVolumeNode')
    imagefiltered.SetAndObserveImageData(real.GetOutput())

    matrix = vtk.vtkMatrix4x4()
    inputImage.GetIJKToRASMatrix(matrix)
    imagefiltered.SetIJKToRASMatrix(matrix)

    slicer.mrmlScene.AddNode(imagefiltered)
    return imagefiltered
    
  def saveInitialRegistration(self):
    
    if self.initialTransformMatrix == None:
      pNode=self.parameterNode()
      transformID = pNode.GetParameter('followupTransformID')
      transform = slicer.mrmlScene.GetNodeByID(transformID)
      m = transform.GetMatrixTransformToParent()
     
      self.initialTransformMatrix = vtk.vtkMatrix4x4()
      self.initialTransformMatrix.DeepCopy(m)
      
  def backToInitialRegistration(self):
    if self.initialTransformMatrix != None:
      pNode=self.parameterNode()
      transformID = pNode.GetParameter('followupTransformID')
      transform = slicer.mrmlScene.GetNodeByID(transformID)
      transform.SetAndObserveMatrixTransformToParent(self.initialTransformMatrix)
      
  def IFeelLucky(self):
    
    self.nbModelNodes = slicer.mrmlScene.GetNumberOfNodesByClass('vtkMRMLModelNode')
    self.applyModelMaker()
    ###chrono start
    self.obturatorSegmentation()
    self.updatedNbModelNodes = 0

    
    # self.startICP()
    
    
    # while queue.empty()!= True:
      # #grabs host from queue
      # host = queue.get()
      # if host == 1:
        # self.obturatorSegmentation()
      # if host ==2:
        # self.startICP()
    
    # queue.join()
    self.fullAutoRegOn = 1
    
    # self.obturatorSegmentation()
  
  
  def RMS(self):
    templateID = 'vtkMRMLModelNode'+str(self.templateIDButton.value)
    obturatorID = 'vtkMRMLModelNode'+str(self.obturatorIDButton.value)
    t1ID = 'vtkMRMLLinearTransformNode'+str(self.t1IDButton.value)
    t2ID = 'vtkMRMLLinearTransformNode'+str(self.t2IDButton.value)
    point = [0,0,0]
    p1 = [0,0,0]
    p2 = [0,0,0]
    template = slicer.mrmlScene.GetNodeByID(templateID)
    obturator = slicer.mrmlScene.GetNodeByID(obturatorID)
    polyDataTemplate = template.GetPolyData()
    polyDataObturator = obturator.GetPolyData()
    transform1=slicer.mrmlScene.GetNodeByID(t1ID)
    transform2=slicer.mrmlScene.GetNodeByID(t2ID)
    m1 = transform1.GetMatrixTransformToParent()
    m2 = transform2.GetMatrixTransformToParent()
    nbTemplate = polyDataTemplate.GetNumberOfPoints()
    nbObturator = polyDataObturator.GetNumberOfPoints()
    distancesquare = 0
    distanceaverage = 0
    # for i in range(nbTemplate):
      # polyDataTemplate.GetPoint(i,point)
      # k = vtk.vtkMatrix4x4()
      # o = vtk.vtkMatrix4x4()
      # k.SetElement(0,3,point[0])
      # k.SetElement(1,3,point[1])
      # k.SetElement(2,3,point[2])
      # k.Multiply4x4(m1,k,o)
      # p1[0] = o.GetElement(0,3)
      # p1[1] = o.GetElement(1,3)
      # p1[2] = o.GetElement(2,3)
      # k = vtk.vtkMatrix4x4()
      # o = vtk.vtkMatrix4x4()
      # k.SetElement(0,3,point[0])
      # k.SetElement(1,3,point[1])
      # k.SetElement(2,3,point[2])
      # k.Multiply4x4(m2,k,o)
      # p2[0] = o.GetElement(0,3)
      # p2[1] = o.GetElement(1,3)
      # p2[2] = o.GetElement(2,3)
      # distancesquare += ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)**0.5/nbTemplate 
      
    for i in range(nbObturator):
      polyDataObturator.GetPoint(i,point)
      k = vtk.vtkMatrix4x4()
      o = vtk.vtkMatrix4x4()
      k.SetElement(0,3,point[0])
      k.SetElement(1,3,point[1])
      k.SetElement(2,3,point[2]+self.pullObturatorValueButton.value)
      k.Multiply4x4(m1,k,o)
      p1[0] = o.GetElement(0,3)
      p1[1] = o.GetElement(1,3)
      p1[2] = o.GetElement(2,3)
      k = vtk.vtkMatrix4x4()
      o = vtk.vtkMatrix4x4()
      k.SetElement(0,3,point[0])
      k.SetElement(1,3,point[1])
      k.SetElement(2,3,point[2])
      k.Multiply4x4(m2,k,o)
      p2[0] = o.GetElement(0,3)
      p2[1] = o.GetElement(1,3)
      p2[2] = o.GetElement(2,3)
      distancesquare +=      (p1[0]-p2[0])**2  +   (p1[1]-p2[1])**2  +   (p1[2]-p2[2])**2 
      distanceaverage +=  (  (p1[0]-p2[0])**2  +   (p1[1]-p2[1])**2  +   (p1[2]-p2[2])**2 )**0.5
    distancesquare= (distancesquare/nbObturator)**0.5
    distanceaverage = distanceaverage/nbObturator
        
    self.stringRMS = "RMS: " + str(distancesquare) + " - Processing time: "+ str(self.processingTime) + " - d.av.: "+ str(distanceaverage)
    print(self.stringRMS)
    self.result.setText(self.stringRMS)

  def chrono(self):
    
    ###reset chrono and  start
    self.t0 = time.clock()

    