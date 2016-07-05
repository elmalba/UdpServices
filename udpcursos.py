from core.core import *
VERSION = 6
DIA = "Viernes"
def json_curso(curso):
    cur={}
    cur['codigo']=curso.codigo
    cur['profesor']=curso.profesor
    cur['facultad']=curso.facultad
    cur['documentos']=curso.documentos
    cur['salas']=curso.salas
    cur['curso']=curso.curso
    cur['hash']=str(curso.mongo_id)
    return cur

def Login_alumno(user,passwd):
    consulta_1 = {'rut': user,'passwd':passwd}
    print consulta_1,"ACAAA"
    alumno = Alumnosx.query.filter(consulta_1).first()
    if alumno == None:
	print "Aqui"
        alumno = alumno_up(Alumnosx(),user,passwd)[0]
    print "aca1"
    Alumno={}
    Alumno['full_name']=alumno.full_name
    print Alumno
    Alumno['hash']=str(alumno.mongo_id)
    Alumno['carrera']          = alumno.carrera
    Alumno['rut']       = alumno.rut
    Alumno['correo_udp']       = alumno.correo_udp
    Alumno['correo_respaldo']  = alumno.correo_respaldo
    Alumno['sufragar']=alumno.sufragar

    print "ACA2"
    Codigos = []
    for codigo in alumno.cursos:
        Codigos.append({'codigo':str(codigo)})
    consulta={ '$or': Codigos}
    cursosx=[]
    for curso in Cursos.query.filter(consulta).all():
        cursosx.append(json_curso(curso))


    ayudantiax=[]
    Codigos = []
    if len(alumno.ayudantia):
        for codigo in alumno.ayudantia:
            Codigos.append({'codigo':str(codigo)})
        consulta={ '$or': Codigos}
        ayudantiax=[]
        for curso in Cursos.query.filter(consulta).all():
            ayudantiax.append(json_curso(curso))

    return {'usuario':Alumno,'cursos':cursosx,'ayudantias':ayudantiax}



class Alumnos(Resource):
    def get(self):
        if True:
            if "token" in request.args:
                usuario,passwd=decode_token(request.args['token'])
            else:
                usuario = request.args['user']
                passwd = request.args['passwd']
            return {'HOLA':123}
        try:
            pass

        except:
            ob = {'resultados': "Usuario y/o password invalidos"}
            print ob
            return ob

    def post(self):

        try:
            if "token" in request.json:
                usuario,passwd=decode_token(request.json['token'])
            else:
                usuario = request.json['user']
                passwd = request.json['passwd']

            return Login_alumno(usuario,passwd)


            pass
        except:
            ob = {'resultados': "Usuario y/o password invalidos"}
            return ob


class Biblioteca_udp(Resource):
    def get(self,codigo):
        return [resultado.json() for resultado in Bilioteca_udp.query.filter({'codigo':codigo }).all()]


api.add_resource(Alumnos, '/Alumnos')
api.add_resource(Biblioteca_udp, '/Curso/<codigo>')


from flask_socketio import SocketIO, emit
from flask import session


socketio = SocketIO(app)

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})

@socketio.on('send')
def test_message(message):
    print message
    emit('send', message, broadcast=True)

