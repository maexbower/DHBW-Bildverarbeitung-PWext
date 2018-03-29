#!/usr/bin/python3
# coding=UTF8
#from PIL import Image

import cv2
import math
import numpy as np
from PIL import Image

class Parser:
    def __init__(self):
        self._images = []
        self._resultImages = []
        self.lower_bound = (0,80,20)
        self.upper_bound = (0, 255, 255)
        self.frame=None
        self.mask=None
        self.filterrange=7
    def importImage(self, path):
        try:
            self._images.append(cv2.imread(path))
        except BaseException as e:
            print('Failed to load Image ', file, 'with error: ', e)
    def setImages(self, images):
        self._images = images
        
    def sethsvfilter(self,colour):
        hsv = colour
        self.lower_bound = ((hsv[0]-self.filterrange),100,100)
        self.upper_bound = ((hsv[0]+self.filterrange),255,255)
        
    def setfilter(self,colour):
        hsv = cv2.cvtColor(colour, cv2.COLOR_BGR2HSV)
        self.lower_bound[0] = (hsv[0]-self.filterrange)
        self.upper_bound[0] = (hsv[0]+self.filterrange)
		
    def filtercolor(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        hsv=cv2.medianBlur(hsv,15)
        #cv2.imshow("hsv", hsv) #debug
        #cv2.waitKey(0)
        self.mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
        #cv2.imshow("mask", self.mask) #debug
        #cv2.waitKey(0)
        im2, self.contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.hierarchy=hierarchy[0]	
		
    def processtree(self, nodeindexnumber):
        #durchläuft effizient den Konturen Baum
        cnt=self.contours[nodeindexnumber]
        nodemetadata=self.hierarchy[nodeindexnumber]
        signvalue= self.processcontour(cnt)
        if(nodemetadata[0]!=(-1)):	#weitere Konturen sind auf der Ebene Vorhanden
            self.processtree(nodemetadata[0])
			
    def processcontour(self,cnt):
        numberofedges = len(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        if(numberofedges>3 and (w >20) and (h>20)):
            mask = np.full((self.frame.shape[0], self.frame.shape[1]), 0, dtype=np.uint8)#create empty mask
            cv2.fillPoly(mask, pts =cnt, color=(0))
            res = cv2.bitwise_and(self.frame,self.frame,mask= self.mask)
            x,y,w,h = cv2.boundingRect(cnt)
            ret=res[y:y+h, x:x+w]
            #cv2.imshow("ret", ret) #debug
            #cv2.waitKey(0)
            self._resultImages.append(ret)
		
    def processImages(self):
        # if the main programm wants to start processing again
        # please make this blocking
        print('processing Images')
        for _img in self._images:
            self.frame=_img
            self.filtercolor()
            self.processtree(0)
        #print('Image Count: ', str(len(self._resultImages)))

    def getmask(self):
        return(self.mask)
             
    def getResult(self):
        # keep source Images maybe?
        return self._resultImages
    def getPILResult(self):
        # You may need to convert the color.
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _results = []
        for _img in self._resultImages:
            _tmpImg = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
            _results.append(Image.fromarray(_tmpImg))
        return _results