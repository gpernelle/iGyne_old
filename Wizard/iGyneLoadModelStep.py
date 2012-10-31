from __main__ import qt, ctk, slicer
import os
import glob
from iGyneStep import *
from Helper import *
import DICOMLib
import PythonQt

class iGyneLoadModelStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '3. Load the template' )
    self.setDescription( 'Load the template. From this template, auto-crop and registration functions will be processed.' )
    self.__parent = super( iGyneLoadModelStep, self )
    self.loadTemplateButton = None
    
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
      
    self.dicomModelUIDRole = 32
    self.dicomModelTypeRole = self.dicomModelUIDRole + 1
    self.dicomModelTypes = ('Root', 'Patient', 'Study', 'Series', 'Image')

  def createUserInterface( self ):
    self.__layout = self.__parent.createUserInterface()
   
    baselineScanLabel = qt.QLabel( 'CT or MR scan:' )
    self.__baselineVolumeSelector = slicer.qMRMLNodeComboBox()
    self.__baselineVolumeSelector.objectName = 'baselineVolumeSelector'
    self.__baselineVolumeSelector.toolTip = "Choose the baseline scan"
    self.__baselineVolumeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__baselineVolumeSelector.setMRMLScene(slicer.mrmlScene)
    self.__baselineVolumeSelector.noneEnabled = False
    self.__baselineVolumeSelector.addEnabled = False
    self.__baselineVolumeSelector.removeEnabled = False
    # self.__layout.connect('nodeAdded(vtkMRMLNode*)',self.__baselineVolumeSelector,'setCurrentNode(vtkMRMLNode*)')
    self.__layout.connect('mrmlSceneChanged(vtkMRMLScene*)',
                        self.__baselineVolumeSelector, 'setMRMLScene(vtkMRMLScene*)')

	
	#Load Template Button 
    self.loadTemplateButton = qt.QPushButton('Load template')
    self.__layout.addRow(self.loadTemplateButton)
    self.loadTemplateButton.connect('clicked()', self.loadTemplate)

	#Load Scan Button
    self.__fileFrame = ctk.ctkCollapsibleButton()
    self.__fileFrame.text = "NRRD File Input"
    self.__fileFrame.collapsed = 1
    fileFrame = qt.QFormLayout(self.__fileFrame)
    self.__layout.addRow(self.__fileFrame)
   
    loadDataButton = qt.QPushButton('Load Scan')
    loadDataButton.connect('clicked()', self.loadData)
    fileFrame.addRow(loadDataButton)

    
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

    # voiGroupBox = qt.QGroupBox()
    # voiGroupBox.setTitle( 'DICOM' )
    dicomFrame.addRow(self.toggleListener)
    # dicomFrame.addRow( voiGroupBox )
    # voiGroupBoxLayout = qt.QFormLayout( voiGroupBox )
    self.dicomApp = ctk.ctkDICOMAppWidget()
    #voiGroupBoxLayout.addRow( self.dicomApp )
    self.detailsPopup = DICOMLib.DICOMDetailsPopup(self.dicomApp,True)
    self.exportButton = qt.QPushButton('Export Slicer Data to Study...')
    self.loadButton = qt.QPushButton('Load to Slicer')
    self.previewLabel = qt.QLabel()
    self.tree = self.detailsPopup.tree
    
    self.showBrowser = qt.QPushButton('Show DICOM Browser')
    dicomFrame.addRow(self.showBrowser)
    self.showBrowser.connect('clicked()', self.detailsPopup.open)
    
    self.__layout.addRow( baselineScanLabel, self.__baselineVolumeSelector )
    
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
    
    
    # dicom = DICOMLib.DICOMWidgets.DICOMDetailsPopup(self.__roiWidget)
    # voiGroupBoxLayout.addRow(dicom.create())
    
    
    
    # self.loadButton = qt.QPushButton('Load Selection to Slicer')
    # self.loadButton.enabled = False 
    # voiGroupBoxLayout.addWidget(self.loadButton)
    
    self.updateWidgetFromParameters(self.parameterNode())


  def loadData(self):
    slicer.util.openAddDataDialog()

  def validate( self, desiredBranchId ):
    '''
    '''
    pNode = self.parameterNode()
    if pNode.GetParameter('skip') != '1':
      self.__parent.validate( desiredBranchId )
      # check here that the selectors are not empty
      baseline = self.__baselineVolumeSelector.currentNode()
      modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
      for modelNode in modelNodes.values():
        if modelNode.GetName()=='Template' :
          template=modelNode
        if modelNode.GetName()=='Obturator_reg' :
          obturator=modelNode
      
      df = template.GetDisplayNode()
      do = obturator.GetDisplayNode()
      df.SetSliceIntersectionVisibility(0)
      do.SetSliceIntersectionVisibility(0)

      if baseline != None and template != None:
        baselineID = baseline.GetID()
        templateID = template.GetID()
        obturatorID = obturator.GetID()
        if baselineID != '' and templateID != '' and baselineID != templateID:
      
          pNode = self.parameterNode()
          pNode.SetParameter('baselineVolumeID', baselineID)
          pNode.SetParameter('templateID', templateID)
          pNode.SetParameter('obturatorID', obturatorID)
          
          self.__parent.validationSucceeded(desiredBranchId)
        else:
          self.__parent.validationFailed(desiredBranchId, 'Error','Please select distinctive baseline and followup volumes!')
      else:
        self.__parent.validationFailed(desiredBranchId, 'Error','Please select both Template and scan/DICOM Volume!')
    
    else:
      self.__parent.validate( desiredBranchId )
      self.__parent.validationSucceeded(desiredBranchId)
  
  
  def onEntry(self,comingFrom,transitionType):
  
    super(iGyneLoadModelStep, self).onEntry(comingFrom, transitionType)
    # setup the interface
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    if pNode.GetParameter('skip') != '1':
      applicator  = pNode.GetParameter('Template')
      if applicator == "4points":
        self.loadTemplate(4)
      if applicator == "3points":
        self.loadTemplate(3)
    elif pNode.GetParameter('skip')=='1':
      self.workflow().goForward() # 4      
      
  def onExit(self, goingTo, transitionType):
   
    pNode= self.parameterNode()
    if pNode.GetParameter('skip') != '1':
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
    template = Helper.getNodeByID(pNode.GetParameter('templateID'))
    #print pNode.GetParameter('templateID')
    #print template
   
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
    template.GetRASBounds(bounds)
    dm.SetElement(0,3,(bounds[0]+bounds[1])/float(2))
    dm.SetElement(1,3,(bounds[2]+bounds[3])/float(2))
    dm.SetElement(2,3,(bounds[4]+bounds[5])/float(2))
    dm.SetElement(0,0,abs(dm.GetElement(0,0)))
    dm.SetElement(1,1,abs(dm.GetElement(1,1)))
    dm.SetElement(2,2,abs(dm.GetElement(2,2)))
    roiTransformNode.SetAndObserveMatrixTransformToParent(dm)     


  def loadTemplate(self,nb):
    pNode = self.parameterNode()
    alreadyloaded = pNode.GetParameter("Template-loaded")
    if alreadyloaded != "1":
      if nb == 3:
        pathToScene = slicer.modules.igynepy.path.replace("iGynePy.py","iGynePyTemplate/Template/3points/Template.mrml")
      elif nb ==4:
        pathToScene = slicer.modules.igynepy.path.replace("iGynePy.py","iGynePyTemplate/Template/4points/Template.mrml")
