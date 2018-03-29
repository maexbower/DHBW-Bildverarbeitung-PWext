#!/usr/bin/python3
# coding=UTF8

import cv2
import numpy as np
def getcolor(frame):
	x, y, w, h = 10, 10, 10, 20
	val=10
	
	while(True):
		image = np.zeros((100,500,3), np.uint8)
		pic = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		#pic = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
		# zeichne Rechteck in Bild
		cv2.rectangle(pic, (x, y), (x+w, y+h), (255, 255, 255), thickness=1)
		  # gebe Hue-Wert an der linken oberen Ecke der ROI aus, um Farbwerte des Tennis balls zu ermitteln:
		#hsvw=pic[y:y+1,x:x+1]#cv.Get2D(pic,y+1,x+1)#read hsv value
		#ausg="HSV: "+str(hsvw[0])+" "+str(hsvw[1])+" "+str(hsvw[2])
		
		cv2.putText(image, "{0}".format(pic[y+1, x+1]),(0,50),cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=1)
		
		cv2.imshow("frame", pic)#hsv bild
		cv2.imshow("framec", image)
		key = cv2.waitKey(0)
		
		
		if(key ==ord('d')):
			x=x+val
		elif(key ==ord('a')):
			x=x-val
		elif(key ==ord('s')):
			y=y+val
		elif(key ==ord('w')):
			y=y-val
		elif(key ==ord('q')):
			if(val==10):
				val=1
			else:
				val=10
		else:
			break
	return		
			
	

"""
i=0
while(i<7):
	string1="schilder/vkz"+str(i)+".png"
	frame = cv2.imread(string1)
	getcolor(frame)
	i=i+1

"""
