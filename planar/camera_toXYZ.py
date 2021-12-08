import numpy as np
import cv2 as cv

class camera_realtimeXYZ:

    #camera variables
    cam_mtx=None
    dist=None
    newcam_mtx=None
    roi=None
    rvec1=None
    tvec1=None
    R_mtx=None
    Rt=None
    P_mtx=None

    #images
    img=None


    def __init__(self):

        imgdir="/home/pi/Desktop/Captures/"
        savedir="../camera_data/"

        self.cam_mtx=np.load(savedir+'cam_mtx.npy')
        self.dist=np.load(savedir+'dist.npy')
        self.newcam_mtx=np.load(savedir+'newcam_mtx.npy')
        self.roi=np.load(savedir+'roi.npy')
        self.rvec1=np.load(savedir+'rvec1.npy')
        self.tvec1=np.load(savedir+'tvec1.npy')
        self.R_mtx=np.load(savedir+'R_mtx.npy')
        self.Rt=np.load(savedir+'Rt.npy')
        self.P_mtx=np.load(savedir+'P_mtx.npy')

        s_arr=np.load(savedir+'s_arr.npy')
        self.scalingfactor=s_arr[0]
        print(self.scalingfactor)
        self.inverse_newcam_mtx = np.linalg.inv(self.newcam_mtx)
        self.inverse_R_mtx = np.linalg.inv(self.R_mtx)
    
    def previewImage(self, text, img):
        #show full screen
        cv.namedWindow(text, cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty(text,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

        cv.imshow(text,img)
        cv.waitKey(2000)
        cv.destroyAllWindows()

    def undistort_image(self,image):
        image_undst = cv.undistort(image, self.cam_mtx, self.dist, None, self.newcam_mtx)

        return image_undst

    def load_background(self,background):
        self.bg_undst=self.undistort_image(background)
        self.bg=background

    
    def calculate_XYZ(self,u,v):
                                      
        #Solve: From Image Pixels, find World Points

        uv_1=np.array([[u,v,1]], dtype=np.float32)
        uv_1=uv_1.T
        suv_1=self.scalingfactor*uv_1
        xyz_c=self.inverse_newcam_mtx.dot(suv_1)
        xyz_c=xyz_c-self.tvec1
        XYZ=self.inverse_R_mtx.dot(xyz_c)

        return XYZ

