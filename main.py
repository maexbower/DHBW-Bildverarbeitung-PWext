import cv2
import math
import numpy as np
from postItParser import Parser
from getcolor import getcolor

i=0
while(i<7):
	string1="Bilder/"+str(i)+".jpg"
	frame = cv2.imread(string1)
	divider=6
	frame = cv2.resize(frame, (0,0), fx=(1/divider), fy=(1/divider))	#verkleinern des Bildes	
	cv2.imshow("in-frame", frame) #debug
	#cv2.waitKey(0)
	
	pl=Parser(frame)
	pl.sethsvfilter([35,0,0])
	pl.processImages()
	#getcolor(frame)
	#for erg in pl.getResult():
	#	cv2.imshow("erg", erg) #debug
	#	cv2.waitKey(0)
	i=i+1

