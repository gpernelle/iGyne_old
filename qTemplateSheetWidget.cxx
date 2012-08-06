/*==============================================================================

  Program: 3D Slicer

  Portions (c) Copyright Brigham and Women's Hospital (BWH) All Rights Reserved.

  See COPYRIGHT.txt
  or http:##www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
  
  This file was originally developed by Xiaojun Chen, SPL.
  and was partially funded by NIH grant P41EB015898, P41RR019703, R03EB013792, and U54EB005149.

==============================================================================*/

## SlicerQt includes
#include "qSlicerApplication.h"
#include "qSlicerIOManager.h"
#include "qSlicerLayoutManager.h"

## Qt includes
#include "qTemplateSheetWidget.h"
#include "ui_qTemplateSheetWidget.h"
###include "ui_qSpinBoxDepthWidget.h"

## CTK includes
#include <ctkPopupWidget.h>
###include "ctkSliderWidget.h"

## MRML includes
#include <vtkMRMLLinearTransformNode.h>
#include <vtkMRMLModelNode.h>
#include <vtkMRMLScene.h>
#include <vtkMRMLAnnotationHierarchyNode.h>
#include <vtkMRMLModelNode.h>
#include <vtkMRMLModelStorageNode.h>
#include <vtkMRMLFreeSurferModelStorageNode.h>
#include <vtkMRMLModelDisplayNode.h>

## VTK includes
#include <vtkColorTransferFunction.h>
#include <vtkPoints.h>
#include <vtkLine.h>
#include <vtkUnstructuredGrid.h>
#include <vtkDataSetMapper.h>
#include <vtkActor.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkProperty.h>
#include <vtkMatrix4x4.h>
#include <vtkPolyData.h>
#include <vtkAxes.h>
#include <vtkTubeFilter.h>
#include <vtkPolyDataMapper.h>
#include <vtkSTLReader.h>
#include <vtkSmartPointer.h>
#include <vtkCylinderSource.h>
#include <vtkTransformPolyDataFilter.h>
#include <vtkTransform.h>
#include <vtkTriangleFilter.h>
#include <vtkDelaunay3D.h>
#include <vtkGeneralTransform.h>
#include <vtkPolyDataNormals.h>
#include <vtkGlyph3D.h>
#include <vtkSphereSource.h>
#include <vtkIterativeClosestPointTransform.h>
#include <vtkLandmarkTransform.h>
#include <vtkCollisionDetectionFilter.h>

## ITK includes
#include <itkImage.h>
#include <itkPointSetToImageRegistrationMethod.h>
#include <itkPointSet.h>
#include <itkVersorRigid3DTransform.h>
#include <itkVersorRigid3DTransformOptimizer.h>
#include <itkNormalizedCorrelationPointSetToImageMetric.h>
#include <itkLinearInterpolateImageFunction.h>
#include <itkImageFileReader.h>
#include <itkGradientMagnitudeImageFilter.h>

const double pi=3.14159265358979f

##-----------------------------------------------------------------------------
class qTemplateSheetWidgetPrivate: public Ui_TemplateSheetWidget
{
  Q_DECLARE_PUBLIC(qTemplateSheetWidget)
protected:
  qTemplateSheetWidget* const q_ptr  

public:
  qTemplateSheetWidgetPrivate(qTemplateSheetWidget& object)
  void init()
  
}

##-----------------------------------------------------------------------------
qTemplateSheetWidgetPrivate::qTemplateSheetWidgetPrivate(qTemplateSheetWidget& object)
  :q_ptr(&object)
{
  
}



##-----------------------------------------------------------------------------
def createSpinbox(self, popup, popupSpinbox):

  popupLayout = qt.QHBoxLayout(popup)  
  popupLayout.addWidget(popupSpinbox) 

  sizePolicy1 = qt.QSizePolicy
  sizePolicy1.setHorizontalStretch(0)
  sizePolicy1.setVerticalStretch(0)
  sizePolicy1.setHeightForWidth(popupSpinbox.sizePolicy().hasHeightForWidth())
  popupSpinbox.setStyleSheet("background-color: rgb(255, 255, 255)")
  popupSpinbox.setSizePolicy(sizePolicy1)
  popupSpinbox.setMaximum(300)
  popupSpinbox.setValue(170)  

