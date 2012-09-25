volume = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode1')
modelNodes = slicer.util.getNodes('vtkMRMLModelNode*')
for modelNode in modelNodes.values():
  if modelNode.GetName()=='Obturator_reg':
    obturator = modelNode


x=  (46.1749-23.8251)/2+23.8251
y = (65.1951-42.9222)/2+42.9222
z = 150/2-120




def AddRoiLabel(X,Y,Z,color):
  roi = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationROINode')
  slicer.mrmlScene.AddNode(roi)
  bounds = [0,0,0,0,0,0]
  # obturator.GetRASBounds(bounds)
  #print(bounds)
  roi.VisibleOn()
  # roi.SetRadiusXYZ((bounds[0]-bounds[1])*1.2,abs(bounds[2]-bounds[3])*1.2,abs(bounds[4]-bounds[5])/2.5)
  transform = slicer.vtkMRMLLinearTransformNode()
  slicer.mrmlScene.AddNode(transform)
  # m = transform.GetMatrixTransformToParent()
  # m.SetElement(0,3,X)
  # m.SetElement(1,3,Y)
  # m.SetElement(2,3,Z)
  transformID = obturator.GetTransformNodeID()
  transform = slicer.mrmlScene.GetNodeByID(transformID)
  M = transform.GetMatrixTransformToParent()
  m = vtk.vtkMatrix4x4()
  
  t = slicer.mrmlScene.CreateNodeByClass('vtkMRMLLinearTransformNode')
  
  slicer.mrmlScene.AddNode(t)
  
  obturator.SetAndObserveTransformNodeID(t.GetID())
  obturator.GetRASBounds(bounds)
  roi.SetRadiusXYZ((bounds[0]-bounds[1])*1.2,abs(bounds[2]-bounds[3])*1.2,abs(bounds[4]-bounds[5])/4)
  obturator.SetAndObserveTransformNodeID(transform.GetID())
  
 
  m.DeepCopy(M)
  
  m0=vtk.vtkMatrix4x4()
  m0.SetElement(0,3,X)
  m0.SetElement(1,3,Y)
  m0.SetElement(2,3,Z)
  m.Multiply4x4(m,m0,m)
  t.SetAndObserveMatrixTransformToParent(m)
  roi.SetAndObserveTransformNodeID(t.GetID())
  cropVolumeNode =slicer.mrmlScene.CreateNodeByClass('vtkMRMLCropVolumeParametersNode')
  cropVolumeNode.SetScene(slicer.mrmlScene)
  cropVolumeNode.SetName('obturator_CropVolume_node')
  # cropVolumeNode.SetIsotropicResampling(True)
  # cropVolumeNode.SetSpacingScalingConst(0.5)
  slicer.mrmlScene.AddNode(cropVolumeNode)
  cropVolumeNode.SetInputVolumeNodeID(volume.GetID())
  cropVolumeNode.SetROINodeID(roi.GetID())
  cropVolumeLogic = slicer.modules.cropvolume.logic()
  cropVolumeLogic.Apply(cropVolumeNode)
  outputVolume = slicer.mrmlScene.GetNodeByID(cropVolumeNode.GetOutputVolumeNodeID())
  outputVolume.SetName("obturatorROI")
  # vl = slicer.modules.volumes.logic()
  # roiSegmentation = vl.CreateLabelVolume(slicer.mrmlScene, outputVolume, 'obturator_segmentation')
  # roiRange = outputVolume.GetImageData().GetScalarRange()
  # # default threshold is half-way of the range
  # # thresholdParameter = str(0)+','+str(roiRange[1])
  # thresh = vtk.vtkImageThreshold()
  # thresh.SetInput(outputVolume.GetImageData())
  # thresh.ThresholdBetween(0, roiRange[1])
  # thresh.SetInValue(10)
  # thresh.SetOutValue(0)
  # thresh.ReplaceOutOn()
  # thresh.ReplaceInOn()
  # thresh.Update()
  # roiSegmentation.SetAndObserveImageData(thresh.GetOutput())
  # labelsColorNode = slicer.modules.colors.logic().GetColorTableNodeID(color)
  # roiSegmentation.GetDisplayNode().SetAndObserveColorNodeID(labelsColorNode)
  
  
  


