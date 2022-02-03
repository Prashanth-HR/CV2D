import numpy as np
import cv2 as cv

savedir="../camera_data/"
newcam_mtx=np.load(savedir+'newcam_mtx.npy')

#load center points from New Camera matrix
cx=newcam_mtx[0,2]
cy=newcam_mtx[1,2]
fx=newcam_mtx[0,0]

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
win_name="Verify"
cv.namedWindow(win_name, cv.WND_PROP_FULLSCREEN)
# cv.setWindowProperty(win_name,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

print("getting images")
print("cx: "+str(cx)+",cy "+str(cy)+",fx "+str(fx))

img = cv.imread('../images/test_images/image4.jpg')
# img = cv.imread('images/cam_calibration/chessboard_25.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


# Find the chess board corners
ret, corners = cv.findChessboardCorners(gray, (7,7), None)
# If found, add object points, image points (after refining them)
if ret == True:
    corners2=cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
    print(corners2)
    # Draw and display the corners
    cv.drawChessboardCorners(img, (7,7), corners2[:1,:,:], ret)
    cv.imshow(win_name, img)
    cv.waitKey(0)

img1=img
    
cv.destroyAllWindows()