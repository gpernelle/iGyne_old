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
    self.loadTemplateButton = None

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
    self.loadTemplateButton = qt.QPushButton('Load template')
    self.__layout.addRow(self.loadTemplateButton)
    self.loadTemplateButton.connect('clicked()', self.loadTemplate)

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
    
  # def loadTemplate(self):
    # pathToScene = slicer.modules.igynepy.path.replace("iGynePy.py","iGynePyTemplate/Template/Template.mrml")
    # slicer.util.loadScene( pathToScene, True)
    # self.loadTemplateButton.setEnabled(0)

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )

    # check here that the selectors are not empty
    baseline = self.__baselineVolumeSelector.currentNode()
    followup = slicer.mrmlScene.GetNodeByID("vtkMRMLModelNode4")
    obturator = slicer.mrmlScene.GetNodeByID("vtkMRMLModelNode5")

    if baseline != None and followup != None:
      baselineID = baseline.GetID()
      followupID = followup.GetID()
      obturatorID = obturator.GetID()
      if baselineID != '' and followupID != '' and baselineID != followupID:
    
        pNode = self.parameterNode()
        pNode.SetParameter('baselineVolumeID', baselineID)
        pNode.SetParameter('followupVolumeID', followupID)
        pNode.SetParameter('obturatorID', obturatorID)
        
        self.__parent.validationSucceeded(desiredBranchId)
      else:
        self.__parent.validationFailed(desiredBranchId, 'Error','Please select distinctive baseline and followup volumes!')
    else:
      self.__parent.validationFailed(desiredBranchId, 'Error','Please select both Template and scan/DICOM Volume!')
        
  def onEntry(self,comingFrom,transitionType):
  
    super(iGyneLoadModelStep, self).onEntry(comingFrom, transitionType)
    # setup the interface
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid) 
    applicator  = pNode.GetParameter('Template')
    if applicator == "Template+Obturator":
      self.loadTemplate()    
    self.updateWidgetFromParameters(self.parameterNode())
   
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


        
  def doStepProcessing(self):
  
  
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()

    baselineVolume = Helper.getNodeByID(pNode.GetParameter('baselineVolumeID'))
    followupVolume = Helper.getNodeByID(pNode.GetParameter('followupVolumeID'))
    roiTransformID = pNode.GetParameter('roiTransformID')
    roiTransformNode = None
    
    if roiTransformID != '':
      roiTransformNode = Helper.getNodeByID(roiTransformID)
    else:
      roiTransformNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLLinearTransformNode')
      slicer.mrmlScene.AddNode(roiTransformNode)
      pNode.SetParameter('roiTransformID', roiTransformNode.GetID())

    dm = vtk.vtkMatrix4x4()
    bounds = [0,0,0,0,0,0]
    followupVolume.GetRASBounds(bounds)
    dm.SetElement(0,3,(bounds[0]+bounds[1])/float(2))
    dm.SetElement(1,3,(bounds[2]+bounds[3])/float(2))
    dm.SetElement(2,3,(bounds[4]+bounds[5])/float(2))
    dm.SetElement(0,0,abs(dm.GetElement(0,0)))
    dm.SetElement(1,1,abs(dm.GetElement(1,1)))
    dm.SetElement(2,2,abs(dm.GetElement(2,2)))
    roiTransformNode.SetAndObserveMatrixTransformToParent(dm)     

  ###############################################################################
