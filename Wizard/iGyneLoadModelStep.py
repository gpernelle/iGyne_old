from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
import PythonQt

class iGyneLoadModelStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '3. Load the template' )
    self.setDescription( 'Load the template. From this template, auto-crop and registration functions will be processed.' )
    self.__parent = super( iGyneLoadModelStep, self )

  def createUserInterface( self ):
 
    self.__layout = self.__parent.createUserInterface()
   
    baselineScanLabel = qt.QLabel( 'CT or MR scan:' )
    self.__baselineVolumeSelector = slicer.qMRMLNodeComboBox()
    self.__baselineVolumeSelector.toolTip = "Choose the baseline scan"
    self.__baselineVolumeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__baselineVolumeSelector.setMRMLScene(slicer.mrmlScene)
    self.__baselineVolumeSelector.addEnabled = 0

    # followupScanLabel = qt.QLabel( 'Followup scan:' )
    # self.__followupVolumeSelector = slicer.qMRMLNodeComboBox()
    # self.__followupVolumeSelector.toolTip = "Choose the followup scan"
    # self.__followupVolumeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    # self.__followupVolumeSelector.setMRMLScene(slicer.mrmlScene)
    # self.__followupVolumeSelector.addEnabled = 0
	
	#Load Template Button 
    loadTemplateButton = qt.QPushButton('Load template')
    self.__layout.addRow(loadTemplateButton)
    loadTemplateButton.connect('clicked()', self.loadTemplate)

	#Load Scan Button
    self.__fileFrame = ctk.ctkCollapsibleButton()
    self.__fileFrame.text = "File Input"
    self.__fileFrame.collapsed = 1
    fileFrame = qt.QFormLayout(self.__fileFrame)
    self.__layout.addRow(self.__fileFrame)
   
    loadDataButton = qt.QPushButton('Load Scan')
    loadDataButton.connect('clicked()', self.loadData)
    fileFrame.addRow(loadDataButton)
    fileFrame.addRow( baselineScanLabel, self.__baselineVolumeSelector )

    
    # DICOM ToolBox
    self.__DICOMFrame = ctk.ctkCollapsibleButton()
    self.__DICOMFrame.text = "DICOM Input"
    self.__DICOMFrame.collapsed = 1
    dicomFrame = qt.QFormLayout(self.__DICOMFrame)
    self.__layout.addRow(self.__DICOMFrame)

    voiGroupBox = qt.QGroupBox()
    voiGroupBox.setTitle( 'DICOM' )
    dicomFrame.addRow( voiGroupBox )
    voiGroupBoxLayout = qt.QFormLayout( voiGroupBox )
    self.__roiWidget = ctk.ctkDICOMAppWidget()
    voiGroupBoxLayout.addRow( self.__roiWidget )
    
    self.updateWidgetFromParameters(self.parameterNode())

  def loadData(self):
     slicer.util.openAddDataDialog()
    
  def loadTemplate(self):
    pathToScene = slicer.modules.igynepy.path.replace("iGynePy.py","iGynePyTemplate/Template/Template.mrml")
    slicer.util.loadScene( pathToScene, True)

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId ) 

    ## check here that the selectors are not empty
    baseline = self.__baselineVolumeSelector.currentNode()
    if baseline != None:
      baselineID = baseline.GetID()
      if baselineID != '':
    
        pNode = self.parameterNode()
        pNode.SetParameter('baselineVolumeID', baselineID)
        self.__parent.validationSucceeded(desiredBranchId)
      else:
        self.__parent.validationFailed(desiredBranchId, 'Error','Please select a nrrd or a DICOM volume!')
        
  def onEntry(self,comingFrom,transitionType):
  
    super(iGyneLoadModelStep, self).onEntry(comingFrom, transitionType)
    # setup the interface
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)    
    self.updateWidgetFromParameterNode(pNode)
   
  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    #error checking
    if goingTo.id() != 'SelectApplicator' and goingTo.id() != 'FirstRegistration':
      return
    super(iGyneLoadModelStep, self).onExit(goingTo, transitionType) 


  def updateWidgetFromParameters(self, parameterNode):
    baselineVolumeID = parameterNode.GetParameter('baselineVolumeID')
    if baselineVolumeID != None:
      self.__baselineVolumeSelector.setCurrentNode(Helper.getNodeByID(baselineVolumeID))
    super(iGyneLoadModelStep, self).onExit(goingTo, transitionType)

        
  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()

    baselineVolume = Helper.getNodeByID(pNode.GetParameter('baselineVolumeID'))
    print(baselineVolume)
    roiTransformID = pNode.GetParameter('roiTransformID')
    roiTransformNode = None
    
    if roiTransformID != '':
      roiTransformNode = Helper.getNodeByID(roiTransformID)
    else:
      roiTransformNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLLinearTransformNode')
      slicer.mrmlScene.AddNode(roiTransformNode)
      pNode.SetParameter('roiTransformID', roiTransformNode.GetID())

    dm = vtk.vtkMatrix4x4()
    baselineVolume.GetIJKToRASDirectionMatrix(dm)
    dm.SetElement(0,3,0)
    dm.SetElement(1,3,0)
    dm.SetElement(2,3,0)
    dm.SetElement(0,0,abs(dm.GetElement(0,0)))
    dm.SetElement(1,1,abs(dm.GetElement(1,1)))
    dm.SetElement(2,2,abs(dm.GetElement(2,2)))
    roiTransformNode.SetAndObserveMatrixTransformToParent(dm)        