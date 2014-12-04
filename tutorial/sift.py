import cv2
import urllib2
import numpy as np


url = "http://img11.360buyimg.com/n1/g13/M09/0B/05/rBEhVFIxaGkIAAAAAAGEV0SZGCMAADEsQOGrOkAAYRv640.jpg"

req = urllib2.urlopen(url)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT()
kp, desc = sift.detectAndCompute(gray, None)
print len(desc), len(desc[0])
img = cv2.drawKeypoints(gray, kp)

#cv2.imwrite('sift_keypoints.jpg', img)