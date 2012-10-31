from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
from EditorLib import *
import math
import functools

import string

'''
TODO:
  add advanced option to specify segmentation
'''

class iGyneNeedlePlanningStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '6. Needle position Planning' )
    self.setDescription( 'Position, color, resize needles as you like' )
    self.__parent = super( iGyneNeedlePlanningStep, self )

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
    pNode = self.parameterNode()
    self.__layout = self.__parent.createUserInterface()
    TemplateSheetWidget = qt.QWidget()
    TemplateSheetWidget.resize(552, 682)
    TemplateSheetLayout = qt.QVBoxLayout(TemplateSheetWidget)
    for i in range(43):
      
      TemplateSheetLayout.addWidget(qt.QLabel(''))

    ##########################################################################################
    
    if 1==1:      #TemplateSheetWidget UI
      self.computerPolydataAndMatrix() 
      self.setNeedleCoordinates()
      TemplateSheetWidget.setObjectName("TemplateSheetWidget")
      
      self.label = qt.QLabel(TemplateSheetWidget)
      self.label.setEnabled(True)
      self.label.setGeometry(qt.QRect(5, 52, 541, 625))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.label.sizePolicy.hasHeightForWidth())
      self.label.setSizePolicy(sizePolicy)
      self.label.setText((""))
      pathToImage = slicer.modules.igynepy.path.replace("iGynePy.py","iGynePyTemplate/Template/TemplateSheet.png")
      self.label.setPixmap(qt.QPixmap(pathToImage))
      self.label.setObjectName("label")
      self.CqColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CqColorPushButton.setEnabled(True)
      self.CqColorPushButton.setGeometry(qt.QRect(174, 185, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CqColorPushButton.sizePolicy.hasHeightForWidth())
      self.CqColorPushButton.setSizePolicy(sizePolicy)
      self.CqColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CqColorPushButton.setObjectName("CqColorPushButton")
      self.CpRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CpRadioButton.setEnabled(True)
      self.CpRadioButton.setGeometry(qt.QRect(128, 247, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CpRadioButton.sizePolicy.hasHeightForWidth())
      self.CpRadioButton.setSizePolicy(sizePolicy)
      self.CpRadioButton.setText((""))
      self.CpRadioButton.setAutoExclusive(False)
      self.CpRadioButton.setObjectName("CpRadioButton")
      self.CpColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CpColorPushButton.setEnabled(True)
      self.CpColorPushButton.setGeometry(qt.QRect(123, 225, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CpColorPushButton.sizePolicy.hasHeightForWidth())
      self.CpColorPushButton.setSizePolicy(sizePolicy)
      self.CpColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CpColorPushButton.setObjectName("CpColorPushButton")
      self.CqRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CqRadioButton.setEnabled(True)
      self.CqRadioButton.setGeometry(qt.QRect(177, 208, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CqRadioButton.sizePolicy.hasHeightForWidth())
      self.CqRadioButton.setSizePolicy(sizePolicy)
      self.CqRadioButton.setText((""))
      self.CqRadioButton.setAutoExclusive(False)
      self.CqRadioButton.setObjectName("CqRadioButton")
      self.CrColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CrColorPushButton.setEnabled(True)
      self.CrColorPushButton.setGeometry(qt.QRect(231, 165, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CrColorPushButton.sizePolicy.hasHeightForWidth())
      self.CrColorPushButton.setSizePolicy(sizePolicy)
      self.CrColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CrColorPushButton.setObjectName("CrColorPushButton")
      self.CrRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CrRadioButton.setEnabled(True)
      self.CrRadioButton.setGeometry(qt.QRect(235, 187, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CrRadioButton.sizePolicy.hasHeightForWidth())
      self.CrRadioButton.setSizePolicy(sizePolicy)
      self.CrRadioButton.setText((""))
      self.CrRadioButton.setAutoExclusive(False)
      self.CrRadioButton.setObjectName("CrRadioButton")
      self.CaRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CaRadioButton.setEnabled(True)
      self.CaRadioButton.setGeometry(qt.QRect(299, 185, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CaRadioButton.sizePolicy.hasHeightForWidth())
      self.CaRadioButton.setSizePolicy(sizePolicy)
      self.CaRadioButton.setText((""))
      self.CaRadioButton.setAutoExclusive(False)
      self.CaRadioButton.setObjectName("CaRadioButton")
      self.CaColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CaColorPushButton.setEnabled(True)
      self.CaColorPushButton.setGeometry(qt.QRect(297, 165, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CaColorPushButton.sizePolicy.hasHeightForWidth())
      self.CaColorPushButton.setSizePolicy(sizePolicy)
      self.CaColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CaColorPushButton.setObjectName("CaColorPushButton")
      self.CbRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CbRadioButton.setEnabled(True)
      self.CbRadioButton.setGeometry(qt.QRect(362, 206, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CbRadioButton.sizePolicy.hasHeightForWidth())
      self.CbRadioButton.setSizePolicy(sizePolicy)
      self.CbRadioButton.setText((""))
      self.CbRadioButton.setAutoExclusive(False)
      self.CbRadioButton.setObjectName("CbRadioButton")
      self.CbColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CbColorPushButton.setEnabled(True)
      self.CbColorPushButton.setGeometry(qt.QRect(360, 184, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CbColorPushButton.sizePolicy.hasHeightForWidth())
      self.CbColorPushButton.setSizePolicy(sizePolicy)
      self.CbColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CbColorPushButton.setObjectName("CbColorPushButton")
      self.CcRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CcRadioButton.setEnabled(True)
      self.CcRadioButton.setGeometry(qt.QRect(410, 245, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CcRadioButton.sizePolicy.hasHeightForWidth())
      self.CcRadioButton.setSizePolicy(sizePolicy)
      self.CcRadioButton.setText((""))
      self.CcRadioButton.setAutoExclusive(False)
      self.CcRadioButton.setObjectName("CcRadioButton")
      self.CcColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CcColorPushButton.setEnabled(True)
      self.CcColorPushButton.setGeometry(qt.QRect(405, 225, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CcColorPushButton.sizePolicy.hasHeightForWidth())
      self.CcColorPushButton.setSizePolicy(sizePolicy)
      self.CcColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CcColorPushButton.setObjectName("CcColorPushButton")
      self.CdRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CdRadioButton.setEnabled(True)
      self.CdRadioButton.setGeometry(qt.QRect(443, 299, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CdRadioButton.sizePolicy.hasHeightForWidth())
      self.CdRadioButton.setSizePolicy(sizePolicy)
      self.CdRadioButton.setText((""))
      self.CdRadioButton.setAutoExclusive(False)
      self.CdRadioButton.setObjectName("CdRadioButton")
      self.CdColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CdColorPushButton.setEnabled(True)
      self.CdColorPushButton.setGeometry(qt.QRect(438, 277, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CdColorPushButton.sizePolicy.hasHeightForWidth())
      self.CdColorPushButton.setSizePolicy(sizePolicy)
      self.CdColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CdColorPushButton.setObjectName("CdColorPushButton")
      self.CeRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CeRadioButton.setEnabled(True)
      self.CeRadioButton.setGeometry(qt.QRect(455, 359, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CeRadioButton.sizePolicy.hasHeightForWidth())
      self.CeRadioButton.setSizePolicy(sizePolicy)
      self.CeRadioButton.setText((""))
      self.CeRadioButton.setAutoExclusive(False)
      self.CeRadioButton.setObjectName("CeRadioButton")
      self.CeColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CeColorPushButton.setEnabled(True)
      self.CeColorPushButton.setGeometry(qt.QRect(453, 337, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CeColorPushButton.sizePolicy.hasHeightForWidth())
      self.CeColorPushButton.setSizePolicy(sizePolicy)
      self.CeColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CeColorPushButton.setObjectName("CeColorPushButton")
      self.CfRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CfRadioButton.setEnabled(True)
      self.CfRadioButton.setGeometry(qt.QRect(443, 417, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CfRadioButton.sizePolicy.hasHeightForWidth())
      self.CfRadioButton.setSizePolicy(sizePolicy)
      self.CfRadioButton.setText((""))
      self.CfRadioButton.setAutoExclusive(False)
      self.CfRadioButton.setObjectName("CfRadioButton")
      self.CfColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CfColorPushButton.setEnabled(True)
      self.CfColorPushButton.setGeometry(qt.QRect(441, 393, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CfColorPushButton.sizePolicy.hasHeightForWidth())
      self.CfColorPushButton.setSizePolicy(sizePolicy)
      self.CfColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CfColorPushButton.setObjectName("CfColorPushButton")
      self.CgRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CgRadioButton.setEnabled(True)
      self.CgRadioButton.setGeometry(qt.QRect(410, 472, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CgRadioButton.sizePolicy.hasHeightForWidth())
      self.CgRadioButton.setSizePolicy(sizePolicy)
      self.CgRadioButton.setText((""))
      self.CgRadioButton.setAutoExclusive(False)
      self.CgRadioButton.setObjectName("CgRadioButton")
      self.CgColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CgColorPushButton.setEnabled(True)
      self.CgColorPushButton.setGeometry(qt.QRect(411, 447, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CgColorPushButton.sizePolicy.hasHeightForWidth())
      self.CgColorPushButton.setSizePolicy(sizePolicy)
      self.CgColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CgColorPushButton.setObjectName("CgColorPushButton")
      self.ChRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.ChRadioButton.setEnabled(True)
      self.ChRadioButton.setGeometry(qt.QRect(363, 511, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.ChRadioButton.sizePolicy.hasHeightForWidth())
      self.ChRadioButton.setSizePolicy(sizePolicy)
      self.ChRadioButton.setText((""))
      self.ChRadioButton.setAutoExclusive(False)
      self.ChRadioButton.setObjectName("ChRadioButton")
      self.ChColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.ChColorPushButton.setEnabled(True)
      self.ChColorPushButton.setGeometry(qt.QRect(360, 487, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.ChColorPushButton.sizePolicy.hasHeightForWidth())
      self.ChColorPushButton.setSizePolicy(sizePolicy)
      self.ChColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.ChColorPushButton.setObjectName("ChColorPushButton")
      self.CiRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CiRadioButton.setEnabled(True)
      self.CiRadioButton.setGeometry(qt.QRect(302, 533, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CiRadioButton.sizePolicy.hasHeightForWidth())
      self.CiRadioButton.setSizePolicy(sizePolicy)
      self.CiRadioButton.setText((""))
      self.CiRadioButton.setAutoExclusive(False)
      self.CiRadioButton.setObjectName("CiRadioButton")
      self.CiColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CiColorPushButton.setEnabled(True)
      self.CiColorPushButton.setGeometry(qt.QRect(297, 511, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CiColorPushButton.sizePolicy.hasHeightForWidth())
      self.CiColorPushButton.setSizePolicy(sizePolicy)
      self.CiColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CiColorPushButton.setObjectName("CiColorPushButton")
      self.CjRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CjRadioButton.setEnabled(True)
      self.CjRadioButton.setGeometry(qt.QRect(236, 533, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CjRadioButton.sizePolicy.hasHeightForWidth())
      self.CjRadioButton.setSizePolicy(sizePolicy)
      self.CjRadioButton.setText((""))
      self.CjRadioButton.setAutoExclusive(False)
      self.CjRadioButton.setObjectName("CjRadioButton")
      self.CjColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CjColorPushButton.setEnabled(True)
      self.CjColorPushButton.setGeometry(qt.QRect(234, 513, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CjColorPushButton.sizePolicy.hasHeightForWidth())
      self.CjColorPushButton.setSizePolicy(sizePolicy)
      self.CjColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CjColorPushButton.setObjectName("CjColorPushButton")
      self.CkRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CkRadioButton.setEnabled(True)
      self.CkRadioButton.setGeometry(qt.QRect(176, 514, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CkRadioButton.sizePolicy.hasHeightForWidth())
      self.CkRadioButton.setSizePolicy(sizePolicy)
      self.CkRadioButton.setText((""))
      self.CkRadioButton.setAutoExclusive(False)
      self.CkRadioButton.setObjectName("CkRadioButton")
      self.CkColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CkColorPushButton.setEnabled(True)
      self.CkColorPushButton.setGeometry(qt.QRect(177, 486, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CkColorPushButton.sizePolicy.hasHeightForWidth())
      self.CkColorPushButton.setSizePolicy(sizePolicy)
      self.CkColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CkColorPushButton.setObjectName("CkColorPushButton")
      self.ClRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.ClRadioButton.setEnabled(True)
      self.ClRadioButton.setGeometry(qt.QRect(128, 473, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.ClRadioButton.sizePolicy.hasHeightForWidth())
      self.ClRadioButton.setSizePolicy(sizePolicy)
      self.ClRadioButton.setText((""))
      self.ClRadioButton.setAutoExclusive(False)
      self.ClRadioButton.setObjectName("ClRadioButton")
      self.ClColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.ClColorPushButton.setEnabled(True)
      self.ClColorPushButton.setGeometry(qt.QRect(123, 456, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.ClColorPushButton.sizePolicy.hasHeightForWidth())
      self.ClColorPushButton.setSizePolicy(sizePolicy)
      self.ClColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.ClColorPushButton.setObjectName("ClColorPushButton")
      self.CmRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CmRadioButton.setEnabled(True)
      self.CmRadioButton.setGeometry(qt.QRect(95, 423, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CmRadioButton.sizePolicy.hasHeightForWidth())
      self.CmRadioButton.setSizePolicy(sizePolicy)
      self.CmRadioButton.setText((""))
      self.CmRadioButton.setAutoExclusive(False)
      self.CmRadioButton.setObjectName("CmRadioButton")
      self.CmColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CmColorPushButton.setEnabled(True)
      self.CmColorPushButton.setGeometry(qt.QRect(96, 402, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CmColorPushButton.sizePolicy.hasHeightForWidth())
      self.CmColorPushButton.setSizePolicy(sizePolicy)
      self.CmColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CmColorPushButton.setObjectName("CmColorPushButton")
      self.CnRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CnRadioButton.setEnabled(True)
      self.CnRadioButton.setGeometry(qt.QRect(86, 359, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CnRadioButton.sizePolicy.hasHeightForWidth())
      self.CnRadioButton.setSizePolicy(sizePolicy)
      self.CnRadioButton.setText((""))
      self.CnRadioButton.setAutoExclusive(False)
      self.CnRadioButton.setObjectName("CnRadioButton")
      self.CnColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CnColorPushButton.setEnabled(True)
      self.CnColorPushButton.setGeometry(qt.QRect(87, 333, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CnColorPushButton.sizePolicy.hasHeightForWidth())
      self.CnColorPushButton.setSizePolicy(sizePolicy)
      self.CnColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CnColorPushButton.setObjectName("CnColorPushButton")
      self.CoRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.CoRadioButton.setEnabled(True)
      self.CoRadioButton.setGeometry(qt.QRect(96, 298, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CoRadioButton.sizePolicy.hasHeightForWidth())
      self.CoRadioButton.setSizePolicy(sizePolicy)
      self.CoRadioButton.setText((""))
      self.CoRadioButton.setAutoExclusive(False)
      self.CoRadioButton.setObjectName("CoRadioButton")
      self.CoColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.CoColorPushButton.setEnabled(True)
      self.CoColorPushButton.setGeometry(qt.QRect(93, 277, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.CoColorPushButton.sizePolicy.hasHeightForWidth())
      self.CoColorPushButton.setSizePolicy(sizePolicy)
      self.CoColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.CoColorPushButton.setObjectName("CoColorPushButton")
      self.BaRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BaRadioButton.setEnabled(True)
      self.BaRadioButton.setGeometry(qt.QRect(273, 242, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BaRadioButton.sizePolicy.hasHeightForWidth())
      self.BaRadioButton.setSizePolicy(sizePolicy)
      self.BaRadioButton.setText((""))
      self.BaRadioButton.setAutoExclusive(False)
      self.BaRadioButton.setObjectName("BaRadioButton")
      self.BaColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BaColorPushButton.setEnabled(True)
      self.BaColorPushButton.setGeometry(qt.QRect(270, 222, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BaColorPushButton.sizePolicy.hasHeightForWidth())
      self.BaColorPushButton.setSizePolicy(sizePolicy)
      self.BaColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BaColorPushButton.setObjectName("BaColorPushButton")
      self.BbColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BbColorPushButton.setEnabled(True)
      self.BbColorPushButton.setGeometry(qt.QRect(330, 237, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BbColorPushButton.sizePolicy.hasHeightForWidth())
      self.BbColorPushButton.setSizePolicy(sizePolicy)
      self.BbColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BbColorPushButton.setObjectName("BbColorPushButton")
      self.BbRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BbRadioButton.setEnabled(True)
      self.BbRadioButton.setGeometry(qt.QRect(333, 256, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BbRadioButton.sizePolicy.hasHeightForWidth())
      self.BbRadioButton.setSizePolicy(sizePolicy)
      self.BbRadioButton.setText((""))
      self.BbRadioButton.setAutoExclusive(False)
      self.BbRadioButton.setObjectName("BbRadioButton")
      self.BcColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BcColorPushButton.setEnabled(True)
      self.BcColorPushButton.setGeometry(qt.QRect(369, 279, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BcColorPushButton.sizePolicy.hasHeightForWidth())
      self.BcColorPushButton.setSizePolicy(sizePolicy)
      self.BcColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BcColorPushButton.setObjectName("BcColorPushButton")
      self.BcRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BcRadioButton.setEnabled(True)
      self.BcRadioButton.setGeometry(qt.QRect(375, 301, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BcRadioButton.sizePolicy.hasHeightForWidth())
      self.BcRadioButton.setSizePolicy(sizePolicy)
      self.BcRadioButton.setText((""))
      self.BcRadioButton.setAutoExclusive(False)
      self.BcRadioButton.setObjectName("BcRadioButton")
      self.BdColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BdColorPushButton.setEnabled(True)
      self.BdColorPushButton.setGeometry(qt.QRect(393, 336, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BdColorPushButton.sizePolicy.hasHeightForWidth())
      self.BdColorPushButton.setSizePolicy(sizePolicy)
      self.BdColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BdColorPushButton.setObjectName("BdColorPushButton")
      self.BdRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BdRadioButton.setEnabled(True)
      self.BdRadioButton.setGeometry(qt.QRect(393, 358, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BdRadioButton.sizePolicy.hasHeightForWidth())
      self.BdRadioButton.setSizePolicy(sizePolicy)
      self.BdRadioButton.setText((""))
      self.BdRadioButton.setAutoExclusive(False)
      self.BdRadioButton.setObjectName("BdRadioButton")
      self.BeColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BeColorPushButton.setEnabled(True)
      self.BeColorPushButton.setGeometry(qt.QRect(372, 396, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BeColorPushButton.sizePolicy.hasHeightForWidth())
      self.BeColorPushButton.setSizePolicy(sizePolicy)
      self.BeColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BeColorPushButton.setObjectName("BeColorPushButton")
      self.BeRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BeRadioButton.setEnabled(True)
      self.BeRadioButton.setGeometry(qt.QRect(375, 418, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BeRadioButton.sizePolicy.hasHeightForWidth())
      self.BeRadioButton.setSizePolicy(sizePolicy)
      self.BeRadioButton.setText((""))
      self.BeRadioButton.setAutoExclusive(False)
      self.BeRadioButton.setObjectName("BeRadioButton")
      self.BfColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BfColorPushButton.setEnabled(True)
      self.BfColorPushButton.setGeometry(qt.QRect(327, 441, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BfColorPushButton.sizePolicy.hasHeightForWidth())
      self.BfColorPushButton.setSizePolicy(sizePolicy)
      self.BfColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BfColorPushButton.setObjectName("BfColorPushButton")
      self.BfRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BfRadioButton.setEnabled(True)
      self.BfRadioButton.setGeometry(qt.QRect(330, 460, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BfRadioButton.sizePolicy.hasHeightForWidth())
      self.BfRadioButton.setSizePolicy(sizePolicy)
      self.BfRadioButton.setText((""))
      self.BfRadioButton.setAutoExclusive(False)
      self.BfRadioButton.setObjectName("BfRadioButton")
      self.BgColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BgColorPushButton.setEnabled(True)
      self.BgColorPushButton.setGeometry(qt.QRect(264, 459, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BgColorPushButton.sizePolicy.hasHeightForWidth())
      self.BgColorPushButton.setSizePolicy(sizePolicy)
      self.BgColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BgColorPushButton.setObjectName("BgColorPushButton")
      self.BgRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BgRadioButton.setEnabled(True)
      self.BgRadioButton.setGeometry(qt.QRect(270, 478, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BgRadioButton.sizePolicy.hasHeightForWidth())
      self.BgRadioButton.setSizePolicy(sizePolicy)
      self.BgRadioButton.setText((""))
      self.BgRadioButton.setAutoExclusive(False)
      self.BgRadioButton.setObjectName("BgRadioButton")
      self.BhColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BhColorPushButton.setEnabled(True)
      self.BhColorPushButton.setGeometry(qt.QRect(204, 441, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BhColorPushButton.sizePolicy.hasHeightForWidth())
      self.BhColorPushButton.setSizePolicy(sizePolicy)
      self.BhColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BhColorPushButton.setObjectName("BhColorPushButton")
      self.BhRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BhRadioButton.setEnabled(True)
      self.BhRadioButton.setGeometry(qt.QRect(210, 463, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BhRadioButton.sizePolicy.hasHeightForWidth())
      self.BhRadioButton.setSizePolicy(sizePolicy)
      self.BhRadioButton.setText((""))
      self.BhRadioButton.setAutoExclusive(False)
      self.BhRadioButton.setObjectName("BhRadioButton")
      self.BiColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BiColorPushButton.setEnabled(True)
      self.BiColorPushButton.setGeometry(qt.QRect(165, 399, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BiColorPushButton.sizePolicy.hasHeightForWidth())
      self.BiColorPushButton.setSizePolicy(sizePolicy)
      self.BiColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BiColorPushButton.setObjectName("BiColorPushButton")
      self.BiRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BiRadioButton.setEnabled(True)
      self.BiRadioButton.setGeometry(qt.QRect(165, 418, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BiRadioButton.sizePolicy.hasHeightForWidth())
      self.BiRadioButton.setSizePolicy(sizePolicy)
      self.BiRadioButton.setText((""))
      self.BiRadioButton.setAutoExclusive(False)
      self.BiRadioButton.setObjectName("BiRadioButton")
      self.BjColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BjColorPushButton.setEnabled(True)
      self.BjColorPushButton.setGeometry(qt.QRect(138, 336, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BjColorPushButton.sizePolicy.hasHeightForWidth())
      self.BjColorPushButton.setSizePolicy(sizePolicy)
      self.BjColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BjColorPushButton.setObjectName("BjColorPushButton")
      self.BjRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BjRadioButton.setEnabled(True)
      self.BjRadioButton.setGeometry(qt.QRect(147, 360, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BjRadioButton.sizePolicy.hasHeightForWidth())
      self.BjRadioButton.setSizePolicy(sizePolicy)
      self.BjRadioButton.setText((""))
      self.BjRadioButton.setAutoExclusive(False)
      self.BjRadioButton.setObjectName("BjRadioButton")
      self.BkColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BkColorPushButton.setEnabled(True)
      self.BkColorPushButton.setGeometry(qt.QRect(162, 279, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BkColorPushButton.sizePolicy.hasHeightForWidth())
      self.BkColorPushButton.setSizePolicy(sizePolicy)
      self.BkColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BkColorPushButton.setObjectName("BkColorPushButton")
      self.BkRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BkRadioButton.setEnabled(True)
      self.BkRadioButton.setGeometry(qt.QRect(162, 301, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BkRadioButton.sizePolicy.hasHeightForWidth())
      self.BkRadioButton.setSizePolicy(sizePolicy)
      self.BkRadioButton.setText((""))
      self.BkRadioButton.setAutoExclusive(False)
      self.BkRadioButton.setObjectName("BkRadioButton")
      self.BlColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.BlColorPushButton.setEnabled(True)
      self.BlColorPushButton.setGeometry(qt.QRect(204, 237, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BlColorPushButton.sizePolicy.hasHeightForWidth())
      self.BlColorPushButton.setSizePolicy(sizePolicy)
      self.BlColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.BlColorPushButton.setObjectName("BlColorPushButton")
      self.BlRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.BlRadioButton.setEnabled(True)
      self.BlRadioButton.setGeometry(qt.QRect(210, 259, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.BlRadioButton.sizePolicy.hasHeightForWidth())
      self.BlRadioButton.setSizePolicy(sizePolicy)
      self.BlRadioButton.setText((""))
      self.BlRadioButton.setAutoExclusive(False)
      self.BlRadioButton.setObjectName("BlRadioButton")
      self.AaColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.AaColorPushButton.setEnabled(True)
      self.AaColorPushButton.setGeometry(qt.QRect(306, 279, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AaColorPushButton.sizePolicy.hasHeightForWidth())
      self.AaColorPushButton.setSizePolicy(sizePolicy)
      self.AaColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.AaColorPushButton.setObjectName("AaColorPushButton")
      self.AaRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.AaRadioButton.setEnabled(True)
      self.AaRadioButton.setGeometry(qt.QRect(306, 304, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AaRadioButton.sizePolicy.hasHeightForWidth())
      self.AaRadioButton.setSizePolicy(sizePolicy)
      self.AaRadioButton.setText((""))
      self.AaRadioButton.setAutoExclusive(False)
      self.AaRadioButton.setObjectName("AaRadioButton")
      self.AbColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.AbColorPushButton.setEnabled(True)
      self.AbColorPushButton.setGeometry(qt.QRect(333, 336, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AbColorPushButton.sizePolicy.hasHeightForWidth())
      self.AbColorPushButton.setSizePolicy(sizePolicy)
      self.AbColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.AbColorPushButton.setObjectName("AbColorPushButton")
      self.AbRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.AbRadioButton.setEnabled(True)
      self.AbRadioButton.setGeometry(qt.QRect(336, 361, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AbRadioButton.sizePolicy.hasHeightForWidth())
      self.AbRadioButton.setSizePolicy(sizePolicy)
      self.AbRadioButton.setText((""))
      self.AbRadioButton.setAutoExclusive(False)
      self.AbRadioButton.setObjectName("AbRadioButton")
      self.AcColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.AcColorPushButton.setEnabled(True)
      self.AcColorPushButton.setGeometry(qt.QRect(300, 399, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AcColorPushButton.sizePolicy.hasHeightForWidth())
      self.AcColorPushButton.setSizePolicy(sizePolicy)
      self.AcColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.AcColorPushButton.setObjectName("AcColorPushButton")
      self.AcRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.AcRadioButton.setEnabled(True)
      self.AcRadioButton.setGeometry(qt.QRect(299, 418, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AcRadioButton.sizePolicy.hasHeightForWidth())
      self.AcRadioButton.setSizePolicy(sizePolicy)
      self.AcRadioButton.setText((""))
      self.AcRadioButton.setAutoExclusive(False)
      self.AcRadioButton.setObjectName("AcRadioButton")
      self.AdColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.AdColorPushButton.setEnabled(True)
      self.AdColorPushButton.setGeometry(qt.QRect(243, 399, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AdColorPushButton.sizePolicy.hasHeightForWidth())
      self.AdColorPushButton.setSizePolicy(sizePolicy)
      self.AdColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.AdColorPushButton.setObjectName("AdColorPushButton")
      self.AdRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.AdRadioButton.setEnabled(True)
      self.AdRadioButton.setGeometry(qt.QRect(239, 415, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AdRadioButton.sizePolicy.hasHeightForWidth())
      self.AdRadioButton.setSizePolicy(sizePolicy)
      self.AdRadioButton.setText((""))
      self.AdRadioButton.setAutoExclusive(False)
      self.AdRadioButton.setObjectName("AdRadioButton")
      self.AeColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.AeColorPushButton.setEnabled(True)
      self.AeColorPushButton.setGeometry(qt.QRect(204, 336, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AeColorPushButton.sizePolicy.hasHeightForWidth())
      self.AeColorPushButton.setSizePolicy(sizePolicy)
      self.AeColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.AeColorPushButton.setObjectName("AeColorPushButton")
      self.AeRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.AeRadioButton.setEnabled(True)
      self.AeRadioButton.setGeometry(qt.QRect(206, 363, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AeRadioButton.sizePolicy.hasHeightForWidth())
      self.AeRadioButton.setSizePolicy(sizePolicy)
      self.AeRadioButton.setText((""))
      self.AeRadioButton.setAutoExclusive(False)
      self.AeRadioButton.setObjectName("AeRadioButton")
      self.AfColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.AfColorPushButton.setEnabled(True)
      self.AfColorPushButton.setGeometry(qt.QRect(243, 279, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AfColorPushButton.sizePolicy.hasHeightForWidth())
      self.AfColorPushButton.setSizePolicy(sizePolicy)
      self.AfColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.AfColorPushButton.setObjectName("AfColorPushButton")
      self.AfRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.AfRadioButton.setEnabled(True)
      self.AfRadioButton.setGeometry(qt.QRect(239, 304, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.AfRadioButton.sizePolicy.hasHeightForWidth())
      self.AfRadioButton.setSizePolicy(sizePolicy)
      self.AfRadioButton.setText((""))
      self.AfRadioButton.setAutoExclusive(False)
      self.AfRadioButton.setObjectName("AfRadioButton")
      self.IuColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.IuColorPushButton.setEnabled(True)
      self.IuColorPushButton.setGeometry(qt.QRect(273, 333, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.IuColorPushButton.sizePolicy.hasHeightForWidth())
      self.IuColorPushButton.setSizePolicy(sizePolicy)
      self.IuColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.IuColorPushButton.setObjectName("IuColorPushButton")
      self.IuRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.IuRadioButton.setEnabled(True)
      self.IuRadioButton.setGeometry(qt.QRect(269, 358, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.IuRadioButton.sizePolicy.hasHeightForWidth())
      self.IuRadioButton.setSizePolicy(sizePolicy)
      self.IuRadioButton.setText((""))
      self.IuRadioButton.setAutoExclusive(False)
      self.IuRadioButton.setObjectName("IuRadioButton")
      self.DaColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DaColorPushButton.setEnabled(True)
      self.DaColorPushButton.setGeometry(qt.QRect(264, 99, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DaColorPushButton.sizePolicy.hasHeightForWidth())
      self.DaColorPushButton.setSizePolicy(sizePolicy)
      self.DaColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DaColorPushButton.setObjectName("DaColorPushButton")
      self.DaRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DaRadioButton.setEnabled(True)
      self.DaRadioButton.setGeometry(qt.QRect(269, 124, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DaRadioButton.sizePolicy.hasHeightForWidth())
      self.DaRadioButton.setSizePolicy(sizePolicy)
      self.DaRadioButton.setText((""))
      self.DaRadioButton.setAutoExclusive(False)
      self.DaRadioButton.setObjectName("DaRadioButton")
      self.DbColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DbColorPushButton.setEnabled(True)
      self.DbColorPushButton.setGeometry(qt.QRect(330, 111, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DbColorPushButton.sizePolicy.hasHeightForWidth())
      self.DbColorPushButton.setSizePolicy(sizePolicy)
      self.DbColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DbColorPushButton.setObjectName("DbColorPushButton")
      self.DbRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DbRadioButton.setEnabled(True)
      self.DbRadioButton.setGeometry(qt.QRect(332, 133, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DbRadioButton.sizePolicy.hasHeightForWidth())
      self.DbRadioButton.setSizePolicy(sizePolicy)
      self.DbRadioButton.setText((""))
      self.DbRadioButton.setAutoExclusive(False)
      self.DbRadioButton.setObjectName("DbRadioButton")
      self.DcColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DcColorPushButton.setEnabled(True)
      self.DcColorPushButton.setGeometry(qt.QRect(390, 129, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DcColorPushButton.sizePolicy.hasHeightForWidth())
      self.DcColorPushButton.setSizePolicy(sizePolicy)
      self.DcColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DcColorPushButton.setObjectName("DcColorPushButton")
      self.DcRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DcRadioButton.setEnabled(True)
      self.DcRadioButton.setGeometry(qt.QRect(392, 154, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DcRadioButton.sizePolicy.hasHeightForWidth())
      self.DcRadioButton.setSizePolicy(sizePolicy)
      self.DcRadioButton.setText((""))
      self.DcRadioButton.setAutoExclusive(False)
      self.DcRadioButton.setObjectName("DcRadioButton")
      self.DdColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DdColorPushButton.setEnabled(True)
      self.DdColorPushButton.setGeometry(qt.QRect(393, 537, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DdColorPushButton.sizePolicy.hasHeightForWidth())
      self.DdColorPushButton.setSizePolicy(sizePolicy)
      self.DdColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DdColorPushButton.setObjectName("DdColorPushButton")
      self.DdRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DdRadioButton.setEnabled(True)
      self.DdRadioButton.setGeometry(qt.QRect(392, 562, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DdRadioButton.sizePolicy.hasHeightForWidth())
      self.DdRadioButton.setSizePolicy(sizePolicy)
      self.DdRadioButton.setText((""))
      self.DdRadioButton.setAutoExclusive(False)
      self.DdRadioButton.setObjectName("DdRadioButton")
      self.DeColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DeColorPushButton.setEnabled(True)
      self.DeColorPushButton.setGeometry(qt.QRect(333, 567, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DeColorPushButton.sizePolicy.hasHeightForWidth())
      self.DeColorPushButton.setSizePolicy(sizePolicy)
      self.DeColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DeColorPushButton.setObjectName("DeColorPushButton")
      self.DeRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DeRadioButton.setEnabled(True)
      self.DeRadioButton.setGeometry(qt.QRect(335, 586, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DeRadioButton.sizePolicy.hasHeightForWidth())
      self.DeRadioButton.setSizePolicy(sizePolicy)
      self.DeRadioButton.setText((""))
      self.DeRadioButton.setAutoExclusive(False)
      self.DeRadioButton.setObjectName("DeRadioButton")
      self.DfColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DfColorPushButton.setEnabled(True)
      self.DfColorPushButton.setGeometry(qt.QRect(267, 579, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DfColorPushButton.sizePolicy.hasHeightForWidth())
      self.DfColorPushButton.setSizePolicy(sizePolicy)
      self.DfColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DfColorPushButton.setObjectName("DfColorPushButton")
      self.DfRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DfRadioButton.setEnabled(True)
      self.DfRadioButton.setGeometry(qt.QRect(269, 598, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DfRadioButton.sizePolicy.hasHeightForWidth())
      self.DfRadioButton.setSizePolicy(sizePolicy)
      self.DfRadioButton.setText((""))
      self.DfRadioButton.setAutoExclusive(False)
      self.DfRadioButton.setObjectName("DfRadioButton")
      self.DgColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DgColorPushButton.setEnabled(True)
      self.DgColorPushButton.setGeometry(qt.QRect(204, 567, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DgColorPushButton.sizePolicy.hasHeightForWidth())
      self.DgColorPushButton.setSizePolicy(sizePolicy)
      self.DgColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DgColorPushButton.setObjectName("DgColorPushButton")
      self.DgRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DgRadioButton.setEnabled(True)
      self.DgRadioButton.setGeometry(qt.QRect(206, 589, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DgRadioButton.sizePolicy.hasHeightForWidth())
      self.DgRadioButton.setSizePolicy(sizePolicy)
      self.DgRadioButton.setText((""))
      self.DgRadioButton.setAutoExclusive(False)
      self.DgRadioButton.setObjectName("DgRadioButton")
      self.DhColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DhColorPushButton.setEnabled(True)
      self.DhColorPushButton.setGeometry(qt.QRect(144, 540, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DhColorPushButton.sizePolicy.hasHeightForWidth())
      self.DhColorPushButton.setSizePolicy(sizePolicy)
      self.DhColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DhColorPushButton.setObjectName("DhColorPushButton")
      self.DhRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DhRadioButton.setEnabled(True)
      self.DhRadioButton.setGeometry(qt.QRect(146, 565, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DhRadioButton.sizePolicy.hasHeightForWidth())
      self.DhRadioButton.setSizePolicy(sizePolicy)
      self.DhRadioButton.setText((""))
      self.DhRadioButton.setAutoExclusive(False)
      self.DhRadioButton.setObjectName("DhRadioButton")
      self.DiColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DiColorPushButton.setEnabled(True)
      self.DiColorPushButton.setGeometry(qt.QRect(144, 138, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DiColorPushButton.sizePolicy.hasHeightForWidth())
      self.DiColorPushButton.setSizePolicy(sizePolicy)
      self.DiColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DiColorPushButton.setObjectName("DiColorPushButton")
      self.DiRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DiRadioButton.setEnabled(True)
      self.DiRadioButton.setGeometry(qt.QRect(146, 157, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DiRadioButton.sizePolicy.hasHeightForWidth())
      self.DiRadioButton.setSizePolicy(sizePolicy)
      self.DiRadioButton.setText((""))
      self.DiRadioButton.setAutoExclusive(False)
      self.DiRadioButton.setObjectName("DiRadioButton")
      self.DjColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.DjColorPushButton.setEnabled(True)
      self.DjColorPushButton.setGeometry(qt.QRect(201, 114, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DjColorPushButton.sizePolicy.hasHeightForWidth())
      self.DjColorPushButton.setSizePolicy(sizePolicy)
      self.DjColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.DjColorPushButton.setObjectName("DjColorPushButton")
      self.DjRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.DjRadioButton.setEnabled(True)
      self.DjRadioButton.setGeometry(qt.QRect(206, 133, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.DjRadioButton.sizePolicy.hasHeightForWidth())
      self.DjRadioButton.setSizePolicy(sizePolicy)
      self.DjRadioButton.setText((""))
      self.DjRadioButton.setAutoExclusive(False)
      self.DjRadioButton.setObjectName("DjRadioButton")
      self.EaColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.EaColorPushButton.setEnabled(True)
      self.EaColorPushButton.setGeometry(qt.QRect(294, 48, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EaColorPushButton.sizePolicy.hasHeightForWidth())
      self.EaColorPushButton.setSizePolicy(sizePolicy)
      self.EaColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.EaColorPushButton.setObjectName("EaColorPushButton")
      self.EaRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.EaRadioButton.setEnabled(True)
      self.EaRadioButton.setGeometry(qt.QRect(297, 69, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EaRadioButton.sizePolicy.hasHeightForWidth())
      self.EaRadioButton.setSizePolicy(sizePolicy)
      self.EaRadioButton.setText((""))
      self.EaRadioButton.setAutoExclusive(False)
      self.EaRadioButton.setObjectName("EaRadioButton")
      self.EbRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.EbRadioButton.setEnabled(True)
      self.EbRadioButton.setGeometry(qt.QRect(348, 77, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EbRadioButton.sizePolicy.hasHeightForWidth())
      self.EbRadioButton.setSizePolicy(sizePolicy)
      self.EbRadioButton.setText((""))
      self.EbRadioButton.setAutoExclusive(False)
      self.EbRadioButton.setObjectName("EbRadioButton")
      self.EbColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.EbColorPushButton.setEnabled(True)
      self.EbColorPushButton.setGeometry(qt.QRect(348, 58, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EbColorPushButton.sizePolicy.hasHeightForWidth())
      self.EbColorPushButton.setSizePolicy(sizePolicy)
      self.EbColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.EbColorPushButton.setObjectName("EbColorPushButton")
      self.EcRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.EcRadioButton.setEnabled(True)
      self.EcRadioButton.setGeometry(qt.QRect(350, 643, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EcRadioButton.sizePolicy.hasHeightForWidth())
      self.EcRadioButton.setSizePolicy(sizePolicy)
      self.EcRadioButton.setText((""))
      self.EcRadioButton.setAutoExclusive(False)
      self.EcRadioButton.setObjectName("EcRadioButton")
      self.EcColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.EcColorPushButton.setEnabled(True)
      self.EcColorPushButton.setGeometry(qt.QRect(348, 624, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EcColorPushButton.sizePolicy.hasHeightForWidth())
      self.EcColorPushButton.setSizePolicy(sizePolicy)
      self.EcColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.EcColorPushButton.setObjectName("EcColorPushButton")
      self.EdRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.EdRadioButton.setEnabled(True)
      self.EdRadioButton.setGeometry(qt.QRect(296, 653, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EdRadioButton.sizePolicy.hasHeightForWidth())
      self.EdRadioButton.setSizePolicy(sizePolicy)
      self.EdRadioButton.setText((""))
      self.EdRadioButton.setAutoExclusive(False)
      self.EdRadioButton.setObjectName("EdRadioButton")
      self.EdColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.EdColorPushButton.setEnabled(True)
      self.EdColorPushButton.setGeometry(qt.QRect(294, 633, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EdColorPushButton.sizePolicy.hasHeightForWidth())
      self.EdColorPushButton.setSizePolicy(sizePolicy)
      self.EdColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.EdColorPushButton.setObjectName("EdColorPushButton")
      self.EeRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.EeRadioButton.setEnabled(True)
      self.EeRadioButton.setGeometry(qt.QRect(245, 653, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EeRadioButton.sizePolicy.hasHeightForWidth())
      self.EeRadioButton.setSizePolicy(sizePolicy)
      self.EeRadioButton.setText((""))
      self.EeRadioButton.setAutoExclusive(False)
      self.EeRadioButton.setObjectName("EeRadioButton")
      self.EeColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.EeColorPushButton.setEnabled(True)
      self.EeColorPushButton.setGeometry(qt.QRect(243, 633, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EeColorPushButton.sizePolicy.hasHeightForWidth())
      self.EeColorPushButton.setSizePolicy(sizePolicy)
      self.EeColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.EeColorPushButton.setObjectName("EeColorPushButton")
      self.EfRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.EfRadioButton.setEnabled(True)
      self.EfRadioButton.setGeometry(qt.QRect(191, 644, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EfRadioButton.sizePolicy.hasHeightForWidth())
      self.EfRadioButton.setSizePolicy(sizePolicy)
      self.EfRadioButton.setText((""))
      self.EfRadioButton.setAutoExclusive(False)
      self.EfRadioButton.setObjectName("EfRadioButton")
      self.EfColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.EfColorPushButton.setEnabled(True)
      self.EfColorPushButton.setGeometry(qt.QRect(186, 624, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EfColorPushButton.sizePolicy.hasHeightForWidth())
      self.EfColorPushButton.setSizePolicy(sizePolicy)
      self.EfColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.EfColorPushButton.setObjectName("EfColorPushButton")
      self.EgRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.EgRadioButton.setEnabled(True)
      self.EgRadioButton.setGeometry(qt.QRect(192, 77, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EgRadioButton.sizePolicy.hasHeightForWidth())
      self.EgRadioButton.setSizePolicy(sizePolicy)
      self.EgRadioButton.setText((""))
      self.EgRadioButton.setAutoExclusive(False)
      self.EgRadioButton.setObjectName("EgRadioButton")
      self.EgColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.EgColorPushButton.setEnabled(True)
      self.EgColorPushButton.setGeometry(qt.QRect(186, 58, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EgColorPushButton.sizePolicy.hasHeightForWidth())
      self.EgColorPushButton.setSizePolicy(sizePolicy)
      self.EgColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.EgColorPushButton.setObjectName("EgColorPushButton")
      self.EhRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.EhRadioButton.setEnabled(True)
      self.EhRadioButton.setGeometry(qt.QRect(242, 68, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EhRadioButton.sizePolicy.hasHeightForWidth())
      self.EhRadioButton.setSizePolicy(sizePolicy)
      self.EhRadioButton.setText((""))
      self.EhRadioButton.setAutoExclusive(False)
      self.EhRadioButton.setObjectName("EhRadioButton")
      self.EhColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.EhColorPushButton.setEnabled(True)
      self.EhColorPushButton.setGeometry(qt.QRect(237, 48, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.EhColorPushButton.sizePolicy.hasHeightForWidth())
      self.EhColorPushButton.setSizePolicy(sizePolicy)
      self.EhColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.EhColorPushButton.setObjectName("EhColorPushButton")
      self.FaRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.FaRadioButton.setEnabled(True)
      self.FaRadioButton.setGeometry(qt.QRect(437, 125, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FaRadioButton.sizePolicy.hasHeightForWidth())
      self.FaRadioButton.setSizePolicy(sizePolicy)
      self.FaRadioButton.setText((""))
      self.FaRadioButton.setAutoExclusive(False)
      self.FaRadioButton.setObjectName("FaRadioButton")
      self.FaColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.FaColorPushButton.setEnabled(True)
      self.FaColorPushButton.setGeometry(qt.QRect(435, 102, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FaColorPushButton.sizePolicy.hasHeightForWidth())
      self.FaColorPushButton.setSizePolicy(sizePolicy)
      self.FaColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.FaColorPushButton.setObjectName("FaColorPushButton")
      self.FbRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.FbRadioButton.setEnabled(True)
      self.FbRadioButton.setGeometry(qt.QRect(455, 152, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FbRadioButton.sizePolicy.hasHeightForWidth())
      self.FbRadioButton.setSizePolicy(sizePolicy)
      self.FbRadioButton.setText((""))
      self.FbRadioButton.setAutoExclusive(False)
      self.FbRadioButton.setObjectName("FbRadioButton")
      self.FbColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.FbColorPushButton.setEnabled(True)
      self.FbColorPushButton.setGeometry(qt.QRect(456, 129, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FbColorPushButton.sizePolicy.hasHeightForWidth())
      self.FbColorPushButton.setSizePolicy(sizePolicy)
      self.FbColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.FbColorPushButton.setObjectName("FbColorPushButton")
      self.FhRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.FhRadioButton.setEnabled(True)
      self.FhRadioButton.setGeometry(qt.QRect(105, 128, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FhRadioButton.sizePolicy.hasHeightForWidth())
      self.FhRadioButton.setSizePolicy(sizePolicy)
      self.FhRadioButton.setText((""))
      self.FhRadioButton.setAutoExclusive(False)
      self.FhRadioButton.setObjectName("FhRadioButton")
      self.FhColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.FhColorPushButton.setEnabled(True)
      self.FhColorPushButton.setGeometry(qt.QRect(102, 109, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FhColorPushButton.sizePolicy.hasHeightForWidth())
      self.FhColorPushButton.setSizePolicy(sizePolicy)
      self.FhColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.FhColorPushButton.setObjectName("FhColorPushButton")
      self.FgRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.FgRadioButton.setEnabled(True)
      self.FgRadioButton.setGeometry(qt.QRect(84, 158, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FgRadioButton.sizePolicy.hasHeightForWidth())
      self.FgRadioButton.setSizePolicy(sizePolicy)
      self.FgRadioButton.setText((""))
      self.FgRadioButton.setAutoExclusive(False)
      self.FgRadioButton.setObjectName("FgRadioButton")
      self.FgColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.FgColorPushButton.setEnabled(True)
      self.FgColorPushButton.setGeometry(qt.QRect(81, 141, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FgColorPushButton.sizePolicy.hasHeightForWidth())
      self.FgColorPushButton.setSizePolicy(sizePolicy)
      self.FgColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.FgColorPushButton.setObjectName("FgColorPushButton")
      self.FcRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.FcRadioButton.setEnabled(True)
      self.FcRadioButton.setGeometry(qt.QRect(458, 566, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FcRadioButton.sizePolicy.hasHeightForWidth())
      self.FcRadioButton.setSizePolicy(sizePolicy)
      self.FcRadioButton.setText((""))
      self.FcRadioButton.setAutoExclusive(False)
      self.FcRadioButton.setObjectName("FcRadioButton")
      self.FcColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.FcColorPushButton.setEnabled(True)
      self.FcColorPushButton.setGeometry(qt.QRect(456, 543, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FcColorPushButton.sizePolicy.hasHeightForWidth())
      self.FcColorPushButton.setSizePolicy(sizePolicy)
      self.FcColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.FcColorPushButton.setObjectName("FcColorPushButton")
      self.FdRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.FdRadioButton.setEnabled(True)
      self.FdRadioButton.setGeometry(qt.QRect(437, 593, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FdRadioButton.sizePolicy.hasHeightForWidth())
      self.FdRadioButton.setSizePolicy(sizePolicy)
      self.FdRadioButton.setText((""))
      self.FdRadioButton.setAutoExclusive(False)
      self.FdRadioButton.setObjectName("FdRadioButton")
      self.FdColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.FdColorPushButton.setEnabled(True)
      self.FdColorPushButton.setGeometry(qt.QRect(432, 576, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FdColorPushButton.sizePolicy.hasHeightForWidth())
      self.FdColorPushButton.setSizePolicy(sizePolicy)
      self.FdColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.FdColorPushButton.setObjectName("FdColorPushButton")
      self.FeRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.FeRadioButton.setEnabled(True)
      self.FeRadioButton.setGeometry(qt.QRect(107, 596, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FeRadioButton.sizePolicy.hasHeightForWidth())
      self.FeRadioButton.setSizePolicy(sizePolicy)
      self.FeRadioButton.setText((""))
      self.FeRadioButton.setAutoExclusive(False)
      self.FeRadioButton.setObjectName("FeRadioButton")
      self.FeColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.FeColorPushButton.setEnabled(True)
      self.FeColorPushButton.setGeometry(qt.QRect(105, 573, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FeColorPushButton.sizePolicy.hasHeightForWidth())
      self.FeColorPushButton.setSizePolicy(sizePolicy)
      self.FeColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.FeColorPushButton.setObjectName("FeColorPushButton")
      self.FfRadioButton = qt.QRadioButton(TemplateSheetWidget)
      self.FfRadioButton.setEnabled(True)
      self.FfRadioButton.setGeometry(qt.QRect(83, 565, 24, 16))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FfRadioButton.sizePolicy.hasHeightForWidth())
      self.FfRadioButton.setSizePolicy(sizePolicy)
      self.FfRadioButton.setText((""))
      self.FfRadioButton.setAutoExclusive(False)
      self.FfRadioButton.setObjectName("FfRadioButton")
      self.FfColorPushButton = qt.QPushButton(TemplateSheetWidget)
      self.FfColorPushButton.setEnabled(True)
      self.FfColorPushButton.setGeometry(qt.QRect(81, 540, 21, 21))
      sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.FfColorPushButton.sizePolicy.hasHeightForWidth())
      self.FfColorPushButton.setSizePolicy(sizePolicy)
      self.FfColorPushButton.setStyleSheet("background-color: rgb(209,220,229);")
      self.FfColorPushButton.setObjectName("FfColorPushButton")
       
      # #-------------------------------------------------------------------    
      

      for i in range(63):
        popupbutton = "popup"+self.option[i]
        # spinbox = "self.popupSpinbox"+self.option[i]
        button= "self."+self.option[i]+"ColorPushButton"
        radiobutton = "self."+self.option[i]+"RadioButton"
        pushbutton = "self.push"+self.option[i]+"Needle"

        #-------------------------------------------------------------------       
        popupbutton = ctk.ctkPopupWidget(eval(button))
        spinbox = qt.QSpinBox(popupbutton)
        self.createSpinbox(popupbutton,spinbox)
        spinbox.connect("valueChanged(int)", functools.partial(self.pushOneNeedle,i))
        #------------------------------------------------------------------- 
        eval(button).setText(self.option[i])
        eval(button).connect("clicked()", lambda who=i: self.setOneNeedleColor(who))
        #------------------------------------------------------------------- 
        eval(radiobutton).connect("clicked()",  lambda who=i: self.showOneNeedle(who))  
   
      #------------------------------------------
      mrmlScene = slicer.mrmlScene
      obturatorID = pNode.GetParameter('obturatorID')
      self.ObturatorNode = mrmlScene.GetNodeByID(obturatorID)
      if self.ObturatorNode :
      
        self.setNeedleCoordinates()
        self.computerPolydataAndMatrix()    
      
        self.m_poly = vtk.vtkPolyData()  
        self.m_poly.DeepCopy(self.ObturatorNode.GetPolyData())


    TemplateSheetWidget.visible = True
    
    self.__layout.addWidget(TemplateSheetWidget)
     
  def refreshSegmented(self):
    self.segmented = [0 for i in range(63)]
    modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
    print 'refresh'
    self.colorLabel()
  
    for modelNode in modelNodes.values():
      if modelNode.GetAttribute("nth")!=None and modelNode.GetDisplayVisibility()==1:
        self.segmented[int(modelNode.GetAttribute("nth"))]=1
        print int(modelNode.GetAttribute("nth"))
    
      if modelNode.GetAttribute("plannednth")!=None:
        button= "self."+self.option[int(modelNode.GetAttribute("plannednth"))]+"RadioButton"
        eval(button).setChecked(modelNode.GetDisplayVisibility())
        
    for i in range(63):
      button= "self."+self.option[i]+"ColorPushButton"
      
      if self.segmented[i]==1:
        eval(button).setText(self.option[i])
        sColor = "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(255,255,255), stop: 1 rgb(" + str(self.color255[i][0]) +","+ str(self.color255[i][1]) +"," + str(self.color255[i][2]) + ")); color: black; font-weight: bold; "
        sColor += "border-width: 2px;"
        sColor +="border-color: rgb(170,0,0);"
        sColor +="border-style: solid;"
        sColor +="border-radius: 3;"
        eval(button).setStyleSheet(sColor)
    
  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )
    self.__parent.validationSucceeded(desiredBranchId)

  def onExit(self, goingTo, transitionType):
    if goingTo.id() != 'SecondRegistration' and goingTo.id() != 'NeedleSegmentation':
      return
    pNode = self.parameterNode()
    super(iGyneNeedlePlanningStep, self).onExit(goingTo, transitionType)

  def onEntry(self,comingFrom,transitionType):
    '''
    Update GUI and visualization
    '''
    super(iGyneNeedlePlanningStep, self).onEntry(comingFrom, transitionType)
    pNode = self.parameterNode()
    if pNode.GetParameter('skip') != '1':
      self.updateWidgetFromParameters(pNode)
      Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')

      pNode.SetParameter('currentStep', self.stepid)
      self.loadNeedles()
      self.refreshSegmented()
    else:
      self.workflow().goForward() # 6  

  def updateWidgetFromParameters(self, pNode):
  
    baselineVolume = Helper.getNodeByID(pNode.GetParameter('baselineVolumeID'))
    transformNodeID = pNode.GetParameter('followupTransformID')
    self.transform = Helper.getNodeByID(transformNodeID)
      
  def createSpinbox(self, popup, popupSpinbox):

    popupLayout = qt.QHBoxLayout(popup)  
    popupLayout.addWidget(popupSpinbox) 
    sizePolicy1 = qt.QSizePolicy()
    sizePolicy1.setHorizontalStretch(0)
    sizePolicy1.setVerticalStretch(0)
    sizePolicy1.setHeightForWidth(popupSpinbox.sizePolicy.hasHeightForWidth())
    popupSpinbox.setStyleSheet("background-color: rgb(255, 255, 255);")
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
    
    
    quad = vtk.vtkQuadric()
    quad.SetCoefficients(1,0.15,1,0,0,0,0,1,0,0)
    sample = vtk.vtkSampleFunction()
    sample.SetModelBounds(-30,30,-30,30,-30,30)
    sample.SetCapping(0)
    sample.SetComputeNormals(1)
    sample.SetSampleDimensions(50,50,50)
    sample.SetImplicitFunction(quad)
    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(sample.GetOutputPort())
    contour.ComputeNormalsOn()
    contour.ComputeScalarsOn()
    contour.GenerateValues(10,0,100)
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
  
  ##-----------------------------------------------------------------------------
  def pushObNeedle(self):

    nDepth = self.popupSpinboxOb.value
    mrmlScene=slicer.mrmlScene  
    obturatorID = pNode.GetParameter('obturatorID')
    self.ObturatorNode = mrmlScene.GetNodeByID(obturatorID)

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
  def showOneNeedle(self,i):
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
        # print PolyData
        polyData = displayNode.GetPolyData()
        polyData.Update()
        nb = int(polyData.GetNumberOfPoints()-1)
        coord = [0,0,0]
        if nb>100:
          fiducialNode = slicer.vtkMRMLAnnotationFiducialNode()
          polyData.GetPoint(nb,coord)    
          fiducialNode.SetName(self.option[i])
          fiducialNode.SetFiducialCoordinates(coord)         
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
          sColor = "background-color: rgb(" + str(self.color255[i][0]) +","+ str(self.color255[i][1]) +"," + str(self.color255[i][2]) + ");"
          colorButtonName = "self." + self.option[i] + "ColorPushButton"
          if self.segmented[i]==0:
            eval(colorButtonName).setStyleSheet(sColor)
          fiducialNode.SetVisible(1)

      if nVisibility ==1:
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
      self.AddModel(i)
      self.showOneNeedle(i)
      self.showOneNeedle(i)
    
  ##-----------------------------------------------------------------------------

  def pushOneNeedle(self,i,nDepth):
    print i, nDepth
    pNode = self.parameterNode()
    needleID = pNode.GetParameter(self.option[i]+'.vtp')
    fidID = pNode.GetParameter("fid"+self.option[i] )    
    # radID = pNode.GetParameter('Rad'+self.option[i]+'.vtp')  
    NeedleNode = slicer.mrmlScene.GetNodeByID(needleID)
    fiducialNode = slicer.mrmlScene.GetNodeByID(fidID)
    # RadNode = slicer.mrmlScene.GetNodeByID(radID)
    print needleID
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
      
      if fiducialNode!=None:
        displayNode =NeedleNode.GetModelDisplayNode()
        polyData = displayNode.GetPolyData()
        polyData.Update()
        nb = int(polyData.GetNumberOfPoints()-1)
        coord = [0,0,0]
        if nb>100:
          polyData.GetPoint(nb,coord)    
          fiducialNode.SetFiducialCoordinates(coord) 
      
    # vtkmat.SetElement(2,3,self.m_vtkmat.GetElement(2,3)+20-nDepth)
    # TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
    # Transform=vtk.vtkTransform()
    # TransformPolyDataFilter.SetInput(self.m_polyRadiation)
    # Transform.SetMatrix(vtkmat)
    # TransformPolyDataFilter.SetTransform(Transform)
    # TransformPolyDataFilter.Update()

    # if RadNode !=None:
      # RadNode.SetAndObservePolyData(TransformPolyDataFilter.GetOutput())
      
  ##-----------------------------------------------------------------------------
  def setOneNeedleColor(self,i):

    color = qt.QColorDialog.getColor(qt.QColor('green'), self)
    sColor = ""
    sColor = "background-color: rgb(" + str(color.red())+ "," + str(color.green()) + "," + str(color.blue()) + ");"
    ColorPushButton = 'self.'+self.option[i]+'ColorPushButton'
    if color.isValid():

      fidname = "fid"+self.option[i]
      pNode = self.parameterNode()
      needleID = pNode.GetParameter(self.option[i]+'.vtp')  
      fidID = pNode.GetParameter(fidname) 
      
      fiducialNode = slicer.mrmlScene.GetNodeByID(fidID)      
      NeedleNode = slicer.mrmlScene.GetNodeByID(needleID)
      if NeedleNode!=None:
        displayNode =NeedleNode.GetModelDisplayNode()

        displayNode.SetColor(color.red()/float(255.0),color.green()/float(255.0),color.blue()/float(255.0))
        sColor = "background-color: rgb(" + str(color.red())+ "," + str(color.green()) + "," + str(color.blue()) + ');'
        print sColor
        eval(ColorPushButton).setStyleSheet(sColor)
        
        if fiducialNode!=None:
          fidDN = fiducialNode.GetDisplayNode()
          fidDN.SetColor(displayNode.GetColor())
          fidTN = fiducialNode.GetAnnotationTextDisplayNode()
          fidTN.SetColor(displayNode.GetColor())
       

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
      vtkmatInitial = self.transform.GetMatrixTransformToParent()

      nContacts=0
      for i in xrange(63):

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
            # self.setRadioButton(i,True)
            
          else:           
            displayNode.SetVisibility(0)
            displayNode.SetSliceIntersectionVisibility(0)
            # self.setRadioButton(i,False)
          
  #-----------------------------------------------------------------------------

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
      
      
  def AddModel(self,i):
  
    vtkmat = vtk.vtkMatrix4x4()
    vtkmat.DeepCopy(self.m_vtkmat)
    vtkmat.SetElement(0,3,self.m_vtkmat.GetElement(0,3)+self.p[0][i])
    vtkmat.SetElement(1,3,self.m_vtkmat.GetElement(1,3)+self.p[1][i])
    vtkmat.SetElement(2,3,self.m_vtkmat.GetElement(2,3)-60)

    TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
    Transform=vtk.vtkTransform()        
    TransformPolyDataFilter.SetInput(self.m_polyCylinder)
    Transform.SetMatrix(vtkmat)
    TransformPolyDataFilter.SetTransform(Transform)
    TransformPolyDataFilter.Update()

    triangles=vtk.vtkTriangleFilter()
    triangles.SetInput(TransformPolyDataFilter.GetOutput())
  
    modelNode = slicer.vtkMRMLModelNode()
    displayNode = slicer.vtkMRMLModelDisplayNode()
    storageNode = slicer.vtkMRMLModelStorageNode()
 
    fileName = self.option[i]+'.vtp'

    mrmlScene = slicer.mrmlScene
    modelNode.SetName(fileName)
    modelNode.SetAttribute('plannednth',str(i))
    modelNode.SetAttribute('planned','1')       
    modelNode.SetAndObservePolyData(triangles.GetOutput())
    
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
    
    modelNode.SetAndObserveTransformNodeID(self.transform.GetID())
    displayNode.SetInputPolyData(modelNode.GetPolyData())
    self.colorLabel()
    displayNode.SetColor(self.color[i])
    displayNode.SetSliceIntersectionVisibility(0)
    pNode= self.parameterNode()
    pNode.SetParameter(fileName,modelNode.GetID())
    mrmlScene.AddNode(modelNode)
    displayNode.SetVisibility(1)
    # self.AddRadiation(i,modelNode.GetID())
    
  def AddRadiation(self,i,needleID):
  
    vtkmat = vtk.vtkMatrix4x4()
    vtkmat.DeepCopy(self.m_vtkmat)
    vtkmat.SetElement(0,3,self.m_vtkmat.GetElement(0,3)+self.p[0][i])
    vtkmat.SetElement(1,3,self.m_vtkmat.GetElement(1,3)+self.p[1][i])
    vtkmat.SetElement(2,3,self.m_vtkmat.GetElement(2,3)-150)

    TransformPolyDataFilter=vtk.vtkTransformPolyDataFilter()
    Transform=vtk.vtkTransform()        
    TransformPolyDataFilter.SetInput(self.m_polyRadiation)
    Transform.SetMatrix(vtkmat)
    TransformPolyDataFilter.SetTransform(Transform)
    TransformPolyDataFilter.Update()
  
    modelNode = slicer.vtkMRMLModelNode()
    displayNode = slicer.vtkMRMLModelDisplayNode()
    storageNode = slicer.vtkMRMLModelStorageNode()
 
    fileName = 'Rad_'+self.option[i]+'.vtp'

    mrmlScene = slicer.mrmlScene
    modelNode.SetName(fileName)
    modelNode.SetAttribute("radiation","planned")
    modelNode.SetAttribute("needleID",str(needleID))    
    modelNode.SetAndObservePolyData(TransformPolyDataFilter.GetOutput())
    
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
    
    modelNode.SetAndObserveTransformNodeID(self.transform.GetID())
    displayNode.SetInputPolyData(modelNode.GetPolyData())

    displayNode.SetSliceIntersectionVisibility(1)
    displayNode.SetScalarVisibility(1)
    displayNode.SetActiveScalarName('scalars')
    displayNode.SetScalarRange(0,230)
    displayNode.SetOpacity(0.1)
    displayNode.SetAndObserveColorNodeID('vtkMRMLColorTableNodeFileHotToColdRainbow.txt')
    displayNode.SetBackfaceCulling(0)
    pNode= self.parameterNode()
    pNode.SetParameter(fileName,modelNode.GetID())
    mrmlScene.AddNode(modelNode)

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
        self.color[i][j] = self.color[i][j]/float(255)



  
 
