#!/usr/bin/python3
# coding=UTF8
# this tool requires the following packages
# reportlab
# pil
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from PIL import Image

class PDFgenerator:
    _outputfile = 'o.pdf'
    _pageformat = A4
    _canvas = None
    _font = 'Helvetica'
    _fontsize = 14
    _width, _height = A4
    _padding = { 'left': 2*cm, 'right': 1.5*cm, 'top': 1.5*cm, 'bottom': 1.5*cm}
    _innerWidth = _width - _padding['left'] - _padding['right']
    _innerHeight = _height - _padding['top'] - _padding['bottom']
    def __init__(self, outputfile = None):
        if outputfile is not None:
            self.setOutput(outputfile)
    def setOutput(self, path):
        if self._canvas is not None:
            print('DEBUG: Pfad kann nach beginn des Erstellens nicht geändert werden')
            return 1
        self._outputfile = path
    def createFile(self):
        self._canvas = Canvas(self._outputfile, pagesize=self._pageformat)
    def saveFile(self):
        self._canvas.save()
        self._canvas = None
    def insertNewPage(self):
        self._canvas.showPage()
    def insertImage(self, image, x = None, y = None, width = None, height = None, keepAspectRatio=True):
        im_width, im_height = image.size
        _width = width
        _height = height
        _x = x
        _y = y
        _keepAspectRatio = keepAspectRatio
        if width is None:
            if im_width >= self._innerWidth :
                _width = self._innerWidth
            else:
                _width = im_width
        if height is None:
            if im_height >= self._innerHeight:
                _height = self._innerHeight
            else:
                _height = im_height
        if x is None:
            _x = self._padding['left']
        if y is None:
            _y = self._padding['bottom']
        try:
            self._canvas.drawInlineImage(image ,x=_x, y=_y, width=_width, height=_height,  preserveAspectRatio=_keepAspectRatio, anchor='c')
            self.insertNewPage()
        except BaseException as e:
            print(image)
            print('failed to process Image', e)
    def insertText(self, x, y, string, fontsize=_fontsize, fontname=_font):
        print('fontsize:', fontsize)
        print('fontname:', fontname)
        self._canvas.setFont(fontname, fontsize)
        self._canvas.drawString(x, y, string)
    def getOutputFile(self):
        return self._outputfile
    def getPadding(self):
        return self._padding