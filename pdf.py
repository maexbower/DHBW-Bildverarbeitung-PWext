#!/usr/bin/python3
# this tool requires the following packages
# reportlab
# pil
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from PIL import Image
import sys, getopt
from postItParser import Parser

def main(argv):
    outputfile = 'test.pdf'
    images = []
    try:
        opts, rest = getopt.getopt(argv,"ho:",["help","ofile="])
    except getopt.GetoptError:
        print('pdf.py -o <outputfile.pdf> file1 [file2] (Using of * in Filenames is possible)...')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('pdf.py -o <outputfile.pdf> file1 [file2] (Using of * in Filenames is possible)...')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Output file is "', outputfile)
    for file in rest:
        try:
            images.append(Image.open(file))
        except BaseException:
            print('Failed to open Image ', file)
    for index, item in enumerate(images):
        images[index] = item.rotate(-90, resample=0, expand=1)
    parser = Parser(images)
    parser.processImages()
    resultImages = parser.getResult()

    pdf = Canvas(outputfile, pagesize=A4)
    width, height = A4
    padding = { 'left': 2*cm, 'right': 1.5*cm, 'top': 1.5*cm, 'bottom': 1.5*cm}
    innerWidth = width - padding['left'] - padding['right']
    innerHeight = height-padding['top']-padding['bottom']
    # move the origin up and to the left
    pdf.translate(padding['left'],padding['bottom'])
    # define a large font
    pdf.setFont("Helvetica", 14)
    # choose some colors
    pdf.setStrokeColorRGB(0.2,0.5,0.3)
    pdf.setFillColorRGB(1,0,1)
    # draw border lines
    pdf.line(0,0,0,innerHeight)
    pdf.line(innerWidth ,0, innerWidth , innerHeight)
    pdf.line(0,0,innerWidth,0)
    pdf.line(0 ,innerHeight, innerWidth , innerHeight)
    # draw a rectangle
    pdf.rect(0.2*cm,0.2*cm,1*cm,1.5*cm, fill=1)
    # make text go straight up
    pdf.rotate(90)
    # change color
    pdf.setFillColorRGB(0,0,0.77)
    # say hello (note after rotate the y coord needs to be negative!)
    pdf.drawString(0.3*cm, -cm, "Hello World")
    pdf.showPage()
    #print(format(images[0]))
    #pdf.drawInlineImage(origImage ,x=padding['left'], y=padding['bottom'], width=innerWidth, height=innerHeight,  preserveAspectRatio=True, anchor='c')
    #pdf.showPage()
    for index, item in enumerate(resultImages):
        print(type(item))
        try:
            pdf.drawInlineImage(item ,x=padding['left'], y=padding['bottom'], width=innerWidth, height=innerHeight,  preserveAspectRatio=True, anchor='c')
        except AttributeError:
            print('failed to process Image', format(item))
        pdf.showPage()
    pdf.save()




if __name__ == "__main__":
   main(sys.argv[1:])