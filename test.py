import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

from camera_toXYZ import camera_realtimeXYZ
from object_recognition import ObjectRecognition

def main():
    cameraXYZ = camera_realtimeXYZ()
    obj_recognition = ObjectRecognition()

    img = cv.imread('images/test_images/multi-obj1.bmp')

    # load a background, so we can extract it and make it easy to detect the object.
    img_bg = cv.imread('images/test_images/background.bmp')

    img_withrectangle = img.copy()
    arr_cnt, validcontours = obj_recognition.obj_recognize(img, img_bg)

    # Iterate for all the detected valid contours..
    cord3D = []
    for i in validcontours:
        c = arr_cnt[i]

        # draw the bounding rectangles
        rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        cv.drawContours(img_withrectangle, [box], 0, (0, 255, 0), 2)

        # compute the center of the contour
        M = cv.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # draw the contour and center of the shape on the image
        # cv.drawContours(img_withrectangle, [c], -1, (0, 255, 0), 2)
        cv.circle(img_withrectangle, (cX, cY), 7, (255, 255, 255), -1)
        cv.putText(img_withrectangle, "center", (cX - 20, cY - 20),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        ##############   Start 2d pixel to 3D real world conversion   #############
        XYZ = cameraXYZ.calculate_XYZ(cX, cY)
        cord3D.append(XYZ)
        # print('Move to postion : \n {}'.format(XYZ))

    savedir = "./camera_data/"
    newcam_mtx = np.load(savedir + 'newcam_mtx.npy')

    # load center points from New Camera matrix from which the distances are calculated..
    cx = int(newcam_mtx[0, 2])
    cy = int(newcam_mtx[1, 2])
    cv.circle(img_withrectangle, (cx, cy), 10, (0, 0, 255), -1)
    cv.putText(img_withrectangle, "Ref point", (cx - 20, cy - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # previewImg('Bounding Rectangle', img_withrectangle)

    return np.squeeze(cord3D)

if __name__ == "__main__":
    main()