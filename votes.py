#!/usr/bin/python
# -*- coding: utf8 -*-
from flask import Flask, request,redirect
from flask_restful import Resource, Api
import random
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
api = Api(app)

todos = {}


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:mmae2010@localhost/votaciones"
db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


class Votes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#rut   = db.Column(db.Text,unique=True)
	opcion = db.Column(db.Text)
	#code   = db.Column(db.Text)
	#ip        = db.Column(db.Text)
	timestamp  = db.Column(db.DateTime)


class Registers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rut   = db.Column(db.Text,unique=True)
	hash_id     = db.Column(db.Text,default="")
	code   = db.Column(db.Text)
	timestamp = db.Column(db.DateTime)


class Availables(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rut   = db.Column(db.Text,unique=True)
	full_name     = db.Column(db.Text)
	hash_id     = db.Column(db.Text,default="")
	carrera       = db.Column(db.Text,default="")
	timestamp = db.Column(db.DateTime)


from core.crypto import *
def code(vote,token):
	token=vote
	fecha = vote.timestamp

	
def Load_db():
	db.drop_all()
	db.create_all()
	ruts = []
	file = open("user.json", "r")
	users=file.read()
	from json import loads
	users=loads(users)
	for user in users.keys():
		available = Availables()
		available.rut = str(users[user]['rut']).lower()
		if available.rut not in ruts:
			ruts.append(available.rut)
			print str(users[user]['full_name'].encode('utf8'))
			available.full_name = str(users[user]['full_name'].encode('utf8'))
			if 'carrera' in users[user]:
				available.carrera =str(users[user]['carrera'].encode('utf8'))
				available.hash_id   =str(users[user]['hash_id'])
			available.timestamp=datetime.now()
			db.session.add(available)
	db.session.commit()


def EjecutarVoto(rut,opcion):
	user = Availables.query.filter_by(rut=rut).first()
	if user != None:
		register = Registers.query.filter_by(rut=rut).first()
		if register == None:
			Register=Registers()
			Register.code=str(random.getrandbits(36))
			Register.hash_id=user.hash_id
			Register.rut=rut
			fecha=datetime.now()
			Register.timestamp=fecha
			db.session.add(Register)
			db.session.commit()
			vote=Votes()


			#vote.rut=rut
			vote.opcion=opcion
			vote.timestamp=datetime.now()
			#vote.ip=request.headers.get('cf-connecting-ip')
			#vote.code=Register.code
			db.session.add(vote)
			db.session.commit()
			notification(rut,register.code)

			return {'message':'Voto emitido validamente','codigo':register.code}
		return {'message':'Tu voto ya fue emitido','codigo':register.code}

	return {'message':'No intentes hacer algo que no puedes hacer'}



class Votar(Resource):
	def get(self):
		rut=request.args['rut']
		rut=str(rut.encode('utf8'))
		sys.setdefaultencoding('utf8')
		available = Availables.query.filter_by(rut=rut).first()
		if available == None:
			return {}
		register= Registers.query.filter_by(rut=rut).first()
		if register == None:
			habilitado=True
			fecha=None
		else:
			habilitado=False
			fecha=register.timestamp.strftime('%m/%d/%Y %H:%M')
		return {'full_name':available.full_name,'carrera':available.carrera,'habilitado':habilitado,'fecha':fecha}
	def post(self):
		rut=  str(request.json['rut'] )
		opcion =  str(request.json['opcion']  )
		accept1 = False
		accept2 = False
		if len(rut)<13:
			accept1 = True
		if opcion  == "Paro Indefinido":
			accept2 = True
		elif opcion =="Clases":
			accept2 = True
		elif opcion =="Blanco":
			accept2= True
		elif opcion =="Nulo":
			accept2= True
		if accept1 and accept1:
			print "ACA2"
			return  EjecutarVoto(rut,opcion)
		return {'message':'No intentes hacer algo que no puedes hacer'}


class Register(Resource):


	def post(self):
		try:
			print request.form
			hash_id= request.form['hash_id']
			token = request.form['token']
			print hash_id
			Ava =Availables()
			Ava.hash_id=hash_id
			Ava.timestamp=datetime.now()
			Ava.token=token
			db.session.add(Ava)
			db.session.commit()
			return {'message':'ok'}
		except:
			return {'message':'error'}

import requests

import threading

def notification(rut,scode):
	threads = list()
	t = threading.Thread(target=notification_url, args=(rut,scode,))
	threads.append(t)
	t.start()

def notification_url(rut,scode):


	url = "https://api.udpcursos.com/Register_vote"
	#payload = "hash="+hash_id+"&token="+token+"&code="+scode
	payload = "rut="+rut+"&code="+scode
	headers = {
	    'cache-control': "no-cache",
	    'postman-token': "ed6c75c9-98fd-eea4-b8fe-456a13f3f547",
	    'content-type': "application/x-www-form-urlencoded"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)

	print(response.text)
@app.route("/reset")
def reset():
	Load_db()
	return "ok"


api.add_resource(Votar, '/Votar')
api.add_resource(Register, '/Register_udpCursos')
@app.errorhandler(404)
def page_not_found(e):
    return redirect("https://udpcursos.com")

if __name__ == '__main__':
	#Load_db()
	app.run(debug=True,host="0.0.0.0",port=5080)
#select date_trunc( 'hour', timestamp ), opcion, count (*) from votes GROUP BY opcion,1  order by date_trunc asc;