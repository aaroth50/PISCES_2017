import glob
import cv2
import numpy as np
import glob
import os
import yaml

with open("stereocalibfinal.yaml", 'r') as stream:    
    try:
        ster = yaml.load(stream)
        
    except yaml.YAMLError as exc:
mtx_ll = np.asarray(ster['mtx_ll'])
dist_ll = np.asarray(ster['dist_ll'])
mtx_rr = np.asarray(ster['mtx_rr'])
dist_rr = np.asarray(ster['dist_rr'])
w_l = ster['w_l']
h_l = ster['h_l']

with open("stereorectifyfinal.yaml", 'r') as stream:
    try:
        rect = yaml.load(stream)
        
    except yaml.YAMLError as exc:
R1 = np.asarray(rect['R1'])
P1 = np.asarray(rect['P1'])
R2 = np.asarray(rect['R2'])
P2 = np.asarray(rect['P2'])

mapLx, mapLy = cv2.initUndistortRectifyMap(mtx_ll, dist_ll, R1, P1, (w_l, h_l), m1type = cv2.CV_32FC1)
mapRx, mapRy = cv2.initUndistortRectifyMap(mtx_rr, dist_rr, R2, P2, (w_l, h_l), m1type = cv2.CV_32FC1)#CV_16SC2,CV_32FC1

imgl = cv2.imread('uncalibstereoimage/leftuncalibimg.jpg') #put file location of single stereo pair
imgr = cv2.imread('uncalibstereoimage/rightuncalibimg.jpg')

finall = cv2.remap(imgl, mapLx, mapLy,interpolation = cv2.INTER_LINEAR)
finalr = cv2.remap(imgr, mapRx, mapRy,interpolation = cv2.INTER_LINEAR)

cv2.imshow('imgfinall',finall)
cv2.waitKey(0)
cv2.imshow('imgfinal',finalr)
cv2.waitKey(0)

cv2.imwrite(os.path.join('stereoimage', 'leftstereoimg.jpg'), finall) #file location of remapped stereo pair
cv2.imwrite(os.path.join('stereoimage', 'rightstereoimg.jpg'), finalr)

#Use this code for a bulk of uncalibrated stereo images
''' 

for i in range(len(os.listdir('uncalibimagebulk'))/2): #parallel or sixfiftycmaway
    imgl = cv2.imread('uncalibimagebulk/left_%02d.jpg'%i)
    imgr = cv2.imread('uncalibimagebulk/right_%02d.jpg'%i)

    finall = cv2.remap(imgl, mapLx, mapLy,interpolation = cv2.INTER_LINEAR)
    finalr = cv2.remap(imgr, mapRx, mapRy,interpolation = cv2.INTER_LINEAR)
    #testl = cv2.undistortPoints(imgl, mtx_l, dist_l, R1, P1)
    #testr = cv2.undistortPoints(imgr, mtx_r, dist_r, R2, P2)

    cv2.imshow('imgfinall',finall)
    cv2.waitKey(0)
    cv2.imshow('imgfinal',finalr)
    cv2.waitKey(0)

    cv2.imwrite(os.path.join('stereoimagebulk', 'left_%02d.jpg'%i), finall)
    cv2.imwrite(os.path.join('stereoimagebulk', 'right_%02d.jpg'%i), finalr)

'''