#      slicer.util.loadScene( pathToScene, True)
      slicer.util.loadScene( pathToScene)
      self.loadTemplateButton.setEnabled(0)
      pNode.SetParameter("Template-loaded","1")
      
      
      
      
  def onDatabaseDirectoryChanged(self,databaseDirectory):
    if not hasattr(slicer, 'dicomDatabase') or not slicer.dicomDatabase:
      slicer.dicomDatabase = ctk.ctkDICOMDatabase()
    databaseFilepath = databaseDirectory + "/ctkDICOM.sql"
    if not (os.access(databaseDirectory, os.W_OK) and os.access(databaseDirectory, os.R_OK)):
      self.messageBox('The database file path "%s" cannot be opened.' % databaseFilepath)
      return
    slicer.dicomDatabase.openDatabase(databaseDirectory + "/ctkDICOM.sql", "SLICER")
    if not slicer.dicomDatabase.isOpen:
      self.messageBox('The database file path "%s" cannot be opened.' % databaseFilepath)
    if self.dicomApp.databaseDirectory != databaseDirectory:
      self.dicomApp.databaseDirectory = databaseDirectory

  def promptForDatabaseDirectory(self):
    fileDialog = ctk.ctkFileDialog(slicer.util.mainWindow())
    fileDialog.setWindowModality(1)
    fileDialog.setWindowTitle("Select DICOM Database Directory")
    fileDialog.setFileMode(2) # prompt for directory
    fileDialog.connect('fileSelected(QString)', self.onDatabaseDirectoryChanged)
    label = qt.QLabel("<p><p>The Slicer DICOM module stores a local database with an index to all datasets that are <br>pushed to slicer, retrieved from remote dicom servers, or imported.<p>Please select a location for this database where you can store the amounts of data you require.<p>Be sure you have write access to the selected directory.", fileDialog)
    fileDialog.setBottomWidget(label)
    fileDialog.open()

  def onTreeClicked(self,index):
    self.model = index.model()
    self.tree.setExpanded(index, not self.tree.expanded(index))
    self.selection = index.sibling(index.row(), 0)
    typeRole = self.selection.data(self.dicomModelTypeRole)
    if typeRole > 0:
      self.loadButton.text = 'Load Selected %s to Slicer' % self.dicomModelTypes[typeRole]
      self.loadButton.enabled = True
      self.sendButton.enabled = True
    else:
      self.loadButton.text = 'Load to Slicer'
      self.loadButton.enabled = False 
      self.sendButton.enabled = False
    if typeRole:
      self.exportAction.enabled = self.dicomModelTypes[typeRole] == "Study"
    else:
      self.exportAction.enabled = False
    self.previewLabel.text = "Selection: " + self.dicomModelTypes[typeRole]
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


  def onLoadButton(self):
    self.progress = qt.QProgressDialog(slicer.util.mainWindow())
    self.progress.minimumDuration = 0
    self.progress.show()
    self.progress.setValue(0)
    self.progress.setMaximum(100)
    uid = self.selection.data(self.dicomModelUIDRole)
    role = self.dicomModelTypes[self.selection.data(self.dicomModelTypeRole)]
    toLoad = {}
    if role == "Patient":
      self.progress.show()
      self.loadPatient(uid)
    elif role == "Study":
      self.progress.show()
      self.loadStudy(uid)
    elif role == "Series":
      self.loadSeries(uid)
    elif role == "Image":
      pass
    self.progress.close()
    self.progress = None

  def onExportClicked(self):
    """Associate a slicer volume as a series in the selected dicom study"""
    uid = self.selection.data(self.dicomModelUIDRole)
    exportDialog = DICOMLib.DICOMExportDialog(uid,onExportFinished=self.onExportFinished)
    self.dicomApp.suspendModel()
    exportDialog.open()

  def onExportFinished(self):
    self.dicomApp.resumeModel()
    self.dicomApp.resetModel()

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

  def loadPatient(self,patientUID):
    studies = slicer.dicomDatabase.studiesForPatient(patientUID)
    s = 1
    self.progress.setLabelText("Loading Studies")
    self.progress.setValue(1)
    slicer.app.processEvents()
    for study in studies:
      self.progress.setLabelText("Loading Study %d of %d" % (s, len(studies)))
      slicer.app.processEvents()
      s += 1
      self.loadStudy(study)
      if self.progress.wasCanceled:
        break

  def loadStudy(self,studyUID):
    series = slicer.dicomDatabase.seriesForStudy(studyUID)
    s = 1
    origText = self.progress.labelText
    for serie in series:
      self.progress.setLabelText(origText + "\nLoading Series %d of %d" % (s, len(series)))
      slicer.app.processEvents()
      s += 1
      self.progress.setValue(100.*s/len(series))
      self.loadSeries(serie)
      if self.progress.wasCanceled:
        break

  def loadSeries(self,seriesUID):
    files = slicer.dicomDatabase.filesForSeries(seriesUID)
    slicer.dicomDatabase.loadFileHeader(files[0])
    seriesDescription = "0008,103e"
    d = slicer.dicomDatabase.headerValue(seriesDescription)
    try:
      name = d[d.index('[')+1:d.index(']')]
    except ValueError:
      name = "Unknown"
    self.progress.labelText += '\nLoading %s' % name
    slicer.app.processEvents()
    self.loadFiles(slicer.dicomDatabase.filesForSeries(seriesUID), name)

  def loadFiles(self, files, name):
    loader = DICOMLib.DICOMLoader(files,name)
    if not loader.volumeNode:
      qt.QMessageBox.warning(slicer.util.mainWindow(), 'Load', 'Could not load volume for: %s' % name)
      print('Tried to load volume as %s using: ' % name, files)

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
    self.dicomApp.resumeModel()
    self.dicomApp.resetModel()

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
    self.mb.open()
    return

  def question(self,text,title='DICOM'):
    return qt.QMessageBox.question(slicer.util.mainWindow(), title, text, 0x14000) == 0x4000

  def okayCancel(self,text,title='DICOM'):
    return qt.QMessageBox.question(slicer.util.mainWindow(), title, text, 0x400400) == 0x400
    
      
   