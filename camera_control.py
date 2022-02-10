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

nodeFile = "config-a2A3840-13gmPRO_40137700.pfs"
print("Loading camera configuration from: ", nodeFile)
py.FeaturePersistence.Load(nodeFile, camera.GetNodeMap(), True)

# # grab one image with a timeout of 1s
# # returns a GrabResult, which is the image plus metadata
# res = camera.GrabOne(5000)
# # full method call
# img = res.GetArray()
# # abbrev
# img = res.Array
# # Image.fromarray(res.Array).save("./images.png")
# print('Dimensions : ', img.shape)
# cv2.namedWindow("img", cv2.WINDOW_NORMAL)
# cv2.imshow("img", img)
# # need to press a key to get the next image, by the last one the program will exit.
# cv2.waitKey(0)
# cv2.destroyAllWindows()

print("Start Grab")
camera.StartGrabbingMax(100)
try:
  while camera.IsGrabbing():
    result = camera.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
    print(result.GrabSucceeded())
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
