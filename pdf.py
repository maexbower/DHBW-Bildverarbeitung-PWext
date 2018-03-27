# this tool requires the following packages
# reportlab
# pil
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
pdf = Canvas('test.pdf')
pdf.setFont('Courier', 12)
pdf.setStrokeColorRGB(1, 0, 0)
pdf.drawString(300, 300, 'CLASSIFIED')
pdf.showPage()
pdf.drawImage('./Bilder/20180302_083050.jpg', 1, 300)
pdf.showPage()
pdf.save()