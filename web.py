#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.crypto import *

def getKey(custom):
    return custom['bloque']


def update_user():
    error=[]
    Xalum=Alumnos.query.filter().all()
    print len(Xalum)
    for alumno in Xalum:
        print alumno.rut
        if True:

            alumno.sufragar={'Votaciones_1':{'habilitado':True,'time':None,'code':None}}
            insert_server_vote(alumno)
            alumno.save()
            print "Guardado"

        try:
            pass
        except:
            error.append(alumno.rut)
            pass
    return error

import requests
def insert_server():

    Xalum=Alumnos.query.filter().all()

    for alumno in Xalum:
        insert_server_vote(alumno)


import threading
def hilo(alumno):
    threads = list()
    t = threading.Thread(target=insert_server_vote, args=(alumno,))
    threads.append(t)
    t.start()
    return

def insert_server_vote(alumno):
        url = "https://votes.udpcursos.com/Register_udpCursos"
        #url = "http://server.udpsalas.cl/Register_udpCursos"

        payload = "hash_id="+str(alumno.mongo_id)+"&token="+str(enconde_token(alumno.rut,alumno.passwd))
        headers = {
        'cache-control': "no-cache",
        'postman-token': "3f90201b-fdbb-42a2-8a60-cc5b059256e2",
        'content-type': "application/x-www-form-urlencoded"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)




@app.route('/Cursos.js', methods=['GET'])
def Curso_js():
    CURXX=[]
    for curso in  Cursos.query.filter({"salas" : { '$elemMatch': { "dia" : DIA } } }).all():
        CURXX=CURXX+curso.arr(DIA)
    CURXX=sorted(CURXX,key=getKey)
    js = render_template("cursos.js", cursos=CURXX,version=VERSION)
    #js = minify(js, mangle=True, mangle_toplevel=True)
    return js
@app.route("/Materia_fdi.js")
def material_fdi():
    import urllib2
    from BeautifulSoup import BeautifulSoup
    def check_folder(domain,url):

        page = urllib2.urlopen(domain+url).read()
        soup = BeautifulSoup(page)
        files = soup.findAll("td",{'class':'fb-n'})
        export={}
        export['folders']={}
        export['files']=[]
        for ixx in range(1,len(files)):
            file=files[ixx].find("a")
            largo= len(file['href'])
            ultimaletra=file['href'][largo-1]

            if ultimaletra=="/":
                print file['href']
                export['folders'][file.getText()]=check_folder(domain,file['href'])
            else:
                export['files'].append(file.getText())
            
            
        return export
    Material={}
    return jsonify(Material_fid=Material)


@app.route("/Cursos_biblioteca.js")
def Cursos_biblioteca():

    BCursos=Cursos.query.all()
    arrx={}
    for b in BCursos:
        codigo=b.codigo.split("-")[0]
        if codigo not in arrx.keys():
            arrx[codigo]=b.curso
    return jsonify(cursos=arrx)



@app.route("/Eventos.js")
def Eventos():
    Evento={}
    Eventos=[]
    Evento['fecha']="07/06/2016"
    Evento['sala']="FDI 101"
    Evento['bloque']="B"
    Evento['curso']="Estática"
    Evento['cursos']=[]
    Evento['profesor']="Daniela Rojas"
    Evento['tipo']="Ayudantia"
    output=[]
    for evento in Evento['cursos']:
        for curso in  Cursos.query.filter({'codigo':{ '$regex': evento} }).all():
            output.append(curso.mongo_id)

    Evento['output']=output

    Eventos.append(Evento)

    Evento={}
    Evento['fecha']="07/06/2016"
    Evento['sala']="FDI 101"
    Evento['bloque']="C"
    Evento['curso']="Simulación"
    Evento['cursos']=[]
    Evento['profesor']="Felipe Jiménez"
    Evento['tipo']="Ayudantia"

    output=[]
    for evento in Evento['cursos']:
        for curso in  Cursos.query.filter({'codigo':{ '$regex': evento} }).all():
            output.append(curso.mongo_id)
    Evento['output']=output
    Eventos.append(Evento)





    Eventos.reverse()
    return render_template("eventos.js", Eventos=Eventos)

@app.route('/api_Cursos', methods=['GET'])
def Curso_api():
    obbx = {}
    for bloque in ["A", "B", "C", "D", "E", "F"]:
        cursos = Cursosx.query.filter({"salas" : { '$elemMatch': { "dia" : DIA,"bloque":bloque }  } }).all()
        obbx[bloque] =[]
        for curso in cursos:
            try:
                obbx[bloque].append(curso.arr(DIA)[0])
            except:
                pass
    obbx['version'] = VERSION
    import json

    return json.dumps(obbx)

dias = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado"]











class Todos_los_cursos(Resource):
    def get(self, todo_id):
        usuario,passwd=decode_token(request.args['token'])
        return {}


    def put(self,todo_id):
        return {}

api.add_resource(Todos_los_cursos, '/todos_los_cursos/<todo_id>')

#suspencion_total()


if __name__ =="__main__":
    #update_user()
    DATA_cursos()
    #app.run(port=5001, host="0.0.0.0", debug=True)
    pass
else:
    pass