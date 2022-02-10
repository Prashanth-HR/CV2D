import pypylon.pylon as py
from PIL import Image
import pypylon.genicam as geni
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
import pandas as pd

# open the camera
tlf = py.TlFactory.GetInstance()
devices = tlf.EnumerateDevices()
for device in devices:
    print(device.GetFriendlyName())
camera = py.InstantCamera(tlf.CreateFirstDevice())
camera.Open()
print("Using device ", camera.GetDeviceInfo().GetModelName())

#######Auto Function ROI #####################################################
## Enable the 'Brightness' auto function (Gain Auto + Exposure Auto)
## for the auto function ROI selected
# camera.AutoFunctionROIUseBrightness.SetValue(True)
# ## Highlight the auto function ROI selected
# camera.AutoFunctionROIHighlight.SetValue(True)

####### Auto Function Profile ###################################################
# ## Set the auto function profile to Exposure Minimum
# camera.AutoFunctionProfile.SetValue("MinimizeExposureTime");
# print("camera.AutoFunctionProfile.GetValue(): ", camera.AutoFunctionProfile.GetValue())
#
# ## Set the auto function profile to Gain Minimum
# camera.AutoFunctionProfile.SetValue("MinimizeGain")
# print("camera.AutoFunctionProfile.GetValue(): ", camera.AutoFunctionProfile.GetValue())

## Enable Gain and Exposure Auto auto functions and set the operating mode to Continuous
camera.GainAuto.SetValue("Continuous")
print("camera.GainAuto.GetValue(): ", camera.GainAuto.GetValue())

camera.ExposureAuto.SetValue("Continuous")
print("camera.ExposureAuto.GetValue(): ", camera.ExposureAuto.GetValue())
camera.ExposureTime.SetValue(30216)
camera.AcquisitionFrameRate.SetValue(100)
camera.Gamma.SetValue(1)
camera.TriggerSelector = "FrameStart"
camera.ChunkSelector.SetValue("AutoBrightnessStatus")
#################################################################
camera.PixelFormat = "Mono10"
# like above, alternative is the long form
camera.PixelFormat.SetValue("Mono10")

# Packet Size
camera.GevSCPSPacketSize.SetValue(1500)
# Inter-Packet Delay
camera.GevSCPD.SetValue(2000)

# grab one image with a timeout of 1s
# returns a GrabResult, which is the image plus metadata
res = camera.GrabOne(3000)
# the raw memory of the image
res.GetBuffer()[:100]
# full method call
img = res.GetArray()
# abbrev
img = res.Array
# Image.fromarray(res.Array).save("./images.png")
print('Dimensions : ', img.shape)
cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.imshow("img", img)
# need to press a key to get the next image, by the last one the program will exit.
cv2.waitKey(0)

camera.StartGrabbingMax(10)
try:
  while camera.IsGrabbing():
    result = camera.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
    if result.GrabSucceeded():
      try:
        # The beef
        Image.fromarray(result.Array).save("./images/images.png")
        print("saved image")
        camera.StopGrabbing()
      finally:
        result.Release()
finally:
  camera.StopGrabbing()
  camera.Close()

camera.Close()
