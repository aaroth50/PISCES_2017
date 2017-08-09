import glob
import cv2
import numpy as np
import glob
import os
import yaml

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*9, 3), np.float32)
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
objpoints = [] 
imgpoints_l = [] 
imgpoints_r = [] 
w_l, h_l = 0, 0
w_r, h_r = 0, 0
d = 0


images_l = sorted(glob.glob('checkerboardpics/left_*'))#put file location of checkerboard pattern here
images_r = sorted(glob.glob('checkerboardpics/right_*'))

for i, fname in enumerate(images_l):
    img_l = cv2.imread(images_l[i])
    img_r = cv2.imread(images_r[i])

    h_l, w_l = img_l.shape[:2]
    h_r, w_r = img_r.shape[:2]

    gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
    gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)

    flag = 0 #choose flags
    flag |= cv2.CALIB_CB_ADAPTIVE_THRESH
    flag |= cv2.CALIB_CB_FILTER_QUADS

    # Find the chess board corners
    ret_l, corners_l = cv2.findChessboardCorners(gray_l, (9, 6), flags = flag)#None
    ret_r, corners_r = cv2.findChessboardCorners(gray_r, (9, 6), flags = flag)

    # If found, add object points, image points (after refining them)
    if ret_l == True:
        objpoints.append(objp)

        reetl = cv2.cornerSubPix(gray_l, corners_l, (11, 11), (-1, -1), criteria)
        imgpoints_l.append(corners_l)

        # Draw the corners
        ret_l = cv2.drawChessboardCorners(img_l, (9, 6), corners_l, ret_l)

    if ret_r == True:

        reetr = cv2.cornerSubPix(gray_r, corners_r, (11, 11), (-1, -1), criteria)
        imgpoints_r.append(corners_r)

        # Draw the corners
        ret_r = cv2.drawChessboardCorners(img_r, (9, 6), corners_r, ret_r)
    d+=1



rt, mtx_l, dist_l, rvecs_l, tvecs_l = cv2.calibrateCamera(objpoints, imgpoints_l, (w_l, h_l),None,None)
rt, mtx_r, dist_r, rvecs_r, tvecs_r = cv2.calibrateCamera(objpoints, imgpoints_r, (w_r, h_r),None,None)

term_crit = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 1000, 1e-8)

flags = 0
#flags |= cv2.CALIB_FIX_INTRINSIC #1
#flags |= cv2.CALIB_USE_INTRINSIC_GUESS #2
flags |= cv2.CALIB_SAME_FOCAL_LENGTH #3
flags |= cv2.CALIB_ZERO_TANGENT_DIST #4
#flags |= cv2.CALIB_FIX_FOCAL_LENGTH #5
#flags |= cv2.CALIB_FIX_ASPECT_RATIO #6
#flags |= cv2.CALIB_FIX_PRINCIPAL_POINT #7
#flags |= cv2.CALIB_RATIONAL_MODEL #8
flags |= cv2.CALIB_FIX_K1 #9
flags |= cv2.CALIB_FIX_K2 #10
flags |= cv2.CALIB_FIX_K3 #11
#flags |= cv2.CALIB_FIX_K4 #12
#flags |= cv2.CALIB_FIX_K5 #13

#4,6,9,10,11|3,4,6,9,10,11| 3,6,9,10,11 | 3,4,9,10,11**

ret, mtx_ll, dist_ll, mtx_rr, dist_rr, R, T, E, F = cv2.stereoCalibrate(
    objpoints, imgpoints_l,
    imgpoints_r, mtx_l, dist_l, mtx_r,
    dist_r, (w_l, h_l), flags=flags, criteria = term_crit)

R1, R2, P1, P2, Q, validPixROI1, validPixROI2S = cv2.stereoRectify(mtx_ll, dist_ll, mtx_rr, dist_rr, 
    (w_l, h_l), R, T, flags = 0,alpha = 0) #flags = 0 or cv2.CALIB_ZERO_DISPARITY, alpha = 0 always

mapLx, mapLy = cv2.initUndistortRectifyMap(mtx_ll, dist_ll, R1, P1, (w_l, h_l), m1type = cv2.CV_32FC1)
mapRx, mapRy = cv2.initUndistortRectifyMap(mtx_rr, dist_rr, R2, P2, (w_l, h_l), m1type = cv2.CV_32FC1)#CV_16SC2,CV_32FC1

with open('stereocalibfinal.yaml', 'w') as f:
    yaml.dump({'ret':  ret, 'mtx_ll': mtx_ll.tolist(),'dist_ll':  dist_ll.tolist(), 'mtx_rr': mtx_rr.tolist(), 'dist_rr': dist_rr.tolist(),
     'R': R.tolist(), 'T': T.tolist(), 'E': E.tolist(), 'F': F.tolist(), 'w_l': w_l, 'h_l': h_l}, f)
    
with open('stereocalibfinal.yaml') as f:
    loaded = yaml.load(f)
loaded = np.array(loaded)


###yaml for the stereorectify values. use if need but it's super dependant on the stereo calibrate values###
with open('stereorectifyfinal.yaml', 'w') as f:
    yaml.dump({'R1': R1.tolist(), 'R2': R2.tolist(),'P1': P1.tolist(), 'P2': P2.tolist(), 'Q': Q.tolist()}, f) #, 'mapLx': mapLx.tolist(), 'mapLy': mapLy.tolist(), 'mapRx': mapRx.tolist(), 'mapRy': mapRy.tolist()

with open('stereorectifyfinal.yaml') as f:
    loaded = yaml.load(f)
loaded = np.array(loaded)

