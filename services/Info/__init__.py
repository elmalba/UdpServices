from flask import Blueprint, render_template, abort
from flask_restful import Resource, Api
simple_page = Blueprint('simple_page', __name__)

api = Api(simple_page)

from flask_restful import Resource, Api

from core.core import Alumnos,Cursosx
class Horarios_libres(Resource):
    def get(self,codigo):

        return {}

class Alumnos_info(Resource):
    def get(self,rut):
        alumno = Alumnos.query.filter({'rut':rut}).first()
        if alumno !=None:
            XAlumno = alumno.json()
            del XAlumno['registro']
            Cursos_asignados =Cursosx.query.filter({'$or':[{'codigo':curso} for curso in  alumno.cursos]}).all()
        else:
            Cursos_asignados = Cursosx.query.filter({'alumnos': {"$elemMatch": {'rut': rut}}}).all()
            XAlumno=[ alumno for alumno in  Cursos_asignados[0].alumnos  if rut == alumno['rut'] ][0]
        XAlumno['cursos']=[]
        for curso in Cursos_asignados:
            XAlumno['cursos'].append({'codigo':curso.codigo,'profesor':curso.profesor_sistema['full_name'],'curso':curso.curso})
        return XAlumno

api.add_resource(Horarios_libres, '/Horarios_libres/<codigo>')
api.add_resource(Alumnos_info, '/Alumno_info/<rut>')