##-----------------------------------------------------------------------------
def loadTemplate(self):

  if slicer.ioManager().openLoadSceneDialog():

    ObutratorNode = slicer.mrmlScene.GetNodeByID("vtkMRMLModelNode5")

    if ObutratorNode!=None:
      self.setNeedleCoordinates()
      computerPolydataAndMatrix()    
      
      m_poly = vtk.vtkPolyData()  
      m_poly.DeepCopy(ObutratorNode.GetPolyData())
      
    NeedleNode = slicer.mrmlScene.GetNodeByID("vtkMRMLModelNode6")
    if NeedleNode==None:
      
      vtkmat = vtk.vtkMatrix4x4()
      vtkmat.DeepCopy(m_vtkmat)
   
      for i in xrange(63):
      
        vtkmat.SetElement(0,3,m_vtkmat.GetElement(0,3)+p[0][i])
        vtkmat.SetElement(1,3,m_vtkmat.GetElement(1,3)+p[1][i])
        vtkmat.SetElement(2,3,m_vtkmat.GetElement(2,3)+(30.0-150.0)/2.0)

        TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
        Transform=vtk.vtkTransform()        
        TransformPolyDataFilter.SetInput(m_polyCylinder)
        Transform.SetMatrix(vtkmat)
        TransformPolyDataFilter.SetTransform(Transform)
        TransformPolyDataFilter.Update()

        triangles=vtk.vtkTriangleFilter()
        triangles.SetInput(TransformPolyDataFilter.GetOutput())  
         
        self.AddModel(i,triangles.GetOutput())
        
    else:
      for i in xrange(63):
      
        fileName= "vtkMRMLModelNode"+str(i+6)
        mrmlScene=slicer.mrmScene
        NeedleNode = mrmlScene.GetNodeByID(filename)
        displayNode =NeedleNode.GetModelDisplayNode()

        nVisibility=displayNode.GetVisibility()  

        if nVisibility==1:
          self.setRadioButton(i,true) 
        else:
          self.setRadioButton(i,false)          
     

##----------------------------------------------------------------------------
def computerPolydataAndMatrix(self):

  Cylinder=vtkCylinderSource()    

  Cylinder.SetResolution(1000)
  Cylinder.SetCapping(1) 
  Cylinder.SetHeight( 200.0f )
  Cylinder.SetRadius( 1.0f )
  m_polyCylinder=Cylinder.GetOutput()

  m_vtkmat = vtk.vtkMatrix4x4()
  m_vtkmat.Identity()

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
  Restru2WorldMatrix.Multiply4x4(RestruMatrix,WorldMatrix,m_vtkmat)  

##----------------------------------------------------------------------------
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

