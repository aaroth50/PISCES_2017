import cv2
from PIL import Image, ImageChops, ImageMath
from PIL.ImageOps import grayscale, colorize
from PIL import ImageOps

right = Image.open('stereoimage/right.jpg') #file location of rectified stereo image
left = Image.open('stereoimage/left.jpg')
width, height = right.size
rightMap = right.load()
leftMap = left.load()

o = Image.blend(right,left,0.5)

o.save("horizontal/horizontallines.jpg", "JPEG") #file location of image to see if images are horizontally aligned

w, h = 1, 0

images = 'horizontal/horizontallines.jpg'

img = cv2.imread(images)

h, w = img.shape[:2]

spacing = h/12

for x in range(1,13):
	cv2.line(img,(0,(x*spacing)),((w-1),(x*spacing)),(0,255,0), 2)
cv2.imwrite('horizontal/horizontallines.jpg', img)
