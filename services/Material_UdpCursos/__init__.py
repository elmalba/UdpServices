from flask import Blueprint
from flask_restful import Resource,Api
from core.core import Biblioteca_udp
material = Blueprint('Material', __name__)
api = Api(material)

class Biblioteca_udp(Resource):
    def get(self,codigo):
        return [resultado.json() for resultado in Bilioteca_udp.query.filter({'codigo':codigo }).all()]
api.add_resource(Biblioteca_udp, '/Curso/<codigo>')
