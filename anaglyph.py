from PIL import Image, ImageChops, ImageMath
from PIL import ImageOps
from PIL.ImageOps import grayscale
from PIL.ImageOps import colorize

right = Image.open('stereoimage/leftstereoimg.jpg')
left = Image.open('stereoimage/rightstereoimg.jpg')

width, height = right.size
rightMap = right.load()
leftMap = left.load()

right = grayscale(right)
right = colorize(right, (0,0,0),(0,255,255)) #cyan (0,255,255)
#right = colorize(right, (0,0,0),(0,0,255)) #blue (0,0,255)

left = grayscale(left)
left = colorize(left, (0,0,0),(255,0,0)) #red (255,0,0)

'''
#This code for blend
o = ImageChops.add(right,left,2)

o.save("3Dpics/anaglyph.jpg", "JPEG")
'''

#This code for additive blending
list_out = []
list_out1 = []
list_out2 = []
for red, cyan in itertools.izip(list(left.getdata()), list(right.getdata())):
	list_out.append(min(red[0], 255))
	list_out1.append(min(cyan[1], 255))
	list_out2.append(min(cyan[2], 255))

image_out = Image.new(right.mode,left.size)
combo = zip(list_out,list_out1,list_out2)
image_out.putdata(combo)

image_out.save("3Dpics/anaglyph.jpg", "JPEG")