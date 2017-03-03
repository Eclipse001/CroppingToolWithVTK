import vtk

def getSliderObjects(sliderRep, sliderWidget, titleText, iren, initVal, minVal, maxVal, posXLeft, posY, callBackFunc): 
    sliderRep.SetMinimumValue(minVal)
    sliderRep.SetMaximumValue(maxVal)
    sliderRep.SetValue(initVal)
    sliderRep.SetTitleText(titleText)
    sliderRep.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
    sliderRep.GetPoint1Coordinate().SetValue(posXLeft, posY, 0)
    sliderRep.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
    sliderRep.GetPoint2Coordinate().SetValue(posXLeft+300, posY, 0)
    sliderRep.SetSliderLength(0.025)
    sliderRep.SetSliderWidth(0.025)
    sliderRep.SetEndCapLength(0.0125)

    sliderWidget.SetInteractor(iren)
    sliderWidget.SetRepresentation(sliderRep)
    sliderWidget.KeyPressActivationOff()
    sliderWidget.SetAnimationModeToAnimate()
    sliderWidget.SetEnabled(True)
    sliderWidget.AddObserver("InteractionEvent", callBackFunc)