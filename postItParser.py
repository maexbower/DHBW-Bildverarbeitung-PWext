#!/usr/bin/python3
# coding=UTF8
#from PIL import Image

import cv2
import math
import numpy as np
from PIL import Image

class Parser:
    """
        Uses opencv to import and parse images. It can find and cut out postits with configured colors
    """

    def __init__(self):
        self._images = []
        self._resultImages = []
        self.lower_bound = (0,80,20)
        self.upper_bound = (0, 255, 255)
        self._colorTable = {'yellow': 25, 'pink': 170, 'blue': 100, 'orange': 15, 'green': 40 }
        self._devider = 5
        self.frame = None
        self.mask = None
        # Tolleranz
        self.filterrange=7


    def importImage(self, path):
        """
            importImage(path : string) -> void
            
            takes the path to an image and imports it to the Parser Class
        """

        try:
            _img = cv2.imread(path)
            # catch file not found problem
            if _img is None:
                print('Image not Found')
                return
            self._images.append(_img)
        except BaseException as e:
            print('Failed to load Image ', path, 'with error: ', e)

    def setImages(self, images):
        """
            setImages(images : List of opencvImage) -> void
            
            Takes a already created List of openCV Images and sets them as Source Images
        """
        self._images = images
        
    def sethsvfilter(self,colour):
        """
            sethsvfilter(colour : Color object with HSV values) -> void
            
            Sets the upper and lower bound of the color filter acording the given HSV values.
        """
        hsv = colour
        self.lower_bound = ((hsv[0]-self.filterrange),100,100)
        self.upper_bound = ((hsv[0]+self.filterrange),255,255)
        
    def setfilter(self,colour):
        """
            setfilter(colour : Color object with BGR values) -> void
            
            Sets the upper and lower bound of the color filter acording the given BGR values.
        """
        hsv = cv2.cvtColor(colour, cv2.COLOR_BGR2HSV)
        self.sethsvfilter(hsv)
		
    def filtercolor(self):
        """
            filtercolor() -> void
            
            resizes the current frame by self._devider, add a blur and filter for the current color (upper and lower bound). Then find contours in the result. 
        """
        # Skaliere Bild zur schnelleren Verarbeiten
        _smallImg = cv2.resize(self.frame, (0,0), fx=(1 / self._devider) ,fy=(1 / self._devider)) 
        hsv = cv2.cvtColor(_smallImg, cv2.COLOR_BGR2HSV)
        # Leichte unschärfe verhindert das Erkennen von Details
        hsv = cv2.medianBlur(hsv, 15)
        # Erstelle Maske auf Basis der definierten Grenzfarben
        self.mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
        self.mask = cv2.resize(self.mask, (0,0), fx=(self._devider) ,fy=(self._devider)) 
        # Erkenne die Konturen der Maske
        # im2 .. eingebenes Bild mit Konturen (in dem Fall die Maske)
        # self.contours .. Array mit den Konturen
        # hierachy .. Baumstruktur der Konturen. Innere Konturen sind Äußeren untergeordnet (z.B. die Kontur der Schrift ist auf einer niedrigeren Ebene als das Postit)
        im2, self.contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Der gesammte Baum ist im ersten Element von hierachy
        if hierarchy is not None:
            self.hierarchy=hierarchy[0]
        else:
            self.hierarchy = None
		
    def processtree(self, nodeindexnumber):
        """
            processtree(nodeindexnumber : int) -> void
            
            go through the contour hierachy 
        """
        #durchläuft effizient den Konturen Baum
        if self.hierarchy is None:
            return
        cnt = self.contours[nodeindexnumber]
        nodemetadata = self.hierarchy[nodeindexnumber]
        signvalue = self.processcontour(cnt)
        if( nodemetadata[0] != (-1) ):	#weitere Konturen sind auf der Ebene Vorhanden
            self.processtree(nodemetadata[0])
			
    def processcontour(self,cnt):
        """
            processcontour(cnt : opencv contour) -> void
            
            if the contour has enough edges and is big enough use the mask and and cut out the contour from the original image.
            It then is saved in the self._resultImages array
        """
        numberofedges = len(cnt)
        # Rechne ein Rechteck um die Konturen
        x,y,w,h = cv2.boundingRect(cnt)
        # kleine Ergebnisse ausfiltern
        if(numberofedges > 3 and (w > 20 * self._devider) and (h > 20 * self._devider)):
            # erstelle Maske und fülle diese mit 0 Werten um bei Bitwise_and auszuschneiden
            mask = np.full((self.frame.shape[0], self.frame.shape[1]), 0, dtype=np.uint8)
            cv2.fillPoly(mask, pts=cnt, color=0)
            # Maske und Bild Zuschneiden um die nächsten Operationen nur auf dem Bildauschnitt zu rechnen
            partImg = self.frame[y:y+h, x:x+w]
            partMask = self.mask[y:y+h, x:x+w]
            # Erstelle weißes Bild um den schwarzen Rahmen zu ersetzen
            white = np.zeros((partImg.shape[0],partImg.shape[1], 3 ), np.uint8)
            white[:,:] = (255,255,255)
            # Erstelle die Maske für den Rand (invertierte Ausschnittsmaske)
            white_mask = cv2.bitwise_not(partMask)
            white_img = cv2.bitwise_and(white, white, mask=white_mask)
            # Schneide Bildausschnitt zu
            ret = cv2.bitwise_and(partImg, partImg, mask=partMask)
            # Überlagere den Bildausschnitt mit der weißen Maske mit voller Deckung bei Schwarz und keine bei allem anderen
            fixed_img = cv2.addWeighted(ret, 1, white_img, 1, 1)
            # Debug anzeige der Zwischenbilder
            #cv2.imshow("ret", fixed_img) #debug
            #cv2.waitKey(0)
            self._resultImages.append(fixed_img)
		
    def processImages(self, startNum=0):
        """
            processImages(startNum=0 : int) -> void
            
            go through the self._images array with the optional given startNum as the first element in the array and search for all configured colors.
        """
        print('processing Images')
        for _img in self._images[startNum:]:
            for index in self._colorTable:
                print('suche Farbe:', index, ' (', self._colorTable[index], ')')
                self.sethsvfilter([self._colorTable[index],0,0])
                self.frame=_img
                self.filtercolor()
                self.processtree(0)

    def getmask(self):
        """
            getmask() -> Array openCV Mask

            returns self.mask
        """
        return(self.mask)
             
    def getResult(self,  startNum=0):
        """
            getResult(startNum=0 : int) -> Array openCV Images

            returns self._resultImages[startNum:]
        """
        return self._resultImages[startNum:]
    def getPILResult(self, startNum=0):
        """
            getPILResult(startNum=0 : int) -> Array PIL Images

            convert all result images into PIL objects and return the list of converted image objects
        """
        # You may need to convert the color.
        _results = []
        for _img in self._resultImages[startNum:]:
            _tmpImg = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
            _results.append(Image.fromarray(_tmpImg))
        return _results