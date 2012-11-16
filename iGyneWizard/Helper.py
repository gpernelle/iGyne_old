# slicer imports
from __main__ import vtk, slicer

# python includes
import sys
import time

class Helper( object ):
  '''
  classdocs
  '''
  @staticmethod
  def SetBgFgVolumes(bg, fg):
    appLogic = slicer.app.applicationLogic()
    selectionNode = appLogic.GetSelectionNode()
    selectionNode.SetReferenceActiveVolumeID(bg)
    selectionNode.SetReferenceSecondaryVolumeID(fg)
    appLogic.PropagateVolumeSelection()

  @staticmethod
  def SetLabelVolume(lb):
    appLogic = slicer.app.applicationLogic()
    selectionNode = appLogic.GetSelectionNode()
    selectionNode.SetReferenceActiveLabelVolumeID(lb)
    appLogic.PropagateVolumeSelection()