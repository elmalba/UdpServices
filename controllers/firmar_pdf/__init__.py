from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj
import os
import shutil
def Firmar_pie_pagina(route):
    input_file = route
    output_file = route.replace("static","static_pdf")
    print input_file

    # Get pages
    reader = PdfReader(input_file)
    pages = [pagexobj(p) for p in reader.pages]


    # Compose new pdf
    canvas = Canvas(output_file)

    for page_num, page in enumerate(pages, start=1):

        # Add page
        canvas.setPageSize((page.BBox[2], page.BBox[3]))
        canvas.doForm(makerl(canvas, page))

        # Draw footer
        footer_text = "Descargado desde https://UdpCursos.com"
        x = 180
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        canvas.drawString(page.BBox[2]-x, 40, footer_text)
        canvas.restoreState()

        canvas.showPage()

    canvas.save()