##-----------------------------------------------------------------------------
def setNeedleCoordinates(self):

  p[0][0]=35
  p[1][0]=34
  p[0][1]=25
  p[1][1]=36.679
  p[0][2]=17.679
  p[1][2]=44
  p[0][3]=15
  p[1][3]=54
  p[0][4]=17.679
  p[1][4]=64
  p[0][5]=25
  p[1][5]=71.321
  p[0][6]=35
  p[1][6]=74
  p[0][7]=45
  p[1][7]=71.321
  p[0][8]=52.321
  p[1][8]=64
  p[0][9]=55
  p[1][9]=54
  p[0][10]=52.321
  p[1][10]=44
  p[0][11]=45
  p[1][11]=36.679
  p[0][12]=29.791
  p[1][12]=24.456
  p[0][13]=20
  p[1][13]=28.019
  p[0][14]=12.019
  p[1][14]=34.716
  p[0][15]=6.809
  p[1][15]=43.739
  p[0][16]=5
  p[1][16]=54
  p[0][17]=6.809
  p[1][17]=64.261
  p[0][18]=12.019
  p[1][18]=73.284
  p[0][19]=20
  p[1][19]=79.981
  p[0][20]=29.791
  p[1][20]=83.544
  p[0][21]=40.209
  p[1][21]=83.544
  p[0][22]=50
  p[1][22]=79.981
  p[0][23]=57.981
  p[1][23]=73.284
  p[0][24]=63.191
  p[1][24]=64.262
  p[0][25]=65
  p[1][25]=54
  p[0][26]=63.191
  p[1][26]=43.739
  p[0][27]=57.981
  p[1][27]=34.716
  p[0][28]=50
  p[1][28]=28.019
  p[0][29]=40.209
  p[1][29]=24.456
  p[0][30]=35
  p[1][30]=14
  p[0][31]=24.647
  p[1][31]=15.363
  p[0][32]=15
  p[1][32]=19.359
  p[0][33]=15
  p[1][33]=88.641
  p[0][34]=24.647
  p[1][34]=92.637
  p[0][35]=35
  p[1][35]=94
  p[0][36]=45.353
  p[1][36]=92.637
  p[0][37]=55
  p[1][37]=88.641
  p[0][38]=55
  p[1][38]=19.359
  p[0][39]=45.353
  p[1][39]=15.363
  p[0][40]=30.642
  p[1][40]=4.19
  p[0][41]=22.059
  p[1][41]=5.704
  p[0][42]=22.059
  p[1][42]=102.296
  p[0][43]=30.642
  p[1][43]=103.81
  p[0][44]=39.358
  p[1][44]=103.81
  p[0][45]=47.941
  p[1][45]=102.296
  p[0][46]=47.941
  p[1][46]=5.704
  p[0][47]=39.358
  p[1][47]=4.19
  p[0][48]=29.7
  p[1][48]=44.82
  p[0][49]=24.4
  p[1][49]=54
  p[0][50]=29.7
  p[1][50]=63.18
  p[0][51]=40.3
  p[1][51]=63.18
  p[0][52]=45.6
  p[1][52]=54
  p[0][53]=40.3
  p[1][53]=44.82
  p[0][54]=35
  p[1][54]=54
  p[0][55]=9
  p[1][55]=12
  p[0][56]=5
  p[1][56]=18
  p[0][57]=5
  p[1][57]=90
  p[0][58]=9
  p[1][58]=96
  p[0][59]=61
  p[1][59]=96
  p[0][60]=65
  p[1][60]=90
  p[0][61]=65
  p[1][61]=18
  p[0][62]=61
  p[1][62]=12


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
def pushIuNeedle(self,nDepth):

  self.pushOneNeedle(54, nDepth)   


##-----------------------------------------------------------------------------
def pushAaNeedle(self,nDepth):

  self.pushOneNeedle(48, nDepth)   


##-----------------------------------------------------------------------------
def pushAbNeedle(self,nDepth):

  self.pushOneNeedle(49, nDepth)   


##-----------------------------------------------------------------------------
def pushAcNeedle(self,nDepth):

  self.pushOneNeedle(50, nDepth)   


##-----------------------------------------------------------------------------
def pushAdNeedle(self,nDepth):

  self.pushOneNeedle(51, nDepth)   


##-----------------------------------------------------------------------------
def pushAeNeedle(self,nDepth):

  self.pushOneNeedle(52, nDepth)   


##-----------------------------------------------------------------------------
def pushAfNeedle(self,nDepth):

  self.pushOneNeedle(53, nDepth)   


##-----------------------------------------------------------------------------
def pushBaNeedle(self,nDepth):

  self.pushOneNeedle(0, nDepth)   


##-----------------------------------------------------------------------------
def pushBbNeedle(self,nDepth):

  self.pushOneNeedle(1, nDepth)   


##-----------------------------------------------------------------------------
def pushBcNeedle(self,nDepth):

  self.pushOneNeedle(2, nDepth)   


##-----------------------------------------------------------------------------
def pushBdNeedle(self,nDepth):

  self.pushOneNeedle(3, nDepth)   


##-----------------------------------------------------------------------------
def pushBeNeedle(self,nDepth):

  self.pushOneNeedle(4, nDepth)   


