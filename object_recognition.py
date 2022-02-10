#
# https://www.kaggle.com/pacogarciam3/lego-set-object-recognition-example

import cv2
import numpy as np

# image with object
img_example = cv2.imread('images/test_images/multi-obj1.bmp')

# load a background, so we can extract it and make it easy to detect the object.
img_bg = cv2.imread('images/test_images/background.bmp')

blur_after_difference = True        # True blurs picture after taking the difference, False blurs both images before
use_adaptive_threshold = False      # True uses adaptive threshold, False uses original Otsu Threshold

class objectRecognition:
    # OpenCV uses BGR while matplotlib uses RGB, so we need to make sure that put these conversion in so the picture
    # look accurate (you can try previewing without these if you like to test).

    # We will be previewing images alongthe way, so lets create a function
    def previewImg(text, img_preview, grayscale=False):
        # plt.imshow(img_preview)
        if grayscale == False:
            # convert a color image from BGR to RGB before previewing
            img_preview = cv2.cvtColor(img_preview, cv2.COLOR_BGR2RGB)
        else:
            # option for Grayscale images
            img_preview = cv2.cvtColor(img_preview, cv2.COLOR_GRAY2RGB)
        cv2.namedWindow(text, cv2.WINDOW_NORMAL)
        cv2.imshow(text, img_preview)
        print('Dimensions : ', img_preview.shape)
        # need to press a key to get the next image, by the last one the program will exit.
        cv2.waitKey(0)

    # our starting Point
    previewImg('Background Image', img_bg)
    previewImg('Example Image', img_example)

    # Background - Gray
    img_bg_gray = cv2.cvtColor(img_bg, cv2.COLOR_BGR2GRAY)
    previewImg("Background Gray", img_bg_gray, True)
    # Image - Gray
    img_gray = cv2.cvtColor(img_example, cv2.COLOR_BGR2GRAY)
    previewImg("Image Gray", img_gray, True)

    if blur_after_difference:
        kernel_size = 123  # Has to be an odd divider of 255, e.g. 123, 51, 25
        img_gray = cv2.resize(img_gray, (img_bg_gray.shape[1], img_bg_gray.shape[0]))
        # Calculate Difference
        diff_gray = cv2.absdiff(img_bg_gray, img_gray)
        previewImg("Pre-Blur", diff_gray, True)
        # Diff Blur
        diff_gray_blur = cv2.GaussianBlur(diff_gray, (kernel_size, kernel_size), 0)
        previewImg("Diff Blur", diff_gray_blur, True)
    
    else:
        kernel_size = 51  # Has to be an odd divider of 255, e.g. 123, 51, 25
        bg_blur = cv2.GaussianBlur(img_bg_gray, (kernel_size, kernel_size), 0)
        img_blur = cv2.GaussianBlur(img_gray, (kernel_size, kernel_size), 0)
        previewImg("Pre-Diff", img_blur, True)
        # Calculate Difference
        diff_gray_blur = cv2.absdiff(bg_blur, img_blur)
        previewImg("diff_blur", diff_gray_blur, True)

    if use_adaptive_threshold:
        img_tresh = cv2.adaptiveThreshold(diff_gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        img_tresh = -img_tresh + 255 # invert black/white to find contours with cv2.findContours()
        previewImg("Adaptive Treshold", img_tresh, True)

    else:
        # find otsu's threshold value with OpenCV function
        ret, img_tresh = cv2.threshold(diff_gray_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        previewImg("Otsu Treshold", img_tresh, True)

    # let's now draw the contour
    # print("img_tresh:{}, Retr_ext:{}, Chain_aprox:{} ".format(img_tresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
    # arr_cnt, hirearchy = cv2.findContours(img_tresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    arr_cnt, a1 = cv2.findContours(img_tresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # let's copy the example image, so we don't paint over it
    img_with_allcontours = img_example.copy()

    cv2.drawContours(img_with_allcontours, arr_cnt, -1, (0, 255, 0), 3)
    previewImg('Contours', img_with_allcontours)

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
        ca = cv2.contourArea(i)

        # Calculate W/H Ratio of image
        x, y, w, h = cv2.boundingRect(i)
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
    #     cv2.drawContours(img_withcontours, arr_cnt, validcontours[i], (0, 255, 0), 3)
    #     previewImg('Contours', img_withcontours)

    # Display a Bounding Rectangle
    img_withrectangle = img_example.copy()
    for i in validcontours:
        # option orientation of the image:
        # x, y, w, h = cv2.boundingRect(arr_cnt[i])
        # cv2.rectangle(img_withrectangle, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # option orientation of the object (minimizes the error):
        rect = cv2.minAreaRect(arr_cnt[i])
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        center = (int(box[0][0] + 0.5 * (box[2][0] - box[0][0])), int(box[0][1] + 0.5 * (box[2][1] - box[0][1])))
        img_withrectangle = cv2.circle(img=img_withrectangle,
                                       center=center,
                                       radius=5,
                                       color=(0, 255, 0),
                                       thickness=-1)

        cv2.drawContours(img_withrectangle, [box], 0, (0, 255, 0), 2)
        previewImg('Bounding Rectangle', img_withrectangle)

    cv2.destroyAllWindows()


exit()
