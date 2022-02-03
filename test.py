import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

from camera_toXYZ import camera_realtimeXYZ
from object_recognition import objectRecognition


def obj_detection(img_example, img_bg):
    # our starting Point
    img_bg_gray = cv.cvtColor(img_bg, cv.COLOR_BGR2GRAY)
    img_gray = cv.cvtColor(img_example, cv.COLOR_BGR2GRAY)
    img_gray = cv.resize(img_gray, (img_bg_gray.shape[1], img_bg_gray.shape[0]))
    diff_gray = cv.absdiff(img_bg_gray, img_gray)
    diff_gray_blur = cv.GaussianBlur(diff_gray, (5, 5), 0)

    ret, img_tresh = cv.threshold(diff_gray_blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    arr_cnt, hirearchy = cv.findContours(img_tresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # get the dimensions of the image
    height, width, channels = img_example.shape

    # shorten the variable names
    w = width
    h = height

    validcontours = []
    contour_index = -1

    # iterate through each contour found
    for i in arr_cnt:

        contour_index = contour_index + 1
        ca = cv.contourArea(i)

        # Calculate W/H Ratio of image
        x, y, w, h = cv.boundingRect(i)
        aspect_ratio = float(w) / h

        # Flag as edge_noise if the object is at a Corner
        # Contours at the edges of the image are most likely not valid contours
        edge_noise = False
        # if contour starts at x=0 then it's on th edge
        if x == 0:
            edge_noise = True
        if y == 0:
            edge_noise = True
        # if the contour x value + its contour width exceeds image width, it is on an edge
        if (x + w) == width:
            edge_noise = True
        if (y + h) == height:
            edge_noise = True

        # DISCARD noise with measure by area (1x1 round plate dimensions is 1300)
        # if by any chance a contour is drawn on one pixel, this catches it.
        if ca > 1300:

            # DISCARD as noise if W/H ratio > 7 to 1 (1x6 plate is 700px to 100px)
            # the conveyor belt has a join line that sometimes is detected as a contour, this ignores it based on w/h ratio
            if aspect_ratio <= 6:

                # DISCARD if at the Edge
                if edge_noise == False:
                    validcontours.append(contour_index)

    return (arr_cnt, validcontours)


def previewImg(text, img_preview, grayscale=False):
    # plt.imshow(img_preview)
    if grayscale == False:
        # convert a color image from BGR to RGB before previewing
        plt.imshow(cv.cvtColor(img_preview, cv.COLOR_BGR2RGB))
    else:
        # option for Grayscale images
        plt.imshow(cv.cvtColor(img_preview, cv.COLOR_GRAY2RGB))
    plt.title(text)
    plt.show()


def main():
    cameraXYZ = camera_realtimeXYZ()

    img = cv.imread('images/test_images/all_2.jpg')

    # load a background, so we can extract it and make it easy to detect the object.
    img_bg = cv.imread('images/test_images/background.jpg')

    img_withrectangle = img.copy()
    arr_cnt, validcontours = obj_detection(img, img_bg)

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
