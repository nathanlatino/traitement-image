import cv2
import numpy as np
from matplotlib import pyplot as plt


def gray_image(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def hist_gray(img):
	plt.hist(gray_image(img).ravel(), 256, [0, 256])
	plt.title('Histogram for gray scale image')
	plt.show()

def hist_color(img):
	color = ('b','g','r')
	for i,col in enumerate(color):
		histr = cv2.calcHist([img],[i],None,[256],[0,256])
		plt.plot(histr,color = col)
		plt.xlim([0,256])
	plt.show()


if __name__ == '__main__':
    img = cv2.imread("./lena.png")
    if img is not None:
        hist_gray(img)
        hist_color(img)
    else:
        print("error img")
