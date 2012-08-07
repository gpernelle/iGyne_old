from __main__ import qt, ctk

from iGyneStep import *
from Helper import *
from iGyneUI import *
import PythonQt

class iGyneSelectProcedureStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '1. Select the Procedure' )
    self.setDescription( 'Select the procedure used in this iGyne case.' )
    self.__parent = super( iGyneSelectProcedureStep, self )

  def createUserInterface( self ):
    '''
    '''

    self.__layout = self.__parent.createUserInterface()
    self.horizontalLayoutWidget = qt.QWidget()
    self.horizontalLayoutWidget.setEnabled(True)
    self.horizontalLayoutWidget.setGeometry(qt.QRect(5, 6, 538, 36))
    self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
    self.horizontalLayout = qt.QHBoxLayout(self.horizontalLayoutWidget)
    self.horizontalLayout.setMargin(0)
    # self.horizontalLayout.setObjectName("horizontalLayout")
    
    self.LoadTemplatePushButton = qt.QPushButton(self.horizontalLayoutWidget)
    self.LoadTemplatePushButton.setEnabled(True)
    # sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred)
    # sizePolicy.setHorizontalStretch(0)
    # sizePolicy.setVerticalStretch(0)
    # sizePolicy.setHeightForWidth(self.LoadTemplatePushButton.sizePolicy.hasHeightForWidth())
    # self.LoadTemplatePushButton.setSizePolicy(sizePolicy)
    self.LoadTemplatePushButton.setText("Load(Scene/Template)")
    self.LoadTemplatePushButton.connect( 'clicked()', self.loadTemplate)
    self.horizontalLayout.addWidget(self.LoadTemplatePushButton)
   
    self.__layout.addWidget(self.horizontalLayoutWidget)
    

  ##-----------------------------------------------------------------------------
  def showAaNeedle(self):

    self.showOneNeedle(48,self.AaRadioButton) 


  ##-----------------------------------------------------------------------------
  def pushAaNeedle(self):

    nDepth = self.popupSpinboxAa.value

    self.pushOneNeedle(48, nDepth)   


  ##-----------------------------------------------------------------------------
  def setAaColor(self):
    
    self.setOneNeedleColor(48,self.AaColorPushButton)  


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
    if NeedleNode:
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
    if NeedleNode:
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
    if NeedleNode:
      NeedleNode.SetAndObservePolyData(triangles.GetOutput())
    
  ##-----------------------------------------------------------------------------
  def setOneNeedleColor(self,i,ColorPushButton):

    color = qt.QColorDialog.getColor(qt.QColor('green'), self)
    sColor = "background-color: rgb(" + str(color.red())+ "," + str(color.green()) + "," + str(color.blue())

    if color.isValid():

      filename= "vtkMRMLModelNode"+str(i+6)
      mrmlScene=slicer.mrmlScene
      NeedleNode = mrmlScene.GetNodeByID(filename)
      if NeedleNode:
        displayNode =NeedleNode.GetModelDisplayNode()

        displayNode.SetColor(color.red()/float(255.0),color.green()/float(255.0),color.blue()/float(255.0))
        ColorPushButton.setStyleSheet(sColor)
      
  ##-----------------------------------------------------------------------------
  def showNeedles(self):

    if self.ShowNeedlesPushButton.isChecked():
      for i in xrange(63): 
        self.showOneNeedle(i,True)

      self.ShowNeedlesPushButton.setChecked(True)
     
      self.AaRadioButton.setChecked(True)
      
    else:
      for i in xrange(63):
        self.showOneNeedle(i,False)

      self.ShowNeedlesPushButton.setChecked(False)
      
      self.AaRadioButton.setChecked(False)
      

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
        if NeedleNode:  
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
    
    pathToScene = slicer.modules.igynepy.path.replace("iGynePy.py","iGynePyTemplate/Template/Template.mrml")
    slicer.util.loadScene( pathToScene, True)
    
    NeedleNode = slicer.mrmlScene.GetNodeByID("vtkMRMLModelNode6")
    ObutratorNode = slicer.mrmlScene.GetNodeByID("vtkMRMLModelNode5")

    if ObutratorNode:
      self.setNeedleCoordinates()
      self.computerPolydataAndMatrix()    
      
      self.m_poly = vtk.vtkPolyData()  
      self.m_poly.DeepCopy(ObutratorNode.GetPolyData())
      
    
    if NeedleNode:
      
      vtkmat = vtk.vtkMatrix4x4()
      vtkmat.DeepCopy(self.m_vtkmat)
   
      for i in xrange(63):
      
        vtkmat.SetElement(0,3,self.m_vtkmat.GetElement(0,3)+p[0][i])
        vtkmat.SetElement(1,3,self.m_vtkmat.GetElement(1,3)+p[1][i])
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
        
    else:
      for i in xrange(63):
      
        filename= "vtkMRMLModelNode"+str(i+6)
        mrmlScene=slicer.mrmlScene
        NeedleNode = mrmlScene.GetNodeByID(filename)
        if NeedleNode:
          displayNode =NeedleNode.GetModelDisplayNode()

          nVisibility=displayNode.GetVisibility()  

          if nVisibility==1:
            self.setRadioButton(i,true) 
          else:
            self.setRadioButton(i,false)          

  def AddModel(self,i,polyData):
    modelNode = vtk.vtkMRMLModelNode()
    displayNode = vtk.vtkMRMLModelDisplayNode()
    storageNode = vtk.vtkMRMLModelStorageNode()

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