##-----------------------------------------------------------------------------
def pushBfNeedle(self,nDepth):

  self.pushOneNeedle(5, nDepth)   


##-----------------------------------------------------------------------------
def pushBgNeedle(self,nDepth):

  self.pushOneNeedle(6, nDepth)   


##-----------------------------------------------------------------------------
def pushBhNeedle(self,nDepth):

  self.pushOneNeedle(7, nDepth)   


##-----------------------------------------------------------------------------
def pushBiNeedle(self,nDepth):

  self.pushOneNeedle(8, nDepth)   


##-----------------------------------------------------------------------------
def pushBjNeedle(self,nDepth):

  self.pushOneNeedle(9, nDepth)   


##-----------------------------------------------------------------------------
def pushBkNeedle(self,nDepth):

  self.pushOneNeedle(10, nDepth)   


##-----------------------------------------------------------------------------
def pushBlNeedle(self,nDepth):

  self.pushOneNeedle(11, nDepth)   


##-----------------------------------------------------------------------------
def pushCaNeedle(self,nDepth):

  self.pushOneNeedle(12, nDepth)   


##-----------------------------------------------------------------------------
def pushCbNeedle(self,nDepth):

  self.pushOneNeedle(13, nDepth)   


##-----------------------------------------------------------------------------
def pushCcNeedle(self,nDepth):

  self.pushOneNeedle(14, nDepth)   


##-----------------------------------------------------------------------------
def pushCdNeedle(self,nDepth):

  self.pushOneNeedle(15, nDepth)   


##-----------------------------------------------------------------------------
def pushCeNeedle(self,nDepth):

  self.pushOneNeedle(16, nDepth)   


##-----------------------------------------------------------------------------
def pushCfNeedle(self,nDepth):

  self.pushOneNeedle(17, nDepth)   


##-----------------------------------------------------------------------------
def pushCgNeedle(self,nDepth):

  self.pushOneNeedle(18, nDepth)   


##-----------------------------------------------------------------------------
def pushChNeedle(self,nDepth):

  self.pushOneNeedle(19, nDepth)   


##-----------------------------------------------------------------------------
def pushCiNeedle(self,nDepth):

  self.pushOneNeedle(20, nDepth)   


##-----------------------------------------------------------------------------
def pushCjNeedle(self,nDepth):

  self.pushOneNeedle(21, nDepth)   


##-----------------------------------------------------------------------------
def pushCkNeedle(self,nDepth):

  self.pushOneNeedle(22, nDepth)   


##-----------------------------------------------------------------------------
def pushClNeedle(self,nDepth):

  self.pushOneNeedle(23, nDepth)   


##-----------------------------------------------------------------------------
def pushCmNeedle(self,nDepth):

  self.pushOneNeedle(24, nDepth)   


##-----------------------------------------------------------------------------
def pushCnNeedle(self,nDepth):

  self.pushOneNeedle(25, nDepth)   


##-----------------------------------------------------------------------------
def pushCoNeedle(self,nDepth):

  self.pushOneNeedle(26, nDepth)   


##-----------------------------------------------------------------------------
def pushCpNeedle(self,nDepth):

  self.pushOneNeedle(27, nDepth)   


##-----------------------------------------------------------------------------
def pushCqNeedle(self,nDepth):

  self.pushOneNeedle(28, nDepth)   


##-----------------------------------------------------------------------------
def pushCrNeedle(self,nDepth):

  self.pushOneNeedle(29, nDepth)   


##-----------------------------------------------------------------------------
def pushDaNeedle(self,nDepth):

  self.pushOneNeedle(30, nDepth)   


##-----------------------------------------------------------------------------
def pushDbNeedle(self,nDepth):

  self.pushOneNeedle(31, nDepth)   


##-----------------------------------------------------------------------------
def pushDcNeedle(self,nDepth):

  self.pushOneNeedle(32, nDepth)   


##-----------------------------------------------------------------------------
def pushDdNeedle(self,nDepth):

  self.pushOneNeedle(33, nDepth)   


