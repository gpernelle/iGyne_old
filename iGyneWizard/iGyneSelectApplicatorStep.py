from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
import PythonQt

class iGyneSelectApplicatorStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '2. Choose Applicator' )
    self.setDescription( 'Choose the applicator you are using. It will load the right template.' )
    self.__parent = super( iGyneSelectApplicatorStep, self )
    self.checkBox1 = qt.QRadioButton('')
    self.checkBox3 = qt.QRadioButton('')
    self.ptcorners3 = qt.QRadioButton('')
    # qt.QTimer.singleShot(0, self.killButton)

  def createUserInterface( self ):
  
    self.__layout = self.__parent.createUserInterface()
    self.checkBox1 = qt.QRadioButton("Syed-Neblett Template and Obturator 4 points")
    self.checkBox1.setChecked(1)
    
    # checkBox2 = qt.QCheckBox("Obturator")
    # checkBox2.setEnabled(0)
    self.checkBox3 = qt.QRadioButton("Syed-Neblett Template and Obturator 3 points")
    self.checkBox3.setChecked(0)

    self.ptcorners3 = qt.QRadioButton("Syed-Neblett Template 3 points in corners")

    # checkBox3 = qt.QCheckBox("Intrauterine Tandem")
    # checkBox3.setCheckable(0)
    checkBox4 = qt.QCheckBox("Intravaginal Ovoids")
    # checkBox4.setCheckable(0)
    checkBox5 = qt.QCheckBox("Seed marker")
    # checkBox5.setCheckable(0)
    checkBox6 = qt.QCheckBox("Rings")
    # checkBox6.setCheckable(0)
    checkBox7 = qt.QCheckBox("Utrecht")
    # checkBox7.setCheckable(0)
    checkBox8 = qt.QCheckBox("Wien")
    # checkBox8.setCheckable(0)
    self.__layout.addRow(self.checkBox1)
    # self.__layout.addRow(checkBox2)
    self.__layout.addRow(self.checkBox3)
    self.__layout.addRow(self.ptcorners3)
    self.__layout.addRow(checkBox4)
    self.__layout.addRow(checkBox5)
    self.__layout.addRow(checkBox6)
    self.__layout.addRow(checkBox7)
    self.__layout.addRow(checkBox8)
    # self.updateWidgetFromParameters(self.parameterNode())
    # qt.QTimer.singleShot(0, self.killButton)

  def onEntry(self,comingFrom,transitionType):
  
    super(iGyneSelectApplicatorStep, self).onEntry(comingFrom, transitionType)
    # setup the interface
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    if pNode.GetParameter('skip')=='1':
      self.workflow().goForward() # 3       


  def onExit(self, goingTo, transitionType):
    pNode = self.parameterNode()
    if pNode.GetParameter('skip')!='1':
      if self.checkBox1.isChecked():
        pNode.SetParameter('Template', "4points")
      if self.checkBox3.isChecked():
        pNode = self.parameterNode()
        pNode.SetParameter('Template', "3points") 
      if self.ptcorners3.isChecked():
        pNode = self.parameterNode()
        pNode.SetParameter('Template', "3pointsCorners")       
    if goingTo.id() != 'SelectProcedure' and goingTo.id() != 'LoadModel':
      return

    super(iGyneSelectApplicatorStep, self).onExit(goingTo, transitionType)

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )    
    self.__parent.validationSucceeded(desiredBranchId)