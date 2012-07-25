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
    qt.QTimer.singleShot(0, self.killButton)

  def killButton(self):
    # hide useless button
    bl = slicer.util.findChildren(text='LoadDiagnosticSeries')
    if len(bl):
      bl[0].hide()

  def createUserInterface( self ):
  
    self.__layout = self.__parent.createUserInterface()
    checkBox1 = qt.QCheckBox("Neslet Template")
    checkBox2 = qt.QCheckBox("Obturator")
    checkBox3 = qt.QCheckBox("Intrauterine Tandem")
    checkBox4 = qt.QCheckBox("Intravaginal Ovoids")
    checkBox5 = qt.QCheckBox("Seed marker")
    checkBox6 = qt.QCheckBox("Rings")
    checkBox7 = qt.QCheckBox("Utrecht")
    checkBox8 = qt.QCheckBox("Wien")
    self.__layout.addRow(checkBox1)
    self.__layout.addRow(checkBox2)
    self.__layout.addRow(checkBox3)
    self.__layout.addRow(checkBox4)
    self.__layout.addRow(checkBox5)
    self.__layout.addRow(checkBox6)
    self.__layout.addRow(checkBox7)
    self.__layout.addRow(checkBox8)
    # self.updateWidgetFromParameters(self.parameterNode())
    qt.QTimer.singleShot(0, self.killButton)

  def onEntry(self,comingFrom,transitionType):
  
    super(iGyneSelectApplicatorStep, self).onEntry(comingFrom, transitionType)
    # setup the interface
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)    
    # self.updateWidgetFromParameterNode(pNode)
    qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    if goingTo.id() != 'SelectProcedure' and goingTo.id() != 'SelectApplicator':
      return
    pNode = self.parameterNode()
    # if goingTo.id() == 'LoadDiagnosticSeries':
      # self.doStepProcessing()

    super(iGyneSelectApplicatorStep, self).onExit(goingTo, transitionType)

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )    
    self.__parent.validationSucceeded(desiredBranchId)