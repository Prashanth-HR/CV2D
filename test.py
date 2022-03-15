import numpy as np
import cv2 as cv
from PIL import Image

from camera_control import Camera

from cam_calibration.camera_toXYZ import camera_realtimeXYZ
from object_recognition import ObjectRecognition

def main():
    cameraXYZ = camera_realtimeXYZ()
    obj_recognition = ObjectRecognition()
    camera = Camera()
    
    
    


    # Programatically take pictures and use those image
    # img = cv.imread('images/image.bmp')
    img = camera.get_image()
    #cv.namedWindow("img", cv.WINDOW_NORMAL)
    #cv.imshow("img", img)
    #cv.waitKey(0)

    Image.fromarray(img).save("./images/image.bmp")

    # load a background and img
    img_bg = cv.imread('images/background.bmp')
    img = cv.imread('images/image.bmp')
    # Get pixel centers of the detected objs
    cordPixels = obj_recognition.obj_recognize(img, img_bg)
    
    # Convert the pixel centers to 3D cords
    cord3D = [cameraXYZ.calculate_XYZ(*cord2D) for cord2D in cordPixels]
    
    print(cord3D)
    
    return np.squeeze(cord3D)

if __name__ == "__main__":
    main()