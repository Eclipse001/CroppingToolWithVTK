#!/usr/bin/env python
import vtk
from vtkSliderCon import *

dir_ = r"CTDATA"


def vtkSliderCallback(obj, event):
    sliderRep = obj.GetRepresentation()
    rad = sliderRep.GetValue()
    sphere.SetRadius(rad)
    sphere.Modified()
    
    functionToStencil.Modified()
    functionToStencil.Update()
    
    stencil.Modified()
    stencil.Update()
    
    volume2.Modified()
    volume2.Update() 

# Read data
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir_)
reader.Update()

# Define an implicit function
quadric = vtk.vtkSuperquadric()
quadric.SetCenter(reader.GetOutput().GetCenter())
quadric.SetScale(180,80,40)

sphere = vtk.vtkSphere()
sphere.SetCenter(reader.GetOutput().GetCenter())
sphere.SetRadius(80)

functionToStencil = vtk.vtkImplicitFunctionToImageStencil()
functionToStencil.SetInput(sphere)
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


# Create two viewports to display original and cropped data
ren1 = vtk.vtkRenderer()
ren1.SetViewport(0.0, 0.0, 0.5, 1.0)


ren2 = vtk.vtkRenderer()
#ren2.SetViewport(0.5, 0.0, 1.0, 1.0)

# Instantiate necessary classes and create VTK pipeline
renWin = vtk.vtkRenderWindow()
#renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.SetSize(800,600)

# Define volume mapper
volumeMapper1 = vtk.vtkSmartVolumeMapper()  
volumeMapper1.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Set the mapper and volume properties
volume1 = vtk.vtkVolume()
volume1.SetMapper(volumeMapper1)
volume1.SetProperty(volumeProperty)  

# Add the volume to the renderer
ren1.AddVolume(volume1)

# Define volume mapper
volumeMapper2 = vtk.vtkSmartVolumeMapper()  
volumeMapper2.SetInputConnection(stencil.GetOutputPort())

# Set the mapper and volume properties
volume2 = vtk.vtkVolume()
volume2.SetMapper(volumeMapper2)
volume2.SetProperty(volumeProperty)  
ren2.AddVolume(volume2)

# Setup the slider widget
sc = SliderConstructor("Sphere radius", iren, 80, 5, 150, 100, vtkSliderCallback)

# Render the scene
renWin.Render()
iren.Start()

# --- end of script --