##-----------------------------------------------------------------------------
def pushDeNeedle(self,nDepth):

  self.pushOneNeedle(34, nDepth)   


##-----------------------------------------------------------------------------
def pushDfNeedle(self,nDepth):

  self.pushOneNeedle(35, nDepth)   


##-----------------------------------------------------------------------------
def pushDgNeedle(self,nDepth):

  self.pushOneNeedle(36, nDepth)   


##-----------------------------------------------------------------------------
def pushDhNeedle(self,nDepth):

  self.pushOneNeedle(37, nDepth)   


##-----------------------------------------------------------------------------
def pushDiNeedle(self,nDepth):

  self.pushOneNeedle(38, nDepth)   


##-----------------------------------------------------------------------------
def pushDjNeedle(self,nDepth):

  self.pushOneNeedle(39, nDepth)   


##-----------------------------------------------------------------------------
def pushEaNeedle(self,nDepth):

  self.pushOneNeedle(40, nDepth)   


##-----------------------------------------------------------------------------
def pushEbNeedle(self,nDepth):

  self.pushOneNeedle(41, nDepth)   


##-----------------------------------------------------------------------------
def pushEcNeedle(self,nDepth):

  self.pushOneNeedle(42, nDepth)   


##-----------------------------------------------------------------------------
def pushEdNeedle(self,nDepth):

  self.pushOneNeedle(43, nDepth)   


##-----------------------------------------------------------------------------
def pushEeNeedle(self,nDepth):

  self.pushOneNeedle(44, nDepth)   


##-----------------------------------------------------------------------------
def pushEfNeedle(self,nDepth):

  self.pushOneNeedle(45, nDepth)   


##-----------------------------------------------------------------------------
def pushEgNeedle(self,nDepth):

  self.pushOneNeedle(46, nDepth)   


##-----------------------------------------------------------------------------
def pushEhNeedle(self,nDepth):

  self.pushOneNeedle(47, nDepth)   


##-----------------------------------------------------------------------------
def pushFaNeedle(self,nDepth):

  self.pushOneNeedle(55, nDepth)   


##-----------------------------------------------------------------------------
def pushFbNeedle(self,nDepth):

  self.pushOneNeedle(56, nDepth)   


##-----------------------------------------------------------------------------
def pushFcNeedle(self,nDepth):

  self.pushOneNeedle(57, nDepth)   


##-----------------------------------------------------------------------------
def pushFdNeedle(self,nDepth):

  self.pushOneNeedle(58, nDepth)   


##-----------------------------------------------------------------------------
def pushFeNeedle(self,nDepth):

  self.pushOneNeedle(59, nDepth)   


##-----------------------------------------------------------------------------
def pushFfNeedle(self,nDepth):

  self.pushOneNeedle(60, nDepth)   


##-----------------------------------------------------------------------------
def pushFgNeedle(self,nDepth):

  self.pushOneNeedle(61, nDepth)   


##-----------------------------------------------------------------------------
def pushFhNeedle(self,nDepth):

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
def pushObutrator(self, nDepth):
  mrmlScene=slicer.mrmScene  
  ObutratorNode = mrmlScene.GetNodeByID("vtkMRMLModelNode5")

  vtkmat = vtk.vtkMatrix4x4()
  vtkmat.Identity()
  vtkmat.SetElement(2,3,nDepth)

  TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
  Transform=vtk.vtkTransform()
  TransformPolyDataFilter.SetInput(m_poly)
  Transform.SetMatrix(vtkmat)
  TransformPolyDataFilter.SetTransform(Transform)
  TransformPolyDataFilter.Update()

  triangles=vtk.vtkTriangleFilter()
  triangles.SetInput(TransformPolyDataFilter.GetOutput())
  ObutratorNode.SetAndObservePolyData(triangles.GetOutput())    

