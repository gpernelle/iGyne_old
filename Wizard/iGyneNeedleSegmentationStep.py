from __main__ import qt, ctk, slicer

from iGyneStep import *
from Helper import *
from EditorLib import *
import math

import string

'''
TODO:
  add advanced option to specify segmentation
'''

class iGyneNeedleSegmentationStep( iGyneStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '6. Needle Segmentation' )
    self.setDescription( 'Segment the needles' )
    self.__parent = super( iGyneNeedleSegmentationStep, self )
    

  def createUserInterface( self ):
    '''
    '''

    self.__layout = self.__parent.createUserInterface()

    
  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validate( desiredBranchId )
    self.__parent.validationSucceeded(desiredBranchId)

  def onExit(self, goingTo, transitionType):
    if goingTo.id() != 'SecondRegistration' and goingTo.id() != 'NeedleSegmentation':
      return

    pNode = self.parameterNode()
   

    super(iGyneNeedleSegmentationStep, self).onExit(goingTo, transitionType)

  def onEntry(self,comingFrom,transitionType):
    '''
    Update GUI and visualization
    '''
    super(iGyneNeedleSegmentationStep, self).onEntry(comingFrom, transitionType)
    pNode = self.parameterNode()
    self.updateWidgetFromParameters(pNode)
    Helper.SetBgFgVolumes(pNode.GetParameter('baselineVolumeID'),'')
    
    # setup color transfer function once
    
    
    labelsColorNode = slicer.modules.colors.logic().GetColorTableNodeID(10)
    self.__needleSegmentationNode.GetDisplayNode().SetAndObserveColorNodeID(labelsColorNode)
    Helper.SetLabelVolume(self.__roiSegmentationNode.GetID())
    self.onThresholdChanged()
    pNode.SetParameter('currentStep', self.stepid)
    


  def updateWidgetFromParameters(self, pNode):
  
    baselineVolume = Helper.getNodeByID(pNode.GetParameter('baselineVolumeID'))

