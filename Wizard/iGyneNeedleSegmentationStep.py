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
    

  def createUserInterface( self ):
    '''
    '''
    self.skip = 0
    pNode = self.parameterNode()
    self.__layout = self.__parent.createUserInterface()
    
    groupbox = qt.QGroupBox()
    groupboxLayout  = qt.QFormLayout(groupbox)
    groupboxLayout.addRow(slicer.modules.editor.widgetRepresentation())
    self.__layout.addRow(groupbox)
    
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
    
    foldername = './NeedleModels/' + datetime
    
    # Set the parameters for the CLI module    
    parameters = {} 
    parameters['inputVolume'] = inputVolumeID
    parameters['inputLabel'] = inputLabelID
    parameters['outputVtk'] = outputID
    parameters['outputFolderName'] = foldername
    module = slicer.modules.mainlabelneedletrackingcli 
    self.__cliNode = None
    self.__cliNode = slicer.cli.run(module, None, parameters, wait_for_completion=True)
    
    boundsAll=[0,0,0,0,0,0]
    
    d = slicer.mrmlScene.GetNodeByID(outputID).GetDisplayNode()
    p = slicer.mrmlScene.GetNodeByID(outputID).GetPolyData()
    p.GetBounds(boundsAll)
    Xdelta = abs(boundsAll[1]-boundsAll[0])
    Ydelta = abs(boundsAll[3]-boundsAll[2])
    Xmin = boundsAll[0]
    Ymin = boundsAll[2]
    d.SetVisibility(1)
    dd = slicer.mrmlScene.GetNodeByID(inputLabelID).GetDisplayNode()
    color = dd.GetColorNodeID()
    
    d.SetScalarVisibility(1)
    d.SetActiveScalarName('NeedleLabel')
    d.SetAndObserveColorNodeID(color)
    
    
    ##### match the needles ######
    self.colorLabel()
    self.setNeedleCoordinates()
    xmin = min(self.p[0])
    xmax = max(self.p[0])
    ymin = min(self.p[1])
    ymax = max(self.p[1])
    xdelta= xmax - xmin
    ydelta = ymax - ymin
    
    for i in xrange(60):
      
      base=[0,0,0]
      pathneedle = os.path.abspath("./") + foldername+'/'+str(i)+'.vtk'
      needlenode = "needlenode" + str(i)
      displaynode = "displaynode" + str(i)
      needlenode = slicer.util.loadModel(pathneedle, True)
      print pathneedle
      if needlenode[0] == True:
        displaynode = needlenode[1].GetDisplayNode()
        polydata = needlenode[1].GetPolyData()
        polydata.GetPoint(0,base)
        print base        

        displaynode.SliceIntersectionVisibilityOn()
        bestmatch = None
        mindist = None
        for j in xrange(63):
          delta = ((self.p[0][j]-base[0])**2+(self.p[1][j]-base[1])**2)**(0.5)
          if delta < mindist or mindist == None:
            bestmatch = j
            mindist = delta
        
        
        displaynode.SetColor(self.color[bestmatch])
    
    

    
    d.SetVisibility(0)
    
    
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
  
    baselineVolume = Helper.getNodeByID(pNode.GetParameter('baselineVolumeID'))
    
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
