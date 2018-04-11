#!/usr/bin/python3
# coding=UTF8

import cv2
from postItParser import Parser
from pdf import PDFgenerator
import sys, getopt


def main(argv):
	_images = []
	_resultImages = []
	_parsedImages = 0
	_parsedResults = 0
	_pdfGen = PDFgenerator()
	_parser = Parser()
	# parse Program Params exit if not all params were given
	if len(argv) <= 1:
		print('main.py -o <outputfile.pdf> file1 [file2] (Using of * in Filenames is possible)...')
		sys.exit(2)
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
	# Erstelle PDF Dateo
	_pdfGen.createFile()
	_pdfGen.insertText((_pdfGen._width - _pdfGen._innerWidth), (_pdfGen._innerHeight / 2),'PostItScanner',fontsize=24)
	_pdfGen.insertNewPage()
	# Verarbeite jede Datei in den restlichen Parametern
	for file in rest:
		print('reading ', file)
		# Importiere Bild in die Parser Klasse
		_parser.importImage(file)
		# Verarbeite das aktuelle Bild
		_parser.processImages(startNum=_parsedImages)
		_parsedImages += 1
		# hole alle Elemente, die beim verarbeiten entstanden sind
		_resultImages = _parser.getPILResult(startNum=_parsedResults)
		print('Found ', str(len(_resultImages)), 'Elements')
		_parsedResults += len(_resultImages)
		if( len(_resultImages) >= 1):
			# Für jedes input Bild wird einer PDF Abschnitt erstellt.
			_pdfGen.insertText( (_pdfGen._width - _pdfGen._innerWidth), (_pdfGen._innerHeight / 2), "Ausschnitte aus " + file, fontsize=24)
			_pdfGen.insertNewPage()
			for _image in _resultImages:
				_pdfGen.insertImage(_image)
	_pdfGen.saveFile()

if __name__ == "__main__":
   main(sys.argv[1:])