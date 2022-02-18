import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from camera_control import Camera

from camera_toXYZ import camera_realtimeXYZ
from object_recognition import ObjectRecognition

def main():
    cameraXYZ = camera_realtimeXYZ()
    obj_recognition = ObjectRecognition()
    camera = Camera()
    
    
    # load a background, so we can extract it and make it easy to detect the object.
    img_bg = cv.imread('images/test_images/background.bmp')


    # Programatically take pictures and use those image
    # img = cv.imread('images/test_images/multi-obj1.bmp')
    img = camera.get_image()

    # Get pixel centers of the detected objs
    cordPixels = obj_recognition.obj_recognize(img, img_bg)
    
    # Convert the pixel centers to 3D cords
    cord3D = [cameraXYZ.calculate_XYZ(*cord2D) for cord2D in cordPixels]
    
    # print(np.squeeze(cord3D))
    
    return np.squeeze(cord3D)

if __name__ == "__main__":
    main()