def AddRoiLabelContour(X,Y,Z,color,outputVolume,roiSegmentation):
  roi = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationROINode')
  slicer.mrmlScene.AddNode(roi)
  bounds = [0,0,0,0,0,0]
  obturator.GetRASBounds(bounds)
  #print(bounds)
  roi.VisibleOn()
  roi.SetRadiusXYZ(abs(bounds[0]-bounds[1])/4,abs(bounds[2]-bounds[3])/4,abs(bounds[4]-bounds[5])/2.5)
  transform = slicer.vtkMRMLLinearTransformNode()
  slicer.mrmlScene.AddNode(transform)
  m = transform.GetMatrixTransformToParent()
  m.SetElement(0,3,X)
  m.SetElement(1,3,Y)
  m.SetElement(2,3,Z)
  # transformID = obturator.GetTransformNodeID()
  # transform = slicer.mrmlScene.GetNodeByID(transformID)
  # m = transform.GetMatrixTransformToParent()
  # m.SetElement(0,3,20)
  # m.SetElement(1,3,0)
  # m.SetElement(2,3,0)
  roi.SetAndObserveTransformNodeID(transform.GetID())
  cropVolumeNode =slicer.mrmlScene.CreateNodeByClass('vtkMRMLCropVolumeParametersNode')
  cropVolumeNode.SetScene(slicer.mrmlScene)
  cropVolumeNode.SetName('obturator_CropVolume_node')
  # cropVolumeNode.SetIsotropicResampling(True)
  # cropVolumeNode.SetSpacingScalingConst(0.5)
  slicer.mrmlScene.AddNode(cropVolumeNode)
  cropVolumeNode.SetInputVolumeNodeID(volume.GetID())
  cropVolumeNode.SetROINodeID(roi.GetID())
  cropVolumeLogic = slicer.modules.cropvolume.logic()
  cropVolumeLogic.Apply(cropVolumeNode)
  # outputVolume = slicer.mrmlScene.GetNodeByID(cropVolumeNode.GetOutputVolumeNodeID())
  # outputVolume.SetName("obturatorROI")
  # # roiRange = outputVolume.GetImageData().GetScalarRange()
  # thresh = vtk.vtkImageThreshold()
  # thresh.SetInput(outputVolume.GetImageData())
  # thresh.ThresholdBetween(0, 1000)
  # thresh.SetInValue(10)
  # thresh.SetOutValue(0)
  # thresh.ReplaceOutOn()
  # thresh.ReplaceInOn()
  # thresh.Update()
  # # roiSegmentation.SetAndObserveImageData(outputVolume.GetImageData())
  # roiSegmentation.SetAndObserveImageData(thresh.GetOutput())
  # labelsColorNode = slicer.modules.colors.logic().GetColorTableNodeID(color)
  # roiSegmentation.GetDisplayNode().SetAndObserveColorNodeID(labelsColorNode)

  

  
# modelNodes = slicer.util.getNodes('vtkMRMLScalarVolumeNode*')
# for modelNode in modelNodes.values():
  # if modelNode.GetName()=='obturator_segmentation':
    # roiSegmentation = modelNode
  # if modelNode.GetName()=='obturatorROI':
    # outputVolume = modelNode
  
 

 
 
AddRoiLabel(x,y,z,10)
# AddRoiLabelContour(x,y-20,z,10,outputVolume,roiSegmentation)
# AddRoiLabelContour(x,y+20,z,10,outputVolume,roiSegmentation)
# AddRoiLabelContour(x+20,y,z,10,outputVolume,roiSegmentation)
# AddRoiLabelContour(x-20,y,z,10,outputVolume,roiSegmentation)
  
  
  
# editUtil = EditorLib.EditUtil.EditUtil()
# parameterNode = editUtil.getParameterNode()
# lm = slicer.app.layoutManager()
# paintEffect = EditorLib.PaintEffectOptions()
# paintEffect.setMRMLDefaults()
# paintEffect.__del__()
# sliceWidget = lm.sliceWidget('Red')
# paintTool = EditorLib.PaintEffectTool(sliceWidget)
# editUtil.setLabel(3)
# for i in range(20):
  # for j in range(20):
    # paintTool.paintAddPoint(60+i,60+j)

    
# paintTool.paintApply()

