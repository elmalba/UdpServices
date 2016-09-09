from flask import Blueprint, request
from flask_restful import Resource, Api
check = Blueprint('check', __name__)

api = Api(check)



from core.mongo_modelos import Alumnos as MongoAlumnos

class Alumnos(Resource):
    def get(self,codigo):
        tupla = MongoAlumnos.query.get(codigo)
        if tupla != None and tupla.token == request.args['token']:
            return {'access':True}
        return {'access':False}

class Profesores(Resource):
    def get(self,codigo):
        tupla = MongoAlumnos.query.get(codigo)
        if tupla != None and tupla.token == request.args['token']:
            return {'access':True}
        return {'access':False}

class Funcionarios(Resource):
    def get(self,codigo):
        tupla = MongoAlumnos.query.get(codigo)
        if tupla != None and tupla.token == request.args['token']:
            return {'access':True}
        return {'access':False}

api.add_resource(Alumnos, '/Alumnos/<codigo>')
api.add_resource(Profesores, '/Profesores/<codigo>')
api.add_resource(Funcionarios, '/Funcionarios/<codigo>')
