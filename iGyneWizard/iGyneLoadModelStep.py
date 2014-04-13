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
    self.setName( '3. Load the CAD Model of the applicator' )
    self.setDescription( 'Load the CAD Models.' )
    self.__parent = super( iGyneLoadModelStep, self )
    self.loadTemplateButton = None
    
    ###############################################################
    # # initialize the dicom infrastructure
    # settings = qt.QSettings()
    # # the dicom database is a global object for slicer
    # if settings.contains('DatabaseDirectory'):
    #   databaseDirectory = settings.value('DatabaseDirectory')
    #   if databaseDirectory: 
    #     slicer.dicomDatabase = ctk.ctkDICOMDatabase()
    #     slicer.dicomDatabase.openDatabase(databaseDirectory + "/ctkDICOM.sql", "SLICER")
    #     # the dicom listener is also global, but only started on app start if 
    #     # the user so chooses
    #     if settings.contains('DICOM/RunListenerAtStart'):
    #       if bool(settings.value('DICOM/RunListenerAtStart')):
    #         if not hasattr(slicer, 'dicomListener'):
    #           try:
    #             slicer.dicomListener = DICOMLib.DICOMListener(slicer.dicomDatabase)
    #             slicer.dicomListener.start()
    #           except (UserWarning,OSError) as message:
    #             # TODO: how to put this into the error log?
    #             print ('Problem trying to start DICOMListener:\n %s' % message)
    # else:
    #   slicer.dicomDatabase = None

    # # TODO: are these wrapped so we can avoid magic numbers?
    # self.dicomModelUIDRole = 32
    # self.dicomModelTypeRole = self.dicomModelUIDRole + 1
    # self.dicomModelTypes = ('Root', 'Patient', 'Study', 'Series', 'Image')

    # # state management for compressing events
    # self.resumeModelRequested = False
    # self.updateRecentActivityRequested = False
    ###############################################################

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

    # Sample Data Button
    sampleDATA = qt.QPushButton('Download Sample Data')
    sampleDATA.connect('clicked()',self.downloadPhantom)
    fileFrame.addRow(sampleDATA)
    
    # Sample Data Status
    self.log = qt.QTextEdit()
    self.log.readOnly = True
    self.__fileFrame.layout().addRow(self.log)
    self.logMessage('<p>Status: <i>Idle</i>\n')
    

    # ###############################################################
    # # DICOM ToolBox
    
    #  # Listener 

    # settings = qt.QSettings()
    # self.toggleListener = qt.QPushButton()
    # if hasattr(slicer, 'dicomListener'):
    #   self.toggleListener.text = "Stop Listener"
    #   slicer.dicomListener.process.connect('stateChanged(int)',self.onListenerStateChanged)
    # else:
    #   self.toggleListener.text = "Start Listener"
    
    # self.toggleListener.connect('clicked()', self.onToggleListener)
    
    # self.__DICOMFrame = ctk.ctkCollapsibleButton()
    # self.__DICOMFrame.text = "DICOM Input"
    # self.__DICOMFrame.collapsed = 1
    # dicomFrame = qt.QFormLayout(self.__DICOMFrame)
    # self.__layout.addRow(self.__DICOMFrame)

    # # voiGroupBox = qt.QGroupBox()
    # # voiGroupBox.setTitle( 'DICOM' )
    # dicomFrame.addRow(self.toggleListener)
    # # dicomFrame.addRow( voiGroupBox )
    # # voiGroupBoxLayout = qt.QFormLayout( voiGroupBox )
    # self.dicomApp = ctk.ctkDICOMAppWidget()
    # #voiGroupBoxLayout.addRow( self.dicomApp )
    # self.detailsPopup = DICOMLib.DICOMDetailsPopup(self.dicomApp,True)
    # self.exportButton = qt.QPushButton('Export Slicer Data to Study...')
    # self.loadButton = qt.QPushButton('Load to Slicer')
    # self.previewLabel = qt.QLabel()
    # self.tree = self.detailsPopup.tree
    
    # self.showBrowser = qt.QPushButton('Show DICOM Browser')
    # dicomFrame.addRow(self.showBrowser)
    # self.showBrowser.connect('clicked()', self.detailsPopup.open)

    # # the recent activity frame
    
    # self.recentActivity = DICOMLib.DICOMRecentActivityWidget(self.__DICOMFrame,detailsPopup=self.detailsPopup)
    # self.__DICOMFrame.layout().addWidget(self.recentActivity.widget)
    # self.requestUpdateRecentActivity()
    
    # if not slicer.dicomDatabase:
    #   self.promptForDatabaseDirectory()
    # else:
    #   self.onDatabaseDirectoryChanged(self.dicomApp.databaseDirectory)
    # if hasattr(slicer, 'dicomListener'):
    #   slicer.dicomListener.fileToBeAddedCallback = self.onListenerToAddFile
    #   slicer.dicomListener.fileAddedCallback = self.onListenerAddedFile
    
    # self.contextMenu = qt.QMenu(self.tree)
    # self.exportAction = qt.QAction("Export to Study", self.contextMenu)
    # self.contextMenu.addAction(self.exportAction)
    # self.exportAction.enabled = False
    # self.deleteAction = qt.QAction("Delete", self.contextMenu)
    # self.contextMenu.addAction(self.deleteAction)
    # self.contextMenu.connect('triggered(QAction*)', self.onContextMenuTriggered)
    
    # self.dicomApp.connect('databaseDirectoryChanged(QString)', self.onDatabaseDirectoryChanged)
    # selectionModel = self.tree.selectionModel()
    # # TODO: can't use this because QList<QModelIndex> is not visible in PythonQt
    # #selectionModel.connect('selectionChanged(QItemSelection, QItemSelection)', self.onTreeSelectionChanged)
    # self.tree.connect('clicked(QModelIndex)', self.onTreeClicked)
    # self.tree.setContextMenuPolicy(3)
    # self.tree.connect('customContextMenuRequested(QPoint)', self.onTreeContextMenuRequested)


    # # enable to the Send button of the app widget and take it over
    # # for our purposes - TODO: fix this to enable it at the ctkDICOM level
    # self.sendButton = slicer.util.findChildren(self.dicomApp, text='Send')[0]
    # self.sendButton.enabled = False
    # self.sendButton.connect('clicked()', self.onSendClicked)
    # self.updateWidgetFromParameters(self.parameterNode())

    self.__layout.addRow( baselineScanLabel, self.__baselineVolumeSelector )

    qt.QTimer.singleShot(0, self.killButton)
      
  def killButton(self):
    # hide useless button
    bl = slicer.util.findChildren(text='NeedleSegmentation')
    if len(bl):
      bl[0].hide()


  def loadData(self):
    slicer.util.openAddDataDialog()

  def validate( self, desiredBranchId ):
    '''
    '''
    pNode = self.parameterNode()
    volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()

    if pNode.GetParameter('skip') != '1':
      self.__parent.validate( desiredBranchId )
      # check here that the selectors are not empty
      
      baseline = self.__baselineVolumeSelector.currentNode()
      template=slicer.util.getNode('Template')
      obturator = slicer.util.getNode('Obturator_reg')

      df = template.GetDisplayNode()
      do = obturator.GetDisplayNode()
      df.SetSliceIntersectionVisibility(0)
      do.SetSliceIntersectionVisibility(0)
      #print template.GetID()

      if baseline != None and template != None and obturator != None:
        baselineID = baseline.GetID()
        templateID = template.GetID()
        obturatorID = obturator.GetID()
      
        pNode = self.parameterNode()
        pNode.SetParameter('baselineVolumeID', baselineID)
        pNode.SetParameter('templateID', templateID)
        pNode.SetParameter('obturatorID', obturatorID)

        self.__parent.validate( desiredBranchId )
        self.__parent.validationSucceeded(desiredBranchId)
       
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
    #print pNode
    if pNode.GetParameter('skip') != '1':
      self.doStepProcessing()
    #error checking
    if goingTo.id() != 'SelectApplicator' and goingTo.id() != 'FirstRegistration':
      return
    super(iGyneLoadModelStep, self).onExit(goingTo, transitionType) 

  def updateWidgetFromParameters(self, parameterNode):
    baselineVolumeID = parameterNode.GetParameter('baselineVolumeID')
    if baselineVolumeID != None:
      self.__baselineVolumeSelector.setCurrentNode(slicer.mrmlScene.GetNodeByID(baselineVolumeID))

  def doStepProcessing(self):

    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()

    baselineVolume = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('baselineVolumeID'))
    template = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('templateID'))
   
    roiTransformID = pNode.GetParameter('roiTransformID')
    roiTransformNode = None
    
    if roiTransformID != '':
      roiTransformNode = slicer.mrmlScene.GetNodeByID(roiTransformID)
    else:
      roiTransformNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLLinearTransformNode')
      slicer.mrmlScene.AddNode(roiTransformNode)
      pNode.SetParameter('roiTransformID', roiTransformNode.GetID())

    if template != None:
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
    '''
    Load scene with template, obturator and landmarks
    '''
    pNode = self.parameterNode()
    alreadyloaded = pNode.GetParameter("Template-loaded")
    if alreadyloaded != "1":
      if nb == 3:
        pathToScene = slicer.modules.igynepy.path.replace("iGynePy.py","Resources/Template/3points/Template.mrml")
      elif nb ==4:
        pathToScene = slicer.modules.igynepy.path.replace("iGynePy.py","Resources/Template/4points/Template.mrml")
      # slicer.util.loadScene( pathToScene, True)
      slicer.util.loadScene( pathToScene)
      self.loadTemplateButton.setEnabled(0)
      pNode.SetParameter("Template-loaded","1")

  #------------------------------------------------------------------------------------
  '''Download Sample Data'''
  #------------------------------------------------------------------------------------
  def logMessage(self,message):
    self.log.insertHtml(message)
    self.log.insertPlainText('\n')
    self.log.ensureCursorVisible()
    self.log.repaint()
    slicer.app.processEvents(qt.QEventLoop.ExcludeUserInputEvents)

  def downloadPhantom(self):
    filePath = self.downloadFileIntoCache('http://slicer.kitware.com/midas3/download?items=11319', 'phantomGYN.nrrd')
    return self.loadVolume(filePath, 'phantomGYN')

  def downloadFileIntoCache(self, uri, name):
    destFolderPath = slicer.mrmlScene.GetCacheManager().GetRemoteCacheDirectory()
    return self.downloadFile(uri, destFolderPath, name)

  def humanFormatSize(self,size):
    """ from http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size"""
    for x in ['bytes','KB','MB','GB']:
      if size < 1024.0 and size > -1024.0:
        return "%3.1f%s" % (size, x)
      size /= 1024.0
    return "%3.1f%s" % (size, 'TB')

  def reportHook(self,blocksSoFar,blockSize,totalSize):
    percent = int((100. * blocksSoFar * blockSize) / totalSize)
    if percent == 100 or (percent - self.downloadPercent >= 10):
      humanSizeSoFar = self.humanFormatSize(blocksSoFar * blockSize)
      humanSizeTotal = self.humanFormatSize(totalSize)
      self.logMessage('<i>Downloaded %s (%d%% of %s)...</i>' % (humanSizeSoFar, percent, humanSizeTotal))
      self.downloadPercent = percent

  def downloadFile(self, uri, destFolderPath, name):
    filePath = destFolderPath + '/' + name
    if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
      import urllib
      self.logMessage('<b>Requesting download</b> <i>%s</i> from %s...\n' % (name, uri))
      # add a progress bar
      self.downloadPercent = 0
      try:
        urllib.urlretrieve(uri, filePath, self.reportHook)
        self.logMessage('<b>Download finished</b>')
      except IOError as e:
        self.logMessage('<b><font color="red">\tDownload failed: %s</font></b>' % e)
    else:
      self.logMessage('<b>File already exists in cache - reusing it.</b>')
    return filePath

  def loadVolume(self, uri, name):
    self.logMessage('<b>Requesting load</b> <i>%s</i> from %s...\n' % (name, uri))
    success, volumeNode = slicer.util.loadVolume(uri, properties = {'name' : name}, returnNode=True)
    if success:
      self.logMessage('<b>Load finished</b>\n')
    else:
      self.logMessage('<b><font color="red">\tLoad failed!</font></b>\n')
    return volumeNode
      
  #--------------------------------------------#
  '''
  DICOM functions
  '''
      
  # def onDatabaseChanged(self):
  #   """Use this because to update the view in response to things
  #   like database inserts.  Ideally the model would do this
  #   directly based on signals from the SQLite database, but
  #   that is not currently available.
  #   https://bugreports.qt-project.org/browse/QTBUG-10775
  #   """
  #   self.dicomApp.suspendModel()
  #   self.requestResumeModel()
  #   self.requestUpdateRecentActivity()

  # def requestUpdateRecentActivity(self):
  #   """This method serves to compress the requests for updating
  #   the recent activity widget since it is time consuming and there can be
  #   many of them coming in a rapid sequence when the 
  #   database is active"""
  #   if self.updateRecentActivityRequested:
  #     return
  #   self.updateRecentActivityRequested = True
  #   qt.QTimer.singleShot(500, self.onUpateRecentActivityRequestTimeout)

  # def onUpateRecentActivityRequestTimeout(self):
  #   self.recentActivity.update()
  #   self.updateRecentActivityRequested = False

  # def requestResumeModel(self):
  #   """This method serves to compress the requests for resuming
  #   the dicom model since it is time consuming and there can be
  #   many of them coming in a rapid sequence when the 
  #   database is active"""
  #   if self.resumeModelRequested:
  #     return
  #   self.resumeModelRequested = True
  #   qt.QTimer.singleShot(500, self.onResumeModelRequestTimeout)

  # def onResumeModelRequestTimeout(self):
  #   self.dicomApp.resumeModel()
  #   self.resumeModelRequested = False

  # def onDatabaseDirectoryChanged(self,databaseDirectory):
  #   if not hasattr(slicer, 'dicomDatabase') or not slicer.dicomDatabase:
  #     slicer.dicomDatabase = ctk.ctkDICOMDatabase()
  #     self.setDatabasePrecacheTags()
  #   databaseFilepath = databaseDirectory + "/ctkDICOM.sql"
  #   if not (os.access(databaseDirectory, os.W_OK) and os.access(databaseDirectory, os.R_OK)):
  #     self.messageBox('The database file path "%s" cannot be opened.' % databaseFilepath)
  #   else:
  #     slicer.dicomDatabase.openDatabase(databaseDirectory + "/ctkDICOM.sql", "SLICER")
  #     if not slicer.dicomDatabase.isOpen:
  #       self.messageBox('The database file path "%s" cannot be opened.' % databaseFilepath)
  #       self.dicomDatabase = None
  #     else:
  #       if self.dicomApp:
  #         if self.dicomApp.databaseDirectory != databaseDirectory:
  #           self.dicomApp.databaseDirectory = databaseDirectory
  #       else:
  #         settings = qt.QSettings()
  #         settings.setValue('DatabaseDirectory', databaseDirectory)
  #         settings.sync()
  #   if slicer.dicomDatabase:
  #     slicer.app.setDICOMDatabase(slicer.dicomDatabase)

  # def setDatabasePrecacheTags(self):
  #   """query each plugin for tags that should be cached on import
  #      and set them for the dicom app widget and slicer"""
  #   tagsToPrecache = list(slicer.dicomDatabase.tagsToPrecache)
  #   for pluginClass in slicer.modules.dicomPlugins:
  #     plugin = slicer.modules.dicomPlugins[pluginClass]()
  #     tagsToPrecache += plugin.tags.values()
  #   tagsToPrecache = list(set(tagsToPrecache))  # remove duplicates
  #   tagsToPrecache.sort()
  #   if hasattr(slicer, 'dicomDatabase'):
  #     slicer.dicomDatabase.tagsToPrecache = tagsToPrecache
  #   if self.dicomApp:
  #     self.dicomApp.tagsToPrecache = tagsToPrecache

  # def promptForDatabaseDirectory(self):
  #   """Ask the user to pick a database directory.
  #   But, if the application is in testing mode, just pick
  #   a temp directory
  #   """
  #   commandOptions = slicer.app.commandOptions()
  #   if commandOptions.testingEnabled:
  #     databaseDirectory = slicer.app.temporaryPath + '/tempDICOMDatbase'
  #     qt.QDir().mkpath(databaseDirectory)
  #     self.onDatabaseDirectoryChanged(databaseDirectory)
  #   else:
  #     settings = qt.QSettings()
  #     databaseDirectory = settings.value('DatabaseDirectory')
  #     if databaseDirectory:
  #       self.onDatabaseDirectoryChanged(databaseDirectory)
  #     else:
  #       fileDialog = ctk.ctkFileDialog(slicer.util.mainWindow())
  #       fileDialog.setWindowModality(1)
  #       fileDialog.setWindowTitle("Select DICOM Database Directory")
  #       fileDialog.setFileMode(2) # prompt for directory
  #       fileDialog.connect('fileSelected(QString)', self.onDatabaseDirectoryChanged)
  #       label = qt.QLabel("<p><p>The Slicer DICOM module stores a local database with an index to all datasets that are <br>pushed to slicer, retrieved from remote dicom servers, or imported.<p>Please select a location for this database where you can store the amounts of data you require.<p>Be sure you have write access to the selected directory.", fileDialog)
  #       fileDialog.setBottomWidget(label)
  #       fileDialog.exec_()

  # def onTreeClicked(self,index):
  #   self.model = index.model()
  #   self.tree.setExpanded(index, not self.tree.expanded(index))
  #   self.selection = index.sibling(index.row(), 0)
  #   typeRole = self.selection.data(self.dicomModelTypeRole)
  #   if typeRole > 0:
  #     self.sendButton.enabled = True
  #   else:
  #     self.sendButton.enabled = False
  #   if typeRole:
  #     self.exportAction.enabled = self.dicomModelTypes[typeRole] == "Study"
  #   else:
  #     self.exportAction.enabled = False
  #   self.detailsPopup.open()
  #   uid = self.selection.data(self.dicomModelUIDRole)
  #   role = self.dicomModelTypes[self.selection.data(self.dicomModelTypeRole)]
  #   self.detailsPopup.offerLoadables(uid, role)

  # def onTreeContextMenuRequested(self,pos):
  #   index = self.tree.indexAt(pos)
  #   self.selection = index.sibling(index.row(), 0)
  #   self.contextMenu.popup(self.tree.mapToGlobal(pos))

  # def onContextMenuTriggered(self,action):
  #   if action == self.deleteAction:
  #     typeRole = self.selection.data(self.dicomModelTypeRole)
  #     role = self.dicomModelTypes[typeRole]
  #     uid = self.selection.data(self.dicomModelUIDRole)
  #     if self.okayCancel('This will remove references from the database\n(Files will not be deleted)\n\nDelete %s?' % role):
  #       # TODO: add delete option to ctkDICOMDatabase
  #       self.dicomApp.suspendModel()
  #       if role == "Patient":
  #         removeWorked = slicer.dicomDatabase.removePatient(uid)
  #       elif role == "Study":
  #         removeWorked = slicer.dicomDatabase.removeStudy(uid)
  #       elif role == "Series":
  #         removeWorked = slicer.dicomDatabase.removeSeries(uid)
  #       if not removeWorked:
  #         self.messageBox(self,"Could not remove %s" % role,title='DICOM')
  #       self.dicomApp.resumeModel()
  #   elif action == self.exportAction:
  #     self.onExportClicked()

  # def onExportClicked(self):
  #   """Associate a slicer volume as a series in the selected dicom study"""
  #   uid = self.selection.data(self.dicomModelUIDRole)
  #   exportDialog = DICOMLib.DICOMExportDialog(uid,onExportFinished=self.onExportFinished)
  #   self.dicomApp.suspendModel()
  #   exportDialog.open()

  # def onExportFinished(self):
  #   self.requestResumeModel()

  # def onSendClicked(self):
  #   """Perform a dicom store of slicer data to a peer"""
  #   # TODO: this should migrate to ctk for a more complete implementation
  #   # - just the basics for now
  #   uid = self.selection.data(self.dicomModelUIDRole)
  #   role = self.dicomModelTypes[self.selection.data(self.dicomModelTypeRole)]
  #   studies = []
  #   if role == "Patient":
  #     studies = slicer.dicomDatabase.studiesForPatient(uid)
  #   if role == "Study":
  #     studies = [uid]
  #   series = []
  #   if role == "Series":
  #     series = [uid]
  #   else:
  #     for study in studies:
  #       series += slicer.dicomDatabase.seriesForStudy(study)
  #   files = []
  #   for serie in series:
  #     files += slicer.dicomDatabase.filesForSeries(serie)
  #   sendDialog = DICOMLib.DICOMSendDialog(files)
  #   sendDialog.open()

  # def setBrowserPersistence(self,onOff):
  #   self.detailsPopup.setModality(not onOff)
  #   self.browserPersistent = onOff

  # def onToggleListener(self):
  #   if hasattr(slicer, 'dicomListener'):
  #     slicer.dicomListener.stop()
  #     del slicer.dicomListener
  #     self.toggleListener.text = "Start Listener"
  #   else:
  #     try:
  #       slicer.dicomListener = DICOMLib.DICOMListener(database=slicer.dicomDatabase)
  #       slicer.dicomListener.start()
  #       self.onListenerStateChanged(slicer.dicomListener.process.state())
  #       slicer.dicomListener.process.connect('stateChanged(QProcess::ProcessState)',self.onListenerStateChanged)
  #       slicer.dicomListener.fileToBeAddedCallback = self.onListenerToAddFile
  #       slicer.dicomListener.fileAddedCallback = self.onListenerAddedFile
  #       self.toggleListener.text = "Stop Listener"
  #     except UserWarning as message:
  #       self.messageBox(self,"Could not start listener:\n %s" % message,title='DICOM')

  # def onListenerStateChanged(self,newState):
  #   """ Called when the indexer process state changes
  #   so we can provide feedback to the user
  #   """
  #   if newState == 0:
  #     slicer.util.showStatusMessage("DICOM Listener not running")
  #   if newState == 1:
  #     slicer.util.showStatusMessage("DICOM Listener starting")
  #   if newState == 2:
  #     slicer.util.showStatusMessage("DICOM Listener running")

  # def onListenerToAddFile(self):
  #   """ Called when the indexer is about to add a file to the database.
  #   Works around issue where ctkDICOMModel has open queries that keep the
  #   database locked.
  #   """
  #   self.dicomApp.suspendModel()

  # def onListenerAddedFile(self):
  #   """Called after the listener has added a file.
  #   Restore and refresh the app model
  #   """
  #   newFile = slicer.dicomListener.lastFileAdded
  #   if newFile:
  #     slicer.util.showStatusMessage("Loaded: %s" % newFile, 1000)
  #   self.requestResumeModel()

  # def onToggleServer(self):
  #   if self.testingServer and self.testingServer.qrRunning():
  #     self.testingServer.stop()
  #     self.toggleServer.text = "Start Testing Server"
  #   else:
  #     #
  #     # create&configure the testingServer if needed, start the server, and populate it
  #     #
  #     if not self.testingServer:
  #       # find the helper executables (only works on build trees
  #       # with standard naming conventions)
  #       self.exeDir = slicer.app.slicerHome 
  #       if slicer.app.intDir:
  #         self.exeDir = self.exeDir + '/' + slicer.app.intDir
  #       self.exeDir = self.exeDir + '/../CTK-build/DCMTK-build'

  #       # TODO: deal with Debug/RelWithDebInfo on windows

  #       # set up temp dir
  #       tmpDir = slicer.app.settings().value('Modules/TemporaryDirectory')
  #       if not os.path.exists(tmpDir):
  #         os.mkdir(tmpDir)
  #       self.tmpDir = tmpDir + '/DICOM'
  #       if not os.path.exists(self.tmpDir):
  #         os.mkdir(self.tmpDir)
  #       self.testingServer = DICOMLib.DICOMTestingQRServer(exeDir=self.exeDir,tmpDir=self.tmpDir)

  #     # look for the sample data to load (only works on build trees
  #     # with standard naming conventions)
  #     self.dataDir =  slicer.app.slicerHome + '/../../Slicer4/Testing/Data/Input/CTHeadAxialDicom'
  #     files = glob.glob(self.dataDir+'/*.dcm')

  #     # now start the server
  #     self.testingServer.start(verbose=self.verboseServer.checked,initialFiles=files)
  #     self.toggleServer.text = "Stop Testing Server"

  # def onRunListenerAtStart(self):
  #   settings = qt.QSettings()
  #   settings.setValue('DICOM/RunListenerAtStart', self.runListenerAtStart.checked)

  # def messageBox(self,text,title='DICOM'):
  #   self.mb = qt.QMessageBox(slicer.util.mainWindow())
  #   self.mb.setWindowTitle(title)
  #   self.mb.setText(text)
  #   self.mb.setWindowModality(1)
  #   self.mb.exec_()
  #   return

  # def question(self,text,title='DICOM'):
  #   return qt.QMessageBox.question(slicer.util.mainWindow(), title, text, 0x14000) == 0x4000

  # def okayCancel(self,text,title='DICOM'):
  #   return qt.QMessageBox.question(slicer.util.mainWindow(), title, text, 0x400400) == 0x400
