import cv2
import numpy as np
from scipy import stats

def show_information(img):
	w, h, c = img.shape
	print("size:", w, "X", h)
	print("type:", type(img))
	print("cannals:", c)
	print("min value:", np.min(img))
	print("max value:", np.max(img))
	print("average value:", np.average(img))
	print("ecart-type:", np.nanstd(img))
	print("mode:", stats.mode(img, axis=None)[0])


if __name__ == '__main__':
	img = cv2.imread("./baboon.png")
	if img is not None:
		show_information(img)
	else:
		print("error img")

