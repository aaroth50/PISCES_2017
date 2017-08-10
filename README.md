# Stereo_Cameras_PISCES

Code from my 2017 summer internship at PISCES used to calibrate, rectify, and create 3D anaglyph images out of stereo images.

## Dependencies

* OpenCV 3.  
* numpy  
* PyYaml  
* PIL

## Description

*stereo_calib_yaml.py*: Takes in stereo images of checkerboard patterns labeled Left_ and Right_ and creates yaml files of the stereo calibration matrices and stereo rectify matrices.

*map_yaml.py*: Uses the yaml files of the stereo calibration matrices and the stereo rectify matrices to map out calibrated and rectified stereo images in a folder with images labeled Left_ and Right_

*horizontal_line.py*: Blends two images together and adds green horizontal lines. I use this to see if my stereo images rectified correctly.

*anaglyph.py*: Takes in a stereo image pair and converts to a single anaglyph image.

## Images

![20170802_203906](https://user-images.githubusercontent.com/24604807/29108854-650d3be8-7c7c-11e7-83ee-511f8c68f2f6.jpg)  
*PISCES's Helelani Rover taking a stereo picture of a stack of rocks on Mauna Kea. The orange mount on the top left of the rover holds the stereoscopic cameras.*


![stackedrock2s-1500exp](https://user-images.githubusercontent.com/24604807/29108594-6358aa04-7c7b-11e7-9238-3d71a338464c.png)  
*Anaglyph image of the stack of rocks shown in the previous image*


![grass](https://user-images.githubusercontent.com/24604807/29108676-b283e580-7c7b-11e7-96f7-6435110c4d50.png)  
*Anaglyph image of some plants growing on the mountain*
