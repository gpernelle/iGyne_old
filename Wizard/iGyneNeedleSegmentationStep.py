from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
from EditorLib import *
import math,time

import string

'''
TODO:
  add advanced option to specify segmentation
'''

class iGyneNeedleSegmentationStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.skip = 1
    self.initialize( stepid )
    self.setName( '6. Needle Segmentation' )
    self.setDescription( 'Segment the needles' )
    self.__parent = super( iGyneNeedleSegmentationStep, self )
    self.analysisGroupBox = None
    self.buttonsGroupBox = None
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
       62:'Fh'}
    

  def createUserInterface( self ):
    '''
    '''
    self.skip = 0
    pNode = self.parameterNode()
    self.__layout = self.__parent.createUserInterface()
    
    #  editor widgetRepresentation
    self.__editorFrame = ctk.ctkCollapsibleButton()
    self.__editorFrame.text = "Editor"
    self.__editorFrame.collapsed = 0
    editorFrame = qt.QFormLayout(self.__editorFrame)
    self.__layout.addRow(self.__editorFrame)
    
    groupbox = qt.QGroupBox()
    groupboxLayout  = qt.QFormLayout(groupbox)
    groupboxLayout.addRow(slicer.modules.editor.widgetRepresentation())
    editorFrame.addRow(groupbox)
    
    needleLabel = qt.QLabel( 'Needle Label:' )
    self.__needleLabelSelector = slicer.qMRMLNodeComboBox()
    self.__needleLabelSelector.toolTip = "Choose the needle-label image"
    self.__needleLabelSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__needleLabelSelector.addAttribute("vtkMRMLScalarVolumeNode", "LabelMap", "1")
    self.__needleLabelSelector.setMRMLScene(slicer.mrmlScene)
    self.__needleLabelSelector.addEnabled = 0
    self.__needleLabelSelector.removeEnabled = 0
    self.__needleLabelSelector.noneEnabled = 0
    self.__layout.connect('mrmlSceneChanged(vtkMRMLScene*)',
                        self.__needleLabelSelector, 'setMRMLScene(vtkMRMLScene*)')
    
    self.__layout.addRow( needleLabel, self.__needleLabelSelector )
    if Helper.getNodeByID(pNode.GetParameter("baselineVolumeID")) == None:
      volumeLabel = qt.QLabel( 'Volume:' )
      self.__volumeSelector = slicer.qMRMLNodeComboBox()
      self.__volumeSelector.toolTip = "Choose the Volume"
      self.__volumeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
      self.__volumeSelector.setMRMLScene(slicer.mrmlScene)
      self.__volumeSelector.addEnabled = 0
      self.__volumeSelector.removeEnabled = 0
      self.__volumeSelector.noneEnabled = 0
      self.__layout.addRow( volumeLabel, self.__volumeSelector )
      self.__layout.connect('mrmlSceneChanged(vtkMRMLScene*)',
                        self.__volumeSelector, 'setMRMLScene(vtkMRMLScene*)')

	
	  #Segment Needle Button 
    self.needleButton = qt.QPushButton('Segment Needles')
    self.__layout.addRow(self.needleButton)
    self.needleButton.connect('clicked()', self.needleSegmentation)
    
    self.updateWidgetFromParameters(self.parameterNode())
    
    
  	#Filter Needles Button
    self.__filterFrame = ctk.ctkCollapsibleButton()
    self.__filterFrame.text = "Filter Needles"
    self.__filterFrame.collapsed = 1
    filterFrame = qt.QFormLayout(self.__filterFrame)
    self.__layout.addRow(self.__filterFrame)
    # Filter spin box
    self.filterValueButton = qt.QSpinBox()
    self.filterValueButton.setMaximum(500)
    fLabel = qt.QLabel("Max Deviation Value: ")
    
   
    self.removeDuplicates = qt.QCheckBox('Remove duplicates by segmenting')
    self.removeDuplicates.setChecked(1)
    self.removeDuplicatesButton = qt.QPushButton('Remove duplicates')
    self.removeDuplicatesButton.connect('clicked()', self.positionFilteringNeedles)
    
    filterNeedlesButton = qt.QPushButton('Filter Needles')
    filterNeedlesButton.connect('clicked()', self.angleFilteringNeedles)
    
    
    
    filterFrame.addRow(self.removeDuplicates)
    filterFrame.addRow(self.removeDuplicatesButton)
    
    filterFrame.addRow(fLabel,self.filterValueButton)
    filterFrame.addRow(filterNeedlesButton)
    
    self.displayFiducialButton = qt.QPushButton('Display Labels On Needles')
    self.displayFiducialButton.connect('clicked()',self.displayFiducial)
    self.analysisReportButton = qt.QPushButton('Print Analysis')
    self.analysisReportButton.connect('clicked()',self.analyzeSegmentation)
    
    
    self.__layout.addRow(self.displayFiducialButton)
    self.__layout.addRow(self.analysisReportButton)
    
  
  def analyzeSegmentation(self):
  
    if self.analysisGroupBox != None:
      self.__layout.removeWidget(self.analysisGroupBox)
      self.analysisGroupBox.deleteLater()
      self.analysisGroupBox = None
    self.analysisGroupBox = qt.QGroupBox()
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
          indice = total/float(nb-1)

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
        
          result = "Needle " + self.option[int(modelNode.GetAttribute("nth"))] + ": Angle Deviation from ref: " + str(angleDeviation)+" Intensity average :" + str(indice) 
          analysisLine = qt.QLabel(result)
          self.analysisGroupBoxLayout.addRow(analysisLine)
        
    else:
    
      m = vtk.vtkMatrix4x4()
      volumeNode = slicer.sliceWidgetRed_sliceLogic.GetBackgroundLayer().GetVolumeNode()
      volumeNode.GetIJKToRASMatrix(m)
      m.Invert()
      imageData = volumeNode.GetImageData()
      
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
        
          indice = total/float(nb-1) 
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
          print tip[0]-base[0],tip[1]-base[1],tip[2]-base[2]
          
          result = "Needle " + self.option[int(modelNode.GetAttribute("nth"))]  +" Intensity average :" + str(indice)
          analysisLine = qt.QLabel(result)
          self.analysisGroupBoxLayout.addRow(analysisLine)
      
  
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
            self.fiducialnode[int(i)].SetVisible(0)
        else:
          displayNode.SetVisibility(1)
          if i !=None and self.fiducialnode[int(i)]!=0:
            self.fiducialnode[int(i)].SetVisible(1)
      
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
    #outputVolumeName = inputImageName.replace(".nrrd","-OutputNeedleModel.vtk")
    #outputVolumeStorageNode.SetFileName(outputVolumeName)
    slicer.mrmlScene.AddNode(self.outputVolumeNode)
    slicer.mrmlScene.AddNode(outputVolumeStorageNode)
    self.outputVolumeNode.AddAndObserveStorageNodeID(outputVolumeStorageNode.GetID())
    outputVolumeStorageNode.WriteData(self.outputVolumeNode)
    
    outputID = self.outputVolumeNode.GetID()
    
    foldername = '/NeedleModels/' + datetime
    
    # Set the parameters for the CLI module    
    parameters = {} 
    parameters['inputVolume'] = inputVolumeID
    parameters['inputLabel'] = inputLabelID
    parameters['outputVtk'] = outputID
    parameters['outputFolderName'] = foldername
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
    self.displaynode = [0 for j in range(63)]
    self.fiducialnode = [0 for j in range(63)]

    for i in xrange(63):
      
      
      pathneedle = foldername+'/'+str(i)+'.vtk'

      self.needlenode[i] = slicer.util.loadModel(pathneedle, True)
      # print pathneedle
      if self.needlenode[i][0] == True:
        self.displaynode[i] = self.needlenode[i][1].GetDisplayNode()
        polydata = self.needlenode[i][1].GetPolyData()
        polydata.GetPoint(0,self.base[i]) 
                
      
        self.displaynode[i].SliceIntersectionVisibilityOn()
        bestmatch = None
        mindist = None
        for j in xrange(63):
          delta = ((self.p[0][j]-(self.base[i][0]))**2+(self.p[1][j]-self.base[i][1])**2)**(0.5)
          if delta < mindist or mindist == None:
            bestmatch = j
            mindist = delta

        self.showOneNeedle(i,0)
        self.displaynode[i].SetColor(self.color[bestmatch])
        self.needlenode[i][1].SetName(self.option[bestmatch]+"_segmented")
        self.needlenode[i][1].SetAttribute("segmented","1")
        self.needlenode[i][1].SetAttribute("nth",str(bestmatch))
    
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
        buttonDisplay.checkable = True
        buttonDisplay.connect("clicked()", lambda who=i: self.displayNeedle(who))
        buttonReformat = qt.QPushButton("Reformat "+self.option[i])
        buttonReformat.connect("clicked()", lambda who=i: self.reformatNeedle(who))
        self.buttonsGroupBoxLayout.addRow(buttonDisplay,buttonReformat)
      

  def displayNeedle(self,i):
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("nth")==str(i):
        print str(i)
        displayNode = modelNode.GetModelDisplayNode()
        nVisibility = displayNode.GetVisibility()
        print nVisibility
        if nVisibility:
          displayNode.SliceIntersectionVisibilityOff()
          displayNode.SetVisibility(0)
        else:
          displayNode.SliceIntersectionVisibilityOn()
          displayNode.SetVisibility(1)
          
  def reformatNeedle(self,i):
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
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
        
        sGreen = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")

        reformatLogic = slicer.vtkSlicerReformatLogic()
        sGreen.SetSliceVisible(1)
        reformatLogic.SetSliceNormal(sGreen,0,-c/b,1)
        m= sGreen.GetSliceToRAS()
        m.SetElement(1,3,base[1])
        m.SetElement(2,3,base[2])
        sGreen.Modified()

      
        
  
  def displayFiducial(self):
    
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    for modelNode in modelNodes.values():
      displayNode = modelNode.GetDisplayNode()
      if modelNode.GetAttribute("segmented") == "1" and modelNode.GetAttribute("nth")!=None:
        # if self.transform != None:
        if 1:
          i = int(modelNode.GetAttribute("nth"))
          if self.fiducialnode[i] == 0:    
            polyData = displayNode.GetPolyData()
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
              
              self.fiducialnode[i].SetVisible(modelNode.GetDisplayNode().GetVisibility())
          else:    
            if modelNode.GetDisplayNode().GetVisibility():
               self.fiducialnode[i].SetVisible(abs(self.fiducialnode[i].GetVisible()-1))
            if self.fiducialnode[i].GetVisible()==1:
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
    if self.skip == 0:
      pNode = self.parameterNode()
      self.updateWidgetFromParameters(pNode)
      Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')
      obturator = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('obturatorID'))
      template = slicer.mrmlScene.GetNodeByID(pNode.GetParameter('templateID'))
      dObturator = obturator.GetDisplayNode()
      dObturator.SetVisibility(0)
      dTemplate = template.GetDisplayNode()
      dTemplate.SetVisibility(0)

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
        # self.vtkmat.DeepCopy(self.m_vtkmat)
        vtkmat.SetElement(0,3,self.p[0][i])
        vtkmat.SetElement(1,3,self.p[1][i])

        vtkmat.Multiply4x4(transformMatrix,vtkmat,vtkmat)

        self.p[0][i] = vtkmat.GetElement(0,3)
        self.p[1][i] = vtkmat.GetElement(1,3)
      
      print self.p[0]
      print self.p[1]
        
        

  def colorLabel(self):
    self.color= [[0,0,0] for i in range(310)] 
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
        self.color[i][j] = self.color[i][j]/float(255)

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
    
  def showOneNeedle(self,i,visibility):
    fidname = "fid"+self.option[i]
    pNode = self.parameterNode()
    needleID = pNode.GetParameter(self.option[i]+'.vtk')
    fidID = pNode.GetParameter(fidname)    
    NeedleNode = slicer.mrmlScene.GetNodeByID(needleID)
    fiducialNode = slicer.mrmlScene.GetNodeByID(fidID)    
    
    if NeedleNode !=None:
      displayNode =NeedleNode.GetModelDisplayNode()
      nVisibility=displayNode.GetVisibility()  

      if fiducialNode == None:
        displayNode.SetVisibility(1)    
        displayNode.SetOpacity(0.9)
        polyData = displayNode.GetPolyData()
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
          fiducialNode.SetVisible(0)
          pNode.SetParameter(fidname,fiducialNode.GetID())
          fiducialNode.SetVisible(1)

      if visibility ==0:

        displayNode.SetVisibility(0)
        displayNode.SetSliceIntersectionVisibility(0)
        if fiducialNode!=None:
          fiducialNode.SetVisible(0)

      else:

        displayNode.SetVisibility(1)
        displayNode.SetSliceIntersectionVisibility(1)
        if fiducialNode!=None:
          fiducialNode.SetVisible(1)

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
 
    fileName = self.option[i]+'.vtk'
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
    displayNode.SetPolyData(modelNode.GetPolyData())
    self.colorLabel()
    displayNode.SetColor(self.color[i])
    displayNode.SetSliceIntersectionVisibility(0)
    pNode= self.parameterNode()
    pNode.SetParameter(fileName,modelNode.GetID())
    mrmlScene.AddNode(modelNode)
    displayNode.SetVisibility(1)
    