def ADD_info():
    from listas import search

    if True:
        CURSOSX =   Cursosx.query.all()
        print len (CURSOSX)
        Cursos=['COC2106-01', 'COC3001-01', 'COC3000-01', 'COC3413-01', 'COC3518-01', 'COC2107-01', 'CII2004-02', 'CII2503-01', 'CII2753-04', 'CII2751-01', 'UAH1068-01', 'CBM1003-01', 'CII2501-01', 'CBM1002-02', 'CII2002-02', 'COC2100-04', 'COC2203-01', 'COC2104-01', 'COC2103-01', 'COC2003-01', 'CFG2051-01', 'COC2001-01', 'FIC1002-08', 'CBF1000-06', 'CBM1003-05', 'CII2003-03', 'CFG5010-01', 'CII2252-02', 'CII2500-03', 'COC2310-01', 'COC2201-01', 'COC2102-01', 'CFG2014-01', 'CBF1002-05', 'CBE2000-03', 'COC2004-01', 'CFG2029-01', 'FIC1001-03', 'CII1000-05', 'CBM1003-07', 'CBM1002-06', 'CIT1010-04', 'CII1001-03', 'CBM1001-09', 'FIC1002-04', 'CBM1000-05', 'CIT2000-01', 'CIT2100-02', 'CBM1001-06', 'CBM1000-06', 'CBM1001-04', 'CBQ1000-04', 'CBM1000-13', 'FIC1000-05', 'CIT1000-04', 'FIC1000-08', 'CBM1000-01', 'CBM1001-01', 'CIT1000-01', 'CBQ1000-01', 'CBQ1000-07', 'CBM1001-07', 'CBM1000-07', 'FIC1000-02', 'CIT1000-07', 'FGD9048-02', 'CIT2003-01', 'CBF1002-03', 'CII2750-01', 'CII2001-03', 'CBF1002-01', 'CII2251-03', 'PER4426-01', 'PER4516-03', 'PER9313-01', 'PER4517-02', 'PER4513-02', 'PER4519-01', 'PER9209-01', 'CII3425-01', 'CII3405-01', 'ICI3303-01', 'CII2500-02', 'CII2000-02', 'CII2751-02', 'CII2750-03', 'CII2251-02', 'INF4404-01', 'IFG1601-01', 'IND1405-01', 'IFG2401-01', 'DIS7355-02', 'CBM1005-03', 'CFG2098-01', 'CBF1001-02', 'CBM1006-01', 'CBM1000-02', 'FIC1000-09', 'CBQ1000-02', 'CBM1001-02', 'CBM1000-08', 'FIC1002-07', 'CBM1001-08', 'CBF1002-04', 'CII2000-04', 'FIC1002-01', 'CII2750-02', 'FIC1001-01', 'CBM1000-09', 'CII3503-01', 'CII3607-01', 'CII2254-02', 'CBM1001-12', 'CBM1000-12', 'CIT1000-12', 'CBQ1000-11', 'FIC1000-11', 'CII2754-02', 'CII3614-01', 'CII3612-01', 'CII3600-01', 'CII3300-01', 'CBM1006-05', 'CBF1001-03', 'CII1000-03', 'CIT1010-02', 'CFG2284-01', 'CII2753-03', 'CII2002-01', 'CII2252-01', 'CII2752-01', 'CII3403-01', 'CII3501-01', 'CII2754-01', 'CII3404-01', 'CIT2000-02', 'CBM1002-04', 'CIT2100-03', 'CBM1003-04', 'CIT2202-01', 'CII2500-01', 'CIT2200-01', 'CIT2002-01', 'CBM1002-08', 'CBF1000-01', 'CIT1000-09', 'CBM2000-01', 'FIC1001-08', 'CIT2001-01', 'CBE2000-06', 'COC3415-01', 'COC2105-01', 'COC2005-01', 'COC2204-01', 'CFG2198-01', 'CFG2160-01', 'COC3100-01', 'COC3519-01', 'CFG2203-01', 'CII2502-01', 'CII2252-03', 'CII2501-03', 'CIT3200-01', 'CIT3416-01', 'CIT3323-01', 'CIT3335-01', 'CIT3422-01']
        for cursos in CURSOSX:
            print "aca",cursos.curso
            if cursos.codigo not in Cursos:

                ixx=0
                if True:
                    for alumno in Alumnosx.query.filter({'cursos':{'$eq':cursos.codigo}}).all():
                #

                        print alumno.rut
                        ok =False
                        try:

                            XCURSOS=search(alumno.rut, alumno.passwd)
                            print Cursos
                            print XCURSOS.iterkeys()
                            for Xcodigo in XCURSOS.iterkeys():
                                if Xcodigo not in Cursos:
                                    CURSOP = Cursosx.query.filter({'codigo': Xcodigo}).first()

                                    print "ENTRO"
                                    xcurso= CursosTEMP()
                                    xcurso.codigo = CURSOP.codigo
                                    xcurso.curso = CURSOP.curso
                                    xcurso.profesor = CURSOP.profesor
                                    xcurso.facultad = CURSOP.facultad
                                    xcurso.keyp = CURSOP.keyp
                                    xcurso.keya = CURSOP.keya
                                    xcurso.documentos = CURSOP.documentos
                                    xcurso.salas = CURSOP.salas
                                    xcurso.profesor_sistema = XCURSOS[Xcodigo]['profesor']
                                    xcurso.alumnos = XCURSOS[Xcodigo]['alumno']
                                    xcurso.noticias = []
                                    xcurso.save()
                                    Cursos.append(Xcodigo)
                                    print "Guardado nuevo",len(Cursos)
                                    ok =True
                            if ok or ixx==3:
                                break
                            ixx=ixx+1


                        except:
                            pass

                            try:
                                pass

                            except:
                                pass


                try:
                    pass
                except:
                    pass
    try:
        pass
    except:
        print "CAMBIO EL PASS",alumno.rut

    print Cursos
    print len (Cursos)

from datetime import datetime
@app.route('/Register_vote', methods=['Post'])
def Alumno_voto():
    rut= request.form['rut']
    code = request.form['code']
    alumno = Alumnos.query.filter({'rut':rut}).first()
    if alumno== None:
        return "{'status':'ok'}"
    alumno.sufragar['Votaciones_2']={}
    alumno.sufragar['Votaciones_2']['habilitado']=False
    alumno.sufragar['Votaciones_2']['time']=datetime.now()
    alumno.sufragar['Votaciones_2']['code']=code
    return "{'status':'ok'}"


def ADD_info2():

    for x in Cursosx.query.all():
        x.suspensiones=[]
        x.save()


#ADD_info2()

#ADD_info()

from flask_cors import CORS
cors = CORS(app, allow_headers='Content-Type')

CORS(app)


from upload_udp import run
run(app,request)






if __name__ =="__main__" and True:
    app.run(host='0.0.0.0',debug=True)
    #socketio.port=5001
    #socketio.host="0.0.0.0"
    #socketio.run(app, host='0.0.0.0')
