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
    """
        Uses opencv to import and parse images. It can find and cut out postits with configured colors
    """
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
        """
            __init__(outputfile : string) -> void
            
            inits class. Sets output File when given as parameter.
        """
        if outputfile is not None:
            self.setOutput(outputfile)
    def setOutput(self, path):
        """
            setOutput(path : string) -> void
            
            sets output path of generated PDF. Can only be done if canvas hasn't been instaciated yet.
            If it fails it returns without changing
        """
        if self._canvas is not None:
            print('DEBUG: Pfad kann nach beginn des Erstellens nicht geändert werden')
            return
        self._outputfile = path
    def createFile(self):
        """
            createFile() -> void
            
            instanciate canvas object
        """
        self._canvas = Canvas(self._outputfile, pagesize=self._pageformat)
    def saveFile(self):
        """
            saveFile() -> void
            
            save PDF file and end editing
        """
        self._canvas.save()
        self._canvas = None
    def insertNewPage(self):
        """
            insertNewPage() -> void
            
            add page break
        """
        self._canvas.showPage()
    def insertImage(self, image, x = None, y = None, width = None, height = None, keepAspectRatio=True):
        """
            insertImage(self, image : PIL Object, x : int, y : int, width : int, height : int, keepAspectRatio : bool) -> void
            
            insert image with the given params. If no param is set it will use the original PIL object size and/or fit it to the page size.
        """
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
        """
            insertText(self, x : int, y : int, string : str, fontsize : int, fontname : str) -> void
            
            ad text with the given param. If no param is set it will use standard valued (size 12 and Helvetica)
        """
        print('fontsize:', fontsize)
        print('fontname:', fontname)
        self._canvas.setFont(fontname, fontsize)
        self._canvas.drawString(x, y, string)
    def getOutputFile(self):
        """
            getOutputFile() -> str
            
            return the output file path
        """
        return self._outputfile
    def getPadding(self):
        """
            getPadding() -> int[]
            
            return the array which contains the page padding
        """
        return self._padding