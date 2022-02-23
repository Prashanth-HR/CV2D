#
# https://www.kaggle.com/pacogarciam3/lego-set-object-recognition-example

import cv2 as cv
import numpy as np
from PIL import Image

# image with object
img_example = cv.imread('images/image.bmp')

# load a background, so we can extract it and make it easy to detect the object.
img_bg = cv.imread('images/background.bmp')

blur_after_difference = True  # True blurs picture after taking the difference, False blurs both images before
use_adaptive_threshold = False  # True uses adaptive threshold, False uses original Otsu Threshold


class ObjectRecognition:
    # OpenCV uses BGR while matplotlib uses RGB, so we need to make sure that put these conversion in so the picture
    # look accurate (you can try previewing without these if you like to test).

    def __init__(self) -> None:
        pass

    # We will be previewing images alongthe way, so lets create a function
    def previewImg(self, text, img_preview, grayscale=False):
        # plt.imshow(img_preview)
        if grayscale == False:
            # convert a color image from BGR to RGB before previewing
            img_preview = cv.cvtColor(img_preview, cv.COLOR_BGR2RGB)
        else:
            # option for Grayscale images
            img_preview = cv.cvtColor(img_preview, cv.COLOR_GRAY2RGB)
        cv.namedWindow(text, cv.WINDOW_NORMAL)
        cv.imshow(text, img_preview)
        # print('Dimensions : ', img_preview.shape)
        # need to press a key to get the next image, by the last one the program will exit.
        cv.waitKey(0)

    def obj_recognize_with_previewImg(self, img_bg, img_example):
        # our starting Point
        self.previewImg('Background Image', img_bg)
        self.previewImg('Example Image', img_example)

        # Background - Gray
        img_bg_gray = cv.cvtColor(img_bg, cv.COLOR_BGR2GRAY)
        self.previewImg("Background Gray", img_bg_gray, True)
        # Image - Gray
        img_gray = cv.cvtColor(img_example, cv.COLOR_BGR2GRAY)
        self.previewImg("Image Gray", img_gray, True)

        if blur_after_difference:
            kernel_size = 255  # Has to be an odd divider of 255, e.g. 123, 51, 25
            img_gray = cv.resize(img_gray, (img_bg_gray.shape[1], img_bg_gray.shape[0]))
            # Calculate Difference
            diff_gray = cv.absdiff(img_bg_gray, img_gray)
            self.previewImg("Pre-Blur", diff_gray, True)
            # Diff Blur
            diff_gray_blur = cv.GaussianBlur(diff_gray, (kernel_size, kernel_size), 0)
            self.previewImg("Diff Blur", diff_gray_blur, True)

        else:
            kernel_size = 51  # Has to be an odd divider of 255, e.g. 123, 51, 25
            bg_blur = cv.GaussianBlur(img_bg_gray, (kernel_size, kernel_size), 0)
            img_blur = cv.GaussianBlur(img_gray, (kernel_size, kernel_size), 0)
            self.previewImg("Pre-Diff", img_blur, True)
            # Calculate Difference
            diff_gray_blur = cv.absdiff(bg_blur, img_blur)
            self.previewImg("diff_blur", diff_gray_blur, True)

        if use_adaptive_threshold:
            img_tresh = cv.adaptiveThreshold(diff_gray_blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11,
                                             2)
            img_tresh = -img_tresh + 255  # invert black/white to find contours with cv.findContours()
            self.previewImg("Adaptive Treshold", img_tresh, True)

        else:
            # find otsu's threshold value with OpenCV function
            ret, img_tresh = cv.threshold(diff_gray_blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            self.previewImg("Otsu Treshold", img_tresh, True)

        # let's now draw the contour
        # print("img_tresh:{}, Retr_ext:{}, Chain_aprox:{} ".format(img_tresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE))
        # arr_cnt, hirearchy = cv.findContours(img_tresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        arr_cnt, a1 = cv.findContours(img_tresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # let's copy the example image, so we don't paint over it
        img_with_allcontours = img_example.copy()

        cv.drawContours(img_with_allcontours, arr_cnt, -1, (0, 255, 0), 3)
        self.previewImg('Contours', img_with_allcontours)

        # !!! It may be possible that various contours are showing at this stage, we'll solve that below.
        '''3 conditions to avoid noise in real world:
            - minimum area to consider an object (e.g. anything smaller than a 1x1 brick I will consider noise).
            - if the object is sitting in an edge (the brick is clipped)
            - if the object has a ratio that exceeds the objects (in this case, the 1x6 plate is the thinnest piece to detect, 
            anything with a longer ratio will be considered noise)'''
        # Just in case, we need to make sure we 'weed out' any contour noise that might generate as images have variations.

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

        # copy the original picture
        img_withcontours = img_example.copy()

        # call out if more than 1 valid contour is found
        if len(validcontours) > 1:
            print("There is more than 1 object in the picture")
        else:
            if len(validcontours) == 1:
                print("One object detected")
            else:
                print("No objects detected")
                # FYI: code below will most likely error out as it tries to iterate on an array

        # it might be possible we have more than 1 validcontour, iterating through them here
        # if there is zero contours, this most likely will error out
        # for i in validcontours:
        #     cv.drawContours(img_withcontours, arr_cnt, validcontours[i], (0, 255, 0), 3)
        #     previewImg('Contours', img_withcontours)

        # Display a Bounding Rectangle
        obj_centers = []
        img_withrectangle = img_example.copy()
        for i in validcontours:
            # option orientation of the image:
            # x, y, w, h = cv.boundingRect(arr_cnt[i])
            # cv.rectangle(img_withrectangle, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # option orientation of the object (minimizes the error):
            rect = cv.minAreaRect(arr_cnt[i])
            box = cv.boxPoints(rect)
            box = np.int0(box)

            center = (int(box[0][0] + 0.5 * (box[2][0] - box[0][0])), int(box[0][1] + 0.5 * (box[2][1] - box[0][1])))
            img_withrectangle = cv.circle(img=img_withrectangle,
                                          center=center,
                                          radius=5,
                                          color=(0, 255, 0),
                                          thickness=-1)

            cv.drawContours(img_withrectangle, [box], 0, (0, 255, 0), 2)
            obj_centers.append(center)
        self.previewImg('Bounding Rectangle', img_withrectangle)
        cv.destroyAllWindows()
        return obj_centers


    def obj_recognize(self, img, img_bg):
        # This method is for final run without any preview image popup's
        # our starting Point
        img_bg_gray = cv.cvtColor(img_bg, cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_gray = cv.resize(img_gray, (img_bg_gray.shape[1], img_bg_gray.shape[0]))
        diff_gray = cv.absdiff(img_bg_gray, img_gray)
        diff_gray_blur = cv.GaussianBlur(diff_gray, (501, 501), 0)

        ret, img_tresh = cv.threshold(diff_gray_blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        arr_cnt, hirearchy = cv.findContours(img_tresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # get the dimensions of the image
        height, width = img_gray.shape

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

        # Iterate for all the detected valid contours and find centers
        obj_centers = []
        img_withrectangle = img.copy()
        for i in validcontours:
            c = arr_cnt[i]

            # draw the bounding rectangles
            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            # cv.drawContours(img_withrectangle, [box], 0, (0, 255, 0), 2)

            # compute the center of the contour
            M = cv.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # draw the contour and center of the shape on the image
            # cv.drawContours(img_withrectangle, [c], -1, (0, 255, 0), 2)
            #  cv.circle(img_withrectangle, (cX, cY), 7, (255, 255, 255), -1)
            #  cv.putText(img_withrectangle, "center", (cX - 20, cY - 20),
            #         cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            img_withrectangle = cv.circle(img=img_withrectangle,
                                          center=(cX, cY),
                                          radius=5,
                                          color=(0, 255, 0),
                                          thickness=-1)
            cv.drawContours(img_withrectangle, [box], 0, (0, 255, 0), 2)
            obj_centers.append([cX, cY])

        #self.previewImg('Bounding Rectangle', img_withrectangle)
        Image.fromarray(img_withrectangle).save("./images/image_boundingbox.bmp")
        return obj_centers

if __name__ == "__main__":
    obj_detection = ObjectRecognition()
    obj_detection.obj_recognize(img_example, img_bg)