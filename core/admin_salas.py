from datetime import datetime
from flask import request

class Curso(Resource):
    def get(self,curso_id):
        Curso=Modelo.get()
        return Curso.json()
    def put(self,curso_id):
        Curso=Modelo.get()
        Curso.update(request.json)

        return Curso.json()

class Cursos(Resource):
    def get(self):
        Curso=Modelo.get()
        return Curso.json()


class Eventos(Resource):
    def get(self):
        Eventox =  Eventos.filter({'fecha':{'$gt':datetime.now()}}).query.all()
        return [Evento.json() for Evento in Eventox]
    def post(self):
        Evento= Eventos()
        Evento.update(request.json)
        Evento.save()
        return  Evento.json()

class Evento(Resource):
    def put(self,curso_id):
        Evento = Eventos.query.get(curso_id)
        Evento.update(request.json)
        Evento.save()
        return Evento.save()

class Salas(Resource):
    def get(self):
        salas = Salas.query.all()
        return [sala.json2() for sala in salas]