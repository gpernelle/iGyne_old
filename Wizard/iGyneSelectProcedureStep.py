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
    groupbox = qt.QGroupBox()
    self.__layout.addRow(groupbox)
    groupboxLayout = qt.QFormLayout(groupbox)
    t= qt.QLabel('')
    t2= qt.QLabel('')
   
    
    groupboxLayout.addRow(self.setupUi(groupbox))
    groupboxLayout.setVerticalSpacing(700)
    groupboxLayout.addRow(t)
    groupboxLayout.addRow(t2)


    
    
   
  def onEntry(self, comingFrom, transitionType):

    super(iGyneSelectProcedureStep, self).onEntry(comingFrom, transitionType)
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    # self.updateWidgetFromParameterNode(pNode)    
    # qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):

    super(iGyneSelectProcedureStep, self).onExit(goingTo, transitionType) 

  # def updateWidgetFromParameters(self, parameterNode):

     # procedure = parameterNode.GetParameter('procedure')

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )    
    self.__parent.validationSucceeded(desiredBranchId)
   
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

  def setupUi(self, TemplateSheetWidget):
    self.computerPolydataAndMatrix() 
    self.setNeedleCoordinates()
    TemplateSheetWidget.setObjectName(("TemplateSheetWidget"))
    TemplateSheetWidget.resize(552, 682)
    self.label = qt.QLabel(TemplateSheetWidget)
    self.label.setEnabled(True)
    self.label.setGeometry(qt.QRect(5, 52, 541, 625))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label.sizePolicy.hasHeightForWidth())
    self.label.setSizePolicy(sizePolicy)
    self.label.setText((""))
    self.label.setPixmap(qt.QPixmap((":/Icons/GyneSheetVert.png")))
    self.label.setObjectName(("label"))
    self.CqColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CqColorPushButton.setEnabled(True)
    self.CqColorPushButton.setGeometry(qt.QRect(174, 185, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CqColorPushButton.sizePolicy.hasHeightForWidth())
    self.CqColorPushButton.setSizePolicy(sizePolicy)
    self.CqColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CqColorPushButton.setObjectName(("CqColorPushButton"))
    self.CpRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CpRadioButton.setEnabled(True)
    self.CpRadioButton.setGeometry(qt.QRect(128, 247, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CpRadioButton.sizePolicy.hasHeightForWidth())
    self.CpRadioButton.setSizePolicy(sizePolicy)
    self.CpRadioButton.setText((""))
    self.CpRadioButton.setAutoExclusive(False)
    self.CpRadioButton.setObjectName(("CpRadioButton"))
    self.CpColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CpColorPushButton.setEnabled(True)
    self.CpColorPushButton.setGeometry(qt.QRect(123, 225, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CpColorPushButton.sizePolicy.hasHeightForWidth())
    self.CpColorPushButton.setSizePolicy(sizePolicy)
    self.CpColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CpColorPushButton.setObjectName(("CpColorPushButton"))
    self.CqRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CqRadioButton.setEnabled(True)
    self.CqRadioButton.setGeometry(qt.QRect(177, 208, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CqRadioButton.sizePolicy.hasHeightForWidth())
    self.CqRadioButton.setSizePolicy(sizePolicy)
    self.CqRadioButton.setText((""))
    self.CqRadioButton.setAutoExclusive(False)
    self.CqRadioButton.setObjectName(("CqRadioButton"))
    self.CrColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CrColorPushButton.setEnabled(True)
    self.CrColorPushButton.setGeometry(qt.QRect(231, 165, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CrColorPushButton.sizePolicy.hasHeightForWidth())
    self.CrColorPushButton.setSizePolicy(sizePolicy)
    self.CrColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CrColorPushButton.setObjectName(("CrColorPushButton"))
    self.CrRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CrRadioButton.setEnabled(True)
    self.CrRadioButton.setGeometry(qt.QRect(235, 187, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CrRadioButton.sizePolicy.hasHeightForWidth())
    self.CrRadioButton.setSizePolicy(sizePolicy)
    self.CrRadioButton.setText((""))
    self.CrRadioButton.setAutoExclusive(False)
    self.CrRadioButton.setObjectName(("CrRadioButton"))
    self.horizontalLayoutWidget = qt.QWidget(TemplateSheetWidget)
    self.horizontalLayoutWidget.setEnabled(True)
    self.horizontalLayoutWidget.setGeometry(qt.QRect(5, 6, 538, 36))
    self.horizontalLayoutWidget.setObjectName(("horizontalLayoutWidget"))
    self.horizontalLayout = qt.QHBoxLayout(self.horizontalLayoutWidget)
    self.horizontalLayout.setMargin(0)
    self.horizontalLayout.setObjectName(("horizontalLayout"))
    self.LoadTemplatePushButton = qt.QPushButton(self.horizontalLayoutWidget)
    self.LoadTemplatePushButton.setEnabled(True)
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.LoadTemplatePushButton.sizePolicy.hasHeightForWidth())
    self.LoadTemplatePushButton.setSizePolicy(sizePolicy)
    self.LoadTemplatePushButton.setObjectName(("LoadTemplatePushButton"))
    self.horizontalLayout.addWidget(self.LoadTemplatePushButton)
    self.AddVolumePushButton = qt.QPushButton(self.horizontalLayoutWidget)
    self.AddVolumePushButton.setEnabled(True)
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AddVolumePushButton.sizePolicy.hasHeightForWidth())
    self.AddVolumePushButton.setSizePolicy(sizePolicy)
    self.AddVolumePushButton.setObjectName(("AddVolumePushButton"))
    self.horizontalLayout.addWidget(self.AddVolumePushButton)
    self.ShowNeedlesPushButton = qt.QPushButton(self.horizontalLayoutWidget)
    self.ShowNeedlesPushButton.setEnabled(True)
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.ShowNeedlesPushButton.sizePolicy.hasHeightForWidth())
    self.ShowNeedlesPushButton.setSizePolicy(sizePolicy)
    self.ShowNeedlesPushButton.setCheckable(True)
    self.ShowNeedlesPushButton.setChecked(False)
    self.ShowNeedlesPushButton.setObjectName(("ShowNeedlesPushButton"))
    self.horizontalLayout.addWidget(self.ShowNeedlesPushButton)
    self.SelectNeedlesPushButton = qt.QPushButton(self.horizontalLayoutWidget)
    self.SelectNeedlesPushButton.setEnabled(True)
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.SelectNeedlesPushButton.sizePolicy.hasHeightForWidth())
    self.SelectNeedlesPushButton.setSizePolicy(sizePolicy)
    self.SelectNeedlesPushButton.setObjectName(("SelectNeedlesPushButton"))
    self.horizontalLayout.addWidget(self.SelectNeedlesPushButton)
    self.ObturatorSpinBox = qt.QSpinBox(self.horizontalLayoutWidget)
    self.ObturatorSpinBox.setEnabled(True)
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.ObturatorSpinBox.sizePolicy.hasHeightForWidth())
    self.ObturatorSpinBox.setSizePolicy(sizePolicy)
    self.ObturatorSpinBox.setMinimum(-50)
    self.ObturatorSpinBox.setMaximum(50)
    self.ObturatorSpinBox.setObjectName(("ObturatorSpinBox"))
    self.horizontalLayout.addWidget(self.ObturatorSpinBox)
    self.CADmodel2ImageRegPushButton = qt.QPushButton(self.horizontalLayoutWidget)
    self.CADmodel2ImageRegPushButton.setEnabled(True)
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CADmodel2ImageRegPushButton.sizePolicy.hasHeightForWidth())
    self.CADmodel2ImageRegPushButton.setSizePolicy(sizePolicy)
    self.CADmodel2ImageRegPushButton.setObjectName(("CADmodel2ImageRegPushButton"))
    self.horizontalLayout.addWidget(self.CADmodel2ImageRegPushButton)
    self.CaRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CaRadioButton.setEnabled(True)
    self.CaRadioButton.setGeometry(qt.QRect(299, 185, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CaRadioButton.sizePolicy.hasHeightForWidth())
    self.CaRadioButton.setSizePolicy(sizePolicy)
    self.CaRadioButton.setText((""))
    self.CaRadioButton.setAutoExclusive(False)
    self.CaRadioButton.setObjectName(("CaRadioButton"))
    self.CaColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CaColorPushButton.setEnabled(True)
    self.CaColorPushButton.setGeometry(qt.QRect(297, 165, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CaColorPushButton.sizePolicy.hasHeightForWidth())
    self.CaColorPushButton.setSizePolicy(sizePolicy)
    self.CaColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CaColorPushButton.setObjectName(("CaColorPushButton"))
    self.CbRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CbRadioButton.setEnabled(True)
    self.CbRadioButton.setGeometry(qt.QRect(362, 206, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CbRadioButton.sizePolicy.hasHeightForWidth())
    self.CbRadioButton.setSizePolicy(sizePolicy)
    self.CbRadioButton.setText((""))
    self.CbRadioButton.setAutoExclusive(False)
    self.CbRadioButton.setObjectName(("CbRadioButton"))
    self.CbColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CbColorPushButton.setEnabled(True)
    self.CbColorPushButton.setGeometry(qt.QRect(360, 184, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CbColorPushButton.sizePolicy.hasHeightForWidth())
    self.CbColorPushButton.setSizePolicy(sizePolicy)
    self.CbColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CbColorPushButton.setObjectName(("CbColorPushButton"))
    self.CcRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CcRadioButton.setEnabled(True)
    self.CcRadioButton.setGeometry(qt.QRect(410, 245, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CcRadioButton.sizePolicy.hasHeightForWidth())
    self.CcRadioButton.setSizePolicy(sizePolicy)
    self.CcRadioButton.setText((""))
    self.CcRadioButton.setAutoExclusive(False)
    self.CcRadioButton.setObjectName(("CcRadioButton"))
    self.CcColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CcColorPushButton.setEnabled(True)
    self.CcColorPushButton.setGeometry(qt.QRect(405, 225, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CcColorPushButton.sizePolicy.hasHeightForWidth())
    self.CcColorPushButton.setSizePolicy(sizePolicy)
    self.CcColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CcColorPushButton.setObjectName(("CcColorPushButton"))
    self.CdRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CdRadioButton.setEnabled(True)
    self.CdRadioButton.setGeometry(qt.QRect(443, 299, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CdRadioButton.sizePolicy.hasHeightForWidth())
    self.CdRadioButton.setSizePolicy(sizePolicy)
    self.CdRadioButton.setText((""))
    self.CdRadioButton.setAutoExclusive(False)
    self.CdRadioButton.setObjectName(("CdRadioButton"))
    self.CdColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CdColorPushButton.setEnabled(True)
    self.CdColorPushButton.setGeometry(qt.QRect(438, 277, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CdColorPushButton.sizePolicy.hasHeightForWidth())
    self.CdColorPushButton.setSizePolicy(sizePolicy)
    self.CdColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CdColorPushButton.setObjectName(("CdColorPushButton"))
    self.CeRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CeRadioButton.setEnabled(True)
    self.CeRadioButton.setGeometry(qt.QRect(455, 359, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CeRadioButton.sizePolicy.hasHeightForWidth())
    self.CeRadioButton.setSizePolicy(sizePolicy)
    self.CeRadioButton.setText((""))
    self.CeRadioButton.setAutoExclusive(False)
    self.CeRadioButton.setObjectName(("CeRadioButton"))
    self.CeColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CeColorPushButton.setEnabled(True)
    self.CeColorPushButton.setGeometry(qt.QRect(453, 337, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CeColorPushButton.sizePolicy.hasHeightForWidth())
    self.CeColorPushButton.setSizePolicy(sizePolicy)
    self.CeColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CeColorPushButton.setObjectName(("CeColorPushButton"))
    self.CfRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CfRadioButton.setEnabled(True)
    self.CfRadioButton.setGeometry(qt.QRect(443, 417, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CfRadioButton.sizePolicy.hasHeightForWidth())
    self.CfRadioButton.setSizePolicy(sizePolicy)
    self.CfRadioButton.setText((""))
    self.CfRadioButton.setAutoExclusive(False)
    self.CfRadioButton.setObjectName(("CfRadioButton"))
    self.CfColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CfColorPushButton.setEnabled(True)
    self.CfColorPushButton.setGeometry(qt.QRect(441, 393, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CfColorPushButton.sizePolicy.hasHeightForWidth())
    self.CfColorPushButton.setSizePolicy(sizePolicy)
    self.CfColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CfColorPushButton.setObjectName(("CfColorPushButton"))
    self.CgRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CgRadioButton.setEnabled(True)
    self.CgRadioButton.setGeometry(qt.QRect(410, 472, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CgRadioButton.sizePolicy.hasHeightForWidth())
    self.CgRadioButton.setSizePolicy(sizePolicy)
    self.CgRadioButton.setText((""))
    self.CgRadioButton.setAutoExclusive(False)
    self.CgRadioButton.setObjectName(("CgRadioButton"))
    self.CgColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CgColorPushButton.setEnabled(True)
    self.CgColorPushButton.setGeometry(qt.QRect(411, 447, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CgColorPushButton.sizePolicy.hasHeightForWidth())
    self.CgColorPushButton.setSizePolicy(sizePolicy)
    self.CgColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CgColorPushButton.setObjectName(("CgColorPushButton"))
    self.ChRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.ChRadioButton.setEnabled(True)
    self.ChRadioButton.setGeometry(qt.QRect(363, 511, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.ChRadioButton.sizePolicy.hasHeightForWidth())
    self.ChRadioButton.setSizePolicy(sizePolicy)
    self.ChRadioButton.setText((""))
    self.ChRadioButton.setAutoExclusive(False)
    self.ChRadioButton.setObjectName(("ChRadioButton"))
    self.ChColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.ChColorPushButton.setEnabled(True)
    self.ChColorPushButton.setGeometry(qt.QRect(360, 487, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.ChColorPushButton.sizePolicy.hasHeightForWidth())
    self.ChColorPushButton.setSizePolicy(sizePolicy)
    self.ChColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.ChColorPushButton.setObjectName(("ChColorPushButton"))
    self.CiRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CiRadioButton.setEnabled(True)
    self.CiRadioButton.setGeometry(qt.QRect(302, 533, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CiRadioButton.sizePolicy.hasHeightForWidth())
    self.CiRadioButton.setSizePolicy(sizePolicy)
    self.CiRadioButton.setText((""))
    self.CiRadioButton.setAutoExclusive(False)
    self.CiRadioButton.setObjectName(("CiRadioButton"))
    self.CiColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CiColorPushButton.setEnabled(True)
    self.CiColorPushButton.setGeometry(qt.QRect(297, 511, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CiColorPushButton.sizePolicy.hasHeightForWidth())
    self.CiColorPushButton.setSizePolicy(sizePolicy)
    self.CiColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CiColorPushButton.setObjectName(("CiColorPushButton"))
    self.CjRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CjRadioButton.setEnabled(True)
    self.CjRadioButton.setGeometry(qt.QRect(236, 533, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CjRadioButton.sizePolicy.hasHeightForWidth())
    self.CjRadioButton.setSizePolicy(sizePolicy)
    self.CjRadioButton.setText((""))
    self.CjRadioButton.setAutoExclusive(False)
    self.CjRadioButton.setObjectName(("CjRadioButton"))
    self.CjColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CjColorPushButton.setEnabled(True)
    self.CjColorPushButton.setGeometry(qt.QRect(234, 513, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CjColorPushButton.sizePolicy.hasHeightForWidth())
    self.CjColorPushButton.setSizePolicy(sizePolicy)
    self.CjColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CjColorPushButton.setObjectName(("CjColorPushButton"))
    self.CkRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CkRadioButton.setEnabled(True)
    self.CkRadioButton.setGeometry(qt.QRect(176, 514, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CkRadioButton.sizePolicy.hasHeightForWidth())
    self.CkRadioButton.setSizePolicy(sizePolicy)
    self.CkRadioButton.setText((""))
    self.CkRadioButton.setAutoExclusive(False)
    self.CkRadioButton.setObjectName(("CkRadioButton"))
    self.CkColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CkColorPushButton.setEnabled(True)
    self.CkColorPushButton.setGeometry(qt.QRect(177, 486, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CkColorPushButton.sizePolicy.hasHeightForWidth())
    self.CkColorPushButton.setSizePolicy(sizePolicy)
    self.CkColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CkColorPushButton.setObjectName(("CkColorPushButton"))
    self.ClRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.ClRadioButton.setEnabled(True)
    self.ClRadioButton.setGeometry(qt.QRect(128, 473, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.ClRadioButton.sizePolicy.hasHeightForWidth())
    self.ClRadioButton.setSizePolicy(sizePolicy)
    self.ClRadioButton.setText((""))
    self.ClRadioButton.setAutoExclusive(False)
    self.ClRadioButton.setObjectName(("ClRadioButton"))
    self.ClColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.ClColorPushButton.setEnabled(True)
    self.ClColorPushButton.setGeometry(qt.QRect(123, 456, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.ClColorPushButton.sizePolicy.hasHeightForWidth())
    self.ClColorPushButton.setSizePolicy(sizePolicy)
    self.ClColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.ClColorPushButton.setObjectName(("ClColorPushButton"))
    self.CmRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CmRadioButton.setEnabled(True)
    self.CmRadioButton.setGeometry(qt.QRect(95, 423, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CmRadioButton.sizePolicy.hasHeightForWidth())
    self.CmRadioButton.setSizePolicy(sizePolicy)
    self.CmRadioButton.setText((""))
    self.CmRadioButton.setAutoExclusive(False)
    self.CmRadioButton.setObjectName(("CmRadioButton"))
    self.CmColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CmColorPushButton.setEnabled(True)
    self.CmColorPushButton.setGeometry(qt.QRect(96, 402, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CmColorPushButton.sizePolicy.hasHeightForWidth())
    self.CmColorPushButton.setSizePolicy(sizePolicy)
    self.CmColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CmColorPushButton.setObjectName(("CmColorPushButton"))
    self.CnRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CnRadioButton.setEnabled(True)
    self.CnRadioButton.setGeometry(qt.QRect(86, 359, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CnRadioButton.sizePolicy.hasHeightForWidth())
    self.CnRadioButton.setSizePolicy(sizePolicy)
    self.CnRadioButton.setText((""))
    self.CnRadioButton.setAutoExclusive(False)
    self.CnRadioButton.setObjectName(("CnRadioButton"))
    self.CnColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CnColorPushButton.setEnabled(True)
    self.CnColorPushButton.setGeometry(qt.QRect(87, 333, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CnColorPushButton.sizePolicy.hasHeightForWidth())
    self.CnColorPushButton.setSizePolicy(sizePolicy)
    self.CnColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CnColorPushButton.setObjectName(("CnColorPushButton"))
    self.CoRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.CoRadioButton.setEnabled(True)
    self.CoRadioButton.setGeometry(qt.QRect(96, 298, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CoRadioButton.sizePolicy.hasHeightForWidth())
    self.CoRadioButton.setSizePolicy(sizePolicy)
    self.CoRadioButton.setText((""))
    self.CoRadioButton.setAutoExclusive(False)
    self.CoRadioButton.setObjectName(("CoRadioButton"))
    self.CoColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.CoColorPushButton.setEnabled(True)
    self.CoColorPushButton.setGeometry(qt.QRect(93, 277, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.CoColorPushButton.sizePolicy.hasHeightForWidth())
    self.CoColorPushButton.setSizePolicy(sizePolicy)
    self.CoColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.CoColorPushButton.setObjectName(("CoColorPushButton"))
    self.BaRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BaRadioButton.setEnabled(True)
    self.BaRadioButton.setGeometry(qt.QRect(273, 242, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BaRadioButton.sizePolicy.hasHeightForWidth())
    self.BaRadioButton.setSizePolicy(sizePolicy)
    self.BaRadioButton.setText((""))
    self.BaRadioButton.setAutoExclusive(False)
    self.BaRadioButton.setObjectName(("BaRadioButton"))
    self.BaColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BaColorPushButton.setEnabled(True)
    self.BaColorPushButton.setGeometry(qt.QRect(270, 222, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BaColorPushButton.sizePolicy.hasHeightForWidth())
    self.BaColorPushButton.setSizePolicy(sizePolicy)
    self.BaColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BaColorPushButton.setObjectName(("BaColorPushButton"))
    self.BbColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BbColorPushButton.setEnabled(True)
    self.BbColorPushButton.setGeometry(qt.QRect(330, 237, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BbColorPushButton.sizePolicy.hasHeightForWidth())
    self.BbColorPushButton.setSizePolicy(sizePolicy)
    self.BbColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BbColorPushButton.setObjectName(("BbColorPushButton"))
    self.BbRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BbRadioButton.setEnabled(True)
    self.BbRadioButton.setGeometry(qt.QRect(333, 256, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BbRadioButton.sizePolicy.hasHeightForWidth())
    self.BbRadioButton.setSizePolicy(sizePolicy)
    self.BbRadioButton.setText((""))
    self.BbRadioButton.setAutoExclusive(False)
    self.BbRadioButton.setObjectName(("BbRadioButton"))
    self.BcColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BcColorPushButton.setEnabled(True)
    self.BcColorPushButton.setGeometry(qt.QRect(369, 279, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BcColorPushButton.sizePolicy.hasHeightForWidth())
    self.BcColorPushButton.setSizePolicy(sizePolicy)
    self.BcColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BcColorPushButton.setObjectName(("BcColorPushButton"))
    self.BcRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BcRadioButton.setEnabled(True)
    self.BcRadioButton.setGeometry(qt.QRect(375, 301, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BcRadioButton.sizePolicy.hasHeightForWidth())
    self.BcRadioButton.setSizePolicy(sizePolicy)
    self.BcRadioButton.setText((""))
    self.BcRadioButton.setAutoExclusive(False)
    self.BcRadioButton.setObjectName(("BcRadioButton"))
    self.BdColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BdColorPushButton.setEnabled(True)
    self.BdColorPushButton.setGeometry(qt.QRect(393, 336, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BdColorPushButton.sizePolicy.hasHeightForWidth())
    self.BdColorPushButton.setSizePolicy(sizePolicy)
    self.BdColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BdColorPushButton.setObjectName(("BdColorPushButton"))
    self.BdRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BdRadioButton.setEnabled(True)
    self.BdRadioButton.setGeometry(qt.QRect(393, 358, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BdRadioButton.sizePolicy.hasHeightForWidth())
    self.BdRadioButton.setSizePolicy(sizePolicy)
    self.BdRadioButton.setText((""))
    self.BdRadioButton.setAutoExclusive(False)
    self.BdRadioButton.setObjectName(("BdRadioButton"))
    self.BeColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BeColorPushButton.setEnabled(True)
    self.BeColorPushButton.setGeometry(qt.QRect(372, 396, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BeColorPushButton.sizePolicy.hasHeightForWidth())
    self.BeColorPushButton.setSizePolicy(sizePolicy)
    self.BeColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BeColorPushButton.setObjectName(("BeColorPushButton"))
    self.BeRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BeRadioButton.setEnabled(True)
    self.BeRadioButton.setGeometry(qt.QRect(375, 418, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BeRadioButton.sizePolicy.hasHeightForWidth())
    self.BeRadioButton.setSizePolicy(sizePolicy)
    self.BeRadioButton.setText((""))
    self.BeRadioButton.setAutoExclusive(False)
    self.BeRadioButton.setObjectName(("BeRadioButton"))
    self.BfColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BfColorPushButton.setEnabled(True)
    self.BfColorPushButton.setGeometry(qt.QRect(327, 441, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BfColorPushButton.sizePolicy.hasHeightForWidth())
    self.BfColorPushButton.setSizePolicy(sizePolicy)
    self.BfColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BfColorPushButton.setObjectName(("BfColorPushButton"))
    self.BfRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BfRadioButton.setEnabled(True)
    self.BfRadioButton.setGeometry(qt.QRect(330, 460, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BfRadioButton.sizePolicy.hasHeightForWidth())
    self.BfRadioButton.setSizePolicy(sizePolicy)
    self.BfRadioButton.setText((""))
    self.BfRadioButton.setAutoExclusive(False)
    self.BfRadioButton.setObjectName(("BfRadioButton"))
    self.BgColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BgColorPushButton.setEnabled(True)
    self.BgColorPushButton.setGeometry(qt.QRect(264, 459, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BgColorPushButton.sizePolicy.hasHeightForWidth())
    self.BgColorPushButton.setSizePolicy(sizePolicy)
    self.BgColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BgColorPushButton.setObjectName(("BgColorPushButton"))
    self.BgRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BgRadioButton.setEnabled(True)
    self.BgRadioButton.setGeometry(qt.QRect(270, 478, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BgRadioButton.sizePolicy.hasHeightForWidth())
    self.BgRadioButton.setSizePolicy(sizePolicy)
    self.BgRadioButton.setText((""))
    self.BgRadioButton.setAutoExclusive(False)
    self.BgRadioButton.setObjectName(("BgRadioButton"))
    self.BhColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BhColorPushButton.setEnabled(True)
    self.BhColorPushButton.setGeometry(qt.QRect(204, 441, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BhColorPushButton.sizePolicy.hasHeightForWidth())
    self.BhColorPushButton.setSizePolicy(sizePolicy)
    self.BhColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BhColorPushButton.setObjectName(("BhColorPushButton"))
    self.BhRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BhRadioButton.setEnabled(True)
    self.BhRadioButton.setGeometry(qt.QRect(210, 463, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BhRadioButton.sizePolicy.hasHeightForWidth())
    self.BhRadioButton.setSizePolicy(sizePolicy)
    self.BhRadioButton.setText((""))
    self.BhRadioButton.setAutoExclusive(False)
    self.BhRadioButton.setObjectName(("BhRadioButton"))
    self.BiColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BiColorPushButton.setEnabled(True)
    self.BiColorPushButton.setGeometry(qt.QRect(165, 399, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BiColorPushButton.sizePolicy.hasHeightForWidth())
    self.BiColorPushButton.setSizePolicy(sizePolicy)
    self.BiColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BiColorPushButton.setObjectName(("BiColorPushButton"))
    self.BiRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BiRadioButton.setEnabled(True)
    self.BiRadioButton.setGeometry(qt.QRect(165, 418, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BiRadioButton.sizePolicy.hasHeightForWidth())
    self.BiRadioButton.setSizePolicy(sizePolicy)
    self.BiRadioButton.setText((""))
    self.BiRadioButton.setAutoExclusive(False)
    self.BiRadioButton.setObjectName(("BiRadioButton"))
    self.BjColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BjColorPushButton.setEnabled(True)
    self.BjColorPushButton.setGeometry(qt.QRect(138, 336, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BjColorPushButton.sizePolicy.hasHeightForWidth())
    self.BjColorPushButton.setSizePolicy(sizePolicy)
    self.BjColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BjColorPushButton.setObjectName(("BjColorPushButton"))
    self.BjRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BjRadioButton.setEnabled(True)
    self.BjRadioButton.setGeometry(qt.QRect(147, 360, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BjRadioButton.sizePolicy.hasHeightForWidth())
    self.BjRadioButton.setSizePolicy(sizePolicy)
    self.BjRadioButton.setText((""))
    self.BjRadioButton.setAutoExclusive(False)
    self.BjRadioButton.setObjectName(("BjRadioButton"))
    self.BkColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BkColorPushButton.setEnabled(True)
    self.BkColorPushButton.setGeometry(qt.QRect(162, 279, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BkColorPushButton.sizePolicy.hasHeightForWidth())
    self.BkColorPushButton.setSizePolicy(sizePolicy)
    self.BkColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BkColorPushButton.setObjectName(("BkColorPushButton"))
    self.BkRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BkRadioButton.setEnabled(True)
    self.BkRadioButton.setGeometry(qt.QRect(162, 301, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BkRadioButton.sizePolicy.hasHeightForWidth())
    self.BkRadioButton.setSizePolicy(sizePolicy)
    self.BkRadioButton.setText((""))
    self.BkRadioButton.setAutoExclusive(False)
    self.BkRadioButton.setObjectName(("BkRadioButton"))
    self.BlColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.BlColorPushButton.setEnabled(True)
    self.BlColorPushButton.setGeometry(qt.QRect(204, 237, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BlColorPushButton.sizePolicy.hasHeightForWidth())
    self.BlColorPushButton.setSizePolicy(sizePolicy)
    self.BlColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.BlColorPushButton.setObjectName(("BlColorPushButton"))
    self.BlRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.BlRadioButton.setEnabled(True)
    self.BlRadioButton.setGeometry(qt.QRect(210, 259, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.BlRadioButton.sizePolicy.hasHeightForWidth())
    self.BlRadioButton.setSizePolicy(sizePolicy)
    self.BlRadioButton.setText((""))
    self.BlRadioButton.setAutoExclusive(False)
    self.BlRadioButton.setObjectName(("BlRadioButton"))
    self.AaColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.AaColorPushButton.setEnabled(True)
    self.AaColorPushButton.setGeometry(qt.QRect(306, 279, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AaColorPushButton.sizePolicy.hasHeightForWidth())
    self.AaColorPushButton.setSizePolicy(sizePolicy)
    self.AaColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.AaColorPushButton.setObjectName(("AaColorPushButton"))
    self.AaRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.AaRadioButton.setEnabled(True)
    self.AaRadioButton.setGeometry(qt.QRect(306, 304, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AaRadioButton.sizePolicy.hasHeightForWidth())
    self.AaRadioButton.setSizePolicy(sizePolicy)
    self.AaRadioButton.setText((""))
    self.AaRadioButton.setAutoExclusive(False)
    self.AaRadioButton.setObjectName(("AaRadioButton"))
    self.AbColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.AbColorPushButton.setEnabled(True)
    self.AbColorPushButton.setGeometry(qt.QRect(333, 336, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AbColorPushButton.sizePolicy.hasHeightForWidth())
    self.AbColorPushButton.setSizePolicy(sizePolicy)
    self.AbColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.AbColorPushButton.setObjectName(("AbColorPushButton"))
    self.AbRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.AbRadioButton.setEnabled(True)
    self.AbRadioButton.setGeometry(qt.QRect(336, 361, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AbRadioButton.sizePolicy.hasHeightForWidth())
    self.AbRadioButton.setSizePolicy(sizePolicy)
    self.AbRadioButton.setText((""))
    self.AbRadioButton.setAutoExclusive(False)
    self.AbRadioButton.setObjectName(("AbRadioButton"))
    self.AcColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.AcColorPushButton.setEnabled(True)
    self.AcColorPushButton.setGeometry(qt.QRect(300, 399, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AcColorPushButton.sizePolicy.hasHeightForWidth())
    self.AcColorPushButton.setSizePolicy(sizePolicy)
    self.AcColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.AcColorPushButton.setObjectName(("AcColorPushButton"))
    self.AcRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.AcRadioButton.setEnabled(True)
    self.AcRadioButton.setGeometry(qt.QRect(299, 418, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AcRadioButton.sizePolicy.hasHeightForWidth())
    self.AcRadioButton.setSizePolicy(sizePolicy)
    self.AcRadioButton.setText((""))
    self.AcRadioButton.setAutoExclusive(False)
    self.AcRadioButton.setObjectName(("AcRadioButton"))
    self.AdColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.AdColorPushButton.setEnabled(True)
    self.AdColorPushButton.setGeometry(qt.QRect(243, 399, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AdColorPushButton.sizePolicy.hasHeightForWidth())
    self.AdColorPushButton.setSizePolicy(sizePolicy)
    self.AdColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.AdColorPushButton.setObjectName(("AdColorPushButton"))
    self.AdRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.AdRadioButton.setEnabled(True)
    self.AdRadioButton.setGeometry(qt.QRect(239, 415, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AdRadioButton.sizePolicy.hasHeightForWidth())
    self.AdRadioButton.setSizePolicy(sizePolicy)
    self.AdRadioButton.setText((""))
    self.AdRadioButton.setAutoExclusive(False)
    self.AdRadioButton.setObjectName(("AdRadioButton"))
    self.AeColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.AeColorPushButton.setEnabled(True)
    self.AeColorPushButton.setGeometry(qt.QRect(204, 336, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AeColorPushButton.sizePolicy.hasHeightForWidth())
    self.AeColorPushButton.setSizePolicy(sizePolicy)
    self.AeColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.AeColorPushButton.setObjectName(("AeColorPushButton"))
    self.AeRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.AeRadioButton.setEnabled(True)
    self.AeRadioButton.setGeometry(qt.QRect(206, 363, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AeRadioButton.sizePolicy.hasHeightForWidth())
    self.AeRadioButton.setSizePolicy(sizePolicy)
    self.AeRadioButton.setText((""))
    self.AeRadioButton.setAutoExclusive(False)
    self.AeRadioButton.setObjectName(("AeRadioButton"))
    self.AfColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.AfColorPushButton.setEnabled(True)
    self.AfColorPushButton.setGeometry(qt.QRect(243, 279, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AfColorPushButton.sizePolicy.hasHeightForWidth())
    self.AfColorPushButton.setSizePolicy(sizePolicy)
    self.AfColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.AfColorPushButton.setObjectName(("AfColorPushButton"))
    self.AfRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.AfRadioButton.setEnabled(True)
    self.AfRadioButton.setGeometry(qt.QRect(239, 304, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AfRadioButton.sizePolicy.hasHeightForWidth())
    self.AfRadioButton.setSizePolicy(sizePolicy)
    self.AfRadioButton.setText((""))
    self.AfRadioButton.setAutoExclusive(False)
    self.AfRadioButton.setObjectName(("AfRadioButton"))
    self.IuColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.IuColorPushButton.setEnabled(True)
    self.IuColorPushButton.setGeometry(qt.QRect(273, 333, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.IuColorPushButton.sizePolicy.hasHeightForWidth())
    self.IuColorPushButton.setSizePolicy(sizePolicy)
    self.IuColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.IuColorPushButton.setObjectName(("IuColorPushButton"))
    self.IuRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.IuRadioButton.setEnabled(True)
    self.IuRadioButton.setGeometry(qt.QRect(269, 358, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.IuRadioButton.sizePolicy.hasHeightForWidth())
    self.IuRadioButton.setSizePolicy(sizePolicy)
    self.IuRadioButton.setText((""))
    self.IuRadioButton.setAutoExclusive(False)
    self.IuRadioButton.setObjectName(("IuRadioButton"))
    self.DaColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DaColorPushButton.setEnabled(True)
    self.DaColorPushButton.setGeometry(qt.QRect(264, 99, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DaColorPushButton.sizePolicy.hasHeightForWidth())
    self.DaColorPushButton.setSizePolicy(sizePolicy)
    self.DaColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DaColorPushButton.setObjectName(("DaColorPushButton"))
    self.DaRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DaRadioButton.setEnabled(True)
    self.DaRadioButton.setGeometry(qt.QRect(269, 124, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DaRadioButton.sizePolicy.hasHeightForWidth())
    self.DaRadioButton.setSizePolicy(sizePolicy)
    self.DaRadioButton.setText((""))
    self.DaRadioButton.setAutoExclusive(False)
    self.DaRadioButton.setObjectName(("DaRadioButton"))
    self.DbColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DbColorPushButton.setEnabled(True)
    self.DbColorPushButton.setGeometry(qt.QRect(330, 111, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DbColorPushButton.sizePolicy.hasHeightForWidth())
    self.DbColorPushButton.setSizePolicy(sizePolicy)
    self.DbColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DbColorPushButton.setObjectName(("DbColorPushButton"))
    self.DbRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DbRadioButton.setEnabled(True)
    self.DbRadioButton.setGeometry(qt.QRect(332, 133, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DbRadioButton.sizePolicy.hasHeightForWidth())
    self.DbRadioButton.setSizePolicy(sizePolicy)
    self.DbRadioButton.setText((""))
    self.DbRadioButton.setAutoExclusive(False)
    self.DbRadioButton.setObjectName(("DbRadioButton"))
    self.DcColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DcColorPushButton.setEnabled(True)
    self.DcColorPushButton.setGeometry(qt.QRect(390, 129, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DcColorPushButton.sizePolicy.hasHeightForWidth())
    self.DcColorPushButton.setSizePolicy(sizePolicy)
    self.DcColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DcColorPushButton.setObjectName(("DcColorPushButton"))
    self.DcRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DcRadioButton.setEnabled(True)
    self.DcRadioButton.setGeometry(qt.QRect(392, 154, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DcRadioButton.sizePolicy.hasHeightForWidth())
    self.DcRadioButton.setSizePolicy(sizePolicy)
    self.DcRadioButton.setText((""))
    self.DcRadioButton.setAutoExclusive(False)
    self.DcRadioButton.setObjectName(("DcRadioButton"))
    self.DdColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DdColorPushButton.setEnabled(True)
    self.DdColorPushButton.setGeometry(qt.QRect(393, 537, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DdColorPushButton.sizePolicy.hasHeightForWidth())
    self.DdColorPushButton.setSizePolicy(sizePolicy)
    self.DdColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DdColorPushButton.setObjectName(("DdColorPushButton"))
    self.DdRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DdRadioButton.setEnabled(True)
    self.DdRadioButton.setGeometry(qt.QRect(392, 562, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DdRadioButton.sizePolicy.hasHeightForWidth())
    self.DdRadioButton.setSizePolicy(sizePolicy)
    self.DdRadioButton.setText((""))
    self.DdRadioButton.setAutoExclusive(False)
    self.DdRadioButton.setObjectName(("DdRadioButton"))
    self.DeColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DeColorPushButton.setEnabled(True)
    self.DeColorPushButton.setGeometry(qt.QRect(333, 567, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DeColorPushButton.sizePolicy.hasHeightForWidth())
    self.DeColorPushButton.setSizePolicy(sizePolicy)
    self.DeColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DeColorPushButton.setObjectName(("DeColorPushButton"))
    self.DeRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DeRadioButton.setEnabled(True)
    self.DeRadioButton.setGeometry(qt.QRect(335, 586, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DeRadioButton.sizePolicy.hasHeightForWidth())
    self.DeRadioButton.setSizePolicy(sizePolicy)
    self.DeRadioButton.setText((""))
    self.DeRadioButton.setAutoExclusive(False)
    self.DeRadioButton.setObjectName(("DeRadioButton"))
    self.DfColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DfColorPushButton.setEnabled(True)
    self.DfColorPushButton.setGeometry(qt.QRect(267, 579, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DfColorPushButton.sizePolicy.hasHeightForWidth())
    self.DfColorPushButton.setSizePolicy(sizePolicy)
    self.DfColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DfColorPushButton.setObjectName(("DfColorPushButton"))
    self.DfRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DfRadioButton.setEnabled(True)
    self.DfRadioButton.setGeometry(qt.QRect(269, 598, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DfRadioButton.sizePolicy.hasHeightForWidth())
    self.DfRadioButton.setSizePolicy(sizePolicy)
    self.DfRadioButton.setText((""))
    self.DfRadioButton.setAutoExclusive(False)
    self.DfRadioButton.setObjectName(("DfRadioButton"))
    self.DgColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DgColorPushButton.setEnabled(True)
    self.DgColorPushButton.setGeometry(qt.QRect(204, 567, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DgColorPushButton.sizePolicy.hasHeightForWidth())
    self.DgColorPushButton.setSizePolicy(sizePolicy)
    self.DgColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DgColorPushButton.setObjectName(("DgColorPushButton"))
    self.DgRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DgRadioButton.setEnabled(True)
    self.DgRadioButton.setGeometry(qt.QRect(206, 589, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DgRadioButton.sizePolicy.hasHeightForWidth())
    self.DgRadioButton.setSizePolicy(sizePolicy)
    self.DgRadioButton.setText((""))
    self.DgRadioButton.setAutoExclusive(False)
    self.DgRadioButton.setObjectName(("DgRadioButton"))
    self.DhColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DhColorPushButton.setEnabled(True)
    self.DhColorPushButton.setGeometry(qt.QRect(144, 540, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DhColorPushButton.sizePolicy.hasHeightForWidth())
    self.DhColorPushButton.setSizePolicy(sizePolicy)
    self.DhColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DhColorPushButton.setObjectName(("DhColorPushButton"))
    self.DhRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DhRadioButton.setEnabled(True)
    self.DhRadioButton.setGeometry(qt.QRect(146, 565, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DhRadioButton.sizePolicy.hasHeightForWidth())
    self.DhRadioButton.setSizePolicy(sizePolicy)
    self.DhRadioButton.setText((""))
    self.DhRadioButton.setAutoExclusive(False)
    self.DhRadioButton.setObjectName(("DhRadioButton"))
    self.DiColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DiColorPushButton.setEnabled(True)
    self.DiColorPushButton.setGeometry(qt.QRect(144, 138, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DiColorPushButton.sizePolicy.hasHeightForWidth())
    self.DiColorPushButton.setSizePolicy(sizePolicy)
    self.DiColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DiColorPushButton.setObjectName(("DiColorPushButton"))
    self.DiRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DiRadioButton.setEnabled(True)
    self.DiRadioButton.setGeometry(qt.QRect(146, 157, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DiRadioButton.sizePolicy.hasHeightForWidth())
    self.DiRadioButton.setSizePolicy(sizePolicy)
    self.DiRadioButton.setText((""))
    self.DiRadioButton.setAutoExclusive(False)
    self.DiRadioButton.setObjectName(("DiRadioButton"))
    self.DjColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.DjColorPushButton.setEnabled(True)
    self.DjColorPushButton.setGeometry(qt.QRect(201, 114, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DjColorPushButton.sizePolicy.hasHeightForWidth())
    self.DjColorPushButton.setSizePolicy(sizePolicy)
    self.DjColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.DjColorPushButton.setObjectName(("DjColorPushButton"))
    self.DjRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.DjRadioButton.setEnabled(True)
    self.DjRadioButton.setGeometry(qt.QRect(206, 133, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.DjRadioButton.sizePolicy.hasHeightForWidth())
    self.DjRadioButton.setSizePolicy(sizePolicy)
    self.DjRadioButton.setText((""))
    self.DjRadioButton.setAutoExclusive(False)
    self.DjRadioButton.setObjectName(("DjRadioButton"))
    self.EaColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.EaColorPushButton.setEnabled(True)
    self.EaColorPushButton.setGeometry(qt.QRect(294, 48, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EaColorPushButton.sizePolicy.hasHeightForWidth())
    self.EaColorPushButton.setSizePolicy(sizePolicy)
    self.EaColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.EaColorPushButton.setObjectName(("EaColorPushButton"))
    self.EaRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.EaRadioButton.setEnabled(True)
    self.EaRadioButton.setGeometry(qt.QRect(297, 69, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EaRadioButton.sizePolicy.hasHeightForWidth())
    self.EaRadioButton.setSizePolicy(sizePolicy)
    self.EaRadioButton.setText((""))
    self.EaRadioButton.setAutoExclusive(False)
    self.EaRadioButton.setObjectName(("EaRadioButton"))
    self.EbRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.EbRadioButton.setEnabled(True)
    self.EbRadioButton.setGeometry(qt.QRect(348, 77, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EbRadioButton.sizePolicy.hasHeightForWidth())
    self.EbRadioButton.setSizePolicy(sizePolicy)
    self.EbRadioButton.setText((""))
    self.EbRadioButton.setAutoExclusive(False)
    self.EbRadioButton.setObjectName(("EbRadioButton"))
    self.EbColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.EbColorPushButton.setEnabled(True)
    self.EbColorPushButton.setGeometry(qt.QRect(348, 58, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EbColorPushButton.sizePolicy.hasHeightForWidth())
    self.EbColorPushButton.setSizePolicy(sizePolicy)
    self.EbColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.EbColorPushButton.setObjectName(("EbColorPushButton"))
    self.EcRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.EcRadioButton.setEnabled(True)
    self.EcRadioButton.setGeometry(qt.QRect(350, 643, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EcRadioButton.sizePolicy.hasHeightForWidth())
    self.EcRadioButton.setSizePolicy(sizePolicy)
    self.EcRadioButton.setText((""))
    self.EcRadioButton.setAutoExclusive(False)
    self.EcRadioButton.setObjectName(("EcRadioButton"))
    self.EcColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.EcColorPushButton.setEnabled(True)
    self.EcColorPushButton.setGeometry(qt.QRect(348, 624, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EcColorPushButton.sizePolicy.hasHeightForWidth())
    self.EcColorPushButton.setSizePolicy(sizePolicy)
    self.EcColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.EcColorPushButton.setObjectName(("EcColorPushButton"))
    self.EdRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.EdRadioButton.setEnabled(True)
    self.EdRadioButton.setGeometry(qt.QRect(296, 653, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EdRadioButton.sizePolicy.hasHeightForWidth())
    self.EdRadioButton.setSizePolicy(sizePolicy)
    self.EdRadioButton.setText((""))
    self.EdRadioButton.setAutoExclusive(False)
    self.EdRadioButton.setObjectName(("EdRadioButton"))
    self.EdColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.EdColorPushButton.setEnabled(True)
    self.EdColorPushButton.setGeometry(qt.QRect(294, 633, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EdColorPushButton.sizePolicy.hasHeightForWidth())
    self.EdColorPushButton.setSizePolicy(sizePolicy)
    self.EdColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.EdColorPushButton.setObjectName(("EdColorPushButton"))
    self.EeRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.EeRadioButton.setEnabled(True)
    self.EeRadioButton.setGeometry(qt.QRect(245, 653, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EeRadioButton.sizePolicy.hasHeightForWidth())
    self.EeRadioButton.setSizePolicy(sizePolicy)
    self.EeRadioButton.setText((""))
    self.EeRadioButton.setAutoExclusive(False)
    self.EeRadioButton.setObjectName(("EeRadioButton"))
    self.EeColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.EeColorPushButton.setEnabled(True)
    self.EeColorPushButton.setGeometry(qt.QRect(243, 633, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EeColorPushButton.sizePolicy.hasHeightForWidth())
    self.EeColorPushButton.setSizePolicy(sizePolicy)
    self.EeColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.EeColorPushButton.setObjectName(("EeColorPushButton"))
    self.EfRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.EfRadioButton.setEnabled(True)
    self.EfRadioButton.setGeometry(qt.QRect(191, 644, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EfRadioButton.sizePolicy.hasHeightForWidth())
    self.EfRadioButton.setSizePolicy(sizePolicy)
    self.EfRadioButton.setText((""))
    self.EfRadioButton.setAutoExclusive(False)
    self.EfRadioButton.setObjectName(("EfRadioButton"))
    self.EfColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.EfColorPushButton.setEnabled(True)
    self.EfColorPushButton.setGeometry(qt.QRect(186, 624, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EfColorPushButton.sizePolicy.hasHeightForWidth())
    self.EfColorPushButton.setSizePolicy(sizePolicy)
    self.EfColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.EfColorPushButton.setObjectName(("EfColorPushButton"))
    self.EgRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.EgRadioButton.setEnabled(True)
    self.EgRadioButton.setGeometry(qt.QRect(192, 77, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EgRadioButton.sizePolicy.hasHeightForWidth())
    self.EgRadioButton.setSizePolicy(sizePolicy)
    self.EgRadioButton.setText((""))
    self.EgRadioButton.setAutoExclusive(False)
    self.EgRadioButton.setObjectName(("EgRadioButton"))
    self.EgColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.EgColorPushButton.setEnabled(True)
    self.EgColorPushButton.setGeometry(qt.QRect(186, 58, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EgColorPushButton.sizePolicy.hasHeightForWidth())
    self.EgColorPushButton.setSizePolicy(sizePolicy)
    self.EgColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.EgColorPushButton.setObjectName(("EgColorPushButton"))
    self.EhRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.EhRadioButton.setEnabled(True)
    self.EhRadioButton.setGeometry(qt.QRect(242, 68, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EhRadioButton.sizePolicy.hasHeightForWidth())
    self.EhRadioButton.setSizePolicy(sizePolicy)
    self.EhRadioButton.setText((""))
    self.EhRadioButton.setAutoExclusive(False)
    self.EhRadioButton.setObjectName(("EhRadioButton"))
    self.EhColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.EhColorPushButton.setEnabled(True)
    self.EhColorPushButton.setGeometry(qt.QRect(237, 48, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.EhColorPushButton.sizePolicy.hasHeightForWidth())
    self.EhColorPushButton.setSizePolicy(sizePolicy)
    self.EhColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.EhColorPushButton.setObjectName(("EhColorPushButton"))
    self.FaRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.FaRadioButton.setEnabled(True)
    self.FaRadioButton.setGeometry(qt.QRect(437, 125, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FaRadioButton.sizePolicy.hasHeightForWidth())
    self.FaRadioButton.setSizePolicy(sizePolicy)
    self.FaRadioButton.setText((""))
    self.FaRadioButton.setAutoExclusive(False)
    self.FaRadioButton.setObjectName(("FaRadioButton"))
    self.FaColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.FaColorPushButton.setEnabled(True)
    self.FaColorPushButton.setGeometry(qt.QRect(435, 102, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FaColorPushButton.sizePolicy.hasHeightForWidth())
    self.FaColorPushButton.setSizePolicy(sizePolicy)
    self.FaColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.FaColorPushButton.setObjectName(("FaColorPushButton"))
    self.FbRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.FbRadioButton.setEnabled(True)
    self.FbRadioButton.setGeometry(qt.QRect(455, 152, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FbRadioButton.sizePolicy.hasHeightForWidth())
    self.FbRadioButton.setSizePolicy(sizePolicy)
    self.FbRadioButton.setText((""))
    self.FbRadioButton.setAutoExclusive(False)
    self.FbRadioButton.setObjectName(("FbRadioButton"))
    self.FbColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.FbColorPushButton.setEnabled(True)
    self.FbColorPushButton.setGeometry(qt.QRect(456, 129, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FbColorPushButton.sizePolicy.hasHeightForWidth())
    self.FbColorPushButton.setSizePolicy(sizePolicy)
    self.FbColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.FbColorPushButton.setObjectName(("FbColorPushButton"))
    self.FhRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.FhRadioButton.setEnabled(True)
    self.FhRadioButton.setGeometry(qt.QRect(105, 128, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FhRadioButton.sizePolicy.hasHeightForWidth())
    self.FhRadioButton.setSizePolicy(sizePolicy)
    self.FhRadioButton.setText((""))
    self.FhRadioButton.setAutoExclusive(False)
    self.FhRadioButton.setObjectName(("FhRadioButton"))
    self.FhColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.FhColorPushButton.setEnabled(True)
    self.FhColorPushButton.setGeometry(qt.QRect(102, 109, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FhColorPushButton.sizePolicy.hasHeightForWidth())
    self.FhColorPushButton.setSizePolicy(sizePolicy)
    self.FhColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.FhColorPushButton.setObjectName(("FhColorPushButton"))
    self.FgRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.FgRadioButton.setEnabled(True)
    self.FgRadioButton.setGeometry(qt.QRect(84, 158, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FgRadioButton.sizePolicy.hasHeightForWidth())
    self.FgRadioButton.setSizePolicy(sizePolicy)
    self.FgRadioButton.setText((""))
    self.FgRadioButton.setAutoExclusive(False)
    self.FgRadioButton.setObjectName(("FgRadioButton"))
    self.FgColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.FgColorPushButton.setEnabled(True)
    self.FgColorPushButton.setGeometry(qt.QRect(81, 141, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FgColorPushButton.sizePolicy.hasHeightForWidth())
    self.FgColorPushButton.setSizePolicy(sizePolicy)
    self.FgColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.FgColorPushButton.setObjectName(("FgColorPushButton"))
    self.FcRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.FcRadioButton.setEnabled(True)
    self.FcRadioButton.setGeometry(qt.QRect(458, 566, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FcRadioButton.sizePolicy.hasHeightForWidth())
    self.FcRadioButton.setSizePolicy(sizePolicy)
    self.FcRadioButton.setText((""))
    self.FcRadioButton.setAutoExclusive(False)
    self.FcRadioButton.setObjectName(("FcRadioButton"))
    self.FcColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.FcColorPushButton.setEnabled(True)
    self.FcColorPushButton.setGeometry(qt.QRect(456, 543, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FcColorPushButton.sizePolicy.hasHeightForWidth())
    self.FcColorPushButton.setSizePolicy(sizePolicy)
    self.FcColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.FcColorPushButton.setObjectName(("FcColorPushButton"))
    self.FdRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.FdRadioButton.setEnabled(True)
    self.FdRadioButton.setGeometry(qt.QRect(437, 593, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FdRadioButton.sizePolicy.hasHeightForWidth())
    self.FdRadioButton.setSizePolicy(sizePolicy)
    self.FdRadioButton.setText((""))
    self.FdRadioButton.setAutoExclusive(False)
    self.FdRadioButton.setObjectName(("FdRadioButton"))
    self.FdColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.FdColorPushButton.setEnabled(True)
    self.FdColorPushButton.setGeometry(qt.QRect(432, 576, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FdColorPushButton.sizePolicy.hasHeightForWidth())
    self.FdColorPushButton.setSizePolicy(sizePolicy)
    self.FdColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.FdColorPushButton.setObjectName(("FdColorPushButton"))
    self.FeRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.FeRadioButton.setEnabled(True)
    self.FeRadioButton.setGeometry(qt.QRect(107, 596, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FeRadioButton.sizePolicy.hasHeightForWidth())
    self.FeRadioButton.setSizePolicy(sizePolicy)
    self.FeRadioButton.setText((""))
    self.FeRadioButton.setAutoExclusive(False)
    self.FeRadioButton.setObjectName(("FeRadioButton"))
    self.FeColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.FeColorPushButton.setEnabled(True)
    self.FeColorPushButton.setGeometry(qt.QRect(105, 573, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FeColorPushButton.sizePolicy.hasHeightForWidth())
    self.FeColorPushButton.setSizePolicy(sizePolicy)
    self.FeColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.FeColorPushButton.setObjectName(("FeColorPushButton"))
    self.FfRadioButton = qt.QRadioButton(TemplateSheetWidget)
    self.FfRadioButton.setEnabled(True)
    self.FfRadioButton.setGeometry(qt.QRect(83, 565, 24, 16))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FfRadioButton.sizePolicy.hasHeightForWidth())
    self.FfRadioButton.setSizePolicy(sizePolicy)
    self.FfRadioButton.setText((""))
    self.FfRadioButton.setAutoExclusive(False)
    self.FfRadioButton.setObjectName(("FfRadioButton"))
    self.FfColorPushButton = qt.QPushButton(TemplateSheetWidget)
    self.FfColorPushButton.setEnabled(True)
    self.FfColorPushButton.setGeometry(qt.QRect(81, 540, 21, 21))
    sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.FfColorPushButton.sizePolicy.hasHeightForWidth())
    self.FfColorPushButton.setSizePolicy(sizePolicy)
    self.FfColorPushButton.setStyleSheet(("background-color: rgb(0, 255, 0);"))
    self.FfColorPushButton.setObjectName(("FfColorPushButton"))
    self.RegistrationProcessingLabel = qt.QLabel(TemplateSheetWidget)
    self.RegistrationProcessingLabel.setEnabled(True)
    self.RegistrationProcessingLabel.setGeometry(qt.QRect(462, 60, 54, 12))
    self.RegistrationProcessingLabel.setText((""))
    self.RegistrationProcessingLabel.setObjectName(("RegistrationProcessingLabel"))
#------------------------------------------------------------------------------------
    # self.AddVolumePushButton.connect( "clicked()", self.addVolume())
    # self.LoadTemplatePushButton.connect( "clicked()", self.loadTemplate())
    self.SelectNeedlesPushButton.connect( "clicked()", self.selectNeedles())

    self.IuRadioButton.connect( "clicked()", self.showIuNeedle())
    self.AaRadioButton.connect( "clicked()", self.showAaNeedle())
    self.AbRadioButton.connect( "clicked()", self.showAbNeedle())
    self.AcRadioButton.connect( "clicked()", self.showAcNeedle())
    self.AdRadioButton.connect( "clicked()", self.showAdNeedle())
    self.AeRadioButton.connect( "clicked()", self.showAeNeedle())
    self.AfRadioButton.connect( "clicked()", self.showAfNeedle())
    self.BaRadioButton.connect( "clicked()", self.showBaNeedle())
    self.BbRadioButton.connect( "clicked()", self.showBbNeedle())
    self.BcRadioButton.connect( "clicked()", self.showBcNeedle())
    self.BdRadioButton.connect( "clicked()", self.showBdNeedle())
    self.BeRadioButton.connect( "clicked()", self.showBeNeedle())
    self.BfRadioButton.connect( "clicked()", self.showBfNeedle())
    self.BgRadioButton.connect( "clicked()", self.showBgNeedle())
    self.BhRadioButton.connect( "clicked()", self.showBhNeedle())
    self.BiRadioButton.connect( "clicked()", self.showBiNeedle())
    self.BjRadioButton.connect( "clicked()", self.showBjNeedle())
    self.BkRadioButton.connect( "clicked()", self.showBkNeedle())
    self.BlRadioButton.connect( "clicked()", self.showBlNeedle())
    self.CaRadioButton.connect( "clicked()", self.showCaNeedle())
    self.CbRadioButton.connect( "clicked()", self.showCbNeedle())
    self.CcRadioButton.connect( "clicked()", self.showCcNeedle())
    self.CdRadioButton.connect( "clicked()", self.showCdNeedle())
    self.CeRadioButton.connect( "clicked()", self.showCeNeedle())
    self.CfRadioButton.connect( "clicked()", self.showCfNeedle())
    self.CgRadioButton.connect( "clicked()", self.showCgNeedle())
    self.ChRadioButton.connect( "clicked()", self.showChNeedle())
    self.CiRadioButton.connect( "clicked()", self.showCiNeedle())
    self.CjRadioButton.connect( "clicked()", self.showCjNeedle())
    self.CkRadioButton.connect( "clicked()", self.showCkNeedle())
    self.ClRadioButton.connect( "clicked()", self.showClNeedle())
    self.CmRadioButton.connect( "clicked()", self.showCmNeedle())
    self.CnRadioButton.connect( "clicked()", self.showCnNeedle())
    self.CoRadioButton.connect( "clicked()", self.showCoNeedle())
    self.CpRadioButton.connect( "clicked()", self.showCpNeedle())
    self.CqRadioButton.connect( "clicked()", self.showCqNeedle())
    self.CrRadioButton.connect( "clicked()", self.showCrNeedle())
    self.DaRadioButton.connect( "clicked()", self.showDaNeedle())
    self.DbRadioButton.connect( "clicked()", self.showDbNeedle())
    self.DcRadioButton.connect( "clicked()", self.showDcNeedle())
    self.DdRadioButton.connect( "clicked()", self.showDdNeedle())
    self.DeRadioButton.connect( "clicked()", self.showDeNeedle())
    self.DfRadioButton.connect( "clicked()", self.showDfNeedle())
    self.DgRadioButton.connect( "clicked()", self.showDgNeedle())
    self.DhRadioButton.connect( "clicked()", self.showDhNeedle())
    self.DiRadioButton.connect( "clicked()", self.showDiNeedle())
    self.DjRadioButton.connect( "clicked()", self.showDjNeedle())
    self.EaRadioButton.connect( "clicked()", self.showEaNeedle())
    self.EbRadioButton.connect( "clicked()", self.showEbNeedle())
    self.EcRadioButton.connect( "clicked()", self.showEcNeedle())
    self.EdRadioButton.connect( "clicked()", self.showEdNeedle())
    self.EeRadioButton.connect( "clicked()", self.showEeNeedle())
    self.EfRadioButton.connect( "clicked()", self.showEfNeedle())
    self.EgRadioButton.connect( "clicked()", self.showEgNeedle())
    self.EhRadioButton.connect( "clicked()", self.showEhNeedle())
    self.FaRadioButton.connect( "clicked()", self.showFaNeedle())
    self.FbRadioButton.connect( "clicked()", self.showFbNeedle())
    self.FcRadioButton.connect( "clicked()", self.showFcNeedle())
    self.FdRadioButton.connect( "clicked()", self.showFdNeedle())
    self.FeRadioButton.connect( "clicked()", self.showFeNeedle())
    self.FfRadioButton.connect( "clicked()", self.showFfNeedle())
    self.FgRadioButton.connect( "clicked()", self.showFgNeedle())
    self.FhRadioButton.connect( "clicked()", self.showFhNeedle())
     
    self.ShowNeedlesPushButton.connect( "clicked()", self.showNeedles())
    # self.CADmodel2ImageRegPushButton.connect( "clicked()", self.registerCADmodelToImage()) 
    # self.ObturatorSpinBox.connect("valueChanged(int)", self.pushObutrator())

    self.IuColorPushButton.connect( "clicked()",self.setIuColor())
    self.AaColorPushButton.connect( "clicked()", self.setAaColor())
    self.AbColorPushButton.connect( "clicked()", self.setAbColor())
    self.AcColorPushButton.connect( "clicked()", self.setAcColor())
    self.AdColorPushButton.connect( "clicked()", self.setAdColor())
    self.AeColorPushButton.connect( "clicked()", self.setAeColor())
    self.AfColorPushButton.connect( "clicked()", self.setAfColor())
    self.BaColorPushButton.connect( "clicked()",self.setBaColor())
    self.BbColorPushButton.connect( "clicked()", self.setBbColor())
    self.BcColorPushButton.connect( "clicked()", self.setBcColor())
    self.BdColorPushButton.connect( "clicked()", self.setBdColor())
    self.BeColorPushButton.connect( "clicked()", self.setBeColor())
    self.BfColorPushButton.connect( "clicked()", self.setBfColor())
    self.BgColorPushButton.connect( "clicked()", self.setBgColor())
    self.BhColorPushButton.connect( "clicked()", self.setBhColor())
    self.BiColorPushButton.connect( "clicked()", self.setBiColor())
    self.BjColorPushButton.connect( "clicked()", self.setBjColor())
    self.BkColorPushButton.connect( "clicked()", self.setBkColor())
    self.BlColorPushButton.connect( "clicked()", self.setBlColor())
    self.CaColorPushButton.connect( "clicked()", self.setCaColor())
    self.CbColorPushButton.connect( "clicked()", self.setCbColor())
    self.CcColorPushButton.connect( "clicked()", self.setCcColor())
    self.CdColorPushButton.connect( "clicked()", self.setCdColor())
    self.CeColorPushButton.connect( "clicked()", self.setCeColor())
    self.CfColorPushButton.connect( "clicked()", self.setCfColor())
    self.CgColorPushButton.connect( "clicked()", self.setCgColor())
    self.ChColorPushButton.connect( "clicked()", self.setChColor())
    self.CiColorPushButton.connect( "clicked()", self.setCiColor())
    self.CjColorPushButton.connect( "clicked()", self.setCjColor())
    self.CkColorPushButton.connect( "clicked()", self.setCkColor())
    self.ClColorPushButton.connect( "clicked()", self.setClColor())
    self.CmColorPushButton.connect( "clicked()", self.setCmColor())
    self.CnColorPushButton.connect( "clicked()", self.setCnColor())
    self.CoColorPushButton.connect( "clicked()", self.setCoColor())
    self.CpColorPushButton.connect( "clicked()", self.setCpColor())
    self.CqColorPushButton.connect( "clicked()", self.setCqColor())
    self.CrColorPushButton.connect( "clicked()", self.setCrColor())
    self.DaColorPushButton.connect( "clicked()", self.setDaColor())
    self.DbColorPushButton.connect( "clicked()", self.setDbColor())
    self.DcColorPushButton.connect( "clicked()", self.setDcColor())
    self.DdColorPushButton.connect( "clicked()", self.setDdColor())
    self.DeColorPushButton.connect( "clicked()", self.setDeColor())
    self.DfColorPushButton.connect( "clicked()", self.setDfColor())
    self.DgColorPushButton.connect( "clicked()", self.setDgColor())
    self.DhColorPushButton.connect( "clicked()", self.setDhColor())
    self.DiColorPushButton.connect( "clicked()", self.setDiColor())
    self.DjColorPushButton.connect( "clicked()", self.setDjColor())
    self.EaColorPushButton.connect( "clicked()", self.setEaColor())
    self.EbColorPushButton.connect( "clicked()", self.setEbColor())
    self.EcColorPushButton.connect( "clicked()", self.setEcColor())
    self.EdColorPushButton.connect( "clicked()", self.setEdColor())
    self.EeColorPushButton.connect( "clicked()", self.setEeColor())
    self.EfColorPushButton.connect( "clicked()", self.setEfColor())
    self.EgColorPushButton.connect( "clicked()", self.setEgColor())
    self.EhColorPushButton.connect( "clicked()", self.setEhColor())  
    self.FaColorPushButton.connect( "clicked()", self.setFaColor())
    self.FbColorPushButton.connect( "clicked()", self.setFbColor())
    self.FcColorPushButton.connect( "clicked()", self.setFcColor())
    self.FdColorPushButton.connect( "clicked()", self.setFdColor())
    self.FeColorPushButton.connect( "clicked()", self.setFeColor())
    self.FfColorPushButton.connect( "clicked()", self.setFfColor())
    self.FgColorPushButton.connect( "clicked()", self.setFgColor())
    self.FhColorPushButton.connect( "clicked()", self.setFhColor())  
     
    popup = ctk.ctkPopupWidget(self.BaColorPushButton)
    self.popupSpinboxBa = qt.QSpinBox(popup)
    self.createSpinbox(popup,self.popupSpinboxBa)
    self.popupSpinboxBa.connect("valueChanged(int)", self.pushBaNeedle())

    popupBb = ctk.ctkPopupWidget(self.BbColorPushButton)
    self.popupSpinboxBb = qt.QSpinBox(popupBb)
    self.createSpinbox(popupBb,self.popupSpinboxBb)
    self.popupSpinboxBb.connect("valueChanged(int)", self.pushBbNeedle())

    popupBc = ctk.ctkPopupWidget(self.BcColorPushButton)
    self.popupSpinboxBc = qt.QSpinBox(popupBc)
    self.createSpinbox(popupBc,self.popupSpinboxBc)
    self.popupSpinboxBc.connect("valueChanged(int)", self.pushBcNeedle())

    popupBd = ctk.ctkPopupWidget(self.BdColorPushButton)
    self.popupSpinboxBd = qt.QSpinBox(popupBd)
    self.createSpinbox(popupBd,self.popupSpinboxBd)
    self.popupSpinboxBd.connect("valueChanged(int)", self.pushBdNeedle())

    popupBe = ctk.ctkPopupWidget(self.BeColorPushButton)
    self.popupSpinboxBe = qt.QSpinBox(popupBe)
    self.createSpinbox(popupBe,self.popupSpinboxBe)
    self.popupSpinboxBe.connect("valueChanged(int)", self.pushBeNeedle())

    popupBf = ctk.ctkPopupWidget(self.BfColorPushButton)
    self.popupSpinboxBf = qt.QSpinBox(popupBf)
    self.createSpinbox(popupBf,self.popupSpinboxBf)
    self.popupSpinboxBf.connect("valueChanged(int)", self.pushBfNeedle())

    popupBg = ctk.ctkPopupWidget(self.BgColorPushButton)
    self.popupSpinboxBg = qt.QSpinBox(popupBg)
    self.createSpinbox(popupBg,self.popupSpinboxBg)
    self.popupSpinboxBg.connect("valueChanged(int)", self.pushBgNeedle())

    popupBh = ctk.ctkPopupWidget(self.BhColorPushButton)
    self.popupSpinboxBh = qt.QSpinBox(popupBh)
    self.createSpinbox(popupBh,self.popupSpinboxBh)
    self.popupSpinboxBh.connect("valueChanged(int)", self.pushBhNeedle())

    popupBi = ctk.ctkPopupWidget(self.BiColorPushButton)
    self.popupSpinboxBi = qt.QSpinBox(popupBi)
    self.createSpinbox(popupBi,self.popupSpinboxBi)
    self.popupSpinboxBi.connect("valueChanged(int)", self.pushBiNeedle())

    popupBj = ctk.ctkPopupWidget(self.BjColorPushButton)
    self.popupSpinboxBj = qt.QSpinBox(popupBj)
    self.createSpinbox(popupBj,self.popupSpinboxBj)
    self.popupSpinboxBj.connect("valueChanged(int)", self.pushBjNeedle())

    popupBk = ctk.ctkPopupWidget(self.BkColorPushButton)
    self.popupSpinboxBk = qt.QSpinBox(popupBk)
    self.createSpinbox(popupBk,self.popupSpinboxBk)
    self.popupSpinboxBk.connect("valueChanged(int)", self.pushBkNeedle())

    popupBl = ctk.ctkPopupWidget(self.BlColorPushButton)
    self.popupSpinboxBl = qt.QSpinBox(popupBl)
    self.createSpinbox(popupBl,self.popupSpinboxBl)
    self.popupSpinboxBl.connect("valueChanged(int)", self.pushBlNeedle())

    popupAa = ctk.ctkPopupWidget(self.AaColorPushButton)
    self.popupSpinboxAa = qt.QSpinBox(popupAa)
    self.createSpinbox(popupAa,self.popupSpinboxAa)
    self.popupSpinboxAa.connect("valueChanged(int)", self.pushAaNeedle())

    popupAb = ctk.ctkPopupWidget(self.AbColorPushButton)
    self.popupSpinboxAb = qt.QSpinBox(popupAb)
    self.createSpinbox(popupAb,self.popupSpinboxAb)
    self.popupSpinboxAb.connect("valueChanged(int)", self.pushAbNeedle())

    popupAc = ctk.ctkPopupWidget(self.AcColorPushButton)
    self.popupSpinboxAc = qt.QSpinBox(popupAc)
    self.createSpinbox(popupAc,self.popupSpinboxAc)
    self.popupSpinboxAc.connect("valueChanged(int)", self.pushAcNeedle())

    popupAd = ctk.ctkPopupWidget(self.AdColorPushButton)
    self.popupSpinboxAd = qt.QSpinBox(popupAd)
    self.createSpinbox(popupAd,self.popupSpinboxAd)
    self.popupSpinboxAd.connect("valueChanged(int)", self.pushAdNeedle())

    popupAe = ctk.ctkPopupWidget(self.AeColorPushButton)
    self.popupSpinboxAe = qt.QSpinBox(popupAe)
    self.createSpinbox(popupAe,self.popupSpinboxAe)
    self.popupSpinboxAe.connect("valueChanged(int)", self.pushAeNeedle())

    popupAf = ctk.ctkPopupWidget(self.AfColorPushButton)
    self.popupSpinboxAf = qt.QSpinBox(popupAf)
    self.createSpinbox(popupAf,self.popupSpinboxAf)
    self.popupSpinboxAf.connect("valueChanged(int)", self.pushAfNeedle())

    popupCa = ctk.ctkPopupWidget(self.CaColorPushButton)
    self.popupSpinboxCa = qt.QSpinBox(popupCa)
    self.createSpinbox(popupCa,self.popupSpinboxCa)
    self.popupSpinboxCa.connect("valueChanged(int)", self.pushCaNeedle())

    popupCb = ctk.ctkPopupWidget(self.CbColorPushButton)
    self.popupSpinboxCb = qt.QSpinBox(popupCb)
    self.createSpinbox(popupCb,self.popupSpinboxCb)
    self.popupSpinboxCb.connect("valueChanged(int)", self.pushCbNeedle())

    popupCc = ctk.ctkPopupWidget(self.CcColorPushButton)
    self.popupSpinboxCc = qt.QSpinBox(popupCc)
    self.createSpinbox(popupCc,self.popupSpinboxCc)
    self.popupSpinboxCc.connect("valueChanged(int)", self.pushCcNeedle())

    popupCd = ctk.ctkPopupWidget(self.CdColorPushButton)
    self.popupSpinboxCd = qt.QSpinBox(popupCd)
    self.createSpinbox(popupCd,self.popupSpinboxCd)
    self.popupSpinboxCd.connect("valueChanged(int)", self.pushCdNeedle())

    popupCe = ctk.ctkPopupWidget(self.CeColorPushButton)
    self.popupSpinboxCe = qt.QSpinBox(popupCe)
    self.createSpinbox(popupCe,self.popupSpinboxCe)
    self.popupSpinboxCe.connect("valueChanged(int)", self.pushCeNeedle())

    popupCf = ctk.ctkPopupWidget(self.CfColorPushButton)
    self.popupSpinboxCf = qt.QSpinBox(popupCf)
    self.createSpinbox(popupCf,self.popupSpinboxCf)
    self.popupSpinboxCf.connect("valueChanged(int)", self.pushCfNeedle())

    popupCg = ctk.ctkPopupWidget(self.CgColorPushButton)
    self.popupSpinboxCg = qt.QSpinBox(popupCg)
    self.createSpinbox(popupCg,self.popupSpinboxCg)
    self.popupSpinboxCg.connect("valueChanged(int)", self.pushCgNeedle())

    popupCh = ctk.ctkPopupWidget(self.ChColorPushButton)
    self.popupSpinboxCh = qt.QSpinBox(popupCh)
    self.createSpinbox(popupCh,self.popupSpinboxCh)
    self.popupSpinboxCh.connect("valueChanged(int)", self.pushChNeedle())

    popupCi = ctk.ctkPopupWidget(self.CiColorPushButton)
    self.popupSpinboxCi = qt.QSpinBox(popupCi)
    self.createSpinbox(popupCi,self.popupSpinboxCi)
    self.popupSpinboxCi.connect("valueChanged(int)", self.pushCiNeedle())

    popupCj = ctk.ctkPopupWidget(self.CjColorPushButton)
    self.popupSpinboxCj = qt.QSpinBox(popupCj)
    self.createSpinbox(popupCj,self.popupSpinboxCj)
    self.popupSpinboxCj.connect("valueChanged(int)", self.pushCjNeedle())

    popupCk = ctk.ctkPopupWidget(self.CkColorPushButton)
    self.popupSpinboxCk = qt.QSpinBox(popupCk)
    self.createSpinbox(popupCk,self.popupSpinboxCk)
    self.popupSpinboxCk.connect("valueChanged(int)", self.pushCkNeedle())

    popupCl = ctk.ctkPopupWidget(self.ClColorPushButton)
    self.popupSpinboxCl = qt.QSpinBox(popupCl)
    self.createSpinbox(popupCl,self.popupSpinboxCl)
    self.popupSpinboxCl.connect("valueChanged(int)", self.pushClNeedle())

    popupCm = ctk.ctkPopupWidget(self.CmColorPushButton)
    self.popupSpinboxCm = qt.QSpinBox(popupCm)
    self.createSpinbox(popupCm,self.popupSpinboxCm)
    self.popupSpinboxCm.connect("valueChanged(int)", self.pushCmNeedle())

    popupCn = ctk.ctkPopupWidget(self.CnColorPushButton)
    self.popupSpinboxCn = qt.QSpinBox(popupCn)
    self.createSpinbox(popupCn,self.popupSpinboxCn)
    self.popupSpinboxCn.connect("valueChanged(int)", self.pushCnNeedle())

    popupCo = ctk.ctkPopupWidget(self.CoColorPushButton)
    self.popupSpinboxCo = qt.QSpinBox(popupCo)
    self.createSpinbox(popupCo,self.popupSpinboxCo)
    self.popupSpinboxCo.connect("valueChanged(int)", self.pushCoNeedle())

    popupCp = ctk.ctkPopupWidget(self.CpColorPushButton)
    self.popupSpinboxCp = qt.QSpinBox(popupCp)
    self.createSpinbox(popupCp,self.popupSpinboxCp)
    self.popupSpinboxCp.connect("valueChanged(int)", self.pushCpNeedle())

    popupCq = ctk.ctkPopupWidget(self.CqColorPushButton)
    self.popupSpinboxCq = qt.QSpinBox(popupCq)
    self.createSpinbox(popupCq,self.popupSpinboxCq)
    self.popupSpinboxCq.connect("valueChanged(int)", self.pushCqNeedle())

    popupCr = ctk.ctkPopupWidget(self.CrColorPushButton)
    self.popupSpinboxCr = qt.QSpinBox(popupCr)
    self.createSpinbox(popupCr,self.popupSpinboxCr)
    self.popupSpinboxCr.connect("valueChanged(int)", self.pushCrNeedle())

    popupDa = ctk.ctkPopupWidget(self.DaColorPushButton)
    self.popupSpinboxDa = qt.QSpinBox(popupDa)
    self.createSpinbox(popupDa,self.popupSpinboxDa)
    self.popupSpinboxDa.connect("valueChanged(int)", self.pushDaNeedle())

    popupDb = ctk.ctkPopupWidget(self.DbColorPushButton)
    self.popupSpinboxDb = qt.QSpinBox(popupDb)
    self.createSpinbox(popupDb,self.popupSpinboxDb)
    self.popupSpinboxDb.connect("valueChanged(int)", self.pushDbNeedle())

    popupDc = ctk.ctkPopupWidget(self.DcColorPushButton)
    self.popupSpinboxDc = qt.QSpinBox(popupDc)
    self.createSpinbox(popupDc,self.popupSpinboxDc)
    self.popupSpinboxDc.connect("valueChanged(int)", self.pushDcNeedle())

    popupDd = ctk.ctkPopupWidget(self.DdColorPushButton)
    self.popupSpinboxDd = qt.QSpinBox(popupDd)
    self.createSpinbox(popupDd,self.popupSpinboxDd)
    self.popupSpinboxDd.connect("valueChanged(int)", self.pushDdNeedle())

    popupDe = ctk.ctkPopupWidget(self.DeColorPushButton)
    self.popupSpinboxDe = qt.QSpinBox(popupDe)
    self.createSpinbox(popupDe,self.popupSpinboxDe)
    self.popupSpinboxDe.connect("valueChanged(int)", self.pushDeNeedle())

    popupDf = ctk.ctkPopupWidget(self.DfColorPushButton)
    self.popupSpinboxDf = qt.QSpinBox(popupDf)
    self.createSpinbox(popupDf,self.popupSpinboxDf)
    self.popupSpinboxDf.connect("valueChanged(int)", self.pushDfNeedle())

    popupDg = ctk.ctkPopupWidget(self.DgColorPushButton)
    self.popupSpinboxDg = qt.QSpinBox(popupDg)
    self.createSpinbox(popupDg,self.popupSpinboxDg)
    self.popupSpinboxDg.connect("valueChanged(int)", self.pushDgNeedle())

    popupDh = ctk.ctkPopupWidget(self.DhColorPushButton)
    self.popupSpinboxDh = qt.QSpinBox(popupDh)
    self.createSpinbox(popupDh,self.popupSpinboxDh)
    self.popupSpinboxDh.connect("valueChanged(int)", self.pushDhNeedle())

    popupDi = ctk.ctkPopupWidget(self.DiColorPushButton)
    self.popupSpinboxDi = qt.QSpinBox(popupDi)
    self.createSpinbox(popupDi,self.popupSpinboxDi)
    self.popupSpinboxDi.connect("valueChanged(int)", self.pushDiNeedle())

    popupDj = ctk.ctkPopupWidget(self.DjColorPushButton)
    self.popupSpinboxDj = qt.QSpinBox(popupDj)
    self.createSpinbox(popupDj,self.popupSpinboxDj)
    self.popupSpinboxDj.connect("valueChanged(int)", self.pushDjNeedle())

    popupEa = ctk.ctkPopupWidget(self.EaColorPushButton)
    self.popupSpinboxEa = qt.QSpinBox(popupEa)
    self.createSpinbox(popupEa,self.popupSpinboxEa)
    self.popupSpinboxEa.connect("valueChanged(int)", self.pushEaNeedle())

    popupEb = ctk.ctkPopupWidget(self.EbColorPushButton)
    self.popupSpinboxEb = qt.QSpinBox(popupEb)
    self.createSpinbox(popupEb,self.popupSpinboxEb)
    self.popupSpinboxEb.connect("valueChanged(int)", self.pushEbNeedle())

    popupEc = ctk.ctkPopupWidget(self.EcColorPushButton)
    self.popupSpinboxEc = qt.QSpinBox(popupEc)
    self.createSpinbox(popupEc,self.popupSpinboxEc)
    self.popupSpinboxEc.connect("valueChanged(int)", self.pushEcNeedle())

    popupEd = ctk.ctkPopupWidget(self.EdColorPushButton)
    self.popupSpinboxEd = qt.QSpinBox(popupEd)
    self.createSpinbox(popupEd,self.popupSpinboxEd)
    self.popupSpinboxEd.connect("valueChanged(int)", self.pushEdNeedle())

    popupEe = ctk.ctkPopupWidget(self.EeColorPushButton)
    self.popupSpinboxEe = qt.QSpinBox(popupEe)
    self.createSpinbox(popupEe,self.popupSpinboxEe)
    self.popupSpinboxEe.connect("valueChanged(int)", self.pushEeNeedle())

    popupEf = ctk.ctkPopupWidget(self.EfColorPushButton)
    self.popupSpinboxEf = qt.QSpinBox(popupEf)
    self.createSpinbox(popupEf,self.popupSpinboxEf)
    self.popupSpinboxEf.connect("valueChanged(int)", self.pushEfNeedle())

    popupEg = ctk.ctkPopupWidget(self.EgColorPushButton)
    self.popupSpinboxEg = qt.QSpinBox(popupEg)
    self.createSpinbox(popupEg,self.popupSpinboxEg)
    self.popupSpinboxEg.connect("valueChanged(int)", self.pushEgNeedle())

    popupEh = ctk.ctkPopupWidget(self.EhColorPushButton)
    self.popupSpinboxEh = qt.QSpinBox(popupEh)
    self.createSpinbox(popupEh,self.popupSpinboxEh)
    self.popupSpinboxEh.connect("valueChanged(int)", self.pushEhNeedle())

    popupFa = ctk.ctkPopupWidget(self.FaColorPushButton)
    self.popupSpinboxFa = qt.QSpinBox(popupFa)
    self.createSpinbox(popupFa,self.popupSpinboxFa)
    self.popupSpinboxFa.connect("valueChanged(int)", self.pushFaNeedle())

    popupFb = ctk.ctkPopupWidget(self.FbColorPushButton)
    self.popupSpinboxFb = qt.QSpinBox(popupFb)
    self.createSpinbox(popupFb,self.popupSpinboxFb)
    self.popupSpinboxFb.connect("valueChanged(int)", self.pushFbNeedle())

    popupFc = ctk.ctkPopupWidget(self.FcColorPushButton)
    self.popupSpinboxFc = qt.QSpinBox(popupFc)
    self.createSpinbox(popupFc,self.popupSpinboxFc)
    self.popupSpinboxFc.connect("valueChanged(int)", self.pushFcNeedle())

    popupFd = ctk.ctkPopupWidget(self.FdColorPushButton)
    self.popupSpinboxFd = qt.QSpinBox(popupFd)
    self.createSpinbox(popupFd,self.popupSpinboxFd)
    self.popupSpinboxFd.connect("valueChanged(int)", self.pushFdNeedle())

    popupFe = ctk.ctkPopupWidget(self.FeColorPushButton)
    self.popupSpinboxFe = qt.QSpinBox(popupFe)
    self.createSpinbox(popupFe,self.popupSpinboxFe)
    self.popupSpinboxFe.connect("valueChanged(int)", self.pushFeNeedle())

    popupFf = ctk.ctkPopupWidget(self.FfColorPushButton)
    self.popupSpinboxFf = qt.QSpinBox(popupFf)
    self.createSpinbox(popupFf,self.popupSpinboxFf)
    self.popupSpinboxFf.connect("valueChanged(int)", self.pushFfNeedle())

    popupFg = ctk.ctkPopupWidget(self.FgColorPushButton)
    self.popupSpinboxFg = qt.QSpinBox(popupFg)
    self.createSpinbox(popupFg,self.popupSpinboxFg)
    self.popupSpinboxFg.connect("valueChanged(int)", self.pushFgNeedle())

    popupFh = ctk.ctkPopupWidget(self.FhColorPushButton)
    self.popupSpinboxFh = qt.QSpinBox(popupFh)
    self.createSpinbox(popupFh,self.popupSpinboxFh)
    self.popupSpinboxFh.connect("valueChanged(int)", self.pushFhNeedle())

    popupIu = ctk.ctkPopupWidget(self.IuColorPushButton)
    self.popupSpinboxIu = qt.QSpinBox(popupIu)
    self.createSpinbox(popupIu,self.popupSpinboxIu)
    self.popupSpinboxIu.connect("valueChanged(int)", self.pushIuNeedle())

    mrmlScene = slicer.mrmlScene
    self.ObturatorNode = mrmlScene.GetNodeByID("vtkMRMLModelNode5")

    if self.ObturatorNode :
    
      self.setNeedleCoordinates()
      self.computerPolydataAndMatrix()    
    
      self.m_poly = vtk.vtkPolyData()  
      self.m_poly.DeepCopy(self.ObturatorNode.GetPolyData())

      for i in xrange(63):
        filename= "vtkMRMLModelNode"+str(i+6)
        mrmlScene=slicer.mrmlScene
        NeedleNode = mrmlScene.GetNodeByID(filename)

        if NeedleNode:
          displayNode =NeedleNode.GetModelDisplayNode()
          nVisibility=displayNode.GetVisibility()  

          if nVisibility==1 :
            self.setRadioButton(i,True)
          else:
            self.setRadioButton(i,False)  

      self.retranslateUi(TemplateSheetWidget)
      # qt.QMetaObject.connectSlotsByName(TemplateSheetWidget)

  def retranslateUi(self, TemplateSheetWidget):
    TemplateSheetWidget.setWindowTitle(qt.QApplication.translate("TemplateSheetWidget", "TemplateSheetWidget", None, qt.QApplication.UnicodeUTF8))
    self.CqColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cq", None, qt.QApplication.UnicodeUTF8))
    self.CpColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cp", None, qt.QApplication.UnicodeUTF8))
    self.CrColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cr", None, qt.QApplication.UnicodeUTF8))
    self.LoadTemplatePushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Load(Scene/Template)", None, qt.QApplication.UnicodeUTF8))
    self.AddVolumePushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "AddVolume", None, qt.QApplication.UnicodeUTF8))
    self.ShowNeedlesPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "ShowNeedles", None, qt.QApplication.UnicodeUTF8))
    self.SelectNeedlesPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "SelectNeedles", None, qt.QApplication.UnicodeUTF8))
    self.CADmodel2ImageRegPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "CADmodel2Image", None, qt.QApplication.UnicodeUTF8))
    self.CaColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ca", None, qt.QApplication.UnicodeUTF8))
    self.CbColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cb", None, qt.QApplication.UnicodeUTF8))
    self.CcColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cc", None, qt.QApplication.UnicodeUTF8))
    self.CdColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cd", None, qt.QApplication.UnicodeUTF8))
    self.CeColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ce", None, qt.QApplication.UnicodeUTF8))
    self.CfColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cf", None, qt.QApplication.UnicodeUTF8))
    self.CgColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cg", None, qt.QApplication.UnicodeUTF8))
    self.ChColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ch", None, qt.QApplication.UnicodeUTF8))
    self.CiColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ci", None, qt.QApplication.UnicodeUTF8))
    self.CjColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cj", None, qt.QApplication.UnicodeUTF8))
    self.CkColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ck", None, qt.QApplication.UnicodeUTF8))
    self.ClColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cl", None, qt.QApplication.UnicodeUTF8))
    self.CmColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cm", None, qt.QApplication.UnicodeUTF8))
    self.CnColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Cn", None, qt.QApplication.UnicodeUTF8))
    self.CoColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Co", None, qt.QApplication.UnicodeUTF8))
    self.BaColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ba", None, qt.QApplication.UnicodeUTF8))
    self.BbColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bb", None, qt.QApplication.UnicodeUTF8))
    self.BcColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bc", None, qt.QApplication.UnicodeUTF8))
    self.BdColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bd", None, qt.QApplication.UnicodeUTF8))
    self.BeColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Be", None, qt.QApplication.UnicodeUTF8))
    self.BfColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bf", None, qt.QApplication.UnicodeUTF8))
    self.BgColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bg", None, qt.QApplication.UnicodeUTF8))
    self.BhColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bh", None, qt.QApplication.UnicodeUTF8))
    self.BiColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bi", None, qt.QApplication.UnicodeUTF8))
    self.BjColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bj", None, qt.QApplication.UnicodeUTF8))
    self.BkColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bk", None, qt.QApplication.UnicodeUTF8))
    self.BlColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Bl", None, qt.QApplication.UnicodeUTF8))
    self.AaColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Aa", None, qt.QApplication.UnicodeUTF8))
    self.AbColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ab", None, qt.QApplication.UnicodeUTF8))
    self.AcColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ac", None, qt.QApplication.UnicodeUTF8))
    self.AdColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ad", None, qt.QApplication.UnicodeUTF8))
    self.AeColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ae", None, qt.QApplication.UnicodeUTF8))
    self.AfColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Af", None, qt.QApplication.UnicodeUTF8))
    self.IuColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Iu", None, qt.QApplication.UnicodeUTF8))
    self.DaColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Da", None, qt.QApplication.UnicodeUTF8))
    self.DbColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Db", None, qt.QApplication.UnicodeUTF8))
    self.DcColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Dc", None, qt.QApplication.UnicodeUTF8))
    self.DdColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Dd", None, qt.QApplication.UnicodeUTF8))
    self.DeColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "De", None, qt.QApplication.UnicodeUTF8))
    self.DfColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Df", None, qt.QApplication.UnicodeUTF8))
    self.DgColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Dg", None, qt.QApplication.UnicodeUTF8))
    self.DhColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Dh", None, qt.QApplication.UnicodeUTF8))
    self.DiColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Di", None, qt.QApplication.UnicodeUTF8))
    self.DjColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Dj", None, qt.QApplication.UnicodeUTF8))
    self.EaColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ea", None, qt.QApplication.UnicodeUTF8))
    self.EbColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Eb", None, qt.QApplication.UnicodeUTF8))
    self.EcColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ec", None, qt.QApplication.UnicodeUTF8))
    self.EdColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ed", None, qt.QApplication.UnicodeUTF8))
    self.EeColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ee", None, qt.QApplication.UnicodeUTF8))
    self.EfColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ef", None, qt.QApplication.UnicodeUTF8))
    self.EgColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Eg", None, qt.QApplication.UnicodeUTF8))
    self.EhColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Eh", None, qt.QApplication.UnicodeUTF8))
    self.FaColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Fa", None, qt.QApplication.UnicodeUTF8))
    self.FbColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Fb", None, qt.QApplication.UnicodeUTF8))
    self.FhColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Fh", None, qt.QApplication.UnicodeUTF8))
    self.FgColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Fg", None, qt.QApplication.UnicodeUTF8))
    self.FcColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Fc", None, qt.QApplication.UnicodeUTF8))
    self.FdColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Fd", None, qt.QApplication.UnicodeUTF8))
    self.FeColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Fe", None, qt.QApplication.UnicodeUTF8))
    self.FfColorPushButton.setText(qt.QApplication.translate("TemplateSheetWidget", "Ff", None, qt.QApplication.UnicodeUTF8))

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

    color = qt.QColorDialog.getColor(qt.QColor(), self)
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
    
        

