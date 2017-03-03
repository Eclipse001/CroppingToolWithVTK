import vtk
from slider import *

dir_ = r"CTDATA"

# Call backs:
def scaleXSliderCallback(obj, event):
    sliderRep = obj.GetRepresentation()
    
    val = sliderRep.GetValue()
    prevScaleSet = quadric.GetScale()
    quadric.SetScale(val,prevScaleSet[1],prevScaleSet[2])
    
    functionToStencil.Modified()
    functionToStencil.Update()
    stencil.Modified()
    stencil.Update()
    volume.Modified()
    volume.Update()

def scaleYSliderCallback(obj, event):
    sliderRep = obj.GetRepresentation()
    
    val = sliderRep.GetValue()
    prevScaleSet = quadric.GetScale()
    quadric.SetScale(prevScaleSet[0],val,prevScaleSet[2])
    
    functionToStencil.Modified()
    functionToStencil.Update()
    stencil.Modified()
    stencil.Update()
    volume.Modified()
    volume.Update()

def scaleZSliderCallback(obj, event):
    sliderRep = obj.GetRepresentation()
    
    val = sliderRep.GetValue()
    prevScaleSet = quadric.GetScale()
    quadric.SetScale(prevScaleSet[0],prevScaleSet[0],val)
    
    functionToStencil.Modified()
    functionToStencil.Update()
    stencil.Modified()
    stencil.Update()
    volume.Modified()
    volume.Update()

def posXSliderCallback(obj, event):
    sliderRep = obj.GetRepresentation()
    
    val = sliderRep.GetValue()
    prevCenterSet = quadric.GetCenter()
    quadric.SetCenter(val,prevCenterSet[1],prevCenterSet[2])
    
    functionToStencil.Modified()
    functionToStencil.Update()
    stencil.Modified()
    stencil.Update()
    volume.Modified()
    volume.Update()

def posYSliderCallback(obj, event):
    sliderRep = obj.GetRepresentation()
    
    val = sliderRep.GetValue()
    prevCenterSet = quadric.GetCenter()
    quadric.SetCenter(prevCenterSet[0],val,prevCenterSet[2])
    
    functionToStencil.Modified()
    functionToStencil.Update()
    stencil.Modified()
    stencil.Update()
    volume.Modified()
    volume.Update()

def posZSliderCallback(obj, event):
    sliderRep = obj.GetRepresentation()
    
    val = sliderRep.GetValue()
    prevCenterSet = quadric.GetCenter()
    quadric.SetCenter(prevCenterSet[0],prevCenterSet[1],val)
    
    functionToStencil.Modified()
    functionToStencil.Update()
    stencil.Modified()
    stencil.Update()
    volume.Modified()
    volume.Update()

# Read data
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir_)
reader.Update()

# Define an implicit function
quadric = vtk.vtkSuperquadric()
quadric.SetCenter(reader.GetOutput().GetCenter())
quadric.SetScale(100,100,100)

functionToStencil = vtk.vtkImplicitFunctionToImageStencil()
functionToStencil.SetInput(quadric)
functionToStencil.SetInformationInput(reader.GetOutput())
functionToStencil.Update()

# Create image   
stencil = vtk.vtkImageStencil()
stencil.SetInputConnection(reader.GetOutputPort())
stencil.SetBackgroundValue(reader.GetOutput().GetScalarRange()[0]-1)
stencil.SetStencilData(functionToStencil.GetOutput())

# Create colour transfer function
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-77, 0.54902, 0.25098, 0.14902)
colorFunc.AddRGBPoint(94, 0.882353, 0.603922, 0.290196)
colorFunc.AddRGBPoint(179, 1, 0.937033, 0.954531)
colorFunc.AddRGBPoint(260, 0.615686, 0, 0)
colorFunc.AddRGBPoint(3071, 0.827451, 0.658824, 1)

# Create opacity transfer function
alphaChannelFunc = vtk.vtkPiecewiseFunction()
alphaChannelFunc.AddPoint(-3024, 0.0)
alphaChannelFunc.AddPoint(-77, 0.0)
alphaChannelFunc.AddPoint(94, 0.29)
alphaChannelFunc.AddPoint(179, 0.55)
alphaChannelFunc.AddPoint(260, 0.84)
alphaChannelFunc.AddPoint(3071, 0.875)

ren = vtk.vtkRenderer()

# Instantiate necessary classes and create VTK pipeline
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.SetSize(1350,750)

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Define volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()  
volumeMapper.SetInputConnection(stencil.GetOutputPort())

# Set the mapper and volume properties
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)  
ren.AddVolume(volume)

# Setup the slider widget
sliderRepSX = vtk.vtkSliderRepresentation2D()
sliderWidgetSX = vtk.vtkSliderWidget()

sliderRepSY = vtk.vtkSliderRepresentation2D()
sliderWidgetSY = vtk.vtkSliderWidget()

sliderRepSZ= vtk.vtkSliderRepresentation2D()
sliderWidgetSZ = vtk.vtkSliderWidget()

getSliderObjects(sliderRepSX, sliderWidgetSX, "Radius X", iren, 100, 5, 205, 0, 500, scaleXSliderCallback)
getSliderObjects(sliderRepSY, sliderWidgetSY, "Radius Y", iren, 100, 5, 205, 0, 300, scaleYSliderCallback)
getSliderObjects(sliderRepSZ, sliderWidgetSZ, "Radius Z", iren, 100, 5, 205, 0, 100, scaleZSliderCallback)

sliderRepPX = vtk.vtkSliderRepresentation2D()
sliderWidgetPX = vtk.vtkSliderWidget()

sliderRepPY = vtk.vtkSliderRepresentation2D()
sliderWidgetPY = vtk.vtkSliderWidget()

sliderRepPZ = vtk.vtkSliderRepresentation2D()
sliderWidgetPZ = vtk.vtkSliderWidget()

getSliderObjects(sliderRepPX, sliderWidgetPX, "Position X", iren, quadric.GetCenter()[0], 25, 225, 1050, 500, posXSliderCallback)
getSliderObjects(sliderRepPY, sliderWidgetPY, "Position Y", iren, quadric.GetCenter()[1], 25, 225, 1050, 300, posYSliderCallback)
getSliderObjects(sliderRepPZ, sliderWidgetPZ, "Position Z", iren, quadric.GetCenter()[2], 25, 225, 1050, 100, posZSliderCallback)

# Render the scene
renWin.Render()
iren.Start()

# --- end of script --