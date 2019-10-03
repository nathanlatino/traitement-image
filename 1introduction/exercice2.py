import cv2
import numpy as np

def splitImageOpenCV(image):
	b,g,r = cv2.split(image)
	printRGB(r,g,b)




def displaySplitImageNumpy(image):
	b = image[:, :, 0]
	g = image[:, :, 1]
	r = image[:, :, 2]
	printRGB(r,g,b)

def printRGB(r,g,b):
	print("Red :\n", r)
	print("Green :\n", g)
	print("Blue :\n", b)


if __name__ == '__main__':
	img = cv2.imread("./images/lena.png")

	# splitImageOpenCV(img)
	displaySplitImageNumpy(img)
