#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.core import *

from flask_restful import Resource, Api
from flask import request
from time import sleep
from services.Sap import *
import requests

api = Api(app)

import threading

threads = list()

def worker(count):
    while len(Pendientes):
        user=Pendientes[0]
        data=login(user['rut'],user['passwd'])
        alumno=Alumnos.query.filter({'rut':user['rut']}).first()
        sleep(1)
        requests.post("http://localhost:3000/api",{'key':str(alumno.mongo_id)})
        Pendientes.pop()
    return

Pendientes=[]

class Alumnos_sap(Resource):
    def get(self):
        i=2
        Pendientes.append({'rut':request.args['rut'],'passwd':request.args['passwd']})
        if len(Pendientes) == 1:
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        return {'lista_espera':len(Pendientes)}

class Alumnos_sap_now(Resource):
    def get(self):
        return login(request.args['rut'],request.args['passwd'])

class Lista_espera(Resource):
    def get(self):
        return {'lista_espera':len(Pendientes)}
api.add_resource(Alumnos_sap,'/alumnos_sap')
api.add_resource(Alumnos_sap_now,'/alumnos_sap_now')
api.add_resource(Lista_espera,'/lista_espera')
app.run(debug=True)