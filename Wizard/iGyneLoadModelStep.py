from __main__ import qt, ctk

from iGyneStep import *
from Helper import *
import PythonQt

class iGyneLoadModelStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '3. Load the template' )
    self.setDescription( 'Load the template. From this template, auto-crop and registration functions will be processed' )
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


  def updateWidgetFromParameters(self, parameterNode):
    baselineVolumeID = parameterNode.GetParameter('baselineVolumeID')
    # followupVolumeID = parameterNode.GetParameter('followupVolumeID')
    if baselineVolumeID != None:
      self.__baselineVolumeSelector.setCurrentNode(Helper.getNodeByID(baselineVolumeID))
    # if followupVolumeID != None:
      # self.__followupVolumeSelector.setCurrentNode(Helper.getNodeByID(followupVolumeID))

  def loadData(self):
     slicer.util.openAddDataDialog()
    
  def loadTemplate(self):
    pathToScene = slicer.modules.igynepy.path.replace("iGynePy.py","iGynePyTemplate/Template/Template.mrml")
    slicer.util.loadScene( pathToScene, True)
    # vl = slicer.modules.volumes.logic()
    # vol1 = vl.AddArchetypeVolume('http://www.slicer.org/slicerWiki/images/5/59/RegLib_C01_1.nrrd', 'Meningioma1', 0)
    # vol2 = vl.AddArchetypeVolume('http://www.slicer.org/slicerWiki/images/e/e3/RegLib_C01_2.nrrd', 'Meningioma2', 0)
    # if vol1 != None and vol2 != None:
      # self.__baselineVolumeSelector.setCurrentNode(vol1)
      # self.__followupVolumeSelector.setCurrentNode(vol1)
      # Helper.SetBgFgVolumes(vol1.GetID(), vol2.GetID())


  def onEntry(self,comingFrom,transitionType):
  
    super(iGyneLoadModelStep, self).onEntry(comingFrom, transitionType)
    # setup the interface
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)    
    # self.updateWidgetFromParameterNode(pNode)
    # qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    if goingTo.id() != 'SelectApplicator' and goingTo.id() != 'FirstRegistration':
      return
    pNode = self.parameterNode()


    super(iGyneLoadModelStep, self).onExit(goingTo, transitionType)

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )    
    self.__parent.validationSucceeded(desiredBranchId)