#################################################################################


  def createSpinbox(self, popup, popupSpinbox):

    popupLayout = qt.QHBoxLayout(popup)  
    popupLayout.addWidget(popupSpinbox) 

    sizePolicy1 = qt.QSizePolicy()
    sizePolicy1.setHorizontalStretch(0)
    sizePolicy1.setVerticalStretch(0)
    sizePolicy1.setHeightForWidth(popupSpinbox.sizePolicy.hasHeightForWidth())
    popupSpinbox.setStyleSheet("background-color: rgb(255, 255, 255)")
    popupSpinbox.setSizePolicy(sizePolicy1)
    popupSpinbox.setMaximum(300)
    popupSpinbox.setValue(170)  

  def setNeedleCoordinates(self):
    self.p = [[0 for j in range(63)] for j in range(3)]
    self.p[0][0]=35
    self.p[1][0]=34
    self.p[0][1]=25
    self.p[1][1]=36.679
    self.p[0][2]=17.679
    self.p[1][2]=44
    self.p[0][3]=15
    self.p[1][3]=54
    self.p[0][4]=17.679
    self.p[1][4]=64
    self.p[0][5]=25
    self.p[1][5]=71.321
    self.p[0][6]=35
    self.p[1][6]=74
    self.p[0][7]=45
    self.p[1][7]=71.321
    self.p[0][8]=52.321
    self.p[1][8]=64
    self.p[0][9]=55
    self.p[1][9]=54
    self.p[0][10]=52.321
    self.p[1][10]=44
    self.p[0][11]=45
    self.p[1][11]=36.679
    self.p[0][12]=29.791
    self.p[1][12]=24.456
    self.p[0][13]=20
    self.p[1][13]=28.019
    self.p[0][14]=12.019
    self.p[1][14]=34.716
    self.p[0][15]=6.809
    self.p[1][15]=43.739
    self.p[0][16]=5
    self.p[1][16]=54
    self.p[0][17]=6.809
    self.p[1][17]=64.261
    self.p[0][18]=12.019
    self.p[1][18]=73.284
    self.p[0][19]=20
    self.p[1][19]=79.981
    self.p[0][20]=29.791
    self.p[1][20]=83.544
    self.p[0][21]=40.209
    self.p[1][21]=83.544
    self.p[0][22]=50
    self.p[1][22]=79.981
    self.p[0][23]=57.981
    self.p[1][23]=73.284
    self.p[0][24]=63.191
    self.p[1][24]=64.262
    self.p[0][25]=65
    self.p[1][25]=54
    self.p[0][26]=63.191
    self.p[1][26]=43.739
    self.p[0][27]=57.981
    self.p[1][27]=34.716
    self.p[0][28]=50
    self.p[1][28]=28.019
    self.p[0][29]=40.209
    self.p[1][29]=24.456
    self.p[0][30]=35
    self.p[1][30]=14
    self.p[0][31]=24.647
    self.p[1][31]=15.363
    self.p[0][32]=15
    self.p[1][32]=19.359
    self.p[0][33]=15
    self.p[1][33]=88.641
    self.p[0][34]=24.647
    self.p[1][34]=92.637
    self.p[0][35]=35
    self.p[1][35]=94
    self.p[0][36]=45.353
    self.p[1][36]=92.637
    self.p[0][37]=55
    self.p[1][37]=88.641
    self.p[0][38]=55
    self.p[1][38]=19.359
    self.p[0][39]=45.353
    self.p[1][39]=15.363
    self.p[0][40]=30.642
    self.p[1][40]=4.19
    self.p[0][41]=22.059
    self.p[1][41]=5.704
    self.p[0][42]=22.059
    self.p[1][42]=102.296
    self.p[0][43]=30.642
    self.p[1][43]=103.81
    self.p[0][44]=39.358
    self.p[1][44]=103.81
    self.p[0][45]=47.941
    self.p[1][45]=102.296
    self.p[0][46]=47.941
    self.p[1][46]=5.704
    self.p[0][47]=39.358
    self.p[1][47]=4.19
    self.p[0][48]=29.7
    self.p[1][48]=44.82
    self.p[0][49]=24.4
    self.p[1][49]=54
    self.p[0][50]=29.7
    self.p[1][50]=63.18
    self.p[0][51]=40.3
    self.p[1][51]=63.18
    self.p[0][52]=45.6
    self.p[1][52]=54
    self.p[0][53]=40.3
    self.p[1][53]=44.82
    self.p[0][54]=35
    self.p[1][54]=54
    self.p[0][55]=9
    self.p[1][55]=12
    self.p[0][56]=5
    self.p[1][56]=18
    self.p[0][57]=5
    self.p[1][57]=90
    self.p[0][58]=9
    self.p[1][58]=96
    self.p[0][59]=61
    self.p[1][59]=96
    self.p[0][60]=65
    self.p[1][60]=90
    self.p[0][61]=65
    self.p[1][61]=18
    self.p[0][62]=61
    self.p[1][62]=12

  def computerPolydataAndMatrix(self):

    Cylinder = vtk.vtkCylinderSource()

    Cylinder.SetResolution(1000)
    Cylinder.SetCapping(1) 
    Cylinder.SetHeight( float(200.0) )
    Cylinder.SetRadius( float(1.0) )
    self.m_polyCylinder=Cylinder.GetOutput()

    self.m_vtkmat = vtk.vtkMatrix4x4()
    self.m_vtkmat.Identity()

    RestruMatrix=vtk.vtkMatrix4x4()
    WorldMatrix=vtk.vtkMatrix4x4()
    Restru2WorldMatrix=vtk.vtkMatrix4x4()

    RestruMatrix.SetElement(0,0,0)
    RestruMatrix.SetElement(1,0,0)
    RestruMatrix.SetElement(2,0,0)
    RestruMatrix.SetElement(3,0,1)

    RestruMatrix.SetElement(0,1,1)
    RestruMatrix.SetElement(1,1,0)
    RestruMatrix.SetElement(2,1,0)
    RestruMatrix.SetElement(3,1,1)

    RestruMatrix.SetElement(0,2,0)
    RestruMatrix.SetElement(1,2,1)
    RestruMatrix.SetElement(2,2,0)
    RestruMatrix.SetElement(3,2,1)

    RestruMatrix.SetElement(0,3,0)
    RestruMatrix.SetElement(1,3,0)
    RestruMatrix.SetElement(2,3,1)
    RestruMatrix.SetElement(3,3,1)

    WorldMatrix.SetElement(0,0,0)
    WorldMatrix.SetElement(1,0,0)
    WorldMatrix.SetElement(2,0,0)
    WorldMatrix.SetElement(3,0,1)

    WorldMatrix.SetElement(0,1,1)
    WorldMatrix.SetElement(1,1,0)
    WorldMatrix.SetElement(2,1,0)
    WorldMatrix.SetElement(3,1,1)

    WorldMatrix.SetElement(0,2,0)
    WorldMatrix.SetElement(1,2,0)
    WorldMatrix.SetElement(2,2,-1)
    WorldMatrix.SetElement(3,2,1)

    WorldMatrix.SetElement(0,3,0)
    WorldMatrix.SetElement(1,3,1)
    WorldMatrix.SetElement(2,3,0)
    WorldMatrix.SetElement(3,3,1)

    WorldMatrix.Invert()
    Restru2WorldMatrix.Multiply4x4(RestruMatrix,WorldMatrix,self.m_vtkmat)

  ##-----------------------------------------------------------------------------
  def showIuNeedle(self):

    self.showOneNeedle(54,self.IuRadioButton) 


  ##-----------------------------------------------------------------------------
  def showAaNeedle(self):

    self.showOneNeedle(48,self.AaRadioButton) 


  ##-----------------------------------------------------------------------------
  def showAbNeedle(self):

    self.showOneNeedle(49,self.AbRadioButton)


  ##-----------------------------------------------------------------------------
  def showAcNeedle(self):

    self.showOneNeedle(50,self.AcRadioButton)


  ##-----------------------------------------------------------------------------
  def showAdNeedle(self):

    self.showOneNeedle(51,self.AdRadioButton)


  ##-----------------------------------------------------------------------------
  def showAeNeedle(self):

    self.showOneNeedle(52,self.AeRadioButton)


  ##-----------------------------------------------------------------------------
  def showAfNeedle(self):

    self.showOneNeedle(53,self.AfRadioButton)


  ##-----------------------------------------------------------------------------
  def showBaNeedle(self):

    self.showOneNeedle(0,self.BaRadioButton) 


  ##-----------------------------------------------------------------------------
  def showBbNeedle(self):

    self.showOneNeedle(1,self.BbRadioButton)


  ##-----------------------------------------------------------------------------
  def showBcNeedle(self):

    self.showOneNeedle(2,self.BcRadioButton)


  ##-----------------------------------------------------------------------------
  def showBdNeedle(self):

    self.showOneNeedle(3,self.BdRadioButton)


  ##-----------------------------------------------------------------------------
  def showBeNeedle(self):

    self.showOneNeedle(4,self.BeRadioButton)


  ##-----------------------------------------------------------------------------
  def showBfNeedle(self):

    self.showOneNeedle(5,self.BfRadioButton)


  ##-----------------------------------------------------------------------------
  def showBgNeedle(self):

    self.showOneNeedle(6,self.BgRadioButton)


  ##-----------------------------------------------------------------------------
  def showBhNeedle(self):

    self.showOneNeedle(7,self.BhRadioButton)


  ##-----------------------------------------------------------------------------
  def showBiNeedle(self):

    self.showOneNeedle(8,self.BiRadioButton)


  ##-----------------------------------------------------------------------------
  def showBjNeedle(self):

    self.showOneNeedle(9,self.BjRadioButton)


  ##-----------------------------------------------------------------------------
  def showBkNeedle(self):

    self.showOneNeedle(10,self.BkRadioButton)


  ##-----------------------------------------------------------------------------
  def showBlNeedle(self):

    self.showOneNeedle(11,self.BlRadioButton)


  ##-----------------------------------------------------------------------------
  def showCaNeedle(self):

    self.showOneNeedle(12,self.CaRadioButton) 


  ##-----------------------------------------------------------------------------
  def showCbNeedle(self):

    self.showOneNeedle(13,self.CbRadioButton)


  ##-----------------------------------------------------------------------------
  def showCcNeedle(self):

    self.showOneNeedle(14,self.CcRadioButton)


  ##-----------------------------------------------------------------------------
  def showCdNeedle(self):

    self.showOneNeedle(15,self.CdRadioButton)


  ##-----------------------------------------------------------------------------
  def showCeNeedle(self):

    self.showOneNeedle(16,self.CeRadioButton)


  ##-----------------------------------------------------------------------------
  def showCfNeedle(self):

    self.showOneNeedle(17,self.CfRadioButton)


  ##-----------------------------------------------------------------------------
  def showCgNeedle(self):

    self.showOneNeedle(18,self.CgRadioButton)


  ##-----------------------------------------------------------------------------
  def showChNeedle(self):

    self.showOneNeedle(19,self.ChRadioButton)


  ##-----------------------------------------------------------------------------
  def showCiNeedle(self):

    self.showOneNeedle(20,self.CiRadioButton)


  ##-----------------------------------------------------------------------------
  def showCjNeedle(self):

    self.showOneNeedle(21,self.CjRadioButton)


  ##-----------------------------------------------------------------------------
  def showCkNeedle(self):

    self.showOneNeedle(22,self.CkRadioButton)


  ##-----------------------------------------------------------------------------
  def showClNeedle(self):

    self.showOneNeedle(23,self.ClRadioButton)


  ##-----------------------------------------------------------------------------
  def showCmNeedle(self):

    self.showOneNeedle(24,self.CmRadioButton)


  ##-----------------------------------------------------------------------------
  def showCnNeedle(self):

    self.showOneNeedle(25,self.CnRadioButton)


  ##-----------------------------------------------------------------------------
  def showCoNeedle(self):

    self.showOneNeedle(26,self.CoRadioButton)


  ##-----------------------------------------------------------------------------
  def showCpNeedle(self):

    self.showOneNeedle(27,self.CpRadioButton)


  ##-----------------------------------------------------------------------------
  def showCqNeedle(self):

    self.showOneNeedle(28,self.CqRadioButton)


  ##-----------------------------------------------------------------------------
  def showCrNeedle(self):

    self.showOneNeedle(29,self.CrRadioButton)


  ##-----------------------------------------------------------------------------
  def showDaNeedle(self):

    self.showOneNeedle(30,self.DaRadioButton) 


  ##-----------------------------------------------------------------------------
  def showDbNeedle(self):

    self.showOneNeedle(31,self.DbRadioButton)


  ##-----------------------------------------------------------------------------
  def showDcNeedle(self):

    self.showOneNeedle(32,self.DcRadioButton)


  ##-----------------------------------------------------------------------------
  def showDdNeedle(self):

    self.showOneNeedle(33,self.DdRadioButton)


  ##-----------------------------------------------------------------------------
  def showDeNeedle(self):

    self.showOneNeedle(34,self.DeRadioButton)


  ##-----------------------------------------------------------------------------
  def showDfNeedle(self):

    self.showOneNeedle(35,self.DfRadioButton)


  ##-----------------------------------------------------------------------------
  def showDgNeedle(self):

    self.showOneNeedle(36,self.DgRadioButton)


  ##-----------------------------------------------------------------------------
  def showDhNeedle(self):

    self.showOneNeedle(37,self.DhRadioButton)


  ##-----------------------------------------------------------------------------
  def showDiNeedle(self):

    self.showOneNeedle(38,self.DiRadioButton)


  ##-----------------------------------------------------------------------------
  def showDjNeedle(self):

    self.showOneNeedle(39,self.DjRadioButton)


  ##-----------------------------------------------------------------------------
  def showEaNeedle(self):

    self.showOneNeedle(40,self.EaRadioButton) 


  ##-----------------------------------------------------------------------------
  def showEbNeedle(self):

    self.showOneNeedle(41,self.EbRadioButton)


  ##-----------------------------------------------------------------------------
  def showEcNeedle(self):

    self.showOneNeedle(42,self.EcRadioButton)


  ##-----------------------------------------------------------------------------
  def showEdNeedle(self):

    self.showOneNeedle(43,self.EdRadioButton)


  ##-----------------------------------------------------------------------------
  def showEeNeedle(self):

    self.showOneNeedle(44,self.EeRadioButton)


  ##-----------------------------------------------------------------------------
  def showEfNeedle(self):

    self.showOneNeedle(45,self.EfRadioButton)


  ##-----------------------------------------------------------------------------
  def showEgNeedle(self):

    self.showOneNeedle(46,self.EgRadioButton)


  ##-----------------------------------------------------------------------------
  def showEhNeedle(self):

    self.showOneNeedle(47,self.EhRadioButton)


  ##-----------------------------------------------------------------------------
  def showFaNeedle(self):

    self.showOneNeedle(55,self.FaRadioButton) 


  ##-----------------------------------------------------------------------------
  def showFbNeedle(self):

    self.showOneNeedle(56,self.FbRadioButton)


  ##-----------------------------------------------------------------------------
  def showFcNeedle(self):

    self.showOneNeedle(57,self.FcRadioButton)


  ##-----------------------------------------------------------------------------
  def showFdNeedle(self):

    self.showOneNeedle(58,self.FdRadioButton)


  ##-----------------------------------------------------------------------------
  def showFeNeedle(self):

    self.showOneNeedle(59,self.FeRadioButton)


  ##-----------------------------------------------------------------------------
  def showFfNeedle(self):

    self.showOneNeedle(60,self.FfRadioButton)


  ##-----------------------------------------------------------------------------
  def showFgNeedle(self):

    self.showOneNeedle(61,self.FgRadioButton)


  ##-----------------------------------------------------------------------------
  def showFhNeedle(self):

    self.showOneNeedle(62,self.FhRadioButton)


  ##-----------------------------------------------------------------------------
  def pushIuNeedle(self):

    nDepth = self.popupSpinboxIu.value

    self.pushOneNeedle(54, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushAaNeedle(self):

    nDepth = self.popupSpinboxAa.value

    self.pushOneNeedle(48, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushAbNeedle(self):

    nDepth = self.popupSpinboxAb.value

    self.pushOneNeedle(49, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushAcNeedle(self):

    nDepth = self.popupSpinboxAc.value

    self.pushOneNeedle(50, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushAdNeedle(self):

    nDepth = self.popupSpinboxAd.value

    self.pushOneNeedle(51, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushAeNeedle(self):

    nDepth = self.popupSpinboxAe.value

    self.pushOneNeedle(52, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushAfNeedle(self):

    nDepth = self.popupSpinboxAf.value

    self.pushOneNeedle(53, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBaNeedle(self):

    nDepth = self.popupSpinboxBa.value

    self.pushOneNeedle(0, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBbNeedle(self):

    nDepth = self.popupSpinboxBb.value

    self.pushOneNeedle(1, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBcNeedle(self):

    nDepth = self.popupSpinboxBc.value

    self.pushOneNeedle(2, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBdNeedle(self):

    nDepth = self.popupSpinboxBd.value

    self.pushOneNeedle(3, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBeNeedle(self):

    nDepth = self.popupSpinboxBe.value

    nDepth = self.popupSpinboxBe.value

    self.pushOneNeedle(4, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBfNeedle(self):

    nDepth = self.popupSpinboxBf.value

    self.pushOneNeedle(5, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBgNeedle(self):

    nDepth = self.popupSpinboxBg.value

    self.pushOneNeedle(6, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBhNeedle(self):

    nDepth = self.popupSpinboxBh.value

    self.pushOneNeedle(7, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBiNeedle(self):

    nDepth = self.popupSpinboxBi.value

    self.pushOneNeedle(8, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBjNeedle(self):

    nDepth = self.popupSpinboxBj.value

    self.pushOneNeedle(9, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBkNeedle(self):

    nDepth = self.popupSpinboxBk.value

    self.pushOneNeedle(10, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushBlNeedle(self):

    nDepth = self.popupSpinboxBl.value

    self.pushOneNeedle(11, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCaNeedle(self):

    nDepth = self.popupSpinboxCa.value

    self.pushOneNeedle(12, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCbNeedle(self):

    nDepth = self.popupSpinboxCb.value

    self.pushOneNeedle(13, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCcNeedle(self):

    nDepth = self.popupSpinboxCc.value

    self.pushOneNeedle(14, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCdNeedle(self):

    nDepth = self.popupSpinboxCd.value

    self.pushOneNeedle(15, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCeNeedle(self):

    nDepth = self.popupSpinboxCe.value

    self.pushOneNeedle(16, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCfNeedle(self):

    nDepth = self.popupSpinboxCf.value

    self.pushOneNeedle(17, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCgNeedle(self):

    nDepth = self.popupSpinboxCg.value

    self.pushOneNeedle(18, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushChNeedle(self):

    nDepth = self.popupSpinboxCh.value

    self.pushOneNeedle(19, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCiNeedle(self):

    nDepth = self.popupSpinboxCi.value

    self.pushOneNeedle(20, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCjNeedle(self):

    nDepth = self.popupSpinboxCj.value

    self.pushOneNeedle(21, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCkNeedle(self):

    nDepth = self.popupSpinboxCk.value

    self.pushOneNeedle(22, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushClNeedle(self):

    nDepth = self.popupSpinboxCl.value

    self.pushOneNeedle(23, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCmNeedle(self):

    nDepth = self.popupSpinboxCm.value

    self.pushOneNeedle(24, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCnNeedle(self):

    nDepth = self.popupSpinboxCn.value

    self.pushOneNeedle(25, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCoNeedle(self):

    nDepth = self.popupSpinboxCo.value

    self.pushOneNeedle(26, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCpNeedle(self):

    nDepth = self.popupSpinboxCp.value

    self.pushOneNeedle(27, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCqNeedle(self):

    nDepth = self.popupSpinboxCq.value

    self.pushOneNeedle(28, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushCrNeedle(self):

    nDepth = self.popupSpinboxCr.value

    self.pushOneNeedle(29, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDaNeedle(self):

    nDepth = self.popupSpinboxDa.value

    self.pushOneNeedle(30, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDbNeedle(self):

    nDepth = self.popupSpinboxDb.value

    self.pushOneNeedle(31, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDcNeedle(self):

    nDepth = self.popupSpinboxDc.value

    self.pushOneNeedle(32, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDdNeedle(self):

    nDepth = self.popupSpinboxDd.value

    self.pushOneNeedle(33, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDeNeedle(self):

    nDepth = self.popupSpinboxDe.value

    self.pushOneNeedle(34, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDfNeedle(self):

    nDepth = self.popupSpinboxDf.value

    self.pushOneNeedle(35, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDgNeedle(self):

    nDepth = self.popupSpinboxDg.value

    self.pushOneNeedle(36, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDhNeedle(self):

    nDepth = self.popupSpinboxDh.value

    self.pushOneNeedle(37, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDiNeedle(self):

    nDepth = self.popupSpinboxDi.value

    self.pushOneNeedle(38, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushDjNeedle(self):

    nDepth = self.popupSpinboxDj.value

    self.pushOneNeedle(39, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushEaNeedle(self):

    nDepth = self.popupSpinboxEa.value

    self.pushOneNeedle(40, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushEbNeedle(self):

    nDepth = self.popupSpinboxEb.value

    self.pushOneNeedle(41, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushEcNeedle(self):

    nDepth = self.popupSpinboxEc.value

    self.pushOneNeedle(42, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushEdNeedle(self):

    nDepth = self.popupSpinboxEd.value

    self.pushOneNeedle(43, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushEeNeedle(self):

    nDepth = self.popupSpinboxEe.value

    self.pushOneNeedle(44, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushEfNeedle(self):

    nDepth = self.popupSpinboxEf.value

    self.pushOneNeedle(45, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushEgNeedle(self):

    nDepth = self.popupSpinboxEg.value

    self.pushOneNeedle(46, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushEhNeedle(self):

    nDepth = self.popupSpinboxEh.value

    self.pushOneNeedle(47, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushFaNeedle(self):

    nDepth = self.popupSpinboxFa.value

    self.pushOneNeedle(55, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushFbNeedle(self):

    nDepth = self.popupSpinboxFb.value

    self.pushOneNeedle(56, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushFcNeedle(self):

    nDepth = self.popupSpinboxFc.value

    self.pushOneNeedle(57, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushFdNeedle(self):

    nDepth = self.popupSpinboxFd.value

    self.pushOneNeedle(58, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushFeNeedle(self):

    nDepth = self.popupSpinboxFe.value

    self.pushOneNeedle(59, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushFfNeedle(self):

    nDepth = self.popupSpinboxFf.value

    self.pushOneNeedle(60, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushFgNeedle(self):

    nDepth = self.popupSpinboxFg.value

    self.pushOneNeedle(61, nDepth)   


  ##-----------------------------------------------------------------------------
  def pushFhNeedle(self):

    nDepth = self.popupSpinboxFh.value

    self.pushOneNeedle(62, nDepth)   


  ##-----------------------------------------------------------------------------
  def setIuColor(self):
    
    self.setOneNeedleColor(54,self.IuColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setAaColor(self):
    
    self.setOneNeedleColor(48,self.AaColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setAbColor(self):
    
    self.setOneNeedleColor(49,self.AbColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setAcColor(self):
    
    self.setOneNeedleColor(50,self.AcColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setAdColor(self):
    
    self.setOneNeedleColor(51,self.AdColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setAeColor(self):
    
    self.setOneNeedleColor(52,self.AeColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setAfColor(self):
    
    self.setOneNeedleColor(53,self.AfColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBaColor(self):
    
    self.setOneNeedleColor(0,self.BaColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBbColor(self):
    
    self.setOneNeedleColor(1,self.BbColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBcColor(self):
    
    self.setOneNeedleColor(2,self.BcColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBdColor(self):
    
    self.setOneNeedleColor(3,self.BdColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBeColor(self):
    
    self.setOneNeedleColor(4,self.BeColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBfColor(self):
    
    self.setOneNeedleColor(5,self.BfColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBgColor(self):
    
    self.setOneNeedleColor(6,self.BgColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBhColor(self):
    
    self.setOneNeedleColor(7,self.BhColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBiColor(self):
    
    self.setOneNeedleColor(8,self.BiColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBjColor(self):
    
    self.setOneNeedleColor(9,self.BjColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBkColor(self):
    
    self.setOneNeedleColor(10,self.BkColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setBlColor(self):
    
    self.setOneNeedleColor(11,self.BlColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCaColor(self):
    
    self.setOneNeedleColor(12,self.CaColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCbColor(self):
    
    self.setOneNeedleColor(13,self.CbColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCcColor(self):
    
    self.setOneNeedleColor(14,self.CcColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCdColor(self):
    
    self.setOneNeedleColor(15,self.CdColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCeColor(self):
    
    self.setOneNeedleColor(16,self.CeColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCfColor(self):
    
    self.setOneNeedleColor(17,self.CfColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCgColor(self):
    
    self.setOneNeedleColor(18,self.CgColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setChColor(self):
    
    self.setOneNeedleColor(19,self.ChColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCiColor(self):
    
    self.setOneNeedleColor(20,self.CiColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCjColor(self):
    
    self.setOneNeedleColor(21,self.CjColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCkColor(self):
    
    self.setOneNeedleColor(22,self.CkColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setClColor(self):
    
    self.setOneNeedleColor(23,self.ClColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCmColor(self):
    
    self.setOneNeedleColor(24,self.CmColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCnColor(self):
    
    self.setOneNeedleColor(25,self.CnColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCoColor(self):
    
    self.setOneNeedleColor(26,self.CoColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCpColor(self):
    
    self.setOneNeedleColor(27,self.CpColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCqColor(self):
    
    self.setOneNeedleColor(28,self.CqColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setCrColor(self):
    
    self.setOneNeedleColor(29,self.CrColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDaColor(self):
    
    self.setOneNeedleColor(30,self.DaColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDbColor(self):
    
    self.setOneNeedleColor(31,self.DbColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDcColor(self):
    
    self.setOneNeedleColor(32,self.DcColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDdColor(self):
    
    self.setOneNeedleColor(33,self.DdColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDeColor(self):
    
    self.setOneNeedleColor(34,self.DeColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDfColor(self):
    
    self.setOneNeedleColor(35,self.DfColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDgColor(self):
    
    self.setOneNeedleColor(36,self.DgColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDhColor(self):
    
    self.setOneNeedleColor(37,self.DhColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDiColor(self):
    
    self.setOneNeedleColor(38,self.DiColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setDjColor(self):
    
    self.setOneNeedleColor(39,self.DjColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setEaColor(self):
    
    self.setOneNeedleColor(40,self.EaColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setEbColor(self):
    
    self.setOneNeedleColor(41,self.EbColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setEcColor(self):
    
    self.setOneNeedleColor(42,self.EcColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setEdColor(self):
    
    self.setOneNeedleColor(43,self.EdColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setEeColor(self):
    
    self.setOneNeedleColor(44,self.EeColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setEfColor(self):
    
    self.setOneNeedleColor(45,self.EfColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setEgColor(self):
    
    self.setOneNeedleColor(46,self.EgColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setEhColor(self):
    
    self.setOneNeedleColor(47,self.EhColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setFaColor(self):
    
    self.setOneNeedleColor(55,self.FaColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setFbColor(self):
    
    self.setOneNeedleColor(56,self.FbColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setFcColor(self):
    
    self.setOneNeedleColor(57,self.FcColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setFdColor(self):
    
    self.setOneNeedleColor(58,self.FdColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setFeColor(self):
    
    self.setOneNeedleColor(59,self.FeColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setFfColor(self):
    
    self.setOneNeedleColor(60,self.FfColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setFgColor(self):
    
    self.setOneNeedleColor(61,self.FgColorPushButton)  


  ##-----------------------------------------------------------------------------
  def setFhColor(self):
    
    self.setOneNeedleColor(62,self.FhColorPushButton)  


  ##-----------------------------------------------------------------------------
  def pushObNeedle(self):

    nDepth = self.popupSpinboxOb.value
    mrmlScene=slicer.mrmlScene  
    self.ObturatorNode = mrmlScene.GetNodeByID("vtkMRMLModelNode5")

    vtkmat = vtk.vtkMatrix4x4()
    vtkmat.Identity()
    vtkmat.SetElement(2,3,nDepth)

    TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
    Transform=vtk.vtkTransform()
    TransformPolyDataFilter.SetInput(self.m_poly)
    Transform.SetMatrix(vtkmat)
    TransformPolyDataFilter.SetTransform(Transform)
    TransformPolyDataFilter.Update()

    triangles=vtk.vtkTriangleFilter()
    triangles.SetInput(TransformPolyDataFilter.GetOutput())
    self.ObturatorNode.SetAndObservePolyData(triangles.GetOutput())    

  ##-----------------------------------------------------------------------------
  def showOneNeedle(self,i,RadioButton):
    
    filename= "vtkMRMLModelNode"+str(i+6)
    mrmlScene=slicer.mrmlScene
    NeedleNode = mrmlScene.GetNodeByID(filename)
    if NeedleNode !=None:
      displayNode =NeedleNode.GetModelDisplayNode()

    nVisibility=displayNode.GetVisibility()  

    if(nVisibility==1):
      displayNode.SetVisibility(0)
      displayNode.SetSliceIntersectionVisibility(0)
      RadioButton.setChecked(False)
    else:
      displayNode.SetVisibility(1)
      displayNode.SetSliceIntersectionVisibility(1)
      RadioButton.setChecked(True)


  ##-----------------------------------------------------------------------------
  def showOneNeedle(self,i,bShowNeedels):

    filename= "vtkMRMLModelNode"+str(i+6)
    mrmlScene=slicer.mrmlScene
    NeedleNode = mrmlScene.GetNodeByID(filename)
    if NeedleNode !=None:
      displayNode =NeedleNode.GetModelDisplayNode()

      if bShowNeedels:
        displayNode.SetVisibility(1)
        displayNode.SetSliceIntersectionVisibility(1)    

      else:
        displayNode.SetVisibility(0)
        displayNode.SetSliceIntersectionVisibility(0)    


  ##-----------------------------------------------------------------------------
  def pushOneNeedle(self,i,nDepth):

    filename= "vtkMRMLModelNode"+str(i+6)
    mrmlScene=slicer.mrmlScene
    NeedleNode = mrmlScene.GetNodeByID(filename)

    vtkmat = vtk.vtkMatrix4x4()
    vtkmat.DeepCopy(self.m_vtkmat) 

    vtkmat.SetElement(0,3,self.m_vtkmat.GetElement(0,3)+self.p[0][i])
    vtkmat.SetElement(1,3,self.m_vtkmat.GetElement(1,3)+self.p[1][i])
    vtkmat.SetElement(2,3,self.m_vtkmat.GetElement(2,3)+110.0-nDepth)

    TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
    Transform=vtk.vtkTransform()
    TransformPolyDataFilter.SetInput(self.m_polyCylinder)
    Transform.SetMatrix(vtkmat)
    TransformPolyDataFilter.SetTransform(Transform)
    TransformPolyDataFilter.Update()

    triangles=vtk.vtkTriangleFilter()
    triangles.SetInput(TransformPolyDataFilter.GetOutput())
    if NeedleNode !=None:
      NeedleNode.SetAndObservePolyData(triangles.GetOutput())
    
  ##-----------------------------------------------------------------------------
  def setOneNeedleColor(self,i,ColorPushButton):

    color = qt.QColorDialog.getColor(qt.QColor('green'), self)
    sColor = ""
    sColor = "background-color: rgb(" + str(color.red())+ "," + str(color.green()) + "," + str(color.blue())

    if color.isValid():

      filename= "vtkMRMLModelNode"+str(i+6)
      mrmlScene=slicer.mrmlScene
      NeedleNode = mrmlScene.GetNodeByID(filename)
      if NeedleNode!=None:
        displayNode =NeedleNode.GetModelDisplayNode()

        displayNode.SetColor(color.red()/float(255.0),color.green()/float(255.0),color.blue()/float(255.0))
        sColor = "background-color: rgb(" + str(color.red())+ "," + str(color.green()) + "," + str(color.blue()) + ')'
        print sColor
        ColorPushButton.setStyleSheet(sColor)
      

  ##-----------------------------------------------------------------------------
  def showNeedles(self):

    if self.ShowNeedlesPushButton.isChecked():
      for i in xrange(63): 
        self.showOneNeedle(i,True)

      self.ShowNeedlesPushButton.setChecked(True)
      self.IuRadioButton.setChecked(True)
      self.AaRadioButton.setChecked(True)
      self.AbRadioButton.setChecked(True)
      self.AcRadioButton.setChecked(True)
      self.AdRadioButton.setChecked(True)
      self.AeRadioButton.setChecked(True)
      self.AfRadioButton.setChecked(True)
      self.BaRadioButton.setChecked(True)
      self.BbRadioButton.setChecked(True)
      self.BcRadioButton.setChecked(True)
      self.BdRadioButton.setChecked(True)
      self.BeRadioButton.setChecked(True)
      self.BfRadioButton.setChecked(True)
      self.BgRadioButton.setChecked(True)
      self.BhRadioButton.setChecked(True)
      self.BiRadioButton.setChecked(True)
      self.BjRadioButton.setChecked(True)
      self.BkRadioButton.setChecked(True)
      self.BlRadioButton.setChecked(True)
      self.CaRadioButton.setChecked(True)
      self.CbRadioButton.setChecked(True)
      self.CcRadioButton.setChecked(True)
      self.CdRadioButton.setChecked(True)
      self.CeRadioButton.setChecked(True)
      self.CfRadioButton.setChecked(True)
      self.CgRadioButton.setChecked(True)
      self.ChRadioButton.setChecked(True)
      self.CiRadioButton.setChecked(True)
      self.CjRadioButton.setChecked(True)
      self.CkRadioButton.setChecked(True)
      self.ClRadioButton.setChecked(True)
      self.CmRadioButton.setChecked(True)
      self.CnRadioButton.setChecked(True)
      self.CoRadioButton.setChecked(True)
      self.CpRadioButton.setChecked(True)
      self.CqRadioButton.setChecked(True)
      self.CrRadioButton.setChecked(True)
      self.DaRadioButton.setChecked(True)
      self.DbRadioButton.setChecked(True)
      self.DcRadioButton.setChecked(True)
      self.DdRadioButton.setChecked(True)
      self.DeRadioButton.setChecked(True)
      self.DfRadioButton.setChecked(True)
      self.DgRadioButton.setChecked(True)
      self.DhRadioButton.setChecked(True)
      self.DiRadioButton.setChecked(True)
      self.DjRadioButton.setChecked(True)
      self.EaRadioButton.setChecked(True)
      self.EbRadioButton.setChecked(True)
      self.EcRadioButton.setChecked(True)
      self.EdRadioButton.setChecked(True)
      self.EeRadioButton.setChecked(True)
      self.EfRadioButton.setChecked(True)
      self.EgRadioButton.setChecked(True)
      self.EhRadioButton.setChecked(True)
      self.FaRadioButton.setChecked(True)
      self.FbRadioButton.setChecked(True)
      self.FcRadioButton.setChecked(True)
      self.FdRadioButton.setChecked(True)
      self.FeRadioButton.setChecked(True)
      self.FfRadioButton.setChecked(True)
      self.FgRadioButton.setChecked(True)
      self.FhRadioButton.setChecked(True)
    else:
      for i in xrange(63):
        self.showOneNeedle(i,False)

      self.ShowNeedlesPushButton.setChecked(False)
      self.IuRadioButton.setChecked(False)
      self.AaRadioButton.setChecked(False)
      self.AbRadioButton.setChecked(False)
      self.AcRadioButton.setChecked(False)
      self.AdRadioButton.setChecked(False)
      self.AeRadioButton.setChecked(False)
      self.AfRadioButton.setChecked(False)
      self.BaRadioButton.setChecked(False)
      self.BbRadioButton.setChecked(False)
      self.BcRadioButton.setChecked(False)
      self.BdRadioButton.setChecked(False)
      self.BeRadioButton.setChecked(False)
      self.BfRadioButton.setChecked(False)
      self.BgRadioButton.setChecked(False)
      self.BhRadioButton.setChecked(False)
      self.BiRadioButton.setChecked(False)
      self.BjRadioButton.setChecked(False)
      self.BkRadioButton.setChecked(False)
      self.BlRadioButton.setChecked(False)
      self.CaRadioButton.setChecked(False)
      self.CbRadioButton.setChecked(False)
      self.CcRadioButton.setChecked(False)
      self.CdRadioButton.setChecked(False)
      self.CeRadioButton.setChecked(False)
      self.CfRadioButton.setChecked(False)
      self.CgRadioButton.setChecked(False)
      self.ChRadioButton.setChecked(False)
      self.CiRadioButton.setChecked(False)
      self.CjRadioButton.setChecked(False)
      self.CkRadioButton.setChecked(False)
      self.ClRadioButton.setChecked(False)
      self.CmRadioButton.setChecked(False)
      self.CnRadioButton.setChecked(False)
      self.CoRadioButton.setChecked(False)
      self.CpRadioButton.setChecked(False)
      self.CqRadioButton.setChecked(False)
      self.CrRadioButton.setChecked(False)
      self.DaRadioButton.setChecked(False)
      self.DbRadioButton.setChecked(False)
      self.DcRadioButton.setChecked(False)
      self.DdRadioButton.setChecked(False)
      self.DeRadioButton.setChecked(False)
      self.DfRadioButton.setChecked(False)
      self.DgRadioButton.setChecked(False)
      self.DhRadioButton.setChecked(False)
      self.DiRadioButton.setChecked(False)
      self.DjRadioButton.setChecked(False)
      self.EaRadioButton.setChecked(False)
      self.EbRadioButton.setChecked(False)
      self.EcRadioButton.setChecked(False)
      self.EdRadioButton.setChecked(False)
      self.EeRadioButton.setChecked(False)
      self.EfRadioButton.setChecked(False)
      self.EgRadioButton.setChecked(False)
      self.EhRadioButton.setChecked(False)
      self.FaRadioButton.setChecked(False)
      self.FbRadioButton.setChecked(False)
      self.FcRadioButton.setChecked(False)
      self.FdRadioButton.setChecked(False)
      self.FeRadioButton.setChecked(False)
      self.FfRadioButton.setChecked(False)
      self.FgRadioButton.setChecked(False)
      self.FhRadioButton.setChecked(False)

  def selectNeedles(self):

    mrmlScene=slicer.mrmlScene
    ModelFromImageNode = slicer.vtkMRMLModelNode()
    ModelFromImageNode = mrmlScene.GetNodeByID("vtkMRMLModelNode70")

    if ModelFromImageNode!=None :
   
      collide = vtk.vtkCollisionDetectionFilter()
      matrix0 = vtk.vtkMatrix4x4()
      matrix1 = vtk.vtkMatrix4x4()    
      matrix2 = vtk.vtkMatrix4x4()  

      collide.SetInput(0,ModelFromImageNode.GetPolyData())
      collide.SetMatrix(0, matrix0)

      transformNode = mrmlScene.GetNodeByID("vtkMRMLLinearTransformNode4")
      vtkmatInitial = transformNode.GetMatrixTransformToParent()

      nContacts=0
      for i in xrange(63):

        sfilename="vtkMRMLModelNode"+ str(i+6)

        NeedleNode = mrmlScene.GetNodeByID(filename)

        vtkmat = vtk.vtkMatrix4x4()
        vtkmat.DeepCopy(self.m_vtkmat) 

        vtkmat.SetElement(0,3,self.m_vtkmat.GetElement(0,3)+self.p[0][i])
        vtkmat.SetElement(1,3,self.m_vtkmat.GetElement(1,3)+self.p[1][i])
        vtkmat.SetElement(2,3,self.m_vtkmat.GetElement(2,3)-100.0)

        matrix1.Multiply4x4(vtkmatInitial,vtkmat,matrix1)

        TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
        Transform=vtk.vtkTransform()
        TransformPolyDataFilter.SetInput(self.m_polyCylinder)
        Transform.SetMatrix(matrix1)
        TransformPolyDataFilter.SetTransform(Transform)
        TransformPolyDataFilter.Update()

        triangles=vtk.vtkTriangleFilter()
        triangles.SetInput(TransformPolyDataFilter.GetOutput())

        collide.SetInput(1,triangles.GetOutput())
        collide.SetMatrix(1, matrix2)
        collide.SetBoxTolerance(0.0)
        collide.SetCellTolerance(0.0)
        collide.SetNumberOfCellsPerBucket(2)
        collide.SetCollisionModeToAllContacts()
        collide.GenerateScalarsOn()
        collide.Update()

        nContacts=collide.GetNumberOfContacts()
        if NeedleNode !=None:  
          displayNode =NeedleNode.GetModelDisplayNode()

          if nContacts>0:
            
            displayNode.SetVisibility(1)
            displayNode.SetSliceIntersectionVisibility(1)
            self.setRadioButton(i,True)
            
          else:
            
            displayNode.SetVisibility(0)
            displayNode.SetSliceIntersectionVisibility(0)
            self.setRadioButton(i,False)
          
  ##-----------------------------------------------------------------------------
  def setRadioButton(self,i,bShowNeedels):
    option = {0:self.BaRadioButton.setChecked(bShowNeedels),
         1:self.BbRadioButton.setChecked(bShowNeedels),
         2:self.BcRadioButton.setChecked(bShowNeedels),
         3:self.BdRadioButton.setChecked(bShowNeedels),
         4:self.BeRadioButton.setChecked(bShowNeedels),
         5:self.BfRadioButton.setChecked(bShowNeedels),
         6:self.BgRadioButton.setChecked(bShowNeedels),
         7:self.BhRadioButton.setChecked(bShowNeedels),
         8:self.BiRadioButton.setChecked(bShowNeedels),
         9:self.BjRadioButton.setChecked(bShowNeedels),
         10:self.BkRadioButton.setChecked(bShowNeedels),
         11:self.BlRadioButton.setChecked(bShowNeedels),
         12:self.CaRadioButton.setChecked(bShowNeedels),
         13:self.CbRadioButton.setChecked(bShowNeedels),
         14:self.CcRadioButton.setChecked(bShowNeedels),
         15:self.CdRadioButton.setChecked(bShowNeedels),
         16:self.CeRadioButton.setChecked(bShowNeedels),
         17:self.CfRadioButton.setChecked(bShowNeedels),
         18:self.CgRadioButton.setChecked(bShowNeedels),
         19:self.ChRadioButton.setChecked(bShowNeedels),
         20:self.CiRadioButton.setChecked(bShowNeedels),
         21:self.CjRadioButton.setChecked(bShowNeedels),
         22:self.CkRadioButton.setChecked(bShowNeedels),
         23:self.ClRadioButton.setChecked(bShowNeedels),
         24:self.CmRadioButton.setChecked(bShowNeedels),
         25:self.CnRadioButton.setChecked(bShowNeedels),
         26:self.CoRadioButton.setChecked(bShowNeedels),
         27:self.CpRadioButton.setChecked(bShowNeedels),
         28:self.CqRadioButton.setChecked(bShowNeedels),
         29:self.CrRadioButton.setChecked(bShowNeedels),
         30:self.DaRadioButton.setChecked(bShowNeedels),
         31:self.DbRadioButton.setChecked(bShowNeedels),
         32:self.DcRadioButton.setChecked(bShowNeedels),
         33:self.DdRadioButton.setChecked(bShowNeedels),
         34:self.DeRadioButton.setChecked(bShowNeedels),
         35:self.DfRadioButton.setChecked(bShowNeedels),
         36:self.DgRadioButton.setChecked(bShowNeedels),
         37:self.DhRadioButton.setChecked(bShowNeedels),
         38:self.DiRadioButton.setChecked(bShowNeedels),
         39:self.DjRadioButton.setChecked(bShowNeedels),
         40:self.EaRadioButton.setChecked(bShowNeedels),
         41:self.EbRadioButton.setChecked(bShowNeedels),
         42:self.EcRadioButton.setChecked(bShowNeedels),
         43:self.EdRadioButton.setChecked(bShowNeedels),
         44:self.EeRadioButton.setChecked(bShowNeedels),
         45:self.EfRadioButton.setChecked(bShowNeedels),
         46:self.EgRadioButton.setChecked(bShowNeedels),
         47:self.EhRadioButton.setChecked(bShowNeedels),
         48:self.AaRadioButton.setChecked(bShowNeedels),
         49:self.AbRadioButton.setChecked(bShowNeedels),
         50:self.AcRadioButton.setChecked(bShowNeedels),
         51:self.AdRadioButton.setChecked(bShowNeedels),
         52:self.AeRadioButton.setChecked(bShowNeedels),
         53:self.AfRadioButton.setChecked(bShowNeedels),
         54:self.IuRadioButton.setChecked(bShowNeedels), 
         55:self.FaRadioButton.setChecked(bShowNeedels),
         56:self.FbRadioButton.setChecked(bShowNeedels),
         57:self.FcRadioButton.setChecked(bShowNeedels),
         58:self.FdRadioButton.setChecked(bShowNeedels),
         59:self.FeRadioButton.setChecked(bShowNeedels),
         60:self.FfRadioButton.setChecked(bShowNeedels),
         61:self.FgRadioButton.setChecked(bShowNeedels),
         62:self.FhRadioButton.setChecked(bShowNeedels)}
         
    option[i]
    
  def loadTemplate(self):
    pNode = self.parameterNode()
    alreadyloaded = pNode.GetParameter("Template-loaded")
    if alreadyloaded != "1":
      pathToScene = slicer.modules.igynepy.path.replace("iGynePy.py","iGynePyTemplate/Template/Template.mrml")
      slicer.util.loadScene( pathToScene, True)
      self.loadTemplateButton.setEnabled(0)
      pNode.SetParameter("Template-loaded","1")
    
    
    ObutratorNode = slicer.mrmlScene.GetNodeByID("vtkMRMLModelNode5")

    if ObutratorNode!=None:
      print("obturator loaded")
      self.setNeedleCoordinates()
      self.computerPolydataAndMatrix()    
      
      self.m_poly = vtk.vtkPolyData()  
      self.m_poly.DeepCopy(ObutratorNode.GetPolyData())
      
    NeedleNode = slicer.mrmlScene.GetNodeByID("vtkMRMLModelNode6")
    if NeedleNode==None:
      print("no needle node loaded")
      vtkmat = vtk.vtkMatrix4x4()
      vtkmat.DeepCopy(self.m_vtkmat)
   
      for i in xrange(63):
      
        vtkmat.SetElement(0,3,self.m_vtkmat.GetElement(0,3)+self.p[0][i])
        vtkmat.SetElement(1,3,self.m_vtkmat.GetElement(1,3)+self.p[1][i])
        vtkmat.SetElement(2,3,self.m_vtkmat.GetElement(2,3)+(30.0-150.0)/2.0)

        TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
        Transform=vtk.vtkTransform()        
        TransformPolyDataFilter.SetInput(self.m_polyCylinder)
        Transform.SetMatrix(vtkmat)
        TransformPolyDataFilter.SetTransform(Transform)
        TransformPolyDataFilter.Update()

        triangles=vtk.vtkTriangleFilter()
        triangles.SetInput(TransformPolyDataFilter.GetOutput())  
        print(Transform) 
        self.AddModel(i,triangles.GetOutput())
        
    else:
      for i in xrange(63):
      
        filename= "vtkMRMLModelNode"+str(i+6)
        mrmlScene=slicer.mrmlScene
        NeedleNode = mrmlScene.GetNodeByID(filename)
        if NeedleNode !=None:
          displayNode =NeedleNode.GetModelDisplayNode()

          nVisibility=displayNode.GetVisibility()  

          if nVisibility==1:
            self.setRadioButton(i,true) 
          else:
            self.setRadioButton(i,false)          

  def AddModel(self,i,polyData):
    modelNode = slicer.vtkMRMLModelNode()
    displayNode = slicer.vtkMRMLModelDisplayNode()
    storageNode = slicer.vtkMRMLModelStorageNode()

    fileName =  "Model_"+ str(i) + ".vtk" 

    mrmlScene = slicer.mrmlScene
    modelNode.SetName(fileName)  
    modelNode.SetAndObservePolyData(polyData)
    mrmlScene.SaveStateForUndo()
    modelNode.SetScene(mrmlScene)
    storageNode.SetScene(mrmlScene)
    storageNode.SetFileName(fileName)  
    displayNode.SetScene(mrmlScene)
    mrmlScene.AddNode(storageNode)
    mrmlScene.AddNode(displayNode)
    modelNode.SetAndObserveStorageNodeID(storageNode.GetID())
    modelNode.SetAndObserveDisplayNodeID(displayNode.GetID())

    transformNode = slicer.mrmlScene.GetNodeByID("vtkMRMLLinearTransformNode4")
    modelNode.SetAndObserveTransformNodeID(transformNode.GetID())
    displayNode.SetPolyData(modelNode.GetPolyData())
    displayNode.SetColor(0,1,0)
    displayNode.SetSliceIntersectionVisibility(0)
    displayNode.SetVisibility(0)

    mrmlScene.AddNode(modelNode)           


