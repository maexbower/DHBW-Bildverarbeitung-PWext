#!/usr/bin/python3
# coding=UTF8

import cv2
import math
import numpy as np
from postItParser import Parser
from getcolor import getcolor
from pdf import PDFgenerator
import sys, getopt


def main(argv):
	_images = []
	_resultImages = []
	_pdfGen = PDFgenerator()
	_parser = Parser()
	# parse Program Params
	try:
		print('Read Args: ', argv)
		opts, rest = getopt.getopt(argv, "ho:",["help","ofile="])
	except getopt.GetoptError:
		print('main.py -o <outputfile.pdf> file1 [file2] (Using of * in Filenames is possible)...')
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print('main.py -o <outputfile.pdf> file1 [file2] (Using of * in Filenames is possible)...')
			sys.exit()
		elif opt in ("-o", "--ofile"):
			_pdfGen.setOutput(arg)
	print('Output file is "', str(_pdfGen.getOutputFile()))
	print('Reading Images...')
	for file in rest:
		print('reading ', file)
		_parser.importImage(file)
	#for index, item in enumerate(images):
	#	images[index] = item.rotate(-90, resample=0, expand=1)
	_parser.sethsvfilter([35,0,0])
	_parser.processImages()
	_resultImages = _parser.getPILResult()
	print('Found ', str(len(_resultImages)), 'Elements')
	_pdfGen.createFile()
	#_pdfGen.insertText(30,200,'PostItScanner',fontsize=24)
	_pdfGen.insertNewPage()
	for _image in _resultImages:
		_pdfGen.insertImage(_image)
	_pdfGen.saveFile()

if __name__ == "__main__":
   main(sys.argv[1:])


""" i=0
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
	i=i+1 """

