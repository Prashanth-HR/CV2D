import json

import pypylon.pylon as py
from PIL import Image
import cv2

class Camera:
    def __init__(self) -> None:
        pass

    def get_image(self):
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

        # demonstrate some feature access
        new_width = camera.Width.GetValue() - camera.Width.GetInc()
        if new_width >= camera.Width.GetMin():
            camera.Width.SetValue(new_width)

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer = 5

        # Grabs 100 times until it gets
        print("Start Grab")
        camera.StartGrabbingMax(100)
        try:
            i = 0
            while camera.IsGrabbing():
                i = i+1
                result = camera.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
                print(i, result.GrabSucceeded())
                # Image grabbed successfully?
                if result.GrabSucceeded():
                    # Access the image data.
                    img = result.Array
                    print("Gray value of first pixel: ", img[0, 0])
                    Image.fromarray(result.Array).save("./images/images.png")
                    print("saved image")

                    camera.StopGrabbing()

                    return img
                else:
                    print("Error: ", result.ErrorCode, result.ErrorDescription)
                result.Release()

        finally:
            camera.StopGrabbing()
            camera.Close()

        camera.Close()


if __name__ == "__main__":
    camera = Camera()
    img = camera.get_image()

    # Show the image
    print('Dimensions : ', img.shape)
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    # need to press a key to get the next image, by the last one the program will exit.
    cv2.waitKey(0)
    cv2.destroyAllWindows()