import numpy as np
import cv2 as cv
import glob


writeValues=False

# Load previously saved data
#load camera calibration
savedir="../camera_data/"
cam_mtx=np.load(savedir+'cam_mtx.npy')
dist=np.load(savedir+'dist.npy')
newcam_mtx=np.load(savedir+'newcam_mtx.npy')
roi=np.load(savedir+'roi.npy')

# pose, rotation and translation vectors..

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)

#add 2.5 to account for 2.5 cm per square in grid
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)


def draw(img, corners, imgpts):
    # print(corners[0].ravel())
    # print(tuple(np.int32(imgpts[0]).ravel()))
    corner = tuple(np.int32(corners[0]).ravel())
    img = cv.line(img, corner, tuple(np.int32(imgpts[0]).ravel()), (255,0,0), 5)
    img = cv.line(img, corner, tuple(np.int32(imgpts[1]).ravel()), (0,255,0), 5)
    img = cv.line(img, corner, tuple(np.int32(imgpts[2]).ravel()), (0,0,255), 5)
    return img



img = cv.imread('../images/test_images/image3.jpg')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
ret, corners = cv.findChessboardCorners(gray, (7,7),None)
if ret == True:
    corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    # Find the rotation and translation vectors.

    print("solvePNP")
    ret,rvecs, tvecs = cv.solvePnP(objp, corners2, newcam_mtx, dist)

    print("pnp rvec1 - Rotation")
    print(rvecs)
    if writeValues==True: np.save(savedir+'rvec1.npy', rvecs)

    print("pnp tvec1 - Translation")
    print(tvecs)
    if writeValues==True: np.save(savedir+'tvec1.npy', tvecs)

    print("R - rodrigues vecs")
    R_mtx, jac=cv.Rodrigues(rvecs)
    print(R_mtx)
    if writeValues==True: np.save(savedir+'R_mtx.npy', R_mtx)

    print("R|t - Extrinsic Matrix")
    Rt=np.column_stack((R_mtx,tvecs))
    print(Rt)
    if writeValues==True: np.save(savedir+'Rt.npy', Rt)

    print("newCamMtx*R|t - Projection Matrix")
    P_mtx=newcam_mtx.dot(Rt)
    print(P_mtx)
    if writeValues==True: np.save(savedir+'P_mtx.npy', P_mtx)

    # project 3D points to image plane
    imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, newcam_mtx, dist)

    img = draw(img,corners2,imgpts)
    cv.imshow('img',img)
    k = cv.waitKey(0) & 0xFF
    if k == ord('s'):
        cv.imwrite('Pose Estimation', img)

cv.destroyAllWindows()