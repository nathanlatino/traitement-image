__author__ = 'Lionel'

import cv2
import numpy as np
from numpy.linalg import inv

def getCornersFromCamera(ch,cw):
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	cap = cv2.VideoCapture(0)
	grab = False
	print "Q pour saisir le damier"
	while not grab:
		# Capture frame-by-frame
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret, corners = cv2.findChessboardCorners(gray, (ch, cw), None)
		chess = frame.copy()
		if ret:
			cv2.imwrite("image.png", frame)
			cv2.circle(frame, (corners[0][0][0],corners[0][0][1]), 2, (0,0,255), 4)
			cv2.putText(frame,'(0, 0)', (int(corners[0][0][0]) + 10, int(corners[0][0][1])), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2, cv2.LINE_AA)
			cv2.imwrite("image_origin.png",frame)
			cv2.drawChessboardCorners(chess, (ch, cw), corners, ret)
			cv2.imwrite("image_chess.png", chess)
			cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		cv2.imshow('camera', chess)
		grab = cv2.waitKey(20) & 0xFF == ord('q')
	cap.release()
	return corners

def createTarget(h,w,s):
	target = np.zeros((w * h, 1, 2))
	target[:, :, 0] = np.repeat(np.arange(0, s * w, s), h).reshape((w*h, 1))
	target[:, :, 1] = np.tile(np.arange(0, s * h, s), w).reshape((w*h, 1))
	return target

def getHomographyMatrix(corners, target):
	#Transformation de coordonnees image [pixel] vers coordonnees damier [cm]
	m, mask = cv2.findHomography(corners, target, cv2.RANSAC, 5.0)
	np.savetxt("matrix.txt", m, delimiter=',')
	return m

def testMatrix(M):
	print "Matrice Homographique"
	print M
	# Camera to World
	#----------------
	ptC = np.array([182, 163, 1])
	ptM = M.dot(ptC)
	ptM /= ptM[2]
	print "Camera:", ptC, "[pixel]  -> World:", ptM, "[cm]"

	# World to Camera	
	#----------------
	ptM = np.array([0, 0, 1])
	ptC = inv(M).dot(ptM)
	ptC /= ptC[2]
	print "World:", ptM, "[cm]   -> Camera:", ptC, "[pixel]"
	
	
	

def main():
	# Number of squares in chessboard
	chessW = 5
	chessH = 8
	# Square size
	size = 2
	corners = getCornersFromCamera(chessH, chessW)
	target = createTarget(chessH,chessW,size)
	matrix = getHomographyMatrix(corners, target)
	testMatrix(matrix)

if __name__ == '__main__':
	main()
