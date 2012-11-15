from __future__ import division
from __main__ import qt, ctk, slicer


from iGyneStep import *
from Helper import *
from EditorLib import *
import math,time, functools, operator
import DICOMLib, EditorLib
import string
import numpy
import thread
import random
import copy

'''
TODO:
  add advanced option to specify segmentation
'''

class iGyneNeedleSegmentationStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.skip = 1
    self.initialize( stepid )
    self.setName( '7. Needle Segmentation' )
    self.setDescription( 'Segment the needles' )
    self.__parent = super( iGyneNeedleSegmentationStep, self )
    self.analysisGroupBox = None
    self.buttonsGroupBox = None
    self.round=1
    self.row=0
    self.table=None
    self.view = None
    self.previousValues=[[0,0,0]]
    self.interactorObserverTags = []    
    self.styleObserverTags = []
    self.option = {0:'Ba',
       1:'Bb',
       2:'Bc',
       3:'Bd',
       4:'Be',
       5:'Bf',
       6:'Bg',
       7:'Bh',
       8:'Bi',
       9:'Bj',
       10:'Bk',
       11:'Bl',
       12:'Ca',
       13:'Cb',
       14:'Cc',
       15:'Cd',
       16:'Ce',
       17:'Cf',
       18:'Cg',
       19:'Ch',
       20:'Ci',
       21:'Cj',
       22:'Ck',
       23:'Cl',
       24:'Cm',
       25:'Cn',
       26:'Co',
       27:'Cp',
       28:'Cq',
       29:'Cr',
       30:'Da',
       31:'Db',
       32:'Dc',
       33:'Dd',
       34:'De',
       35:'Df',
       36:'Dg',
       37:'Dh',
       38:'Di',
       39:'Dj',
       40:'Ea',
       41:'Eb',
       42:'Ec',
       43:'Ed',
       44:'Ee',
       45:'Ef',
       46:'Eg',
       47:'Eh',
       48:'Aa',
       49:'Ab',
       50:'Ac',
       51:'Ad',
       52:'Ae',
       53:'Af',
       54:'Iu', 
       55:'Fa',
       56:'Fb',
       57:'Fc',
       58:'Fd',
       59:'Fe',
       60:'Ff',
       61:'Fg',
       62:'Fh',
       63:'--'}

    # initialize the dicom infrastructure
    settings = qt.QSettings()
    # the dicom database is a global object for slicer
    if settings.contains('DatabaseDirectory'):
      databaseDirectory = settings.value('DatabaseDirectory')
      if databaseDirectory: 
        slicer.dicomDatabase = ctk.ctkDICOMDatabase()
        slicer.dicomDatabase.openDatabase(databaseDirectory + "/ctkDICOM.sql", "SLICER")
        # the dicom listener is also global, but only started on app start if 
        # the user so chooses
        if settings.contains('DICOM/RunListenerAtStart'):
          if bool(settings.value('DICOM/RunListenerAtStart')):
            if not hasattr(slicer, 'dicomListener'):
              try:
                slicer.dicomListener = DICOMLib.DICOMListener(slicer.dicomDatabase)
                slicer.dicomListener.start()
              except (UserWarning,OSError) as message:
                # TODO: how to put this into the error log?
                print ('Problem trying to start DICOMListener:\n %s' % message)
    else:
      slicer.dicomDatabase = None

    # TODO: are these wrapped so we can avoid magic numbers?
    self.dicomModelUIDRole = 32
    self.dicomModelTypeRole = self.dicomModelUIDRole + 1
    self.dicomModelTypes = ('Root', 'Patient', 'Study', 'Series', 'Image')

    # state management for compressing events
    self.resumeModelRequested = False
    self.updateRecentActivityRequested = False
    
  def createUserInterface( self ):
    '''
    '''
    self.skip = 0
    pNode = self.parameterNode()
    self.__layout = self.__parent.createUserInterface()
    
    #-------------------------------------------------------------
    # DICOM ToolBox
     # Listener 
    settings = qt.QSettings()
    self.toggleListener = qt.QPushButton()
    if hasattr(slicer, 'dicomListener'):
      self.toggleListener.text = "Stop Listener"
      slicer.dicomListener.process.connect('stateChanged(int)',self.onListenerStateChanged)
    else:
      self.toggleListener.text = "Start Listener"
    self.toggleListener.connect('clicked()', self.onToggleListener)
    self.__DICOMFrame = ctk.ctkCollapsibleButton()
    self.__DICOMFrame.text = "DICOM Input"
    self.__DICOMFrame.collapsed = 1
    dicomFrame = qt.QFormLayout(self.__DICOMFrame)
    self.__layout.addRow(self.__DICOMFrame)
    dicomFrame.addRow(self.toggleListener)
    self.dicomApp = ctk.ctkDICOMAppWidget()
    self.detailsPopup = DICOMLib.DICOMDetailsPopup(self.dicomApp,True)
    self.exportButton = qt.QPushButton('Export Slicer Data to Study...')
    self.loadButton = qt.QPushButton('Load to Slicer')
    self.previewLabel = qt.QLabel()
    self.tree = self.detailsPopup.tree
    self.showBrowser = qt.QPushButton('Show DICOM Browser')
    dicomFrame.addRow(self.showBrowser)
    self.showBrowser.connect('clicked()', self.detailsPopup.open)

    # the recent activity frame
    self.recentActivity = DICOMLib.DICOMRecentActivityWidget(self.__DICOMFrame,detailsPopup=self.detailsPopup)
    self.__DICOMFrame.layout().addWidget(self.recentActivity.widget)
    self.requestUpdateRecentActivity()
    
    if not slicer.dicomDatabase:
      self.promptForDatabaseDirectory()
    else:
      self.onDatabaseDirectoryChanged(self.dicomApp.databaseDirectory)
    if hasattr(slicer, 'dicomListener'):
      slicer.dicomListener.fileToBeAddedCallback = self.onListenerToAddFile
      slicer.dicomListener.fileAddedCallback = self.onListenerAddedFile
    
    self.contextMenu = qt.QMenu(self.tree)
    self.exportAction = qt.QAction("Export to Study", self.contextMenu)
    self.contextMenu.addAction(self.exportAction)
    self.exportAction.enabled = False
    self.deleteAction = qt.QAction("Delete", self.contextMenu)
    self.contextMenu.addAction(self.deleteAction)
    self.contextMenu.connect('triggered(QAction*)', self.onContextMenuTriggered)
    
    self.dicomApp.connect('databaseDirectoryChanged(QString)', self.onDatabaseDirectoryChanged)
    selectionModel = self.tree.selectionModel()
    # TODO: can't use this because QList<QModelIndex> is not visible in PythonQt
    #selectionModel.connect('selectionChanged(QItemSelection, QItemSelection)', self.onTreeSelectionChanged)
    self.tree.connect('clicked(QModelIndex)', self.onTreeClicked)
    self.tree.setContextMenuPolicy(3)
    self.tree.connect('customContextMenuRequested(QPoint)', self.onTreeContextMenuRequested)

    # enable to the Send button of the app widget and take it over
    # for our purposes - TODO: fix this to enable it at the ctkDICOM level
    self.sendButton = slicer.util.findChildren(self.dicomApp, text='Send')[0]
    self.sendButton.enabled = False
    self.sendButton.connect('clicked()', self.onSendClicked)

    #-----------------------------------------------------------------------------
    # segmentation report
    self.analysisGroupBox = qt.QGroupBox()
    self.analysisGroupBox.setFixedHeight(330)
    self.analysisGroupBox.setTitle( 'Segmentation Report' )
    self.__layout.addRow( self.analysisGroupBox )
    self.analysisGroupBoxLayout = qt.QFormLayout( self.analysisGroupBox )    


    #----------------------------------------------------------------------------
    #  editor widgetRepresentation
    # editUtil = EditorLib.EditUtil.EditUtil()
    # parameterNode = editUtil.getParameterNode()
    # sliceLogic = editUtil.getSliceLogic()
    # islandTool = EditorLib.IdentifyIslandsEffectLogic(sliceLogic)
    # parameterNode.SetParameter("IslandEffect,minimumSize",'0')
    # self.__editorFrame = ctk.ctkCollapsibleButton()
    # self.__editorFrame.text = "Editor"
    # self.__editorFrame.collapsed = 0
    # editorFrame = qt.QFormLayout(self.__editorFrame)
    # self.__layout.addRow(self.__editorFrame)
    
    # groupbox = qt.QGroupBox()
    # groupboxLayout  = qt.QFormLayout(groupbox)
    # groupboxLayout.addRow(slicer.modules.editor.widgetRepresentation())
    # editorFrame.addRow(groupbox)
    
    #-----------------------------------------------------------------------------
    # Volume and Label selection. For use with CLI module for straight needle detection
    # needleLabel = qt.QLabel( 'Needle Label:' )
    # self.__needleLabelSelector = slicer.qMRMLNodeComboBox()
    # self.__needleLabelSelector.toolTip = "Choose the needle-label image"
    # self.__needleLabelSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    # self.__needleLabelSelector.addAttribute("vtkMRMLScalarVolumeNode", "LabelMap", "1")
    # self.__needleLabelSelector.setMRMLScene(slicer.mrmlScene)
    # self.__needleLabelSelector.addEnabled = 0
    # self.__needleLabelSelector.removeEnabled = 0
    # self.__needleLabelSelector.noneEnabled = 0
    # self.__layout.connect('mrmlSceneChanged(vtkMRMLScene*)',
    #                     self.__needleLabelSelector, 'setMRMLScene(vtkMRMLScene*)')
    
    # self.__layout.addRow( needleLabel, self.__needleLabelSelector )
    # if Helper.getNodeByID(pNode.GetParameter("baselineVolumeID")) == None:
    #   volumeLabel = qt.QLabel( 'Volume:' )
    #   self.__volumeSelector = slicer.qMRMLNodeComboBox()
    #   self.__volumeSelector.toolTip = "Choose the Volume"
    #   self.__volumeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    #   self.__volumeSelector.setMRMLScene(slicer.mrmlScene)
    #   self.__volumeSelector.addEnabled = 0
    #   self.__volumeSelector.removeEnabled = 0
    #   self.__volumeSelector.noneEnabled = 0
    #   self.__layout.addRow( volumeLabel, self.__volumeSelector )
    #   self.__layout.connect('mrmlSceneChanged(vtkMRMLScene*)',
    #                     self.__volumeSelector, 'setMRMLScene(vtkMRMLScene*)')

    #-----------------------------------------------------------------------------

    # give needle tips
    self.fiducialButton = qt.QPushButton('Start Giving Needle Tips')
    self.fiducialButton.checkable = True
    self.__layout.addRow(self.fiducialButton)
    self.fiducialButton.connect('toggled(bool)', self.onRunButtonToggled)

    # #Segment Needle Button 
    # self.needleButton = qt.QPushButton('Segment Needles')
    # self.__layout.addRow(self.needleButton)
    # self.needleButton.connect('clicked()', self.needleSegmentation)
    # self.needleButton.setEnabled(0)

    #Segment Needle Button 
    self.needleButton2 = qt.QPushButton('Segment/Update Needles - Python')
    self.__layout.addRow(self.needleButton2)
    self.needleButton2.connect('clicked()', self.needleDetection)

    #New insertion - create new round of needles with different colors
    self.newInsertionButton = qt.QPushButton('New Insertion Needle')
    self.__layout.addRow(self.newInsertionButton)
    self.newInsertionButton.connect('clicked()', self.newInsertionNeedle)

    #Delete Needles Button 
    self.deleteNeedleButton = qt.QPushButton('Delete Segmented Needles')
    self.__layout.addRow(self.deleteNeedleButton)
    self.deleteNeedleButton.connect('clicked()', self.deleteSegmentedNeedle)

    #Reset Needle Detection Button 
    self.resetDetectionButton = qt.QPushButton('Reset Needle Detection')
    self.__layout.addRow(self.resetDetectionButton)
    self.resetDetectionButton.connect('clicked()', self.resetNeedleDetection)
    
    self.updateWidgetFromParameters(self.parameterNode())
      
  	#Filter Needles Button
    self.__filterFrame = ctk.ctkCollapsibleButton()
    self.__filterFrame.text = "Filter Needles"
    self.__filterFrame.collapsed = 1
    filterFrame = qt.QFormLayout(self.__filterFrame)
    
    # Filter spin box
    # self.filterValueButton = qt.QSpinBox()
    # self.filterValueButton.setMaximum(500)
    # fLabel = qt.QLabel("Max Deviation Value: ")
    
    # self.removeDuplicates = qt.QCheckBox('Remove duplicates by segmenting')
    # self.removeDuplicates.setChecked(1)
    # self.removeDuplicatesButton = qt.QPushButton('Remove duplicates')
    # self.removeDuplicatesButton.connect('clicked()', self.positionFilteringNeedles)
    
    # filterNeedlesButton = qt.QPushButton('Filter Needles')
    # filterNeedlesButton.connect('clicked()', self.angleFilteringNeedles)
    
    # filterFrame.addRow(self.removeDuplicates)
    # filterFrame.addRow(self.removeDuplicatesButton)
    
    # filterFrame.addRow(fLabel,self.filterValueButton)
    # filterFrame.addRow(filterNeedlesButton)
    
    self.displayFiducialButton = qt.QPushButton('Display Labels On Needles')
    self.displayFiducialButton.connect('clicked()',self.displayFiducial)
    # self.displayRadPlannedButton = qt.QPushButton('Hide Radiation On Planned Needles')
    # self.displayRadPlannedButton.checkable = True
    # self.displayRadPlannedButton.connect('clicked()',self.displayRadPlanned)
    # self.displayRadSegmentedButton = qt.QPushButton('Hide Radiation On Segmented Needles')
    # self.displayRadSegmentedButton.checkable = True
    # self.displayRadSegmentedButton.connect('clicked()',self.displayRadSegmented)
    self.displayContourButton = qt.QPushButton('Draw Isosurfaces')
    self.displayContourButton.checkable = False
    self.displayContourButton.connect('clicked()',self.drawIsoSurfaces)
    self.hideContourButton = qt.QPushButton('Hide Isosurfaces')
    self.hideContourButton.checkable = True
    self.hideContourButton.connect('clicked()',self.hideIsoSurfaces)
    self.hideContourButton.setEnabled(0)
    # self.analysisReportButton = qt.QPushButton('Print Analysis')
    # self.analysisReportButton.connect('clicked()',self.analyzeSegmentation)
    
    
    self.__layout.addRow(self.displayFiducialButton)
    # self.__layout.addRow(self.displayRadPlannedButton)
    # self.__layout.addRow(self.displayRadSegmentedButton)
    self.__layout.addRow(self.displayContourButton)
    self.__layout.addRow(self.hideContourButton)
    # self.__layout.addRow(self.analysisReportButton)
    

    # Bending parameters
    self.__bendingFrame = ctk.ctkCollapsibleButton()
    self.__bendingFrame.text = "Needle Detection Parameters"
    self.__bendingFrame.collapsed = 1
    bendingFrame = qt.QFormLayout(self.__bendingFrame)
    
    # nb points per line spin box
    self.nbPointsPerLine = qt.QSpinBox()
    self.nbPointsPerLine.setMinimum(2)
    self.nbPointsPerLine.setMaximum(500)
    self.nbPointsPerLine.setValue(20)
    nbPointsPerLineLabel = qt.QLabel("Number of points per line: ")
    bendingFrame.addRow( nbPointsPerLineLabel, self.nbPointsPerLine)
    
    # nb radius iteration spin box
    self.nbRadiusIterations = qt.QSpinBox()
    self.nbRadiusIterations.setMinimum(2)
    self.nbRadiusIterations.setMaximum(50)
    self.nbRadiusIterations.setValue(20)
    nbRadiusIterationsLabel = qt.QLabel("Number of distance iterations: ")
    bendingFrame.addRow( nbRadiusIterationsLabel, self.nbRadiusIterations)
    
    # distance max spin box
    self.distanceMax = qt.QSpinBox()
    self.distanceMax.setMinimum(0)
    self.distanceMax.setMaximum(50)
    self.distanceMax.setValue(10)
    distanceMaxLabel = qt.QLabel("rMax: ")
    bendingFrame.addRow( distanceMaxLabel, self.distanceMax)
    
    # nb rotating iterations spin box
    self.nbRotatingIterations = qt.QSpinBox()
    self.nbRotatingIterations.setMinimum(2)
    self.nbRotatingIterations.setMaximum(500)
    self.nbRotatingIterations.setValue(15)
    nbRotatingIterationsLabel = qt.QLabel("Number of rotating steps: ")
    bendingFrame.addRow( nbRotatingIterationsLabel, self.nbRotatingIterations)
    
    # nb heights per needle spin box
    self.numberOfPointsPerNeedle = qt.QSpinBox()
    self.numberOfPointsPerNeedle.setMinimum(1)
    self.numberOfPointsPerNeedle.setMaximum(50)
    self.numberOfPointsPerNeedle.setValue(7)
    numberOfPointsPerNeedleLabel = qt.QLabel("Number of Control Points: ")
    bendingFrame.addRow( numberOfPointsPerNeedleLabel, self.numberOfPointsPerNeedle)

    # nb heights per needle spin box
    self.stepsize = qt.QSpinBox()
    self.stepsize.setMinimum(1)
    self.stepsize.setMaximum(50)
    self.stepsize.setValue(5)
    stepsizeLabel = qt.QLabel("Stepsize: ")
    bendingFrame.addRow( stepsizeLabel, self.stepsize)

    #lenghtNeedle
    self.lenghtNeedleParameter = qt.QSpinBox()
    self.lenghtNeedleParameter.setMinimum(1)
    self.lenghtNeedleParameter.setMaximum(200)
    self.lenghtNeedleParameter.setValue(70)
    stepsizeLabel = qt.QLabel("Lenght of the needles: ")
    bendingFrame.addRow( stepsizeLabel, self.lenghtNeedleParameter)

    # Compute gradient?
    self.gradient=qt.QCheckBox('Compute gradient?')
    self.gradient.setChecked(1)
    bendingFrame.addRow(self.gradient)

    # Filter ControlPoints?
    self.filterControlPoints=qt.QCheckBox('Filter Control Points?')
    self.filterControlPoints.setChecked(0)
    bendingFrame.addRow(self.filterControlPoints)

    # Draw Fiducial Points?
    self.drawFiducialPoints=qt.QCheckBox('Draw Control Points?')
    self.drawFiducialPoints.setChecked(0)
    bendingFrame.addRow(self.drawFiducialPoints)
    
    self.__layout.addRow(self.__filterFrame)
    self.__layout.addRow(self.__bendingFrame)
    # reset module
    
    resetButton = qt.QPushButton( 'Reset Module' )
    resetButton.connect( 'clicked()', self.onResetButton )
    self.__layout.addRow(resetButton)
  
  def onResetButton( self ):
    '''
    '''
    
    self.workflow().goBackward() # 5
    self.workflow().goBackward() # 4
    self.workflow().goBackward() # 3
    self.workflow().goBackward() # 2
    self.workflow().goBackward() # 1
    
  def drawIsoSurfaces0( self ):
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    v= vtk.vtkAppendPolyData()
    
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("nth")!=None and modelNode.GetDisplayVisibility()==1 :
        v.AddInput(modelNode.GetPolyData())
       
    modeller = vtk.vtkImplicitModeller()
    modeller.SetInput(v.GetOutput())
    modeller.SetSampleDimensions(self.dim.value,self.dim.value,self.dim.value)
    modeller.SetCapping(0)
    modeller.SetAdjustBounds(self.abonds.value)
    modeller.SetProcessModeToPerVoxel() 
    modeller.SetAdjustDistance(self.adist.value/100)
    modeller.SetMaximumDistance(self.maxdist.value/100)    
    
    contourFilter = vtk.vtkContourFilter()
    contourFilter.SetNumberOfContours(self.nb.value)
    contourFilter.SetInputConnection(modeller.GetOutputPort())    
    contourFilter.ComputeNormalsOn()
    contourFilter.ComputeScalarsOn()
    contourFilter.UseScalarTreeOn()
    contourFilter.SetValue(self.contour.value,self.contourValue.value)
    contourFilter.SetValue(self.contour2.value,self.contourValue2.value)
    contourFilter.SetValue(self.contour3.value,self.contourValue3.value)
    contourFilter.SetValue(self.contour4.value,self.contourValue4.value)
    contourFilter.SetValue(self.contour5.value,self.contourValue5.value)

    isoSurface = contourFilter.GetOutput()   
    self.AddContour(isoSurface)  
 
  def drawIsoSurfaces( self ):
    self.hideContourButton.setEnabled(1)
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
       
    v= vtk.vtkAppendPolyData()
    canContinue = 0
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("nth")!=None and modelNode.GetDisplayVisibility()==1 :
        canContinue = 1
        v.AddInput(modelNode.GetPolyData())
       
    if canContinue ==1:
      modeller = vtk.vtkImplicitModeller()
      modeller.SetInput(v.GetOutput())
      modeller.SetSampleDimensions(60,60,60)
      modeller.SetCapping(0)
      modeller.AdjustBoundsOn()
      modeller.SetProcessModeToPerVoxel() 
      modeller.SetAdjustDistance(1)
      modeller.SetMaximumDistance(1.0)    
      
      contourFilter = vtk.vtkContourFilter()
      contourFilter.SetNumberOfContours(1)
      contourFilter.SetInputConnection(modeller.GetOutputPort())    
      contourFilter.ComputeNormalsOn()
      contourFilter.ComputeScalarsOn()
      contourFilter.UseScalarTreeOn()
      contourFilter.SetValue(1,10)
      # contourFilter.SetValue(2,13)
      # contourFilter.SetValue(3,15)
      # contourFilter.SetValue(4,20)
      # contourFilter.SetValue(5,25)
      isoSurface = contourFilter.GetOutput()

      self.AddContour(isoSurface)

  def hideIsoSurfaces(self):
    contourNode = None
    contourNode = slicer.util.getNode('Contours')
    if contourNode != None:
      contourNode.SetDisplayVisibility(abs(self.hideContourButton.isChecked()-1))
      contourNode.GetModelDisplayNode().SetSliceIntersectionVisibility(abs(self.hideContourButton.isChecked()-1))

  def displayRadPlanned(self):
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      displayNode = modelNode.GetDisplayNode()
      if modelNode.GetAttribute("radiation") == "planned":
        needleNode = slicer.mrmlScene.GetNodeByID(modelNode.GetAttribute("needleID"))
        if needleNode.GetDisplayVisibility()==1:
          modelNode.SetDisplayVisibility(abs(int(self.displayRadPlannedButton.checked)-1))
            
  def displayRadSegmented(self):
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("radiation") == "segmented":
        needleNode = slicer.mrmlScene.GetNodeByID(modelNode.GetAttribute("needleID"))
        if needleNode != None:
          if needleNode.GetDisplayVisibility()==1:
            modelNode.SetDisplayVisibility(abs(int(self.displayRadSegmentedButton.checked)-1))
            d = modelNode.GetDisplayNode()
            d.SetSliceIntersectionVisibility(abs(int(self.displayRadSegmentedButton.checked)-1))
            
  def displayContour(self,i,visibility):
    # print i, visibility
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("contour") == "1" and modelNode.GetAttribute("nth")==str(i) :
        needleNode = slicer.mrmlScene.GetNodeByID(modelNode.GetAttribute("needleID"))
        if needleNode != None:
          if needleNode.GetDisplayVisibility()==1:
            modelNode.SetDisplayVisibility(visibility)
            d = modelNode.GetDisplayNode()
            d.SetSliceIntersectionVisibility(visibility)
            
  def displayContours(self):
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("contour") == "1":
        needleNode = slicer.mrmlScene.GetNodeByID(modelNode.GetAttribute("needleID"))
        if needleNode != None:
          if needleNode.GetDisplayVisibility()==1:
            modelNode.SetDisplayVisibility(abs(int(self.displayContourButton.checked)-1))
            d = modelNode.GetDisplayNode()
            d.SetSliceIntersectionVisibility(abs(int(self.displayContourButton.checked)-1))

  def analyzeSegmentation(self):
  
    if self.analysisGroupBox != None:
      self.__layout.removeWidget(self.analysisGroupBox)
      self.analysisGroupBox.deleteLater()
      self.analysisGroupBox = None
    self.analysisGroupBox = qt.QGroupBox()
    self.analysisGroupBox.setFixedHeight(600)
    self.analysisGroupBox.setTitle( 'Segmentation Report' )
    self.__layout.addRow( self.analysisGroupBox )
    self.analysisGroupBoxLayout = qt.QFormLayout( self.analysisGroupBox )
    if self.transform !=None :
      # transformation matrix
      m = self.transform.GetMatrixTransformToParent()
      m_t = vtk.vtkMatrix4x4()
      m_t.DeepCopy(m)
      
      # data from a the first planned-needle found
      modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
      stop = 1
      for modelNode in modelNodes.values():
        if modelNode.GetAttribute("planned") == "1" and stop:
          stop = 0
          polyData = modelNode.GetPolyData()
          polyData.Update()
          nb = polyData.GetNumberOfPoints()
          base = [0,0,0]
          tip = [0,0,0]
          polyData.GetPoint(nb-1,tip)
          polyData.GetPoint(0,base)
          # evaluate the angle after the coordinate system transformation - used after as reference
          vtkmat = vtk.vtkMatrix4x4()              
          vtkmat.SetElement(0,3,base[0])       
          vtkmat.SetElement(1,3,base[1])
          vtkmat.SetElement(2,3,base[2])       
          m_t.Multiply4x4(m_t,vtkmat,vtkmat)
          base[0] = vtkmat.GetElement(0,3)      
          base[1] = vtkmat.GetElement(1,3)
          base[2] = vtkmat.GetElement(2,3)
          vtkmat = vtk.vtkMatrix4x4()              
          vtkmat.SetElement(0,3,tip[0])       
          vtkmat.SetElement(1,3,tip[1]) 
          vtkmat.SetElement(2,3,tip[2])      
          m_t.Multiply4x4(m_t,vtkmat,vtkmat)
          tip[0] = vtkmat.GetElement(0,3)       
          tip[1] = vtkmat.GetElement(1,3)
          tip[2] = vtkmat.GetElement(2,3)

          phi1 = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[1]-base[1])**2)**0.5))
          theta1 = math.degrees(math.acos((tip[1]-base[1])/((tip[1]-base[1])**2+(tip[2]-base[2])**2)**0.5))
          psi1 = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[2]-base[2])**2)**0.5))
           

      m = vtk.vtkMatrix4x4()
      volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
      volumeNode.GetIJKToRASMatrix(m)
      m.Invert()
      imageData = volumeNode.GetImageData()
      indice=0
      
      # model and view for stats table
      self.keys = ("Label", "Intensity Average","Angle Deviation")
      self.view = qt.QTableView()
      self.view.setMinimumHeight(300)
      self.labelStats = {}
      self.labelStats['Labels'] = []
      self.view.sortingEnabled = True
      self.items = []
      self.model = qt.QStandardItemModel()
      self.view.setModel(self.model)
      self.view.verticalHeader().visible = False
      row = 0
      modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
      for modelNode in modelNodes.values():
        displayNode = modelNode.GetDisplayNode()
        if modelNode.GetAttribute("segmented") == "1" and displayNode.GetVisibility()==1:        
          polyData = modelNode.GetPolyData()
          polyData.Update()
          nb = polyData.GetNumberOfPoints()
          ijk=[0,0,0]
          ras=[0,0,0]
          total=0
          for i in range(nb):
            polyData.GetPoint(i,ras)
            k = vtk.vtkMatrix4x4()
            o = vtk.vtkMatrix4x4()
            k.SetElement(0,3,ras[0])
            k.SetElement(1,3,ras[1])
            k.SetElement(2,3,ras[2])
            k.Multiply4x4(m,k,o)
            ijk[0] = int(round(o.GetElement(0,3)))
            ijk[1] = int(round(o.GetElement(1,3)))
            ijk[2] = int(round(o.GetElement(2,3)))
            pixelValue = imageData.GetScalarComponentAsDouble(ijk[0], ijk[1], ijk[2], 0)
            total += pixelValue
          indice = total/(nb-1)

          polyData = modelNode.GetPolyData()
          polyData.Update()
          nb = polyData.GetNumberOfPoints()
          base = [0,0,0]
          tip = [0,0,0]
          polyData.GetPoint(nb-1,tip)
          polyData.GetPoint(0,base)
          phi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[1]*100-base[1]*100)**2)**0.5))
          theta = math.degrees(math.acos((tip[1]-base[1])/((tip[1]-base[1])**2+(tip[2]-base[2])**2)**0.5))
          psi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]-base[0])**2+(tip[2]-base[2])**2)**0.5))
          angleDeviation = (phi1-phi)**2+(theta1-theta)**2+(psi1-psi)**2
        
          # result = "Needle " + self.option[int(modelNode.GetAttribute("nth"))] + ": Angle Deviation from ref: " + str(angleDeviation)+" Intensity average :" + str(indice) 
          # analysisLine = qt.QLabel(result)
          # self.analysisGroupBoxLayout.addRow(analysisLine)
          
          self.labelStats["Labels"].append(int(modelNode.GetAttribute("nth")))
          self.labelStats[int(modelNode.GetAttribute("nth")),"Label"] = self.option[int(modelNode.GetAttribute("nth"))]
          self.labelStats[int(modelNode.GetAttribute("nth")),"Intensity Average"] = indice
          self.labelStats[int(modelNode.GetAttribute("nth")),"Angle Deviation"] = angleDeviation 
                
      for i in self.labelStats["Labels"]:
        color = qt.QColor()
        color.setRgb(self.color255[i][0],self.color255[i][1],self.color255[i][2])
        item = qt.QStandardItem()
        item.setData(color,1)
        self.model.setItem(row,0,item)
        self.items.append(item)
        col = 1
        for k in self.keys:
          item = qt.QStandardItem()
          item.setText(self.labelStats[i,k])
          self.model.setItem(row,col,item)
          self.items.append(item)
          col += 1
        row += 1

      self.view.setColumnWidth(0,30)
      self.model.setHeaderData(0,1," ")
      col = 1
      for k in self.keys:
        self.view.setColumnWidth(col,15*len(k))
        self.model.setHeaderData(col,1,k)
        col += 1    
      self.analysisGroupBoxLayout.addRow(self.view)
      
    else:
    
      m = vtk.vtkMatrix4x4()
      volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
      volumeNode.GetIJKToRASMatrix(m)
      m.Invert()
      imageData = volumeNode.GetImageData()
     
      # model and view for stats table
      self.keys = ("Label", "Intensity Average")
      self.view = qt.QTableView()
      self.view.setMinimumHeight(300)
      self.labelStats = {}
      self.labelStats['Labels'] = []
      self.view.sortingEnabled = True
      self.items = []
      self.model = qt.QStandardItemModel()
      self.view.setModel(self.model)
      self.view.verticalHeader().visible = False
      row = 0
      
      modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
      for modelNode in modelNodes.values():
        displayNode = modelNode.GetDisplayNode()
        if modelNode.GetAttribute("segmented") == "1" and displayNode.GetVisibility()==1:        
          polyData = modelNode.GetPolyData()
          polyData.Update()
          nb = polyData.GetNumberOfPoints()
          ijk=[0,0,0]
          ras=[0,0,0]
          total=0
          for i in range(nb):
            polyData.GetPoint(i,ras)
            k = vtk.vtkMatrix4x4()
            o = vtk.vtkMatrix4x4()
            k.SetElement(0,3,ras[0])
            k.SetElement(1,3,ras[1])
            k.SetElement(2,3,ras[2])
            k.Multiply4x4(m,k,o)
            ijk[0] = int(round(o.GetElement(0,3)))
            ijk[1] = int(round(o.GetElement(1,3)))
            ijk[2] = int(round(o.GetElement(2,3)))
            pixelValue = imageData.GetScalarComponentAsDouble(ijk[0], ijk[1], ijk[2], 0)
            total += pixelValue
        
          indice = total/(nb-1) 
          polyData = modelNode.GetPolyData()
          polyData.Update()
          nb = polyData.GetNumberOfPoints()
          base = [0,0,0]
          tip = [0,0,0]
          polyData.GetPoint(nb-1,tip)
          polyData.GetPoint(0,base)
          phi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[1]*100-base[1]*100)**2)**0.5))
          theta = math.degrees(math.acos((tip[1]-base[1])/((tip[1]-base[1])**2+(tip[2]-base[2])**2)**0.5))
          psi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]-base[0])**2+(tip[2]-base[2])**2)**0.5))
          # print tip[0]-base[0],tip[1]-base[1],tip[2]-base[2]
          
          # result = "Needle " + self.option[int(modelNode.GetAttribute("nth"))]  +" Intensity average :" + str(indice)
          # analysisLine = qt.QLabel(result)
          # self.analysisGroupBoxLayout.addRow(analysisLine)
          
          # add an entry to the LabelStats list
          self.labelStats["Labels"].append(int(modelNode.GetAttribute("nth")))
          self.labelStats[int(modelNode.GetAttribute("nth")),"Label"] = self.option[int(modelNode.GetAttribute("nth"))]
          self.labelStats[int(modelNode.GetAttribute("nth")),"Intensity Average"] = str(indice) 
      
      for i in self.labelStats["Labels"]:
        color = qt.QColor()
        color.setRgb(self.color255[i][0],self.color255[i][1],self.color255[i][2])
        item = qt.QStandardItem()
        item.setData(color,1)
        self.model.setItem(row,0,item)
        self.items.append(item)
        col = 1
        for k in self.keys:
          item = qt.QStandardItem()
          item.setText(self.labelStats[i,k])
          self.model.setItem(row,col,item)
          self.items.append(item)
          col += 1
        row += 1

      self.view.setColumnWidth(0,30)
      self.model.setHeaderData(0,1," ")
      col = 1
      for k in self.keys:
        self.view.setColumnWidth(col,15*len(k))
        self.model.setHeaderData(col,1,k)
        col += 1 
      
      self.analysisGroupBoxLayout.addRow(self.view)
      
  def angleDeviationEvaluation(self, modelNode):
    if self.transform !=None :
      # transformation matrix
      m = self.transform.GetMatrixTransformToParent()
      m_t = vtk.vtkMatrix4x4()
      m_t.DeepCopy(m)
      
      # data from a the first planned-needle found
      modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
      stop = 1
      for modelNode in modelNodes.values():
        if modelNode.GetAttribute("planned") == "1" and stop:
          stop = 0
          polyData = modelNode.GetPolyData()
          polyData.Update()
          nb = polyData.GetNumberOfPoints()
          base = [0,0,0]
          tip = [0,0,0]
          polyData.GetPoint(nb-1,tip)
          polyData.GetPoint(0,base)
          # evaluate the angle after the coordinate system transformation - used after as reference
          vtkmat = vtk.vtkMatrix4x4()              
          vtkmat.SetElement(0,3,base[0])       
          vtkmat.SetElement(1,3,base[1])
          vtkmat.SetElement(2,3,base[2])       
          m_t.Multiply4x4(m_t,vtkmat,vtkmat)
          base[0] = vtkmat.GetElement(0,3)      
          base[1] = vtkmat.GetElement(1,3)
          base[2] = vtkmat.GetElement(2,3)
          vtkmat = vtk.vtkMatrix4x4()              
          vtkmat.SetElement(0,3,tip[0])       
          vtkmat.SetElement(1,3,tip[1]) 
          vtkmat.SetElement(2,3,tip[2])      
          m_t.Multiply4x4(m_t,vtkmat,vtkmat)
          tip[0] = vtkmat.GetElement(0,3)       
          tip[1] = vtkmat.GetElement(1,3)
          tip[2] = vtkmat.GetElement(2,3)

          phi1 = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[1]-base[1])**2)**0.5))
          theta1 = math.degrees(math.acos((tip[1]-base[1])/((tip[1]-base[1])**2+(tip[2]-base[2])**2)**0.5))
          psi1 = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[2]-base[2])**2)**0.5))

      modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
      for modelNode in modelNodes.values():
        displayNode = modelNode.GetDisplayNode()
        if modelNode.GetAttribute("segmented") == "1" and displayNode.GetVisibility()==1:
          polyData = modelNode.GetPolyData()
          polyData.Update()
          nb = polyData.GetNumberOfPoints()
          base = [0,0,0]
          tip = [0,0,0]
          polyData.GetPoint(nb-1,tip)
          polyData.GetPoint(0,base)
          phi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[1]*100-base[1]*100)**2)**0.5))
          theta = math.degrees(math.acos((tip[1]-base[1])/((tip[1]-base[1])**2+(tip[2]-base[2])**2)**0.5))
          psi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]-base[0])**2+(tip[2]-base[2])**2)**0.5))
          self.angleDeviation = (phi1-phi)**2+(theta1-theta)**2+(psi1-psi)**2  
  
  def positionFilteringNeedles(self):
    # remove "duplicates"
    for i in xrange(63):
      if self.base[i] != [0,0,0]:
        for j in xrange(63):
          if j != i :
            distance = (self.base[i][0] - self.base[j][0])**2 + (self.base[i][1] - self.base[j][1])**2
            # print(i,j,distance)
            if distance < 25:
              iPolyData = self.needlenode[i][1].GetPolyData()
              iNb = int(iPolyData.GetNumberOfPoints()-1)
              iPolyData.GetPoint(iNb,self.tip[i])
              jPolyData = self.needlenode[j][1].GetPolyData()
              jNb = int(iPolyData.GetNumberOfPoints()-1)
              jPolyData.GetPoint(jNb,self.tip[j])
              
              if self.tip[i][2]>=self.tip[j][2]:
                self.displaynode[j].SetVisibility(0)
              else:
                self.displaynode[i].SetVisibility(0)
                self.displaynode[i].SliceIntersectionVisibilityOff()
                slicer.mrmlScene.RemoveNode(self.needlenode[i][1])
                slicer.mrmlScene.RemoveNode(self.bentNeedleNode[i][1])
                
    self.removeDuplicatesButton.setEnabled(0)
    self.removeDuplicatesButton.setChecked(1)

  def angleFilteringNeedles(self):
    
    # transformation matrix
    m = self.transform.GetMatrixTransformToParent()
    m_t = vtk.vtkMatrix4x4()
    m_t.DeepCopy(m)
    
    # data from a the first planned-needle found
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    stop = 1
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("planned") == "1" and stop:
        stop = 0
        polyData = modelNode.GetPolyData()
        polyData.Update()
        nb = polyData.GetNumberOfPoints()
        base = [0,0,0]
        tip = [0,0,0]
        polyData.GetPoint(nb-1,tip)
        polyData.GetPoint(0,base)
        # evaluate the angle after the coordinate system transformation - used after as reference
        vtkmat = vtk.vtkMatrix4x4()              
        vtkmat.SetElement(0,3,base[0])       
        vtkmat.SetElement(1,3,base[1])
        vtkmat.SetElement(2,3,base[2])       
        m_t.Multiply4x4(m_t,vtkmat,vtkmat)
        base[0] = vtkmat.GetElement(0,3)      
        base[1] = vtkmat.GetElement(1,3)
        base[2] = vtkmat.GetElement(2,3)
        vtkmat = vtk.vtkMatrix4x4()              
        vtkmat.SetElement(0,3,tip[0])       
        vtkmat.SetElement(1,3,tip[1]) 
        vtkmat.SetElement(2,3,tip[2])      
        m_t.Multiply4x4(m_t,vtkmat,vtkmat)
        tip[0] = vtkmat.GetElement(0,3)       
        tip[1] = vtkmat.GetElement(1,3)
        tip[2] = vtkmat.GetElement(2,3)

        phi1 = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[1]-base[1])**2)**0.5))
        theta1 = math.degrees(math.acos((tip[1]-base[1])/((tip[1]-base[1])**2+(tip[2]-base[2])**2)**0.5))
        psi1 = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[2]-base[2])**2)**0.5))
    
    # data from segmented-needles and angle evaluation
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      displayNode = modelNode.GetDisplayNode()
      if modelNode.GetAttribute("segmented") == "1":
        polyData = modelNode.GetPolyData()
        polyData.Update()
        nb = polyData.GetNumberOfPoints()
        base = [0,0,0]
        tip = [0,0,0]
        polyData.GetPoint(nb-1,tip)
        polyData.GetPoint(0,base)
        phi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[1]*100-base[1]*100)**2)**0.5))
        theta = math.degrees(math.acos((tip[1]-base[1])/((tip[1]-base[1])**2+(tip[2]-base[2])**2)**0.5))
        psi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]-base[0])**2+(tip[2]-base[2])**2)**0.5))
        angleDeviation = (phi1-phi)**2+(theta1-theta)**2+(psi1-psi)**2
        print("diff angle:",angleDeviation)
        
        
        displayNode = modelNode.GetDisplayNode()
        i = modelNode.GetAttribute("nth")
        if angleDeviation >= self.filterValueButton.value :
          displayNode.SetVisibility(0)
          if i !=None and self.fiducialnode[int(i)]!=0:
            self.fiducialnode[int(i)].SetDisplayVisibility(0)
        else:
          displayNode.SetVisibility(1)
          if i !=None and self.fiducialnode[int(i)]!=0:
            self.fiducialnode[int(i)].SetDisplayVisibility(1)
      
      # display/hide label+needle
      nVisibility = displayNode.GetVisibility()
      
      if nVisibility == 1:
        displayNode.SliceIntersectionVisibilityOn()
      else:
        displayNode.SliceIntersectionVisibilityOff()
    
    self.addButtons()
                
  def needleSegmentation(self):
    scene = slicer.mrmlScene
    pNode = self.parameterNode()
    if Helper.getNodeByID(pNode.GetParameter("baselineVolumeID")) == None:
      inputVolume = self.__volumeSelector.currentNode()
      inputVolumeID = self.__volumeSelector.currentNode().GetID()
    else:
      inputVolume = Helper.getNodeByID(pNode.GetParameter("baselineVolumeID"))
      inputVolumeID = Helper.getNodeByID(pNode.GetParameter("baselineVolumeID")).GetID()
    inputLabelID = self.__needleLabelSelector.currentNode().GetID()
    
    datetime = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
    
    inputVolume.SetAttribute("foldername",datetime)
    self.outputVolumeNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelNode')
    self.outputVolumeNode.SetName("Output Needle Model")
    outputVolumeStorageNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelStorageNode')
    slicer.mrmlScene.AddNode(self.outputVolumeNode)
    slicer.mrmlScene.AddNode(outputVolumeStorageNode)
    self.outputVolumeNode.AddAndObserveStorageNodeID(outputVolumeStorageNode.GetID())
    outputVolumeStorageNode.WriteData(self.outputVolumeNode)
    
    outputID = self.outputVolumeNode.GetID()
    
    self.foldername = '/NeedleModels/' + datetime
    
    # Set the parameters for the CLI module    
    parameters = {} 
    parameters['inputVolume'] = inputVolumeID
    parameters['inputLabel'] = inputLabelID
    parameters['outputVtk'] = outputID
    parameters['outputFolderName'] = self.foldername
    parameters['nbPointsPerLine'] = self.nbPointsPerLine.value
    parameters['nbRadiusIterations'] = self.nbRadiusIterations.value
    parameters['distanceMax'] = self.distanceMax.value
    parameters['numberOfPointsPerNeedle'] = self.numberOfPointsPerNeedle.value
    parameters['nbRotatingIterations'] = self.nbRotatingIterations.value
    
    module = slicer.modules.mainlabelneedletrackingcli 
    self.__cliNode = None
    self.__cliNode = slicer.cli.run(module, None, parameters, wait_for_completion=True)
        
    
    ##### match the needles ######

    self.colorLabel()
    self.setNeedleCoordinates()
    self.computerPolydataAndMatrix()
    xmin = min(self.p[0])
    xmax = max(self.p[0])
    ymin = min(self.p[1])
    ymax = max(self.p[1])
    xdelta= xmax - xmin
    ydelta = ymax - ymin
    self.base = [[0 for j in range(3)] for j in range(63)]
    self.tip = [[0 for j in range(3)] for j in range(63)]
    self.needlenode = [[0 for j in range(2)] for j in range(63)]
    self.bentNeedleNode = [[0 for j in range(2)] for j in range(63)]
    # self.contourNode = [[0 for j in range(2)] for j in range(63)]
    self.displaynode = [0 for j in range(63)]
    self.displaynodeB = [0 for j in range(63)]
    # self.displayContourNode = [0 for j in range(63)]
    self.fiducialnode = [0 for j in range(63)]
    k=0
    for i in xrange(63):

      pathneedle = self.foldername+'/'+str(i)+'.vtp'
      pathBentNeedle =  self.foldername+'/'+str(i)+'_bent.vtp'
      self.needlenode[i] = slicer.util.loadModel(pathneedle, True)
      self.bentNeedleNode[i] = slicer.util.loadModel(pathBentNeedle, True)


      if self.needlenode[i][0] == True and self.needlenode[i][1] != None:
        self.displaynode[i] = self.needlenode[i][1].GetDisplayNode()
        self.displaynodeB[i] = self.bentNeedleNode[i][1].GetDisplayNode()

         
        polydata = self.needlenode[i][1].GetPolyData()
        polydata.GetPoint(0,self.base[i])        
      
        self.displaynode[i].SliceIntersectionVisibilityOn()
        self.displaynodeB[i].SliceIntersectionVisibilityOn()
        bestmatch = None
        mindist = None
        for j in xrange(63):
          delta = ((self.p[0][j]-(self.base[i][0]))**2+(self.p[1][j]-self.base[i][1])**2)**(0.5)
          if delta < mindist or mindist == None:
            bestmatch = j
            mindist = delta
        if self.transform ==None :
          bestmatch = k
          k +=1
        self.displaynode[i].SetColor(self.color[bestmatch])
        self.displaynodeB[i].SetColor(self.color[bestmatch])
        self.needlenode[i][1].SetName(self.option[bestmatch]+"_segmented")
        self.bentNeedleNode[i][1].SetName(self.option[bestmatch]+"_optimized")
        self.needlenode[i][1].SetAttribute("segmented","1")
        self.bentNeedleNode[i][1].SetAttribute("optimized","1")
        self.needlenode[i][1].SetAttribute("nth",str(bestmatch))
        self.bentNeedleNode[i][1].SetAttribute("nth",str(bestmatch))
        self.needlenode[i][1].SetAttribute("needleID",self.needlenode[i][1].GetID())
        self.bentNeedleNode[i][1].SetAttribute("needleID",self.bentNeedleNode[i][1].GetID())
 
        
    
    if self.removeDuplicates.isChecked():
      self.positionFilteringNeedles()

    d = slicer.mrmlScene.GetNodeByID(outputID).GetDisplayNode()
    d.SetVisibility(0)
    
    self.__editorFrame.collapsed = 1
    
    self.addButtons()
  
  def addButtons(self):
    if self.buttonsGroupBox != None:
      self.__layout.removeWidget(self.buttonsGroupBox)
      self.buttonsGroupBox.deleteLater()
      self.buttonsGroupBox = None
    self.buttonsGroupBox = qt.QGroupBox()
    self.buttonsGroupBox.setTitle( 'Manage Needles' )
    self.__layout.addRow( self.buttonsGroupBox )
    self.buttonsGroupBoxLayout = qt.QFormLayout( self.buttonsGroupBox )
    
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("segmented") == "1":
        i = int(modelNode.GetAttribute("nth"))
        buttonDisplay = qt.QPushButton("Hide "+self.option[i])
        buttonBentDisplay = qt.QPushButton("Hide Bent "+self.option[i])
        # buttonDisplayContour = qt.QPushButton("Distance "+self.option[i])
        buttonDisplay.checkable = True
        buttonBentDisplay.checkable = True
        # buttonDisplayContour.checkable = True
        if modelNode.GetDisplayVisibility() ==0:
          buttonDisplay.setChecked(1)
          # buttonDisplayContour.setChecked(1)
        buttonDisplay.connect("clicked()", lambda who=i: self.displayNeedle(who))
        buttonBentDisplay.connect("clicked()", lambda who=i: self.displayBentNeedle(who))
        # buttonDisplayContour.connect("clicked()", functools.partial(self.displayContour,i,buttonDisplayContour.checked))
        buttonReformat = qt.QPushButton("Reformat "+self.option[i])
        buttonReformat.connect("clicked()", lambda who=i: self.reformatNeedle(who))
        widget = qt.QWidget()
        hlay = qt.QHBoxLayout(widget)
        hlay.addWidget(buttonDisplay)
        hlay.addWidget(buttonBentDisplay)
        # hlay.addWidget(buttonDisplayContour)
        hlay.addWidget(buttonReformat)
        self.buttonsGroupBoxLayout.addRow(widget)
  
  def displayBentNeedle(self,i):
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("nth")==str(i) and modelNode.GetAttribute("optimized")=='1' :
        displayNode = modelNode.GetModelDisplayNode()
        nVisibility = displayNode.GetVisibility()
        # print nVisibility
        if nVisibility:
          displayNode.SliceIntersectionVisibilityOff()
          displayNode.SetVisibility(0)
        else:
          displayNode.SliceIntersectionVisibilityOn()
          displayNode.SetVisibility(1)
  
  def displayNeedle(self,i):
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("nth")==str(i) and modelNode.GetAttribute("segmented")=='1' :
        displayNode = modelNode.GetModelDisplayNode()
        nVisibility = displayNode.GetVisibility()
        # print nVisibility
        if nVisibility:
          displayNode.SliceIntersectionVisibilityOff()
          displayNode.SetVisibility(0)
        else:
          displayNode.SliceIntersectionVisibilityOn()
          displayNode.SetVisibility(1)
          
          # if self.displayRadSegmentedButton.checked == 0:
            # for radNode in modelNodes.values():
              # if radNode.GetName()=='Rad'+self.option[i]+'.vtk':
                # radNode.SetDisplayVisibility(1)
          
          # if self.displayContourButton.checked == 0:
            # for radNode in modelNodes.values():
              # if radNode.GetName()==self.option[i]+'_segmented_contour':
                # radNode.SetDisplayVisibility(1)
                  
    # modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    # for modelNode in modelNodes.values():
      # if modelNode.GetAttribute("radiation") == "segmented":
        # needleNode = slicer.mrmlScene.GetNodeByID(modelNode.GetAttribute("needleID"))
        # if needleNode.GetDisplayVisibility()==0:
          # modelNode.SetDisplayVisibility(0)
    # modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    # for modelNode in modelNodes.values():
      # if modelNode.GetAttribute("contour") == "1":
        # needleNode = slicer.mrmlScene.GetNodeByID(modelNode.GetAttribute("needleID"))
        # if needleNode.GetDisplayVisibility()==0:
          # modelNode.SetDisplayVisibility(0)
          
  def displayNeedleID(self,ID):
    modelNode = slicer.util.getNode('vtkMRMLModelNode'+str(ID))
    displayNode = modelNode.GetModelDisplayNode()
    nVisibility = displayNode.GetVisibility()
    # print nVisibility
    if nVisibility:
      displayNode.SliceIntersectionVisibilityOff()
      displayNode.SetVisibility(0)
    else:
      displayNode.SliceIntersectionVisibilityOn()
      displayNode.SetVisibility(1)

  def reformatNeedleID(self,ID):
    for i in range(2):  
      modelNode = slicer.util.getNode('vtkMRMLModelNode'+str(ID))
      polyData = modelNode.GetPolyData()
      nb = polyData.GetNumberOfPoints()
      base = [0,0,0]
      tip = [0,0,0]
      polyData.GetPoint(nb-1,tip)
      polyData.GetPoint(0,base)
      a,b,c = tip[0]-base[0],tip[1]-base[1],tip[2]-base[2]
      
      sYellow = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
      if sYellow ==None :
        sYellow = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNode2")        
      reformatLogic = slicer.vtkSlicerReformatLogic()
      sYellow.SetSliceVisible(1)
      reformatLogic.SetSliceNormal(sYellow,1,-a/b,0)
      m= sYellow.GetSliceToRAS()
      m.SetElement(0,3,base[0])
      m.SetElement(1,3,base[1])
      m.SetElement(2,3,base[2])
      sYellow.Modified()

  def reformatNeedle(self,i):
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for i in range(2):  # bug from slicer? need to do it 2 times
      for modelNode in modelNodes.values():
        if modelNode.GetAttribute("nth")==str(i):
          polyData = modelNode.GetPolyData()
          nb = polyData.GetNumberOfPoints()
          base = [0,0,0]
          tip = [0,0,0]
          polyData.GetPoint(nb-1,tip)
          polyData.GetPoint(0,base)
          phi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]*-base[0])**2+(tip[1]*100-base[1]*100)**2)**0.5))
          theta = math.degrees(math.acos((tip[1]-base[1])/((tip[1]-base[1])**2+(tip[2]-base[2])**2)**0.5))
          psi = math.degrees(math.acos((tip[0]-base[0])/((tip[0]-base[0])**2+(tip[2]-base[2])**2)**0.5))
          print base[0],tip[0],base[1],tip[1],base[2],tip[2]
          a,b,c = tip[0]-base[0],tip[1]-base[1],tip[2]-base[2]
          print '---------'
          
          sYellow = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
          if sYellow ==None :
            sYellow = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNode2")        
          reformatLogic = slicer.vtkSlicerReformatLogic()
          sYellow.SetSliceVisible(1)
          reformatLogic.SetSliceNormal(sYellow,1,-a/b,0)
          m= sYellow.GetSliceToRAS()
          m.SetElement(0,3,base[0])
          m.SetElement(1,3,base[1])
          m.SetElement(2,3,base[2])
          sYellow.Modified()
 
  def displayFiducial(self):
    
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      displayNode = modelNode.GetDisplayNode()
      if modelNode.GetAttribute("segmented") == "1" and modelNode.GetAttribute("nth")!=None:
        # if self.transform != None:
        if 1:
          i = int(modelNode.GetAttribute("nth"))
          if self.fiducialnode[i] == 0:    
            polyData = modelNode.GetPolyData()
            nb = int(polyData.GetNumberOfPoints()-1)
            coord = [0,0,0]
            if nb>10:
              self.fiducialnode[i] = slicer.vtkMRMLAnnotationFiducialNode()
              polyData.GetPoint(nb,coord)    
              self.fiducialnode[i].SetName(self.option[i])
              self.fiducialnode[i].SetFiducialCoordinates(coord)         
              self.fiducialnode[i].Initialize(slicer.mrmlScene)
              self.fiducialnode[i].SetLocked(1)
              self.fiducialnode[i].SetSelectable(0)
              fidDN = self.fiducialnode[i].GetDisplayNode()
              fidDN.SetColor(modelNode.GetDisplayNode().GetColor())
              fidDN.SetGlyphScale(0)
              fidTN = self.fiducialnode[i].GetAnnotationTextDisplayNode()
              fidTN.SetTextScale(3)
              fidTN.SetColor(modelNode.GetDisplayNode().GetColor())
              
              self.fiducialnode[i].SetDisplayVisibility(modelNode.GetDisplayNode().GetVisibility())
          else:    
            if modelNode.GetDisplayNode().GetVisibility():
               self.fiducialnode[i].SetDisplayVisibility(abs(self.fiducialnode[i].GetDisplayVisibility()-1))
            if self.fiducialnode[i].GetDisplayVisibility()==1:
              self.displayFiducialButton.text = "Hide Labels on Needles"
            else:
              self.displayFiducialButton.text = "Display Labels on Needles"
             
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
    pNode = self.parameterNode()
    self.colorLabel()
    if pNode.GetParameter('skip') != '1':
      self.updateWidgetFromParameters(pNode)
      Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')
      obturator = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('obturatorID'))
      template = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('templateID'))
      dObturator = obturator.GetDisplayNode()
      dObturator.SetVisibility(0)
      dTemplate = template.GetDisplayNode()
      dTemplate.SetVisibility(0)
      self.colorLabel()

    pNode.SetParameter('skip','0')  
    pNode.SetParameter('currentStep', self.stepid)
      
  def updateWidgetFromParameters(self, pNode):
  
    self.baselineVolume = Helper.getNodeByID(pNode.GetParameter('baselineVolumeID'))
    transformNodeID = pNode.GetParameter('followupTransformID')
    self.transform = Helper.getNodeByID(transformNodeID)
    
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
    pNode = self.parameterNode()
    transformNodeID = pNode.GetParameter('followupTransformID')
    transformNode = Helper.getNodeByID(transformNodeID)
    if transformNode != None:
      transformMatrix = transformNode.GetMatrixTransformToParent()
      for i in xrange(63):
        vtkmat = vtk.vtkMatrix4x4()
        vtkmatOut = vtk.vtkMatrix4x4()
        vtkmat.SetElement(0,3,self.p[0][i])
        vtkmat.SetElement(1,3,self.p[1][i])

        vtkmat.Multiply4x4(transformMatrix,vtkmat,vtkmatOut)

        self.p[0][i] = vtkmatOut.GetElement(0,3)
        self.p[1][i] = vtkmatOut.GetElement(1,3)
                 
  def findLabelNeedleID(self,ID):
    volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
    imageData = volumeNode.GetImageData()
    imageDimensions = imageData.GetDimensions()
    m = vtk.vtkMatrix4x4()
    minZ=None
    mindist=None
    volumeNode.GetIJKToRASMatrix(m)
    Z = m.GetElement(2,3)
    needleNode = slicer.mrmlScene.GetNodeByID(ID)
    polydata = needleNode.GetPolyData()
    nb = polydata.GetNumberOfPoints()
    for i in range(nb):
      if 20*i<nb:
        pt=[0,0,0]
        polydata.GetPoint(20*i,pt)
        if (pt[2]-Z)**2<minZ or minZ == None:
          minZ = (pt[2]-Z)**2
          bestNB = 20*i
    self.setNeedleCoordinates()
    print bestNB
    A=[0,0,0]
    polydata.GetPoint(bestNB,A)
    for j in xrange(63):
      delta = ((self.p[0][j]-(A[0]))**2+(self.p[1][j]-A[1])**2)**(0.5)
      if delta < mindist or mindist == None:
        bestmatch = j
        mindist = delta
        
    result = [bestmatch,mindist]
    return result

  def colorLabel(self):
    self.color= [[0,0,0] for i in range(310)]
    self.color255= [[0,0,0] for i in range(310)]    
    self.color[0]=[221,108,158]
    self.color[1]=[128,174,128]
    self.color[2]=[241,214,145]
    self.color[3]=[177,122,101]
    self.color[4]=[111,184,210]
    self.color[5]=[216,101,79]
    self.color[6]=[221,130,101]
    self.color[7]=[144,238,144]
    self.color[8]=[192,104,88]
    self.color[9]=[220,245,20]
    self.color[10]=[78,63,0]
    self.color[11]=[255,250,220]
    self.color[12]=[230,220,70]
    self.color[13]=[200,200,235]
    self.color[14]=[250,250,210]
    self.color[15]=[244,214,49]
    self.color[16]=[0,151,206]
    self.color[17]=[183,156,220]
    self.color[18]=[183,214,211]
    self.color[19]=[152,189,207]
    self.color[20]=[178,212,242]
    self.color[21]=[68,172,100]
    self.color[22]=[111,197,131]
    self.color[23]=[85,188,255]
    self.color[24]=[0,145,30]
    self.color[25]=[214,230,130]
    self.color[26]=[218,255,255]
    self.color[27]=[170,250,250]
    self.color[28]=[140,224,228]
    self.color[29]=[188,65,28]
    self.color[30]=[216,191,216]
    self.color[31]=[145,60,66]
    self.color[32]=[150,98,83]
    self.color[33]=[250,250,225]
    self.color[34]=[200,200,215]
    self.color[35]=[68,131,98]
    self.color[36]=[83,146,164]
    self.color[37]=[162,115,105]
    self.color[38]=[141,93,137]
    self.color[39]=[182,166,110]
    self.color[40]=[188,135,166]
    self.color[41]=[154,150,201]
    self.color[42]=[177,140,190]
    self.color[43]=[30,111,85]
    self.color[44]=[210,157,166]
    self.color[45]=[48,129,126]
    self.color[46]=[98,153,112]
    self.color[47]=[69,110,53]
    self.color[48]=[166,113,137]
    self.color[49]=[122,101,38]
    self.color[50]=[253,135,192]
    self.color[51]=[145,92,109]
    self.color[52]=[46,101,131]
    self.color[53]=[0,108,112]
    self.color[54]=[127,150,88]
    self.color[55]=[159,116,163]
    self.color[56]=[125,102,154]
    self.color[57]=[106,174,155]
    self.color[58]=[154,146,83]
    self.color[59]=[126,126,55]
    self.color[60]=[201,160,133]
    self.color[61]=[78,152,141]
    self.color[62]=[174,140,103]
    self.color[63]=[139,126,177]
    self.color[64]=[148,120,72]
    self.color[65]=[186,135,135]
    self.color[66]=[99,106,24]
    self.color[67]=[156,171,108]
    self.color[68]=[64,123,147]
    self.color[69]=[138,95,74]
    self.color[70]=[97,113,158]
    self.color[71]=[126,161,197]
    self.color[72]=[194,195,164]
    self.color[73]=[88,106,215]
    self.color[74]=[82,174,128]
    self.color[75]=[57,157,110]
    self.color[76]=[60,143,83]
    self.color[77]=[92,162,109]
    self.color[78]=[255,244,209]
    self.color[79]=[201,121,77]
    self.color[80]=[70,163,117]
    self.color[81]=[188,91,95]
    self.color[82]=[166,84,94]
    self.color[83]=[182,105,107]
    self.color[84]=[229,147,118]
    self.color[85]=[174,122,90]
    self.color[86]=[201,112,73]
    self.color[87]=[194,142,0]
    self.color[88]=[241,213,144]
    self.color[89]=[203,179,77]
    self.color[90]=[229,204,109]
    self.color[91]=[255,243,152]
    self.color[92]=[209,185,85]
    self.color[93]=[248,223,131]
    self.color[94]=[255,230,138]
    self.color[95]=[196,172,68]
    self.color[96]=[255,255,167]
    self.color[97]=[255,250,160]
    self.color[98]=[255,237,145]
    self.color[99]=[242,217,123]
    self.color[100]=[222,198,101]
    self.color[101]=[213,124,109]
    self.color[102]=[184,105,108]
    self.color[103]=[150,208,243]
    self.color[104]=[62,162,114]
    self.color[105]=[242,206,142]
    self.color[106]=[250,210,139]
    self.color[107]=[255,255,207]
    self.color[108]=[182,228,255]
    self.color[109]=[175,216,244]
    self.color[110]=[197,165,145]
    self.color[111]=[172,138,115]
    self.color[112]=[202,164,140]
    self.color[113]=[224,186,162]
    self.color[114]=[255,245,217]
    self.color[115]=[206,110,84]
    self.color[116]=[210,115,89]
    self.color[117]=[203,108,81]
    self.color[118]=[233,138,112]
    self.color[119]=[195,100,73]
    self.color[120]=[181,85,57]
    self.color[121]=[152,55,13]
    self.color[122]=[159,63,27]
    self.color[123]=[166,70,38]
    self.color[124]=[218,123,97]
    self.color[125]=[225,130,104]
    self.color[126]=[224,97,76]
    self.color[127]=[184,122,154]
    self.color[128]=[211,171,143]
    self.color[129]=[47,150,103]
    self.color[130]=[173,121,88]
    self.color[131]=[188,95,76]
    self.color[132]=[255,239,172]
    self.color[133]=[226,202,134]
    self.color[134]=[253,232,158]
    self.color[135]=[244,217,154]
    self.color[136]=[205,179,108]
    self.color[137]=[186,124,161]
    self.color[138]=[255,255,220]
    self.color[139]=[234,234,194]
    self.color[140]=[204,142,178]
    self.color[141]=[180,119,153]
    self.color[142]=[216,132,105]
    self.color[143]=[255,253,229]
    self.color[144]=[205,167,142]
    self.color[145]=[204,168,143]
    self.color[146]=[255,224,199]
    self.color[147]=[139,150,98]
    self.color[148]=[249,180,111]
    self.color[149]=[157,108,162]
    self.color[150]=[203,136,116]
    self.color[151]=[185,102,83]
    self.color[152]=[247,182,164]
    self.color[153]=[222,154,132]
    self.color[154]=[124,186,223]
    self.color[155]=[249,186,150]
    self.color[156]=[244,170,147]
    self.color[157]=[255,181,158]
    self.color[158]=[255,190,165]
    self.color[159]=[227,153,130]
    self.color[160]=[213,141,113]
    self.color[161]=[193,123,103]
    self.color[162]=[216,146,127]
    self.color[163]=[230,158,140]
    self.color[164]=[245,172,147]
    self.color[165]=[241,172,151]
    self.color[166]=[177,124,92]
    self.color[167]=[171,85,68]
    self.color[168]=[217,198,131]
    self.color[169]=[212,188,102]
    self.color[170]=[185,135,134]
    self.color[171]=[198,175,125]
    self.color[172]=[194,98,79]
    self.color[173]=[255,238,170]
    self.color[174]=[206,111,93]
    self.color[175]=[216,186,0]
    self.color[176]=[255,226,77]
    self.color[177]=[255,243,106]
    self.color[178]=[255,234,92]
    self.color[179]=[240,210,35]
    self.color[180]=[224,194,0]
    self.color[181]=[213,99,79]
    self.color[182]=[217,102,81]
    self.color[183]=[0,147,202]
    self.color[184]=[0,122,171]
    self.color[185]=[186,77,64]
    self.color[186]=[240,255,30]
    self.color[187]=[185,232,61]
    self.color[188]=[0,226,255]
    self.color[189]=[251,159,255]
    self.color[190]=[230,169,29]
    self.color[191]=[0,194,113]
    self.color[192]=[104,160,249]
    self.color[193]=[221,108,158]
    self.color[194]=[137,142,0]
    self.color[195]=[230,70,0]
    self.color[196]=[0,147,0]
    self.color[197]=[0,147,248]
    self.color[198]=[231,0,206]
    self.color[199]=[129,78,0]
    self.color[200]=[0,116,0]
    self.color[201]=[0,0,255]
    self.color[202]=[157,0,0]
    self.color[203]=[100,100,130]
    self.color[204]=[205,205,100]
    for i in range(310):
      for j in range(3):
        self.color255[i][j] = self.color[i][j]
        self.color[i][j] = self.color[i][j]/(255)

  def computerPolydataAndMatrix(self):

    Cylinder = vtk.vtkCylinderSource()

    Cylinder.SetResolution(1000)
    Cylinder.SetCapping(1) 
    Cylinder.SetHeight( float(200.0) )
    Cylinder.SetRadius( float(1.0) )
    self.m_polyCylinder=Cylinder.GetOutput()
    
    quad = vtk.vtkQuadric()
    quad.SetCoefficients(1,1,1,0,0,0,0,1,0,0)
    sample = vtk.vtkSampleFunction()
    sample.SetModelBounds(-30,30,-60,60,-30,30)
    sample.SetCapping(0)
    sample.SetComputeNormals(1)
    sample.SetSampleDimensions(50,50,50)
    sample.SetImplicitFunction(quad)
    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(sample.GetOutputPort())
    contour.ComputeNormalsOn()
    contour.ComputeScalarsOn()
    contour.GenerateValues(4,0,100)
    self.m_polyRadiation = contour.GetOutput()

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
    
  def showOneNeedle(self,i,visibility):
    fidname = "fid"+self.option[i]
    pNode = self.parameterNode()
    needleID = pNode.GetParameter(self.option[i]+'.vtp')
    fidID = pNode.GetParameter(fidname)    
    NeedleNode = slicer.mrmlScene.GetNodeByID(needleID)
    fiducialNode = slicer.mrmlScene.GetNodeByID(fidID)    
    
    if NeedleNode !=None:
      displayNode =NeedleNode.GetModelDisplayNode()
      nVisibility=displayNode.GetVisibility()  

      if fiducialNode == None:
        displayNode.SetVisibility(1)    
        displayNode.SetOpacity(0.9)
        polyData = NeedleNode.GetPolyData()
        polyData.Update()
        nb = int(polyData.GetNumberOfPoints()-1)
        coord = [0,0,0]
        if nb>100:
          fiducialNode = slicer.vtkMRMLAnnotationFiducialNode()
          polyData.GetPoint(nb,coord)    
          fiducialNode.SetName(self.option[i])
          fiducialNode.SetFiducialCoordinates(coord)         
          if self.transform != None:
            fiducialNode.SetAndObserveTransformNodeID(self.transform.GetID())
          fiducialNode.Initialize(slicer.mrmlScene)
          fiducialNode.SetLocked(1)
          fiducialNode.SetSelectable(0)
          fidDN = fiducialNode.GetDisplayNode()
          fidDN.SetColor(NeedleNode.GetDisplayNode().GetColor())
          fidDN.SetGlyphScale(0)
          fidTN = fiducialNode.GetAnnotationTextDisplayNode()
          fidTN.SetTextScale(3)
          fidTN.SetColor(NeedleNode.GetDisplayNode().GetColor())
          fiducialNode.SetDisplayVisibility(0)
          pNode.SetParameter(fidname,fiducialNode.GetID())
          fiducialNode.SetDisplayVisibility(1)

      if visibility ==0:

        displayNode.SetVisibility(0)
        displayNode.SetSliceIntersectionVisibility(0)
        if fiducialNode!=None:
          fiducialNode.SetDisplayVisibility(0)

      else:

        displayNode.SetVisibility(1)
        displayNode.SetSliceIntersectionVisibility(1)
        if fiducialNode!=None:
          fiducialNode.SetDisplayVisibility(1)

    else:
      vtkmat = vtk.vtkMatrix4x4()
      vtkmat.DeepCopy(self.m_vtkmat)
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
      self.AddModel(i,triangles.GetOutput())
      self.showOneNeedle(i,visibility)
      
  def loadNeedles(self):
    pNode = self.parameterNode()
    alreadyloaded = pNode.GetParameter("Needles-loaded")
    obturatorID = pNode.GetParameter('obturatorID')    
    ObutratorNode = slicer.mrmlScene.GetNodeByID(obturatorID)

    if ObutratorNode!=None:
      print("obturator loaded")
      self.setNeedleCoordinates()
      self.computerPolydataAndMatrix()    
      
      self.m_poly = vtk.vtkPolyData()  
      self.m_poly.DeepCopy(ObutratorNode.GetPolyData())
            
  def AddModel(self,i,polyData):
    modelNode = slicer.vtkMRMLModelNode()
    displayNode = slicer.vtkMRMLModelDisplayNode()
    storageNode = slicer.vtkMRMLModelStorageNode()
 
    fileName = self.option[i]+'.vtp'
    print("filename:",fileName)

    mrmlScene = slicer.mrmlScene
    modelNode.SetName(fileName)  
    modelNode.SetAndObservePolyData(polyData)
    modelNode.SetAttribute("planned","1")
    
    mrmlScene.SaveStateForUndo()
    modelNode.SetScene(mrmlScene)
    storageNode.SetScene(mrmlScene)
    storageNode.SetFileName(fileName)  
    displayNode.SetScene(mrmlScene)
    displayNode.SetVisibility(1)
    mrmlScene.AddNode(storageNode)
    mrmlScene.AddNode(displayNode)
    mrmlScene.AddNode(modelNode)
    modelNode.SetAndObserveStorageNodeID(storageNode.GetID())
    modelNode.SetAndObserveDisplayNodeID(displayNode.GetID())
    if self.transform != None:
      modelNode.SetAndObserveTransformNodeID(self.transform.GetID())
    displayNode.SetColor(self.color[i])
    displayNode.SetSliceIntersectionVisibility(0)
    pNode= self.parameterNode()
    pNode.SetParameter(fileName,modelNode.GetID())
    mrmlScene.AddNode(modelNode)
    displayNode.SetVisibility(1)
  
  def AddContour(self,polyData):
    # print polyData
    scene = slicer.mrmlScene
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    contourNode = None
    contourNode = slicer.util.getNode('Contours')
    if contourNode != None:
      slicer.mrmlScene.RemoveNode(contourNode.GetStorageNode())
      contourNode.RemoveAllDisplayNodeIDs()
      slicer.mrmlScene.RemoveNode(contourNode)        
  
    modelNode = slicer.vtkMRMLModelNode()
    modelNode.SetScene(scene)
    modelNode.SetAndObservePolyData(polyData)
    # display node
    displayNode = slicer.vtkMRMLModelDisplayNode()
 
    modelNode.SetName('Contours')  
    
    scene.AddNode(displayNode)
    scene.AddNode(modelNode)
     
    displayNode.SetVisibility(1)
    displayNode.SetOpacity(0.06)
    displayNode.SetSliceIntersectionVisibility(1)
    displayNode.SetScalarVisibility(1)
    displayNode.SetActiveScalarName('ImageScalars') 
    displayNode.SetAndObserveColorNodeID('vtkMRMLColorTableNodeFileHotToColdRainbow2.txt')
    displayNode.SetScalarRange(10,40)
    displayNode.SetBackfaceCulling(0)
    displayNode.SetScene(scene)
    scene.AddNode(displayNode)
    modelNode.SetAndObserveDisplayNodeID(displayNode.GetID())
    # add to scene
    displayNode.SetInputPolyData(modelNode.GetPolyData())
    scene.AddNode(modelNode)

    pNode= self.parameterNode()
    pNode.SetParameter('Contours',modelNode.GetID())

    qt.QApplication.processEvents()
	
    # if int(slicer.app.repositoryRevision)>= 20973:
    #   parameters = {}
    #   parameters['nodeID'] = modelNode.GetID()
    #   parameters['fileName'] = self.foldername+'/Isocontours.vtp'
    #   slicer.app.coreIOManager().saveNodes('modelFile', parameters)
    # else:
    #   storageNode = slicer.vtkMRMLModelStorageNode()
    #   storageNode.SetScene(mrmlScene)
    #   mrmlScene.AddNode(storageNode)
    #   storageNode.SetFileName(self.foldername+'/Isocontours.vtp')
    #   modelNode.SetAndObserveStorageNodeID(storageNode.GetID())
    #   storageNode.WriteData(modelNode)
	
    # slicer.mrmlScene.RemoveNode(storageNode)
    # modelNode.SetDisplayVisibility(0)
    # slicer.mrmlScene.RemoveNode(modelNode)
	
    # contourModel = slicer.util.loadModel(self.foldername+'/Isocontours.vtp', True)
    # if contourModel[0] == True and contourModel[1] != None:
    #   contourModel[1].SetAttribute("isocontours","1")
    #   displayNode = contourModel[1].GetDisplayNode()
    #   displayNode.SetVisibility(1)
    #   displayNode.SetSliceIntersectionVisibility(1)
    #   displayNode.SetPolyData(modelNode.GetPolyData())
    #   displayNode.SetActiveScalarName('ImageScalars')
    #   displayNode.SetScalarRange(10,40)
    #   displayNode.SetOpacity(0.06)
    #   displayNode.SetAndObserveColorNodeID('vtkMRMLColorTableNodeFileHotToColdRainbow2.txt')
    #   displayNode.SetBackfaceCulling(0)
      
  #-----------------------------------------------------------
  # Needle Detection
  def array2(self):
    inputLabelID = self.__needleLabelSelector.currentNode().GetID()
    labelnode=slicer.mrmlScene.GetNodeByID(inputLabelID)
    i = labelnode.GetImageData()
    shape = list(i.GetDimensions())
    shape.reverse()
    a = vtk.util.numpy_support.vtk_to_numpy(i.GetPointData().GetScalars()).reshape(shape)
    labels=[]
    val=[[0,0,0] for i in range(a.max()+1)]
    for i in xrange(2,a.max()+1):
      w =numpy.transpose(numpy.where(a==i))
      # labels.append(w.mean(axis=0))
      val[i]=[0,0,0]
      val[i][0]=w[int(round(w.shape[0]/2))][2]
      val[i][1]=w[int(round(w.shape[0]/2))][1]
      val[i][2]=w[int(round(w.shape[0]/2))][0]
      if val[i] not in self.previousValues:
        labels.append(val[i])
        self.previousValues.append(val[i])
    return labels

  def factorial(self,n):
    '''factorial(n): return the factorial of the integer n.
    factorial(0) = 1
    factorial(n) with n<0 is -factorial(abs(n))
    '''
    result = 1
    for i in xrange(1, abs(n)+1):
     result *= i
    if n >= 0:
      return result
    else:
      return -result
      
  def binomial(self,n, k):
    if not 0 <= k <= n:
      return 0
    if k == 0 or k == n:
      return 1
    # calculate n!/k! as one product, avoiding factors that 
    # just get canceled
    P = k+1
    for i in xrange(k+2, n+1):
      P *= i
    # if you are paranoid:
    # C, rem = divmod(P, factorial(n-k))
    # assert rem == 0
    # return C
    return P//self.factorial(n-k)

  def Fibonacci(self,n):
    F=[0,1]
    for i in range(1,n+1):
      F.append(F[i-1]+F[i])
    return F

  def stepSize(self,k,l):
    F = self.Fibonacci(l+1)
    s =(sum(self.Fibonacci(k),-1)+F[k+1])/(sum(self.Fibonacci(l+1),-1))
    return s

  def ijk2ras(self,A):
    m=vtk.vtkMatrix4x4()
    volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
    volumeNode.GetIJKToRASMatrix(m)
    imageData = volumeNode.GetImageData()
    ras=[0,0,0]
    k = vtk.vtkMatrix4x4()
    o = vtk.vtkMatrix4x4()
    k.SetElement(0,3,A[0])
    k.SetElement(1,3,A[1])
    k.SetElement(2,3,A[2])
    k.Multiply4x4(m,k,o)
    ras[0] = o.GetElement(0,3)
    ras[1] = o.GetElement(1,3)
    ras[2] = o.GetElement(2,3)
    return ras

  def ras2ijk(self,A):
    m=vtk.vtkMatrix4x4()
    volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
    volumeNode.GetIJKToRASMatrix(m)
    m.Invert()
    imageData = volumeNode.GetImageData()
    ijk=[0,0,0]
    k = vtk.vtkMatrix4x4()
    o = vtk.vtkMatrix4x4()
    k.SetElement(0,3,A[0])
    k.SetElement(1,3,A[1])
    k.SetElement(2,3,A[2])
    k.Multiply4x4(m,k,o)
    ijk[0] = o.GetElement(0,3)
    ijk[1] = o.GetElement(1,3)
    ijk[2] = o.GetElement(2,3)
    return ijk
  
  def needleDetection(self):
    # Apply Island Effect
    editUtil = EditorLib.EditUtil.EditUtil()
    parameterNode = editUtil.getParameterNode()
    sliceLogic = editUtil.getSliceLogic()
    lm = slicer.app.layoutManager()
    sliceWidget = lm.sliceWidget('Red')
    islandsEffect = EditorLib.IdentifyIslandsEffectOptions()
    islandsEffect.setMRMLDefaults()
    islandsEffect.__del__()
    islandTool = EditorLib.IdentifyIslandsEffectLogic(sliceLogic)
    parameterNode.SetParameter("IslandEffect,minimumSize",'0')
    islandTool.removeIslands()
    # select the image node from the Red slice viewer
    m=vtk.vtkMatrix4x4()
    volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
    volumeNode.GetIJKToRASMatrix(m)
    imageData = volumeNode.GetImageData()
    spacing = volumeNode.GetSpacing()
    # chrono starts
    self.t0 = time.clock()
    # radius variation from 0 to rMax
    label=self.array2()
    for I in xrange(len(label)):
      A=label[I]
      colorVar = I/(len(label))
      self.needleDetectionThread(A, imageData, colorVar,spacing)

  def needleDetectionThread(self,A, imageData,colorVar,spacing):
    ijk = [0,0,0]
    bestPoint = [0,0,0]
    lenghtNeedle = self.lenghtNeedleParameter.value/spacing[2]
    ### initialisation of the parameters
    tIter = self.nbPointsPerLine.value
    rIter = self.nbRadiusIterations.value
    rMax = self.distanceMax.value/spacing[0]
    NbStepsNeedle = self.numberOfPointsPerNeedle.value-1
    nbRotatingStep = self.nbRotatingIterations.value
    dims=[0,0,0]
    imageData.GetDimensions(dims)
    pixelValue = numpy.zeros(shape=(dims[0],dims[1],dims[2]))
    ### difference: evaluate difference in average intensity between to position : new one and old one (oldtotal)
    difference = 0
    oldtotal = 0
    A0=A
    controlPoints = []
    controlPointsIJK = []
    controlPoints.append(self.ijk2ras(A))
    controlPointsIJK.append(A)
    bestControlPoints = []
    bestControlPoints.append(self.ijk2ras(A))
    for step in range(0,NbStepsNeedle+2):
      
      if step==0:
        C0 = [A[0],A[1],A[2]-3]
        rMax =5
        tIter=5
        rIter=5
      # elif step==NbStepsNeedle+1:
      #   stepsize = 30
      #   C0 = [2*A[0]-tip0[0],2*A[1]-tip0[1],A[2]-stepsize]
      #   rMax = self.distanceMax.value
      #   rIter = self.nbRadiusIterations.value
      else:
        stepsize = max(self.stepSize(step,NbStepsNeedle+1)*lenghtNeedle,self.stepsize.value/spacing[2])
        C0 = [2*A[0]-tip0[0],2*A[1]-tip0[1],A[2]-stepsize]
        rMax = max(stepsize,self.distanceMax.value/spacing[0])
        rIter = max(int(stepsize/(2))+5,self.nbRadiusIterations.value)
      
      if step==NbStepsNeedle+1:
        bestPoint = [(A[0]-A0[0])/(0.5*step)+A[0],(A[1]-A0[1])/(0.5*step)+A[1],(A[2]-A0[2])/(0.5*step)+A[2]]
      else:
      # if 1==1:
        estimator = 0
        minEstimator = 0  
        for R in range(rIter+1):
          r=rMax*(float(R)/rIter)
          ### angle variation from 0 to 360
          area=0
          for thetaStep in xrange(nbRotatingStep ):
            angleInDegree = float(thetaStep*360)/nbRotatingStep
            theta = math.radians(angleInDegree)
            ###
            C = [C0[0]+r*(math.cos(theta)),C0[1]+r*(math.sin(theta)),C0[2]]
            total = 0
            M=[[0,0,0] for i in xrange(tIter+1)]
            
            if step==NbStepsNeedle+1:
            # if 0==1:
              M=[[0,0,0] for i in xrange(100+1)]
              controlPointsAndLastPoint = copy.deepcopy(controlPointsIJK)
              controlPointsAndLastPoint.insert(len(controlPointsIJK),C)
              print controlPointsAndLastPoint
              n = len(controlPointsAndLastPoint)

              # calculates tIter = number of points per segment 
              for t in range(100+1):
                tt = t/tIter
                # x,y,z coordinates
                for i in range(3):
                  for j in range(n):
                    M[t][i]+=self.binomial(n,j)*(1-tt)**(n-j)*tt**j*controlPointsAndLastPoint[j][i]
                  ijk[i]=M[t][i]
                if ijk[0]<dims[0] and ijk[1]<dims[1] and ijk[2]<dims[2]:
                  center=imageData.GetScalarComponentAsDouble(ijk[0], ijk[1], ijk[2], 0)
                  total += center
            else:
              # calculates tIter = number of points per segment 
              for t in xrange(tIter+1):
                tt = t/(tIter)
                # x,y,z coordinates
                for i in range(3):
                  M[t][i] = (1-tt)*A[i] + tt*C[i]
                  ijk[i]=M[t][i]
                
                # first, test if points are in the image space 
                if ijk[0]<dims[0] and ijk[0]>0 and  ijk[1]<dims[1] and ijk[1]>0 and ijk[2]<dims[2] and ijk[2]>0:
                  center=imageData.GetScalarComponentAsDouble(ijk[0], ijk[1], ijk[2], 0)
                  total += center
                  if self.gradient.isChecked():
                    total += center - imageData.GetScalarComponentAsDouble(ijk[0]+5, ijk[1], ijk[2], 0)/4
                    total += center - imageData.GetScalarComponentAsDouble(ijk[0]-5, ijk[1], ijk[2], 0)/4
                    total += center - imageData.GetScalarComponentAsDouble(ijk[0], ijk[1]+5, ijk[2], 0)/4
                    total += center - imageData.GetScalarComponentAsDouble(ijk[0], ijk[1]-5, ijk[2], 0)/4
                    total += center - imageData.GetScalarComponentAsDouble(ijk[0]+5, ijk[1]+5, ijk[2], 0)/4
                    total += center - imageData.GetScalarComponentAsDouble(ijk[0]-5, ijk[1]-5, ijk[2], 0)/4
                    total += center - imageData.GetScalarComponentAsDouble(ijk[0]-5, ijk[1]+5, ijk[2], 0)/4
                    total += center - imageData.GetScalarComponentAsDouble(ijk[0]+5, ijk[1]-5, ijk[2], 0)/4
                
            if R==0:
              initialIntensity = total
              
            if total != 0:     
              estimator = total
              if estimator<initialIntensity:
                area+=1
                
              if estimator<minEstimator or minEstimator == 0:
                minEstimator=estimator
                if minEstimator!=0:  
                  bestPoint=C
                  
      tip0=A 
      A=bestPoint
      print area
      if area < 5:
        bestControlPoints.append(self.ijk2ras(A))
      controlPoints.append(self.ijk2ras(A))
      controlPointsIJK.append(A)
      
      # Draw Fiducial points at the control points if the checkbox is checked
      if self.drawFiducialPoints.isChecked():
        fiducial = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationFiducialNode')
        fiducial.SetName(str(step)+"-"+str(area)) 
        fiducial.Initialize(slicer.mrmlScene)
        fiducial.SetFiducialCoordinates(controlPoints[step+1])
    if len(bestControlPoints) >= 3 and self.filterControlPoints.isChecked():
      self.addNeedleToScene(bestControlPoints,colorVar)
    elif len(controlPoints) >= 2:
      self.addNeedleToScene(controlPoints,colorVar)

  def addNeedleToScene(self,controlPoint,colorVar): 
    ### Create a line from list of point
    # initialisation
    print controlPoint
    label=None
    scene = slicer.mrmlScene
    points = vtk.vtkPoints()
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    lines = vtk.vtkCellArray()
    polyData.SetLines(lines)
    linesIDArray = lines.GetData()
    linesIDArray.Reset()
    linesIDArray.InsertNextTuple1(0)
    polygons = vtk.vtkCellArray()
    polyData.SetPolys( polygons )
    idArray = polygons.GetData()
    idArray.Reset()
    idArray.InsertNextTuple1(0)
    nbEvaluationPoints=50
    n = len(controlPoint)-1
    Q=[[0,0,0] for t in range(nbEvaluationPoints+1)]
    # start calculation
    for t in range(nbEvaluationPoints):
      tt = float(t)/(1*nbEvaluationPoints)
      for j in range(3):
        for i in range(n+1):
          Q[t][j]+=self.binomial(n,i)*(1-tt)**(n-i)*tt**i*controlPoint[i][j]
          
      pointIndex = points.InsertNextPoint(*Q[t])
      linesIDArray.InsertNextTuple1(pointIndex)
      linesIDArray.SetTuple1( 0, linesIDArray.GetNumberOfTuples() - 1 )
      lines.SetNumberOfCells(1)
    ### Create model node
    model = slicer.vtkMRMLModelNode()
    model.SetScene(scene)
    model.SetAndObservePolyData(polyData)
    ### Create display node
    modelDisplay = slicer.vtkMRMLModelDisplayNode()
    if self.round==1: 
      modelDisplay.SetColor(1,1-colorVar,colorVar) # yellow to magenta
    elif self.round==2:
      modelDisplay.SetColor(colorVar,1,1) # cyan
    elif self.round==3:
      modelDisplay.SetColor(1,0.5+colorVar/2,1) # 
    elif self.round==4:
      modelDisplay.SetColor(0.5+colorVar/2,1,0.5+colorVar/2) #
    else:
      modelDisplay.SetColor(random.randrange(0,10,1)/(10),random.randrange(0,10,1)/(10),random.randrange(0,10,1)/(10))

    modelDisplay.SetScene(scene)
    scene.AddNode(modelDisplay)
    model.SetAndObserveDisplayNodeID(modelDisplay.GetID())
    ### Add to scene
    modelDisplay.SetInputPolyData(model.GetPolyData())
    scene.AddNode(model)
    ###Create Tube around the line
    tube=vtk.vtkTubeFilter()
    polyData = model.GetPolyData()
    tube.SetInput(polyData)
    tube.SetRadius(1)
    tube.SetNumberOfSides(50)
    tube.Update()
    model.SetAndObservePolyData(tube.GetOutput())
    model.GetDisplayNode().SliceIntersectionVisibilityOn()
    model.SetName('python-catch-round_'+str(self.round)+'-ID-'+str(model.GetID()))
    processingTime = time.clock()-self.t0
    print processingTime
    # if registration has been done, find the label for the needle
    if self.transform!=None:
      label = self.findLabelNeedleID(model.GetID())
      modelDisplay.SetColor(self.color[label[0]][0],self.color[label[0]][1],self.color[label[0]][2])
      model.SetAttribute("nth",str(label[0]))
    else:
      nth = model.GetID().strip('vtkMRMLModelNode')
      modelDisplay.SetColor(self.color[int(nth)][0],self.color[int(nth)][1],self.color[int(nth)][2])
      model.SetAttribute("nth",str(nth))

    self.addSegmentedNeedleToTable(int(model.GetID().strip('vtkMRMLModelNode')),label)

  def deleteSegmentedNeedle(self):
    while slicer.util.getNodes('python-catch-round_'+str(self.round)) != {}:
      nodes = slicer.util.getNodes('python-catch-round_'+str(self.round))
      for node in nodes.values():
        slicer.mrmlScene.RemoveNode(node)

  def newInsertionNeedle(self):
    messageBox = qt.QMessageBox.information( self, 'Information','You are creating a new set of needles')
    self.round +=1
    self.newInsertionButton.setText('Start a new set of needles - Round ' + str(self.round+1)+'?')
    self.deleteNeedleButton.setText('Delete Needles from round ' + str(self.round))

  def resetNeedleDetection(self):
    ret = messageBox = qt.QMessageBox.question( self, 'Attention','''
      Are you sure that you want to reset the needle detection? 
      It will delete every segmented needles...
      ''',qt.QMessageBox.Ok, qt.QMessageBox.Cancel)
    if ret == qt.QMessageBox.Ok:
      while slicer.util.getNodes('python-catch*') != {}:
        nodes = slicer.util.getNodes('python-catch*')
        for node in nodes.values():
          slicer.mrmlScene.RemoveNode(node)
      self.previousValues=[[0,0,0]]
      self.round=1
      self.newInsertionButton.setText('Start a new set of needles - Round ' + str(self.round+1)+'?')
      self.deleteNeedleButton.setText('Delete Needles from round ' + str(self.round))
      # reset report table
      self.table =None
      self.row=0
      self.initTableView()

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
    print("here")
    self.removeObservers() 

  def removeObservers(self):
    # remove observers and reset
    for observee,tag in self.styleObserverTags:
      observee.RemoveObserver(tag)
    self.styleObserverTags = []
    self.sliceWidgetsPerStyle = {}

  def processEvent(self,observee,event=None):
    '''
    get the mouse clicks and create a fiducial node at this position. Used later for the fiducial registration
    '''
    if self.sliceWidgetsPerStyle.has_key(observee) and event == "LeftButtonPressEvent":
      if slicer.app.repositoryRevision<= 21022:
        sliceWidget = self.sliceWidgetsPerStyle[observee]
        style = sliceWidget.sliceView().interactorStyle()          
        xy = style.GetInteractor().GetEventPosition()
        xyz = sliceWidget.convertDeviceToXYZ(xy)
        ras = sliceWidget.convertXYZToRAS(xyz)
      else:
        sliceWidget = self.sliceWidgetsPerStyle[observee]
        sliceLogic = sliceWidget.sliceLogic()
        sliceNode = sliceWidget.mrmlSliceNode()
        interactor = observee.GetInteractor()
        xy = interactor.GetEventPosition()
        xyz = sliceWidget.sliceView().convertDeviceToXYZ(xy);
        ras = sliceWidget.sliceView().convertXYZToRAS(xyz)
      
      colorVar = random.randrange(50,100,1)/(100)
      volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
      imageData = volumeNode.GetImageData()
      spacing = volumeNode.GetSpacing()
      ijk=self.ras2ijk(ras)
      self.t0=time.clock()
      self.needleDetectionThread(ijk, imageData, colorVar,spacing)

  def onRunButtonToggled(self, checked):
    if checked:
      self.start()
      self.fiducialButton.text = "Stop Giving Tips"  
    else:
      self.stop()
      self.fiducialButton.text = "Start Giving Needle Tips"  

  #-----------------------------------------------------------
  # Needle segmentation report
  # model and view for stats table
  def initTableView(self):
    if self.table==None:
      self.colorLabel()
      self.keys = ("Label","Round" ,"Reliability")
      self.labelStats = {}
      self.labelStats['Labels'] = []
      self.items = []
      self.model = qt.QStandardItemModel()
      self.model.setColumnCount(6)
      self.model.setHeaderData(0,1,"")
      self.model.setHeaderData(1,1,"Label")
      self.model.setHeaderData(2,1,"R.")
      self.model.setHeaderData(3,1,"Reliability")
      self.model.setHeaderData(4,1,"Display")
      self.model.setHeaderData(5,1,"Reformat")
      if self.view == None:
        self.view = qt.QTableView()
        self.view.setMinimumHeight(300)
        self.view.sortingEnabled = True
        self.view.verticalHeader().visible = False
      # col = 1
      # for k in self.keys:
      #   # self.view.setColumnWidth(col,15*len(k))
      #   # self.model.setHeaderData(col,1,k)
      #   col += 1 
      self.view.setModel(self.model)
      self.view.setColumnWidth(0,18)
      self.view.setColumnWidth(1,58)
      self.view.setColumnWidth(2,28)
      self.table = 1

  def addSegmentedNeedleToTable(self,ID,label=None):
    
    self.initTableView()
    if label !=None:
      ref = int(label[0])
      needleLabel = self.option[ref]
      reliability = label[1]
    else:
      needleLabel = str(ID)
      ref = ID
      reliability = '-'
    # ref = int(modelNode.GetAttribute("nth"))
    
    self.labelStats["Labels"].append(ref)
    self.labelStats[ref,"Label"] = needleLabel
    self.labelStats[ref,"Round"] = str(self.round)
    self.labelStats[ref,"Reliability"] = str(reliability) 
      
    
    color = qt.QColor()
    color.setRgb(self.color255[ref][0],self.color255[ref][1],self.color255[ref][2])
    item = qt.QStandardItem()
    item.setData(color,1)
    self.model.setItem(self.row,0,item)
    self.items.append(item)
    col = 1
    for k in self.keys:
      item = qt.QStandardItem()
      item.setText(self.labelStats[ref,k])
      self.model.setItem(self.row,col,item)
      self.items.append(item)
      col += 1
    displayButton = qt.QPushButton("Display")
    displayButton.checked = True
    displayButton.checkable = True
    displayButton.connect("clicked()", lambda who=ID: self.displayNeedleID(who))
    index = self.model.index(self.row,4)
    self.view.setIndexWidget(index,displayButton)
    reformatButton = qt.QPushButton("Reformat")
    reformatButton.connect("clicked()", lambda who=ID: self.reformatNeedleID(who))
    index2 = self.model.index(self.row,5)
    self.view.setIndexWidget(index2,reformatButton)
    self.row += 1  
  
    self.analysisGroupBoxLayout.addRow(self.view)


  #-----------------------------------------------------------
  # Radiation

  def AddRadiation(self,i,needleID):
    pass
    # needleNode = slicer.mrmlScene.GetNodeByID(needleID)
    # polyData = needleNode.GetPolyData()
    # nb = polyData.GetNumberOfPoints()
    # base = [0,0,0]
    # tip = [[0,0,0] for k in range(11)]
    # if nb>100:
      
      # polyData.GetPoint(nb-1,tip[10])
      # polyData.GetPoint(0,base)
    
    # a = tip[10][0]-base[0]
    # b = tip[10][1]-base[1]
    # c = tip[10][2]-base[2]
    
    # for l in range(7):
      # tip[9-l][0] = tip[10][0]-0.1*a*(l+1)
      # tip[9-l][1] = tip[10][1]-0.1*b*(l+1)
      # tip[9-l][2] = tip[10][2]-0.1*c*(l+1)
    # for l in range(1,3):
      # tip[l][0] = tip[10][0]+0.1*a*l
      # tip[l][1] = tip[10][1]+0.1*b*l
      # tip[l][2] = tip[10][2]+0.1*c*l
         
    # rad = vtk.vtkAppendPolyData()  
    
    # for l in range(1,11):
      # TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
      # Transform=vtk.vtkTransform()        
      # TransformPolyDataFilter.SetInput(self.m_polyRadiation)

      # vtkmat = Transform.GetMatrix()
      # vtkmat.SetElement(0,3,tip[l][0])
      # vtkmat.SetElement(1,3,tip[l][1])
      # vtkmat.SetElement(2,3,tip[l][2])
      # TransformPolyDataFilter.SetTransform(Transform)
      # TransformPolyDataFilter.Update()
    
      # rad.AddInput(TransformPolyDataFilter.GetOutput())
    
    # modelNode = slicer.vtkMRMLModelNode()
    # displayNode = slicer.vtkMRMLModelDisplayNode()
    # storageNode = slicer.vtkMRMLModelStorageNode()
 
    # fileName = 'Rad'+self.option[i]+'.vtk'

    # mrmlScene = slicer.mrmlScene
    # modelNode.SetName(fileName)
    # modelNode.SetAttribute("radiation","segmented")
    # modelNode.SetAttribute("needleID",str(needleID))    
    # modelNode.SetAndObservePolyData(rad.GetOutput()) 

    # modelNode.SetScene(mrmlScene)
    # storageNode.SetScene(mrmlScene)
    # storageNode.SetFileName(fileName)  
    # displayNode.SetScene(mrmlScene)
    # displayNode.SetVisibility(0)
    # mrmlScene.AddNode(storageNode)
    # mrmlScene.AddNode(displayNode)
    # mrmlScene.AddNode(modelNode)
    # modelNode.SetAndObserveStorageNodeID(storageNode.GetID())
    # modelNode.SetAndObserveDisplayNodeID(displayNode.GetID())
    
    # displayNode.SetPolyData(modelNode.GetPolyData())

    # displayNode.SetSliceIntersectionVisibility(0)
    # displayNode.SetScalarVisibility(1)
    # displayNode.SetActiveScalarName('scalars')
    # displayNode.SetScalarRange(0,230)
    # displayNode.SetOpacity(0.06)
    # displayNode.SetAndObserveColorNodeID('vtkMRMLColorTableNodeFileHotToColdRainbow.txt')
    # displayNode.SetBackfaceCulling(0)
    # pNode= self.parameterNode()
    # pNode.SetParameter(fileName,modelNode.GetID())
    # mrmlScene.AddNode(modelNode)

    #--------------------------------------------#
  
  #-----------------------------------------------------------
  '''
  DICOM functions
  '''
      
  def onDatabaseChanged(self):
    """Use this because to update the view in response to things
    like database inserts.  Ideally the model would do this
    directly based on signals from the SQLite database, but
    that is not currently available.
    https://bugreports.qt-project.org/browse/QTBUG-10775
    """
    self.dicomApp.suspendModel()
    self.requestResumeModel()
    self.requestUpdateRecentActivity()

  def requestUpdateRecentActivity(self):
    """This method serves to compress the requests for updating
    the recent activity widget since it is time consuming and there can be
    many of them coming in a rapid sequence when the 
    database is active"""
    if self.updateRecentActivityRequested:
      return
    self.updateRecentActivityRequested = True
    qt.QTimer.singleShot(500, self.onUpateRecentActivityRequestTimeout)

  def onUpateRecentActivityRequestTimeout(self):
    self.recentActivity.update()
    self.updateRecentActivityRequested = False

  def requestResumeModel(self):
    """This method serves to compress the requests for resuming
    the dicom model since it is time consuming and there can be
    many of them coming in a rapid sequence when the 
    database is active"""
    if self.resumeModelRequested:
      return
    self.resumeModelRequested = True
    qt.QTimer.singleShot(500, self.onResumeModelRequestTimeout)

  def onResumeModelRequestTimeout(self):
    self.dicomApp.resumeModel()
    self.resumeModelRequested = False

  def onDatabaseDirectoryChanged(self,databaseDirectory):
    if not hasattr(slicer, 'dicomDatabase') or not slicer.dicomDatabase:
      slicer.dicomDatabase = ctk.ctkDICOMDatabase()
      self.setDatabasePrecacheTags()
    databaseFilepath = databaseDirectory + "/ctkDICOM.sql"
    if not (os.access(databaseDirectory, os.W_OK) and os.access(databaseDirectory, os.R_OK)):
      self.messageBox('The database file path "%s" cannot be opened.' % databaseFilepath)
    else:
      slicer.dicomDatabase.openDatabase(databaseDirectory + "/ctkDICOM.sql", "SLICER")
      if not slicer.dicomDatabase.isOpen:
        self.messageBox('The database file path "%s" cannot be opened.' % databaseFilepath)
        self.dicomDatabase = None
      else:
        if self.dicomApp:
          if self.dicomApp.databaseDirectory != databaseDirectory:
            self.dicomApp.databaseDirectory = databaseDirectory
        else:
          settings = qt.QSettings()
          settings.setValue('DatabaseDirectory', databaseDirectory)
          settings.sync()
    if slicer.dicomDatabase:
      slicer.app.setDICOMDatabase(slicer.dicomDatabase)

  def setDatabasePrecacheTags(self):
    """query each plugin for tags that should be cached on import
       and set them for the dicom app widget and slicer"""
    tagsToPrecache = list(slicer.dicomDatabase.tagsToPrecache)
    for pluginClass in slicer.modules.dicomPlugins:
      plugin = slicer.modules.dicomPlugins[pluginClass]()
      tagsToPrecache += plugin.tags.values()
    tagsToPrecache = list(set(tagsToPrecache))  # remove duplicates
    tagsToPrecache.sort()
    if hasattr(slicer, 'dicomDatabase'):
      slicer.dicomDatabase.tagsToPrecache = tagsToPrecache
    if self.dicomApp:
      self.dicomApp.tagsToPrecache = tagsToPrecache

  def promptForDatabaseDirectory(self):
    """Ask the user to pick a database directory.
    But, if the application is in testing mode, just pick
    a temp directory
    """
    commandOptions = slicer.app.commandOptions()
    if commandOptions.testingEnabled:
      databaseDirectory = slicer.app.temporaryPath + '/tempDICOMDatbase'
      qt.QDir().mkpath(databaseDirectory)
      self.onDatabaseDirectoryChanged(databaseDirectory)
    else:
      settings = qt.QSettings()
      databaseDirectory = settings.value('DatabaseDirectory')
      if databaseDirectory:
        self.onDatabaseDirectoryChanged(databaseDirectory)
      else:
        fileDialog = ctk.ctkFileDialog(slicer.util.mainWindow())
        fileDialog.setWindowModality(1)
        fileDialog.setWindowTitle("Select DICOM Database Directory")
        fileDialog.setFileMode(2) # prompt for directory
        fileDialog.connect('fileSelected(QString)', self.onDatabaseDirectoryChanged)
        label = qt.QLabel("<p><p>The Slicer DICOM module stores a local database with an index to all datasets that are <br>pushed to slicer, retrieved from remote dicom servers, or imported.<p>Please select a location for this database where you can store the amounts of data you require.<p>Be sure you have write access to the selected directory.", fileDialog)
        fileDialog.setBottomWidget(label)
        fileDialog.exec_()

  def onTreeClicked(self,index):
    self.model = index.model()
    self.tree.setExpanded(index, not self.tree.expanded(index))
    self.selection = index.sibling(index.row(), 0)
    typeRole = self.selection.data(self.dicomModelTypeRole)
    if typeRole > 0:
      self.sendButton.enabled = True
    else:
      self.sendButton.enabled = False
    if typeRole:
      self.exportAction.enabled = self.dicomModelTypes[typeRole] == "Study"
    else:
      self.exportAction.enabled = False
    self.detailsPopup.open()
    uid = self.selection.data(self.dicomModelUIDRole)
    role = self.dicomModelTypes[self.selection.data(self.dicomModelTypeRole)]
    self.detailsPopup.offerLoadables(uid, role)

  def onTreeContextMenuRequested(self,pos):
    index = self.tree.indexAt(pos)
    self.selection = index.sibling(index.row(), 0)
    self.contextMenu.popup(self.tree.mapToGlobal(pos))

  def onContextMenuTriggered(self,action):
    if action == self.deleteAction:
      typeRole = self.selection.data(self.dicomModelTypeRole)
      role = self.dicomModelTypes[typeRole]
      uid = self.selection.data(self.dicomModelUIDRole)
      if self.okayCancel('This will remove references from the database\n(Files will not be deleted)\n\nDelete %s?' % role):
        # TODO: add delete option to ctkDICOMDatabase
        self.dicomApp.suspendModel()
        if role == "Patient":
          removeWorked = slicer.dicomDatabase.removePatient(uid)
        elif role == "Study":
          removeWorked = slicer.dicomDatabase.removeStudy(uid)
        elif role == "Series":
          removeWorked = slicer.dicomDatabase.removeSeries(uid)
        if not removeWorked:
          self.messageBox(self,"Could not remove %s" % role,title='DICOM')
        self.dicomApp.resumeModel()
    elif action == self.exportAction:
      self.onExportClicked()

  def onExportClicked(self):
    """Associate a slicer volume as a series in the selected dicom study"""
    uid = self.selection.data(self.dicomModelUIDRole)
    exportDialog = DICOMLib.DICOMExportDialog(uid,onExportFinished=self.onExportFinished)
    self.dicomApp.suspendModel()
    exportDialog.open()

  def onExportFinished(self):
    self.requestResumeModel()

  def onSendClicked(self):
    """Perform a dicom store of slicer data to a peer"""
    # TODO: this should migrate to ctk for a more complete implementation
    # - just the basics for now
    uid = self.selection.data(self.dicomModelUIDRole)
    role = self.dicomModelTypes[self.selection.data(self.dicomModelTypeRole)]
    studies = []
    if role == "Patient":
      studies = slicer.dicomDatabase.studiesForPatient(uid)
    if role == "Study":
      studies = [uid]
    series = []
    if role == "Series":
      series = [uid]
    else:
      for study in studies:
        series += slicer.dicomDatabase.seriesForStudy(study)
    files = []
    for serie in series:
      files += slicer.dicomDatabase.filesForSeries(serie)
    sendDialog = DICOMLib.DICOMSendDialog(files)
    sendDialog.open()

  def setBrowserPersistence(self,onOff):
    self.detailsPopup.setModality(not onOff)
    self.browserPersistent = onOff

  def onToggleListener(self):
    if hasattr(slicer, 'dicomListener'):
      slicer.dicomListener.stop()
      del slicer.dicomListener
      self.toggleListener.text = "Start Listener"
    else:
      try:
        slicer.dicomListener = DICOMLib.DICOMListener(database=slicer.dicomDatabase)
        slicer.dicomListener.start()
        self.onListenerStateChanged(slicer.dicomListener.process.state())
        slicer.dicomListener.process.connect('stateChanged(QProcess::ProcessState)',self.onListenerStateChanged)
        slicer.dicomListener.fileToBeAddedCallback = self.onListenerToAddFile
        slicer.dicomListener.fileAddedCallback = self.onListenerAddedFile
        self.toggleListener.text = "Stop Listener"
      except UserWarning as message:
        self.messageBox(self,"Could not start listener:\n %s" % message,title='DICOM')

  def onListenerStateChanged(self,newState):
    """ Called when the indexer process state changes
    so we can provide feedback to the user
    """
    if newState == 0:
      slicer.util.showStatusMessage("DICOM Listener not running")
    if newState == 1:
      slicer.util.showStatusMessage("DICOM Listener starting")
    if newState == 2:
      slicer.util.showStatusMessage("DICOM Listener running")

  def onListenerToAddFile(self):
    """ Called when the indexer is about to add a file to the database.
    Works around issue where ctkDICOMModel has open queries that keep the
    database locked.
    """
    self.dicomApp.suspendModel()

  def onListenerAddedFile(self):
    """Called after the listener has added a file.
    Restore and refresh the app model
    """
    newFile = slicer.dicomListener.lastFileAdded
    if newFile:
      slicer.util.showStatusMessage("Loaded: %s" % newFile, 1000)
    self.requestResumeModel()

  def onToggleServer(self):
    if self.testingServer and self.testingServer.qrRunning():
      self.testingServer.stop()
      self.toggleServer.text = "Start Testing Server"
    else:
      #
      # create&configure the testingServer if needed, start the server, and populate it
      #
      if not self.testingServer:
        # find the helper executables (only works on build trees
        # with standard naming conventions)
        self.exeDir = slicer.app.slicerHome 
        if slicer.app.intDir:
          self.exeDir = self.exeDir + '/' + slicer.app.intDir
        self.exeDir = self.exeDir + '/../CTK-build/DCMTK-build'

        # TODO: deal with Debug/RelWithDebInfo on windows

        # set up temp dir
        tmpDir = slicer.app.settings().value('Modules/TemporaryDirectory')
        if not os.path.exists(tmpDir):
          os.mkdir(tmpDir)
        self.tmpDir = tmpDir + '/DICOM'
        if not os.path.exists(self.tmpDir):
          os.mkdir(self.tmpDir)
        self.testingServer = DICOMLib.DICOMTestingQRServer(exeDir=self.exeDir,tmpDir=self.tmpDir)

      # look for the sample data to load (only works on build trees
      # with standard naming conventions)
      self.dataDir =  slicer.app.slicerHome + '/../../Slicer4/Testing/Data/Input/CTHeadAxialDicom'
      files = glob.glob(self.dataDir+'/*.dcm')

      # now start the server
      self.testingServer.start(verbose=self.verboseServer.checked,initialFiles=files)
      self.toggleServer.text = "Stop Testing Server"

  def onRunListenerAtStart(self):
    settings = qt.QSettings()
    settings.setValue('DICOM/RunListenerAtStart', self.runListenerAtStart.checked)

  def messageBox(self,text,title='DICOM'):
    self.mb = qt.QMessageBox(slicer.util.mainWindow())
    self.mb.setWindowTitle(title)
    self.mb.setText(text)
    self.mb.setWindowModality(1)
    self.mb.exec_()
    return

  def question(self,text,title='DICOM'):
    return qt.QMessageBox.question(slicer.util.mainWindow(), title, text, 0x14000) == 0x4000

  def okayCancel(self,text,title='DICOM'):
    return qt.QMessageBox.question(slicer.util.mainWindow(), title, text, 0x400400) == 0x400
    