##-----------------------------------------------------------------------------
def showOneNeedle(self,i,RadioButton):
  
  fileName= "vtkMRMLModelNode"+str(i+6)
  mrmlScene=slicer.mrmScene
  NeedleNode = mrmlScene.GetNodeByID(filename)
  displayNode =NeedleNode.GetModelDisplayNode()

  nVisibility=displayNode.GetVisibility()  

  if(nVisibility==1):
    displayNode.SetVisibility(0)
    displayNode.SetSliceIntersectionVisibility(0)
    RadioButton.setChecked(false)
  else:
    displayNode.SetVisibility(1)
    displayNode.SetSliceIntersectionVisibility(1)
    RadioButton.setChecked(true)


##-----------------------------------------------------------------------------
def showOneNeedle(self,i,bShowNeedels):

  fileName= "vtkMRMLModelNode"+str(i+6)
  mrmlScene=slicer.mrmScene
  NeedleNode = mrmlScene.GetNodeByID(filename)
  displayNode =NeedleNode.GetModelDisplayNode()

  if bShowNeedels:
    displayNode.SetVisibility(1)
    displayNode.SetSliceIntersectionVisibility(1)    

  else:
    displayNode.SetVisibility(0)
    displayNode.SetSliceIntersectionVisibility(0)    


##-----------------------------------------------------------------------------
def pushOneNeedle(self,i,nDepth):

  fileName= "vtkMRMLModelNode"+str(i+6)
  mrmlScene=slicer.mrmScene
  NeedleNode = mrmlScene.GetNodeByID(filename)

  vtkmat = vtk.vtkMatrix4x4()
  vtkmat.DeepCopy(m_vtkmat) 

  vtkmat.SetElement(0,3,m_vtkmat.GetElement(0,3)+p[0][i])
  vtkmat.SetElement(1,3,m_vtkmat.GetElement(1,3)+p[1][i])
  vtkmat.SetElement(2,3,m_vtkmat.GetElement(2,3)+110.0-nDepth)

  TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
  Transform=vtk.vtkTransform()
  TransformPolyDataFilter.SetInput(m_polyCylinder)
  Transform.SetMatrix(vtkmat)
  TransformPolyDataFilter.SetTransform(Transform)
  TransformPolyDataFilter.Update()

  triangles=vtk.vtkTriangleFilter()
  triangles.SetInput(TransformPolyDataFilter.GetOutput())
  NeedleNode.SetAndObservePolyData(triangles.GetOutput())
  
##-----------------------------------------------------------------------------
def setOneNeedleColor(self,i,ColorPushButton):

  color = qt.QColorDialog.getColor(qt.QColor(), self)
  sColor = "background-color: rgb(" + str(color.red())+ "," + str(color.green()) + "," + str(color.blue()))

  if color.isValid():

    fileName= "vtkMRMLModelNode"+str(i+6)
    mrmlScene=slicer.mrmScene
    NeedleNode = mrmlScene.GetNodeByID(filename)
    displayNode =NeedleNode.GetModelDisplayNode()

    displayNode.SetColor(color.red()/float(255.0),color.green()/float(255.0),color.blue()/float(255.0))
    ColorPushButton.setStyleSheet(sColor)
    

