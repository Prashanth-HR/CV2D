import numpy as np
import cv2 as cv

from camera_toXYZ import camera_realtimeXYZ


# mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(img,(x,y),8,(0,255,0),1)
        XYZ = cameraXYZ.calculate_XYZ(x,y)
        print('Move to postion : {}'.format(XYZ))

win_name="Test: "
cv.namedWindow(win_name, cv.WND_PROP_FULLSCREEN)
#cv.setWindowProperty(win_name,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

img = cv.imread('../images/test_images/image4.jpg')
cameraXYZ = camera_realtimeXYZ()

savedir="../camera_data/"
newcam_mtx=np.load(savedir+'newcam_mtx.npy')
#load center points from New Camera matrix
cx=newcam_mtx[0,2]
cy=newcam_mtx[1,2]

cv.circle(img,(np.int32(cx),np.int32(cy)), 10, (0,0,255), thickness=2)
# Create a black image, a window and bind the function to window
cv.setMouseCallback(win_name,draw_circle)
while(1):
    cv.imshow(win_name,img)
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()


