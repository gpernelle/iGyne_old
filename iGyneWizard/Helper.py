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
  def Info( message ):
    '''
    
    '''

    #print "[iGynePy " + time.strftime( "%m/%d/%Y %H:%M:%S" ) + "]: " + str( message )
    #sys.stdout.flush()

  @staticmethod
  def Warning( message ):
    '''
    
    '''

    #print "[iGynePy " + time.strftime( "%m/%d/%Y %H:%M:%S" ) + "]: WARNING: " + str( message )
    #sys.stdout.flush()

  @staticmethod
  def Error( message ):
    '''
    
    '''

    print "[iGynePy " + time.strftime( "%m/%d/%Y %H:%M:%S" ) + "]: ERROR: " + str( message )
    sys.stdout.flush()


  @staticmethod
  def Debug( message ):
    '''
    
    '''

    showDebugOutput = 0
    from time import strftime
    if showDebugOutput:
        print "[iGynePy " + time.strftime( "%m/%d/%Y %H:%M:%S" ) + "] DEBUG: " + str( message )
        sys.stdout.flush()

  @staticmethod
  def CreateSpace( n ):
    '''
    '''
    spacer = ""
    for s in range( n ):
      spacer += " "

    return spacer


  @staticmethod
  def GetNthStepId( n ):
    '''
    '''
    steps = [None, # 0
             'SelectProcedure', # 1
             'SelectApplicator', # 2
             'LoadTemplate', # 3
             'AnalyzeROI', # 4
             'ReportROI', # 5
             ]                        

    if n < 0 or n > len( steps ):
      n = 0

    return steps[n]

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

  @staticmethod
  def findChildren(widget=None,name="",text=""):
    """ return a list of child widgets that match the passed name """
    # TODO: figure out why the native QWidget.findChildren method
    # does not seem to work from PythonQt
    if not widget:
      widget = mainWindow()
    children = []
    parents = [widget]
    while parents != []:
      p = parents.pop()
      parents += p.children()
      if name and p.name.find(name)>=0:
        children.append(p)
      elif text: 
        try:
          p.text
          if p.text.find(text)>=0:
            children.append(p)
        except AttributeError:
          pass
    return children

  @staticmethod
  def getNodeByID(id):
    return slicer.mrmlScene.GetNodeByID(id)

  @staticmethod
  def getNodeByName(name):
    """get the first MRML node that has the given name
    - use a regular expression to match names post-pended with numbers"""
 
    slicer.mrmlScene.InitTraversal()
    node = slicer.mrmlScene.GetNextNode()
    while node:
      try:
        nodeName = node.GetName()
        if nodeName.find(name) == 0:
          # prefix matches, is the rest all numbers?
          if nodeName == name or nodeName[len(name):].isdigit():
            return node
      except:
        pass
      node = slicer.mrmlScene.GetNextNode()
    return None

  @staticmethod
  def readFileAsString(fname):
    s = ''
    with open(fname, 'r') as f:
      s = f.read()
    return s
