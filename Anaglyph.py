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

left = grayscale(left)
left = colorize(left, (0,0,0),(255,0,0)) #red (255,0,0)

o = ImageChops.add(right,left,2)

o.save("3Dpics/anaglyph.jpg", "JPEG")

