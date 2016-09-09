from flask import Blueprint
from flask_restful import Resource, Api
from core.mongo_modelos import Cursos
Login_alumno = Blueprint('Login_alumno', __name__)

api = Api(Login_alumno)


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


def Check_Login(DATA):
    if "token" in DATA:
        usuario,passwd=decode_token(DATA)
    else:
        usuario = DATA['user']
        passwd = DATA['passwd']
    return Login_alumno(usuario,passwd)

class Alumnos(Resource):
    def get(self):
        return Check_Login(request.args)
    def post(self):
        return Check_Login(request.json)

api.add_resource(Alumnos, '/Login')