##-----------------------------------------------------------------------------
def showNeedles(self):

  if(self.ShowNeedlesPushButton.isChecked())
    for i in xrange(63): 
      showOneNeedle(i,true)

    self.ShowNeedlesPushButton.setChecked(true)
    self.IuRadioButton.setChecked(true)
    self.AaRadioButton.setChecked(true)
    self.AbRadioButton.setChecked(true)
    self.AcRadioButton.setChecked(true)
    self.AdRadioButton.setChecked(true)
    self.AeRadioButton.setChecked(true)
    self.AfRadioButton.setChecked(true)
    self.BaRadioButton.setChecked(true)
    self.BbRadioButton.setChecked(true)
    self.BcRadioButton.setChecked(true)
    self.BdRadioButton.setChecked(true)
    self.BeRadioButton.setChecked(true)
    self.BfRadioButton.setChecked(true)
    self.BgRadioButton.setChecked(true)
    self.BhRadioButton.setChecked(true)
    self.BiRadioButton.setChecked(true)
    self.BjRadioButton.setChecked(true)
    self.BkRadioButton.setChecked(true)
    self.BlRadioButton.setChecked(true)
    self.CaRadioButton.setChecked(true)
    self.CbRadioButton.setChecked(true)
    self.CcRadioButton.setChecked(true)
    self.CdRadioButton.setChecked(true)
    self.CeRadioButton.setChecked(true)
    self.CfRadioButton.setChecked(true)
    self.CgRadioButton.setChecked(true)
    self.ChRadioButton.setChecked(true)
    self.CiRadioButton.setChecked(true)
    self.CjRadioButton.setChecked(true)
    self.CkRadioButton.setChecked(true)
    self.ClRadioButton.setChecked(true)
    self.CmRadioButton.setChecked(true)
    self.CnRadioButton.setChecked(true)
    self.CoRadioButton.setChecked(true)
    self.CpRadioButton.setChecked(true)
    self.CqRadioButton.setChecked(true)
    self.CrRadioButton.setChecked(true)
    self.DaRadioButton.setChecked(true)
    self.DbRadioButton.setChecked(true)
    self.DcRadioButton.setChecked(true)
    self.DdRadioButton.setChecked(true)
    self.DeRadioButton.setChecked(true)
    self.DfRadioButton.setChecked(true)
    self.DgRadioButton.setChecked(true)
    self.DhRadioButton.setChecked(true)
    self.DiRadioButton.setChecked(true)
    self.DjRadioButton.setChecked(true)
    self.EaRadioButton.setChecked(true)
    self.EbRadioButton.setChecked(true)
    self.EcRadioButton.setChecked(true)
    self.EdRadioButton.setChecked(true)
    self.EeRadioButton.setChecked(true)
    self.EfRadioButton.setChecked(true)
    self.EgRadioButton.setChecked(true)
    self.EhRadioButton.setChecked(true)
    self.FaRadioButton.setChecked(true)
    self.FbRadioButton.setChecked(true)
    self.FcRadioButton.setChecked(true)
    self.FdRadioButton.setChecked(true)
    self.FeRadioButton.setChecked(true)
    self.FfRadioButton.setChecked(true)
    self.FgRadioButton.setChecked(true)
    self.FhRadioButton.setChecked(true)
  else:
    for i in xrange(63):
      showOneNeedle(i,false)

    self.ShowNeedlesPushButton.setChecked(false)
    self.IuRadioButton.setChecked(false)
    self.AaRadioButton.setChecked(false)
    self.AbRadioButton.setChecked(false)
    self.AcRadioButton.setChecked(false)
    self.AdRadioButton.setChecked(false)
    self.AeRadioButton.setChecked(false)
    self.AfRadioButton.setChecked(false)
    self.BaRadioButton.setChecked(false)
    self.BbRadioButton.setChecked(false)
    self.BcRadioButton.setChecked(false)
    self.BdRadioButton.setChecked(false)
    self.BeRadioButton.setChecked(false)
    self.BfRadioButton.setChecked(false)
    self.BgRadioButton.setChecked(false)
    self.BhRadioButton.setChecked(false)
    self.BiRadioButton.setChecked(false)
    self.BjRadioButton.setChecked(false)
    self.BkRadioButton.setChecked(false)
    self.BlRadioButton.setChecked(false)
    self.CaRadioButton.setChecked(false)
    self.CbRadioButton.setChecked(false)
    self.CcRadioButton.setChecked(false)
    self.CdRadioButton.setChecked(false)
    self.CeRadioButton.setChecked(false)
    self.CfRadioButton.setChecked(false)
    self.CgRadioButton.setChecked(false)
    self.ChRadioButton.setChecked(false)
    self.CiRadioButton.setChecked(false)
    self.CjRadioButton.setChecked(false)
    self.CkRadioButton.setChecked(false)
    self.ClRadioButton.setChecked(false)
    self.CmRadioButton.setChecked(false)
    self.CnRadioButton.setChecked(false)
    self.CoRadioButton.setChecked(false)
    self.CpRadioButton.setChecked(false)
    self.CqRadioButton.setChecked(false)
    self.CrRadioButton.setChecked(false)
    self.DaRadioButton.setChecked(false)
    self.DbRadioButton.setChecked(false)
    self.DcRadioButton.setChecked(false)
    self.DdRadioButton.setChecked(false)
    self.DeRadioButton.setChecked(false)
    self.DfRadioButton.setChecked(false)
    self.DgRadioButton.setChecked(false)
    self.DhRadioButton.setChecked(false)
    self.DiRadioButton.setChecked(false)
    self.DjRadioButton.setChecked(false)
    self.EaRadioButton.setChecked(false)
    self.EbRadioButton.setChecked(false)
    self.EcRadioButton.setChecked(false)
    self.EdRadioButton.setChecked(false)
    self.EeRadioButton.setChecked(false)
    self.EfRadioButton.setChecked(false)
    self.EgRadioButton.setChecked(false)
    self.EhRadioButton.setChecked(false)
    self.FaRadioButton.setChecked(false)
    self.FbRadioButton.setChecked(false)
    self.FcRadioButton.setChecked(false)
    self.FdRadioButton.setChecked(false)
    self.FeRadioButton.setChecked(false)
    self.FfRadioButton.setChecked(false)
    self.FgRadioButton.setChecked(false)
    self.FhRadioButton.setChecked(false)

