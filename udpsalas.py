#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.core import *
from core.crypto import *

from services.Documentos_portal import documentos

app.register_blueprint(documentos, url_prefix='/Documentos')

def login(user, passwd):
    consulta_1 = {'rut': user}
    alumno = Alumnosx.query.filter(consulta_1).first()
    if alumno == None:
        alumno = alumno_up(Alumnosx(),user,passwd)[0]
    elif str(alumno.passwd) != str(passwd):
        alumno_up(alumno,user,passwd)[0]


    Codes = alumno.cursos + alumno.ayudantia

    Curso_output = []
    Codigos = []
    for codigo in Codes:
        Codigos.append({'codigo':str(codigo)})

    cursos_xo=[]

    consulta={ '$or': Codigos}

    print "POR AQUO",consulta
    cursos = Cursosx.query.filter(consulta).all()
    print len (cursos)
    Codigos = []
    for curso in cursos:
        Codigos.append(str(curso.mongo_id))
        cursos_xo.append({ 'hash' :str(curso.mongo_id),'curso' : str(curso.curso),'profesor':str(curso.profesor),'seccion':curso.codigo.split("-")[1]})

    return jsonify(codigos=Codigos,cursos=cursos_xo)



@app.route('/Cursos.js', methods=['GET'])
def Curso_js():
    def getKey(custom):
        return custom['bloque']

    CURXX=[]
    for curso in  Cursos.query.filter({"salas" : { '$elemMatch': { "dia" : DIA } } }).all():
        CURXX=CURXX+curso.arr(DIA)
    CURXX=sorted(CURXX,key=getKey)
    js = render_template("cursos.js", cursos=CURXX,version=VERSION)
    #js = minify(js, mangle=True, mangle_toplevel=True)
    return js



@app.route("/Eventos.js")
def Eventos():
    Eventos=[]
    Evento={}
    Evento['fecha']="07/06/2016"
    Evento['sala']="de Estudios piso -1"
    Evento['bloque']="10:00 - 13:00"
    Evento['curso']="Mecanica"
    Evento['cursos']=["CBF1000"]
    Evento['profesor']="CAEA UDP"
    Evento['tipo']="Mesa de Estudio"

    output=[]
    for evento in Evento['cursos']:
        for curso in  Cursos.query.filter({'codigo':{ '$regex': evento} }).all():
            output.append(curso.mongo_id)
    Evento['output']=output
    Eventos.append(Evento)


    Evento={}
    Evento['fecha']="07/06/2016"
    Evento['sala']="de Estudios piso -1"
    Evento['bloque']="14:00 - 17:00"
    Evento['curso']="Calculo I"
    Evento['cursos']=["CBM1001"]
    Evento['profesor']="CAEA UDP"
    Evento['tipo']="Mesa de Estudio"

    output=[]
    for evento in Evento['cursos']:
        for curso in  Cursos.query.filter({'codigo':{ '$regex': evento} }).all():
            output.append(curso.mongo_id)
    Evento['output']=output
    Eventos.append(Evento)


    Evento={}
    Evento['fecha']="07/06/2016"
    Evento['sala']="de Estudios piso -1"
    Evento['bloque']="14:00 - 17:00"
    Evento['curso']="Algebra y Geometria"
    Evento['cursos']=["CBM1000"]
    Evento['profesor']="CAEA UDP"
    Evento['tipo']="Mesa de Estudio"

    output=[]
    for evento in Evento['cursos']:
        for curso in  Cursos.query.filter({'codigo':{ '$regex': evento} }).all():
            output.append(curso.mongo_id)
    Evento['output']=output
    Eventos.append(Evento)


    Eventos.reverse()
    return render_template("eventos.js", Eventos=Eventos)





if __name__ =="__main__":
    #update_user()
    #DATA_cursos()
    app.run(port=5001, host="0.0.0.0", debug=True)

