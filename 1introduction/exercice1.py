import cv2

def loadAndDisplayColorImage(imagePath):
	img = cv2.imread(imagePath)
	cv2.imshow(imagePath, img)

def importColorImageAsGray(imagePath):
	img = cv2.imread(imagePath, 0)
	cv2.imshow(imagePath, img)

def importColorImageAndConvert(imagePath):
	img = cv2.imread(imagePath, 0)
	imgOutput = img
	cv2.cvtColor(img, imgOutput, cv2.COLOR_BGR2GRAY)
	cv2.imshow(imagePath, imgOutput)

if __name__ == '__main__':
	loadAndDisplayColorImage("./images/lena.png")
	# importColorImageAsGray("./images/lena.png")
	# importColorImageAndConvert("./images/lena.png")

	while(True):
		if(cv2.waitKey(1) == ord('q')):
			break
	cv2.destroyAllWindows

