from __future__ import print_function
import cv2 as cv
import numpy as np

"""

cv.samples.addSamplesDataSearchPath('C:/Users/haum/PycharmProjects/pcmr/images')
#src = cv.imread(cv.samples.findFile(args.input), cv.IMREAD_GRAYSCALE)
src = cv.imread(cv.samples.findFile('spoon_s.jpg'), cv.IMREAD_GRAYSCALE)
if src is None:
    print('Could not open or find the image:', args.input)
    exit(0)
#-- Step 1: Detect the keypoints using SIFT Detector
detector = cv.SIFT_create()
keypoints = detector.detect(src)
#-- Draw keypoints
img_keypoints = np.empty((src.shape[0], src.shape[1], 3), dtype=np.uint8)
cv.drawKeypoints(src, keypoints, img_keypoints)
#-- Show detected (drawn) keypoints
cv.imshow('SIFT Keypoints', img_keypoints)
cv.waitKey()

"""

cv.samples.addSamplesDataSearchPath('./images/')
img1 = cv.imread(cv.samples.findFile('tum_logo1.png'), cv.IMREAD_GRAYSCALE)
#img1 = cv.resize(img1, (540, 540))
img2 = cv.imread(cv.samples.findFile('tum_logo2.png'), cv.IMREAD_GRAYSCALE)
#img2 = cv.resize(img2, (540, 540))
if img1 is None or img2 is None:
    print('Could not open or find the images!')
    exit(0)
#-- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
detector = cv.SIFT_create()
keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
keypoints2, descriptors2 = detector.detectAndCompute(img2, None)
#-- Step 2: Matching descriptor vectors with a FLANN based matcher
# Since SURF is a floating-point descriptor NORM_L2 is used
matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)
#-- Filter matches using the Lowe's ratio test
ratio_thresh = 0.7
good_matches = []
for m,n in knn_matches:
    if m.distance < ratio_thresh * n.distance:
        good_matches.append(m)
#-- Draw matches
img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
cv.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, img_matches, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
#-- Show detected matches
cv.namedWindow('Good Matches',cv.WINDOW_NORMAL)
cv.resizeWindow('Good Matches', 1000,1500)
cv.imshow('Good Matches', img_matches)
cv.waitKey(0)