from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj
import os
import shutil




def file_x(route):
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

def check_folder(route):

    folders= os.listdir(route)
    export={}
    export['folders']={}
    export['files']=[]
    for files in folders:
        sub_folder = "/"+files
        if os.path.isdir(route+sub_folder):
            new=route
            new=new.replace("static","static_pdf")
            os.makedirs(new+sub_folder)
            export['folders'][files]=check_folder(route+sub_folder)

        else:
            try:
                extend = files.split(".")
                extend = extend[len(extend)-1]
                if extend =="pdf":
                    file_x(route+"/"+files)
                    export['files'].append(files)
                else:
                    shutil.copy2(route+"/"+files,route.replace("static","static_new")+"/"+files)
            except:
                pass
    return export



print check_folder(os.getcwd()+"/"+'static')