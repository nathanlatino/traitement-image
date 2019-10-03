'''
Created on 30 oct. 2014

@author: Lionel
'''

import cv2
import numpy as np

# Number of scare in chessboard
chessW = 6
chessH = 9

# Number of image needed
nbimg = 10

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessW*chessH,3), np.float32)
objp[:,:2] = np.mgrid[0:chessH,0:chessW].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

newcameramtx = None
mtx = None
dist = None
calibrated = False
mapx = None
mapy = None

def findChess(img):
    global calibrated
    global mapx
    global mapy
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (chessH,chessW),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        
        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)
    if len(imgpoints) == nbimg:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        h,  w = img.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
        calibrated = True
        print "Calibration Ok"
        print "-------------------------------------------------"
        print "mtx : ", mtx
        print "dist : ",dist
        np.savetxt("mtx.txt", mtx, delimiter=',')
        np.savetxt("dist.txt", dist, delimiter=',')
        np.savetxt("rvecs.txt", rvecs, delimiter=',')
        np.savetxt("tvecs.txt", tvecs, delimiter=',')
    
    return ret, corners

def readCamera():
    cap = cv2.VideoCapture(0)
    global calibrated
    global mapx
    global mapy
    waitTime = 1000
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Display the resulting frame
        if calibrated == True:
            waitTime = 1
            dst = cv2.remap(frame,mapx,mapy,cv2.INTER_LINEAR)
            cv2.imshow('camera',dst)
        else:
            ret, corners = findChess(frame)
            if ret == True:
                cv2.drawChessboardCorners(frame, (chessH,chessW), corners,ret)
            cv2.imshow('camera',frame)
        
        if cv2.waitKey(waitTime) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    readCamera()