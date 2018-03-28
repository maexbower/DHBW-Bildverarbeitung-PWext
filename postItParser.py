from PIL import Image
class Parser:
    _images = []
    _resultImages = []
    def __init__(self, images):
        self._images = images
    def setImages(self, images):
        self._images = images
    def processImages(self):
        # if the main programm wants to start processing again
        # please make this blocking
        self._resultImages = self._images
        print('processing Images')
        print('Image Count: ', str(len(self._resultImages)))
    def getResult(self):
        # keep source Images maybe?
        return self._resultImages