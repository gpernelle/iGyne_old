from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
import PythonQt
import string
import json
import time

class iGyneFirstRegistrationStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '4. Register the template' )
    self.setDescription( 'Register the template based on 3 or 4 fiducial points. \
    If you previously chose 3pts, choose them counterclockwise, starting from the one in the middle.\
      Otherwise, start from the top left corner' )
    self.__parent = super( iGyneFirstRegistrationStep, self )
    self.interactorObserverTags = []    
    self.styleObserverTags = []
    self.volume = None
    self.fixedLandmarks = None
    self.movingLandmarks = None
    self.__roiTransformNode = None
    self.__baselineVolume = None
    self.__roi = None
    self.__roiObserverTag = None
    self.RMS = 0
    self.__threshold = [ -1, -1 ]  
    self.__roiSegmentationNode = None
    self.__roiVolume = None
    self.click = 0
    self.register = 0

  def createUserInterface( self ):
    '''
    '''
    self.__layout = self.__parent.createUserInterface()
     
    self.fiducialButton = qt.QPushButton('Choose Fiducial Points')
    self.fiducialButton.checkable = True
    self.__layout.addRow(self.fiducialButton)
    self.fiducialButton.connect('toggled(bool)', self.onRunButtonToggled)
  
    self.firstRegButton = qt.QPushButton('Run Initial Registration')
    self.__registrationStatus = qt.QLabel('Register Template and Scan')
    self.__layout.addRow(self.__registrationStatus, self.firstRegButton)
    self.firstRegButton.checkable = False
    self.__layout.addRow(self.firstRegButton)
    self.firstRegButton.connect('clicked()', self.firstRegistration)

    # define cropping area
    self.drawRectlangelButton = qt.QPushButton('Outline Area Containing Fiducial Points')
    self.drawRectlangelButton.checkable = True
    self.__layout.addRow(self.drawRectlangelButton)
    self.drawRectlangelButton.connect('toggled(bool)',self.onDrawRectangleButtonToggled)

    # option for horizontal template
    self.horizontalTemplate=qt.QCheckBox('Horizontal Template?')
    self.__layout.addRow(self.horizontalTemplate)
    
    self.automaticRegistrationButton = qt.QPushButton('Automatic Registration')
    self.automaticRegistrationButton.connect('clicked()', self.automaticRegistration)
    self.__layout.addRow(self.automaticRegistrationButton)
    
    # Hough parameters - Cropping box: used to limit the volume where to find the circles
    self.__houghFrame = ctk.ctkCollapsibleButton()
    self.__houghFrame.text = "Hough Transform Parameters"
    self.__houghFrame.collapsed = 1
    houghFrame = qt.QFormLayout(self.__houghFrame)
    
    # Auto-value option
    self.autoLimit = qt.QCheckBox('Auto limit Hought Transform computation volume?')
    self.autoLimit.checked = True
    houghFrame.addRow(self.autoLimit)

    # Auto-value option
    self.autoValue = qt.QCheckBox('Automatic values?')
    self.autoValue.checked = True
    houghFrame.addRow(self.autoValue)

    # Ratio height
    self.ratioHeightCroppedVolume = qt.QSpinBox()
    self.ratioHeightCroppedVolume.setMinimum(1)
    self.ratioHeightCroppedVolume.setMaximum(15)
    self.ratioHeightCroppedVolume.setValue(2)
    ratioHeightCroppedVolumeLabel = qt.QLabel("Divide the height by: ")
    houghFrame.addRow(ratioHeightCroppedVolumeLabel, self.ratioHeightCroppedVolume)
    # Ratio width
    self.ratioWidthCroppedVolume = qt.QSpinBox()
    self.ratioWidthCroppedVolume.setMinimum(1)
    self.ratioWidthCroppedVolume.setMaximum(15)
    self.ratioWidthCroppedVolume.setValue(4)
    ratioWidthCroppedVolumeLabel = qt.QLabel("Divide the width by: ")
    houghFrame.addRow(ratioWidthCroppedVolumeLabel, self.ratioWidthCroppedVolume)
    # Ratio length
    self.ratioLengthCroppedVolume = qt.QSpinBox()
    self.ratioLengthCroppedVolume.setMinimum(1)
    self.ratioLengthCroppedVolume.setMaximum(15)
    self.ratioLengthCroppedVolume.setValue(4)
    ratioLengthCroppedVolumeLabel = qt.QLabel("Divide the length by: ")
    houghFrame.addRow(ratioLengthCroppedVolumeLabel, self.ratioLengthCroppedVolume)


    # Threshold slider for template segmentation
    threshLabel = qt.QLabel('Threshold for CHT:')
    self.__threshRange = slicer.qMRMLRangeWidget()
    self.__threshRange.decimals = 0
    self.__threshRange.singleStep = 1
    self.__threshRange.minimum = 80
    self.__threshRange.minimumValue = 110
    self.__threshRange.maximum = 255
    self.__threshRange.maximumValue = 255
    houghFrame.addRow(threshLabel,self.__threshRange)
    self.__layout.addRow(self.__houghFrame)

    # reset module button 
    # resetButton = qt.QPushButton( 'Reset Module' )
    # resetButton.connect( 'clicked()', self.onResetButton )
    # self.__layout.addWidget( resetButton )
    qt.QTimer.singleShot(0, self.killButton)
      
  def killButton(self):
    # hide useless button
    bl = slicer.util.findChildren(text='NeedleSegmentation')
    if len(bl):
      bl[0].hide()

  def onResetButton( self ):
    '''
    '''
    self.workflow().goBackward() # 3
    self.workflow().goBackward() # 2
    self.workflow().goBackward() # 1

  def ijk2ras(self,A,volumeNode):
    m=vtk.vtkMatrix4x4()
    # volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
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

  def cropTemplateArea(self):
    # TODO: draw a rectangle with the mouse
    # observer: left button pressed -> get XYZ / left button released -> get XYZ
    volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
    imageData = volumeNode.GetImageData()
    imageDimensions = imageData.GetDimensions()
    m = vtk.vtkMatrix4x4()
    volumeNode.GetIJKToRASMatrix(m)
    
    if self.autoValue.isChecked():
      hValue = round(m.GetElement(2,2)*imageDimensions[2]/float(25))
      self.ratioHeightCroppedVolume.setValue(max(1,hValue-4))
    # create ROI
    if self.autoLimit.isChecked():
      a=self.ratioLengthCroppedVolume.value
      b=self.ratioWidthCroppedVolume.value
      c=self.ratioHeightCroppedVolume.value
    else:
      a,b,c=1,1,1
    roi = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationROINode')
    slicer.mrmlScene.AddNode(roi)
    roi.SetROIAnnotationVisibility(1)
    roi.SetRadiusXYZ(imageDimensions[0]/a,imageDimensions[1]/b,imageDimensions[2]/c)
    roi.SetXYZ(0,0,m.GetElement(2,3)+imageDimensions[2]/c)
    roi.SetLocked(1)

    #crop volume
    cropVolumeNode =slicer.mrmlScene.CreateNodeByClass('vtkMRMLCropVolumeParametersNode')
    cropVolumeNode.SetScene(slicer.mrmlScene)
    cropVolumeNode.SetName('obturator_CropVolume_node')
    cropVolumeNode.SetIsotropicResampling(False)
    slicer.mrmlScene.AddNode(cropVolumeNode)
    cropVolumeNode.SetInputVolumeNodeID(volumeNode.GetID())
    cropVolumeNode.SetROINodeID(roi.GetID())
    cropVolumeLogic = slicer.modules.cropvolume.logic()
    cropVolumeLogic.Apply(cropVolumeNode)
    roiVolume = slicer.mrmlScene.GetNodeByID(cropVolumeNode.GetOutputVolumeNodeID())
    roiVolume.SetName("template-area-ROI")
    return roiVolume

  def automaticRegistration(self):
    '''
    Detect the brigh circles in the MR volume, corresponding to the Vitamin E
    capsules positioned at the corners of the obturator
    Use Hough transform CLI module
    '''
    self.inputVolume = self.cropTemplateArea()
    outputVolume = slicer.mrmlScene.CreateNodeByClass('vtkMRMLScalarVolumeNode')
    slicer.mrmlScene.AddNode(outputVolume)
    
    # Hough transform parameters
    parameters = {}
    parameters["inputVolume"] = self.inputVolume
    parameters["outputVolume"] = outputVolume
    parameters["numberOfSpheres"] = 8
    parameters["minRadius"] = 0
    parameters["maxRadius"] = 8
    parameters["sigmaGradient"] = 2000
    parameters["variance"] = 0.7
    parameters["sphereRadiusRatio"] = 12
    parameters["votingRadiusRatio"] = 10
    parameters["threshold"] = self.__threshRange.minimumValue
    parameters["outputThreshold"] = 0.1
    parameters["gradientThreshold"] = 100
    parameters["nbOfThreads"] = 8
    parameters["samplingRatio"] = 1
    
    houghtransformcli = slicer.modules.houghtransformcli
    self.__cliNode = None
    self.__cliNode = slicer.cli.run(houghtransformcli, self.__cliNode, parameters)
    self.__cliObserverTag = self.__cliNode.AddObserver('ModifiedEvent', self.processRegistrationCompletion)
    self.__registrationStatus.setText('Wait ...')
    self.__cliObserverTag = self.__cliNode.AddObserver('ModifiedEvent', self.processDataHoughTransform)
    self.__registrationStatus.setText('Wait ...')
    self.firstRegButton.setEnabled(0)

  def processDataHoughTransform(self, node, event):
    '''
    Filter ans sort the detected circles found by the Hough transform.
    The order must correspond to the order of the landmarks
    '''
    pNode=self.parameterNode()
    status = node.GetStatusString()
    self.__registrationStatus.setText('Hough Transforn '+status)
    if status == 'Completed':
      self.firstRegButton.setEnabled(1)

      # first remove previously detected circle if some exist
      fixedAnnotationList = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('fixedLandmarksListID'))
      if fixedAnnotationList != None:
        fixedAnnotationList.RemoveAllChildrenNodes()

      # read the file where the output of the hough transform has been written
      file = open("./output.txt", "r").readlines()
      sphereCenters = [[0,0,0] for i in range(9)]
      nbLine = 0
      for line in file:
        if len(line) >= 10:
          sphereCenters[nbLine] = self.ijk2ras(json.loads(line),self.inputVolume)
        nbLine += 1
      for i in range(nbLine+1):
        for j in range(nbLine+1): 
          if i != j and sphereCenters[i]!=[0,0,0]:
            d2 = (sphereCenters[i][0]-sphereCenters[j][0])**2+(sphereCenters[i][1]-sphereCenters[j][1])**2+(sphereCenters[i][2]-sphereCenters[j][2])**2
            d = d2**0.5
            # print sphereCenters[i],sphereCenters[j]
            # print d
       
      point = [0]
      for i in range(nbLine+1):
        U,V,W = 0,0,0
        for j in range(nbLine+1): 
          if i != j and sphereCenters[i]!=[0,0,0]:
            d2 = (sphereCenters[i][0]-sphereCenters[j][0])**2+(sphereCenters[i][1]-sphereCenters[j][1])**2+(sphereCenters[i][2]-sphereCenters[j][2])**2
            d = d2**0.5
            # print sphereCenters[i],sphereCenters[j]
            print d
            if d >=45 and d<=53:
              U += 1
            elif d >53 and d<60:  
              V +=1
            elif d >=70 and d<80:  
              W +=1 
        print U,V,W      
        if U+V+W>=3:
          print sphereCenters[i]
          point.extend([i])

      point.remove(0)
      minX = [999,999,999,999]
      maxX = [-999,-999,-999,-999]
      
      print point
      print sphereCenters
      sorted = [[0,0,0] for l in range(4)]
      sortedConverted = [[0,0,0] for l in range(4)]
      for i in range(2):  
        for k in point:
          if sphereCenters[k][0]<= minX[0]:
            minX[0] = sphereCenters[k][0]
            minX[1] = k
          elif sphereCenters[k][0]<= minX[2]:
            minX[2] = sphereCenters[k][0]
            minX[3] = k
          if sphereCenters[k][0]>= maxX[0]:
            maxX[0] = sphereCenters[k][0]
            maxX[1] = k
          elif sphereCenters[k][0]>= maxX[2]:
            maxX[2] = sphereCenters[k][0]
            maxX[3] = k    

      if sphereCenters[minX[1]][1] < sphereCenters[minX[3]][1]:
        sorted[0] = minX[1]
        sorted[1] = minX[3]
      else:
        sorted[0] = minX[3]
        sorted[1] = minX[1]      
        
      if sphereCenters[maxX[1]][1]>sphereCenters[maxX[3]][1]:
        sorted[2] = maxX[1]
        sorted[3] = maxX[3]
      else:
        sorted[2] = maxX[3]
        sorted[3] = maxX[1]
      
      sorted2 = [0,0,0,0]
      print self.horizontalTemplate
      if self.horizontalTemplate.isChecked():
        sorted2[0]=sorted[2]
        sorted2[2]=sorted[0]
        sorted2[1]=sorted[3]
        sorted2[3]=sorted[1]
      else:
        sorted2[0]=sorted[3]
        sorted2[2]=sorted[1]
        sorted2[1]=sorted[0]
        sorted2[3]=sorted[2]
      
      ijkToRAS = vtk.vtkMatrix4x4()  
      
      logic = slicer.modules.annotations.logic()
      logic.SetActiveHierarchyNodeID(pNode.GetParameter('fixedLandmarksListID'))
      if pNode.GetParameter("Template")=='4points':
        nbPoints=4
      elif pNode.GetParameter("Template")=='3pointsCorners':
        nbPoints=3
      for k in range(nbPoints) :  
        fiducial = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationFiducialNode')
        fiducial.SetReferenceCount(fiducial.GetReferenceCount()-1)
        fiducial.SetFiducialCoordinates(sphereCenters[sorted2[k]])
        fiducial.SetName(str(k)) 
        fiducial.Initialize(slicer.mrmlScene)
        # adding to hierarchy is handled by the Reporting logic
        # self.fixedLandmarks.AddItem(fiducial)
    
      sRed = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
      if sRed ==None :
        sRed = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNode1")        
      
      # sRed.SetSliceVisible(1)
     
      m= sRed.GetSliceToRAS()
      m.SetElement(0,3,sortedConverted[3][0])
      m.SetElement(1,3,sortedConverted[3][1])
      m.SetElement(2,3,sortedConverted[3][2])
      sRed.Modified()
    
    self.firstRegistration()
    
  def onRunButtonToggled(self, checked):
    if checked:
      self.start('fiducials')
      self.fiducialButton.text = "Stop"  
    else:
      self.stop()
      self.fiducialButton.text = "Choose Fiducial Points"

  def onDrawRectangleButtonToggled(self, checked):
    if checked:
      self.start('rectangle')
      self.drawRectlangelButton.text = "Stop"  
    else:
      self.stop()
      self.drawRectlangelButton.text = "Outline Area with Fiducial Markers"

  def firstRegistration(self):
    '''
    landmark registration (fiducial registration CLI Module)
    '''
    pNode = self.parameterNode()
    baselineVolumeID = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
    templateID = pNode.GetParameter('templateID')
    self.__followupTransform = slicer.mrmlScene.GetNodeByID('vtkMRMLLinearTransformNode4')
    slicer.mrmlScene.AddNode(self.__followupTransform)
    sliceNodeCount = slicer.mrmlScene.GetNumberOfNodesByClass('vtkMRMLAnnotationHierarchyNode')
    self.movingLandmarks = vtk.vtkCollection()
    for nodeIndex in xrange(sliceNodeCount):
      sliceNode = slicer.mrmlScene.GetNthNodeByClass(nodeIndex, 'vtkMRMLAnnotationHierarchyNode') 
      if sliceNode.GetName() == "Fiducial List_moved":
        sliceNode.GetAssociatedChildrenNodes(self.movingLandmarks)
    
    self.OutputMessage = ""
    parameters = {}
    parameters["fixedLandmarks"] = pNode.GetParameter('fixedLandmarksListID')
    parameters["movingLandmarks"] = pNode.GetParameter('movingLandmarksListID')
    parameters["saveTransform"] = self.__followupTransform
    parameters["transformType"] = "Rigid"
    parameters["rms"] = self.RMS
    parameters["outputMessage"] = self.OutputMessage
    
    fidreg = slicer.modules.fiducialregistration
    self.__cliNode = None
    self.__cliNode = slicer.cli.run(fidreg, self.__cliNode, parameters)
    self.__cliObserverTag = self.__cliNode.AddObserver('ModifiedEvent', self.processRegistrationCompletion)
    self.__registrationStatus.setText('Wait ...')
    self.firstRegButton.setEnabled(0)

  def processRegistrationCompletion(self, node, event):
    status = node.GetStatusString()
    self.__registrationStatus.setText('Registration '+status)
    if status == 'Completed':
      self.firstRegButton.setEnabled(1)
  
      pNode = self.parameterNode()
      templateNode = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('templateID'))
      obturatorNode = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('obturatorID'))
      
      df = templateNode.GetDisplayNode()
      df.SetSliceIntersectionVisibility(1)
      do = obturatorNode.GetDisplayNode()
      do.SetSliceIntersectionVisibility(1)
      
      roiNode = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('roiTransformID'))
      templateNode.SetAndObserveTransformNodeID(self.__followupTransform.GetID())
      obturatorNode.SetAndObserveTransformNodeID(self.__followupTransform.GetID())
      roiNode.SetAndObserveTransformNodeID(self.__followupTransform.GetID())
  
      Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')

      pNode.SetParameter('followupTransformID', self.__followupTransform.GetID())
      self.registered = 1

  def start(self,action):    
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
          if action=='fiducials':
            tag = style.AddObserver(event, self.processEvent)
          elif action=='rectangle':
            tag = style.AddObserver(event, self.processEventRectangle)
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
    if self.fixedLandmarks == None :
      self.fixedLandmarks = vtk.vtkCollection()

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
      
      # print 'xy is:', xy
      # print 'xyz is:', xyz
      # print 'ras is:', ras
      logic = slicer.modules.annotations.logic()
      logic.SetActiveHierarchyNodeID("vtkMRMLAnnotationHierarchyNode4")
      fiducial = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationFiducialNode')
      fiducial.SetReferenceCount(fiducial.GetReferenceCount()-1)
      fiducial.SetFiducialCoordinates(ras)
      pNode = self.parameterNode()

      applicator  = pNode.GetParameter('Template')  
      if applicator == "3points":  
        
        if self.click == 0:
          fiducial.SetName("top")
          self.click += 1
        elif self.click == 1:
          fiducial.SetName("left")
          self.click += 1
        elif self.click == 2:
          fiducial.SetName("right")
          self.click = 0
          self.fiducialButton.setEnabled(0)
          time.sleep(0.5)
          slicer.mrmlScene.Modified()
          self.firstRegistration()
          self.stop()
      
      elif applicator == "4points":  
        
        if self.click == 0:
          fiducial.SetName("1")
          self.click += 1
        elif self.click == 1:
          fiducial.SetName("2")
          self.click += 1
        elif self.click == 2:
          fiducial.SetName("3")
          self.click += 1
        elif self.click == 3:
          fiducial.SetName("4")
          self.click = 0
          self.fiducialButton.setEnabled(0)
          self.firstRegistration()
          self.stop()

      elif applicator == "3pointsCorners":  
        
        if self.click == 0:
          fiducial.SetName("1")
          self.click += 1
        elif self.click == 1:
          fiducial.SetName("2")
          self.click += 1
        elif self.click == 2:
          fiducial.SetName("3")
          self.click += 1
          self.click = 0
          self.fiducialButton.setEnabled(0)
          self.firstRegistration()
          self.stop()
        
      fiducial.Initialize(slicer.mrmlScene)
      self.fixedLandmarks.AddItem(fiducial)
      
  # def processEvent(self,observee,event=None):
  #   '''
  #   get the mouse clicks and create a fiducial node at this position. Used later for the fiducial registration
  #   '''
  #   if self.fixedLandmarks == None :
  #     self.fixedLandmarks = vtk.vtkCollection()

  #   if self.sliceWidgetsPerStyle.has_key(observee) and event == "LeftButtonPressEvent":
  #     if slicer.app.repositoryRevision<= 21022:
  #       sliceWidget = self.sliceWidgetsPerStyle[observee]
  #       style = sliceWidget.sliceView().interactorStyle()          
  #       xy = style.GetInteractor().GetEventPosition()
  #       xyz = sliceWidget.convertDeviceToXYZ(xy)
  #       ras = sliceWidget.convertXYZToRAS(xyz)
  #     else:
  #       sliceWidget = self.sliceWidgetsPerStyle[observee]
  #       sliceLogic = sliceWidget.sliceLogic()
  #       sliceNode = sliceWidget.mrmlSliceNode()
  #       interactor = observee.GetInteractor()
  #       xy = interactor.GetEventPosition()
  #       xyz = sliceWidget.sliceView().convertDeviceToXYZ(xy);
  #       ras = sliceWidget.sliceView().convertXYZToRAS(xyz)

  #     if self.click == 0:
  #       firstCorner=ras
  #       self.click += 1
  #     elif self.click == 1:
  #       lastCorner=ras

  #       #crop volume (IJK or RAS?)
  #   volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
  #   imageData = volumeNode.GetImageData()
  #   imageDimensions = imageData.GetDimensions()
  #   m = vtk.vtkMatrix4x4()
  #   volumeNode.GetIJKToRASMatrix(m)
  #   a = (firstCorner[0]+lastCorner[0])/2
  #   b = (firstCorner[1]+lastCorner[1])/2
  #   c = (firstCorner[2]+lastCorner[2])/2
  #   ra = abs(lastCorner[0]-firstCorner[0])
  #   rb = abs(lastCorner[1]-firstCorner[1])
  #   rc = min(ra/float(rb),rb/float(ra))
  #   roi = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationROINode')
  #   slicer.mrmlScene.AddNode(roi)
  #   roi.SetROIAnnotationVisibility(1)
  #   roi.SetRadiusXYZ(ra,rb,rc)
  #   roi.SetXYZ(a,b,c)
  #   roi.SetLocked(1)

  #   #crop volume
  #   cropVolumeNode =slicer.mrmlScene.CreateNodeByClass('vtkMRMLCropVolumeParametersNode')
  #   cropVolumeNode.SetScene(slicer.mrmlScene)
  #   cropVolumeNode.SetName('template-area_CropVolume_node')
  #   cropVolumeNode.SetIsotropicResampling(False)
  #   slicer.mrmlScene.AddNode(cropVolumeNode)
  #   cropVolumeNode.SetInputVolumeNodeID(volumeNode.GetID())
  #   cropVolumeNode.SetROINodeID(roi.GetID())
  #   cropVolumeLogic = slicer.modules.cropvolume.logic()
  #   cropVolumeLogic.Apply(cropVolumeNode)
  #   roiVolume = slicer.mrmlScene.GetNodeByID(cropVolumeNode.GetOutputVolumeNodeID())
  #   roiVolume.SetName("template-area-ROI")


  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )    
    self.__parent.validationSucceeded(desiredBranchId)

  def onEntry(self,comingFrom,transitionType):
    super(iGyneFirstRegistrationStep, self).onEntry(comingFrom, transitionType)
    pNode = self.parameterNode()
    print pNode
    volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()

    if pNode.GetParameter('skip') != '1' and volumeNode != None:
      
      #hough transform parameters
      imageData = volumeNode.GetImageData()
      imageDimensions = imageData.GetDimensions()
      m = vtk.vtkMatrix4x4()
      volumeNode.GetIJKToRASMatrix(m)
      hValue = round(m.GetElement(2,2)*imageDimensions[2]/float(25))
      self.ratioHeightCroppedVolume.setValue(hValue)

      # setup the interface
      lm = slicer.app.layoutManager()
      lm.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
      pNode = self.parameterNode()
   
      self.__template = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('templateID'))
      self.__baselineVolume = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('baselineVolumeID'))

      pNode.SetParameter('currentStep', self.stepid)
      
      # get ID from fiducial list
      hierarchyNodes = slicer.util.getNodes('vtkMRMLAnnotationHierarchyNode*')
      for hierarchyNode in hierarchyNodes.values():
        if hierarchyNode.GetName()=='Fiducial List_fixed':
          fixedLandmarksListID=hierarchyNode.GetID()
          pNode.SetParameter('fixedLandmarksListID',fixedLandmarksListID)
        elif hierarchyNode.GetName()=='Fiducial List_moving':
          movingLandmarksListID=hierarchyNode.GetID()
          pNode.SetParameter('movingLandmarksListID',movingLandmarksListID)

      # disable automatic registration in case of use of 3 fiducials only (old cases)
      if pNode.GetParameter('Template')=='3points':
        self.automaticRegistrationButton.setEnabled(0)
        self.setDescription( 'Register the template based on 3 fiducial points. Choose the points counterclockwise, starting from the one in the middle.' )
      elif pNode.GetParameter('Template')=='4points':
        self.automaticRegistrationButton.setEnabled(1)
        self.setDescription( 'Register the template based on 4 fiducial points. Choose the points counterclockwise, starting from top left corner.' )

    else:
      self.workflow().goForward() # 5
      
  def onExit(self, goingTo, transitionType):
    pNode = self.parameterNode()
    if pNode.GetParameter('skip') != '1':
      slicer.mrmlScene.RemoveNode(slicer.util.getNode("template-area-ROI"))
      slicer.mrmlScene.RemoveNode(slicer.util.getNode("AnnotationROI*"))
      # hide fiducial nodes
      fiducialNodes = slicer.util.getNodes('vtkMRMLAnnotationFiducialNode*')
      for fiducialNode in fiducialNodes.values():
        fiducialNode.SetDisplayVisibility(0)
        
    if goingTo.id() != 'LoadModel' and goingTo.id() != 'SecondRegistration':
      return
    super(iGyneFirstRegistrationStep, self).onExit(goingTo, transitionType)