def selectNeedles(self):

  mrmlScene=slicer.mrmScene
  ModelFromImageNode = vtkMRMLModelNode()
  ModelFromImageNode = mrmlScene.GetNodeByID("vtkMRMLModelNode70")

  if ModelFromImageNode!=None :
 
    collide = vtk.vtkCollisionDetectionFilter()
    matrix0 = vtk.vtkMatrix4x4()
    matrix1 = vtk.vtkMatrix4x4()    
    matrix2 = vtk.vtkMatrix4x4()  

    collide.SetInput(0,ModelFromImageNode.GetPolyData())
    collide.SetMatrix(0, matrix0)

    transformNode = mrmlScene.GetNodeByID("vtkMRMLLinearTransformNode4"))
    vtkmatInitial = transformNode.GetMatrixTransformToParent()

    nContacts=0
    for i in xrange(63):

      sfileName="vtkMRMLModelNode"+ str(i+6)

      NeedleNode = mrmlScene.GetNodeByID(filename)

      vtkmat = vtk.vtkMatrix4x4()
      vtkmat.DeepCopy(m_vtkmat) 

      vtkmat.SetElement(0,3,m_vtkmat.GetElement(0,3)+p[0][i])
      vtkmat.SetElement(1,3,m_vtkmat.GetElement(1,3)+p[1][i])
      vtkmat.SetElement(2,3,m_vtkmat.GetElement(2,3)-100.0)

      matrix1.Multiply4x4(vtkmatInitial,vtkmat,matrix1)

      TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
      Transform=vtk.vtkTransform()
      TransformPolyDataFilter.SetInput(m_polyCylinder)
      Transform.SetMatrix(matrix1)
      TransformPolyDataFilter.SetTransform(Transform)
      TransformPolyDataFilter.Update()

      triangles=vtk.vtkTriangleFilter()
      triangles.SetInput(TransformPolyDataFilter.GetOutput())

      collide.SetInput(1,(vtkPolyData *) triangles.GetOutput())
      collide.SetMatrix(1, matrix2)
      collide.SetBoxTolerance(0.0)
      collide.SetCellTolerance(0.0)
      collide.SetNumberOfCellsPerBucket(2)
      collide.SetCollisionModeToAllContacts()
      collide.GenerateScalarsOn()
      collide.Update()

      nContacts=collide.GetNumberOfContacts()
      displayNode =NeedleNode.GetModelDisplayNode()

      if nContacts>0:
        
        displayNode.SetVisibility(1)
        displayNode.SetSliceIntersectionVisibility(1)
        self.setRadioButton(i,true)
        
      else:
        
        displayNode.SetVisibility(0)
        displayNode.SetSliceIntersectionVisibility(0)
        self.setRadioButton(i,false)
        
      
    
  

##-----------------------------------------------------------------------------
def setRadioButton(i,bShowNeedels):
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
  
      

