from flask import Blueprint, render_template, abort
from flask_restful import Resource, Api
from datetime import datetime
upload = Blueprint('Upload', __name__)
api = Api(upload)
from core.core import Alumnos,Bilioteca_udp
from services.acceso import Alumnos,Profesores,Funcionarios
from config import AVAILABLES

class Upload_available(Resource):
    def get(self,codigo):
        if request.args['code_access'] in AVAILABLES.iterkeys():
            return Alumnos.get(codigo) or Profesores.get(codigo) or Funcionarios.self(codigo)
        return False
class Upload_file(Resource):
    def post(self):

        B=Bilioteca_udp()
        B.codigo=codigo
        B.identificador=flowIdentifier
        B.fecha=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        B.rut=alumno.rut
        B.responsable=alumno.full_name
        B.categoria=categoria
        B.archivo=archivo
        B.url=url+'static/'+codigo+"/"+categoria+"/"+nombre
        B.denuncias={}
        B.validar=1
        B.save()
        return B.json()

api.add_resource(Upload_available, '/Available/<codigo>')
api.add_resource(Upload_file, '/Ready')