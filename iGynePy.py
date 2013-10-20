from __main__ import vtk, qt, ctk, slicer
import os.path,time
import iGyneWizard

class iGynePy:
  def __init__( self, parent ):
    parent.title = "iGynePy"
    parent.categories = ["Wizards"]
    parent.contributors = ["Guillaume Pernelle", "Xiaojun Chen", "Yi Gao", "Tina Kapur", "Jan Egger", "Carolina Vale"]
    parent.helpText = "https://github.com/gpernelle/iGynePy/wiki";
    parent.acknowledgementText = " Version : " + "iGyne v2.0."
    self.parent = parent

class iGynePyWidget:
  def __init__( self, parent=None ):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout( qt.QVBoxLayout() )
      self.parent.setMRMLScene( slicer.mrmlScene )
    else:
      self.parent = parent
    self.layout = self.parent.layout()

    # this flag is 1 if there is an update in progress
    self.__updating = 1

    # the pointer to the logic and the mrmlManager
    self.__mrmlManager = None
    self.__logic = None

    if not parent: 
      self.setup()

      # after setup, be ready for events
      self.__updating = 0

      self.parent.show()

    if slicer.mrmlScene.GetTagByClassName( "vtkMRMLScriptedModuleNode" ) != 'ScriptedModule':
      slicer.mrmlScene.RegisterNodeClass(vtkMRMLScriptedModuleNode())

  def setup( self ):
    '''
    Create and start the iGyne workflow.
    '''
    self.workflow = ctk.ctkWorkflow()

    workflowWidget = ctk.ctkWorkflowStackedWidget()
    workflowWidget.setWorkflow( self.workflow )
    
    # create all wizard steps
    selectProcedureStep = iGyneWizard.iGyneSelectProcedureStep( 'SelectProcedure'  )
    selectApplicatorStep = iGyneWizard.iGyneSelectApplicatorStep( 'SelectApplicator'  )
    loadModelStep = iGyneWizard.iGyneLoadModelStep( 'LoadModel'  )
    firstRegistrationStep = iGyneWizard.iGyneFirstRegistrationStep( 'FirstRegistration'  )
    secondRegistrationStep = iGyneWizard.iGyneSecondRegistrationStep( 'SecondRegistration'  )
    needlePlanningStep = iGyneWizard.iGyneNeedlePlanningStep( 'NeedlePlanning'  )
    needleSegmentationStep = iGyneWizard.iGyneNeedleSegmentationStep( 'NeedleSegmentation'  )


    # add the wizard steps to an array for convenience
    allSteps = []

    allSteps.append( selectProcedureStep )
    allSteps.append( selectApplicatorStep )
    allSteps.append( loadModelStep )
    allSteps.append( firstRegistrationStep )
    allSteps.append( secondRegistrationStep )
    allSteps.append( needlePlanningStep )
    allSteps.append( needleSegmentationStep )


    self.workflow.addTransition( selectProcedureStep, selectApplicatorStep )
    self.workflow.addTransition( selectApplicatorStep, loadModelStep )
    self.workflow.addTransition( loadModelStep, firstRegistrationStep )
    self.workflow.addTransition( firstRegistrationStep, secondRegistrationStep )
    self.workflow.addTransition( secondRegistrationStep, needlePlanningStep )
    self.workflow.addTransition( needlePlanningStep, needleSegmentationStep )
    self.workflow.addTransition(selectProcedureStep,needleSegmentationStep)


    nNodes = slicer.mrmlScene.GetNumberOfNodesByClass('vtkMRMLScriptedModuleNode')

    self.parameterNode = None
    for n in xrange(nNodes):
      compNode = slicer.mrmlScene.GetNthNodeByClass(n, 'vtkMRMLScriptedModuleNode')
      nodeid = None
      if compNode.GetModuleName() == 'iGyne':
        self.parameterNode = compNode
        print 'Found existing iGyne parameter node'
        break
    if self.parameterNode == None:
      self.parameterNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLScriptedModuleNode')
      self.parameterNode.SetModuleName('iGyne')
      slicer.mrmlScene.AddNode(self.parameterNode)
 
    # Propagate the workflow, the logic and the MRML Manager to the steps
    for s in allSteps:
        s.setWorkflow( self.workflow )
        s.setParameterNode (self.parameterNode)

    # restore workflow step
    currentStep = self.parameterNode.GetParameter('currentStep')
    if currentStep != '':
      print 'Restoring workflow step to ', currentStep
      if currentStep == 'SelectProcedure':
        self.workflow.setInitialStep(selectProcedureStep)
      if currentStep == 'SelectApplicator':
        self.workflow.setInitialStep(selectApplicatorStep)
      if currentStep == 'LoadModel':
        self.workflow.setInitialStep(loadModelStep)
      if currentStep == 'FirstRegistration':
        self.workflow.setInitialStep(firstRegistrationStep)
      if currentStep == 'SecondRegistration':
        self.workflow.setInitialStep(secondRegistrationStep)
      if currentStep == 'NeedlePlanning':
        self.workflow.setInitialStep(needlePlanningStep)
      if currentStep == 'NeedleSegmentation':
        self.workflow.setInitialStep(needleSegmentationStep)
    else:
      print 'currentStep in parameter node is empty!'
        
    # start the workflow and show the widget
    self.workflow.start()
    workflowWidget.visible = True
    self.layout.addWidget( workflowWidget )     
 
  def enter(self):
    print "iGyne: enter() called"
