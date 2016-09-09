from flask import Blueprint
from flask_restful import Resource, Api
documentos = Blueprint('Documentos', __name__)
api = Api(documentos)

from core.mongo_modelos import Cursos as Cursosx

class Documentos(Resource):
    def get(self, curso_id):
        Curso = Cursosx.query.get(curso_id)
        return Curso.documentos
api.add_resource(Documentos, '/<curso_id>')